from __future__ import annotations

import json
import sqlite3
from contextlib import contextmanager
from decimal import Decimal
from pathlib import Path
from typing import Iterable, Iterator, Mapping, Sequence

import pandas as pd


class QueryError(RuntimeError):
    pass


@contextmanager
def _connect(path: str | Path) -> Iterator[sqlite3.Connection]:
    con = sqlite3.connect(Path(path))
    con.row_factory = sqlite3.Row
    try:
        yield con
    finally:
        con.close()


def _as_list(value: str | Sequence[str] | None) -> list[str]:
    if value is None:
        return []
    if isinstance(value, str):
        return [value]
    return list(value)


class UnifiedDatabase:
    """Read-only query facade over a built CBR Unified SQLite database."""

    def __init__(self, path: str | Path):
        self.path = Path(path)
        if not self.path.exists():
            raise FileNotFoundError(self.path)

    def validation(self) -> dict[str, object]:
        with _connect(self.path) as con:
            row = con.execute("SELECT json_value FROM build_metadata WHERE key='validation'").fetchone()
        if row is None:
            raise QueryError("Database has no validation metadata")
        return json.loads(row[0])

    def sources(self) -> pd.DataFrame:
        with _connect(self.path) as con:
            return pd.read_sql_query(
                "SELECT source_id, source_revision_id, requested_url, resolved_url, registry_filename, sha256, bytes, acquired_at_utc FROM source_revisions ORDER BY source_id",
                con,
            )

    def indicators(
        self,
        text: str | None = None,
        *,
        language: str = "ru",
        source_ids: str | Sequence[str] | None = None,
    ) -> pd.DataFrame:
        if language not in {"ru", "en"}:
            raise ValueError("language must be 'ru' or 'en'")
        sources = _as_list(source_ids)
        where: list[str] = []
        args: list[object] = []
        if sources:
            where.append("source_id IN (%s)" % ",".join("?" for _ in sources))
            args.extend(sources)
        if text:
            cols = ("name_ru", "label_ru_source", "label_ru_normalized") if language == "ru" else ("name_en", "name_ru", "label_ru_source")
            where.append("(" + " OR ".join(f"LOWER({c}) LIKE LOWER(?)" for c in cols) + ")")
            args.extend([f"%{text}%"] * len(cols))
        sql = "SELECT * FROM source_concepts"
        if where:
            sql += " WHERE " + " AND ".join(where)
        sql += " ORDER BY source_id, source_local_key"
        with _connect(self.path) as con:
            df = pd.read_sql_query(sql, con, params=args)
        if not df.empty:
            df.insert(0, "display_name", df["name_ru"] if language == "ru" else df["name_en"])
        return df

    def observations(
        self,
        *,
        source_ids: str | Sequence[str] | None = None,
        concept_ids: str | Sequence[str] | None = None,
        start: str | None = None,
        end: str | None = None,
        frequency: str | Sequence[str] | None = None,
        period_role: str | Sequence[str] | None = None,
        dimensions: Mapping[str, str | Sequence[str]] | None = None,
        language: str = "ru",
        decimal_values: bool = False,
    ) -> pd.DataFrame:
        if language not in {"ru", "en"}:
            raise ValueError("language must be 'ru' or 'en'")
        where: list[str] = []
        args: list[object] = []

        def include(column: str, values: str | Sequence[str] | None) -> None:
            vals = _as_list(values)
            if vals:
                where.append(f"o.{column} IN (%s)" % ",".join("?" for _ in vals))
                args.extend(vals)

        include("source_id", source_ids)
        include("source_concept_id", concept_ids)
        include("frequency", frequency)
        include("period_role", period_role)
        if start:
            where.append("o.period >= ?")
            args.append(start)
        if end:
            where.append("o.period <= ?")
            args.append(end)

        sql = """
            SELECT
                o.*,
                c.name_ru,
                c.name_en,
                c.label_ru_source,
                c.translation_status,
                c.row_axis
            FROM observations o
            JOIN source_concepts c ON c.source_concept_id = o.source_concept_id
        """
        if where:
            sql += " WHERE " + " AND ".join(where)
        sql += " ORDER BY o.source_id, o.source_concept_id, o.period, o.sheet_exact, o.cell_coordinate"
        with _connect(self.path) as con:
            df = pd.read_sql_query(sql, con, params=args)
        if df.empty:
            return df

        parsed_dims = df["dimensions_json"].map(json.loads)
        if dimensions:
            keep = []
            for dims in parsed_dims:
                ok = True
                for key, wanted in dimensions.items():
                    values = _as_list(wanted)
                    if str(dims.get(key, "")) not in values:
                        ok = False
                        break
                keep.append(ok)
            df = df.loc[keep].copy()
            parsed_dims = parsed_dims.loc[keep]
        if df.empty:
            return df

        dim_keys = sorted({k for dims in parsed_dims for k in dims})
        for key in dim_keys:
            df[f"dim_{key}"] = parsed_dims.map(lambda d, k=key: d.get(k, ""))
        df.insert(0, "indicator", df["name_ru"] if language == "ru" else df["name_en"])
        if decimal_values:
            df["value"] = df["value_exact"].map(Decimal)
        else:
            df["value"] = pd.to_numeric(df["value_exact"], errors="raise")
        return df

    def pivot(
        self,
        *,
        index: str | Sequence[str] = "period",
        columns: str | Sequence[str] = "indicator",
        values: str = "value",
        **observation_filters: object,
    ) -> pd.DataFrame:
        df = self.observations(**observation_filters)
        if df.empty:
            return df
        index_cols = _as_list(index)
        column_cols = _as_list(columns)
        keys = index_cols + column_cols
        missing = [c for c in keys + [values] if c not in df.columns]
        if missing:
            raise QueryError(f"Pivot columns not present in selected data: {missing}")
        duplicates = df.duplicated(keys, keep=False)
        if duplicates.any():
            sample_cols = keys + ["source_id", "source_concept_id", "sheet_exact", "cell_coordinate", "dimensions_json"]
            sample = df.loc[duplicates, [c for c in sample_cols if c in df.columns]].head(12).to_dict("records")
            raise QueryError(
                "Pivot is ambiguous: multiple observations map to the same requested cell. "
                f"Add dimensions/source/concept to the pivot or filters. Sample={sample}"
            )
        return df.pivot(index=index_cols, columns=column_cols, values=values)

    def raw_cell(self, raw_cell_id: str) -> dict[str, object]:
        with _connect(self.path) as con:
            row = con.execute(
                """
                SELECT r.*, d.role AS disposition_role, d.reason AS disposition_reason
                FROM raw_cells r
                JOIN raw_cell_dispositions d ON d.raw_cell_id=r.raw_cell_id
                WHERE r.raw_cell_id=?
                """,
                (raw_cell_id,),
            ).fetchone()
        if row is None:
            raise KeyError(raw_cell_id)
        return dict(row)

    def lineage(self, observation_id: str) -> dict[str, object]:
        with _connect(self.path) as con:
            row = con.execute(
                """
                SELECT o.*, c.name_ru, c.name_en, r.requested_url, r.resolved_url, r.sha256,
                       rc.ooxml_type, rc.value_lexical, rc.text_resolved, rc.formula,
                       d.role AS disposition_role, d.reason AS disposition_reason
                FROM observations o
                JOIN source_concepts c ON c.source_concept_id=o.source_concept_id
                JOIN source_revisions r ON r.source_revision_id=o.source_revision_id
                JOIN raw_cells rc ON rc.raw_cell_id=o.raw_cell_id
                JOIN raw_cell_dispositions d ON d.raw_cell_id=o.raw_cell_id
                WHERE o.observation_id=?
                """,
                (observation_id,),
            ).fetchone()
        if row is None:
            raise KeyError(observation_id)
        result = dict(row)
        result["dimensions"] = json.loads(str(result.pop("dimensions_json")))
        return result
