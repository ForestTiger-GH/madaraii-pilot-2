from __future__ import annotations

import json
import sqlite3
from contextlib import contextmanager
from decimal import Decimal
from pathlib import Path
from typing import Iterator, Mapping, Sequence

import pandas as pd

from .registry import SOURCE_BY_ID


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
    """Read-only facade. Validated databases are required by default."""

    def __init__(self, path: str | Path, *, allow_unvalidated: bool = False):
        self.path = Path(path)
        if not self.path.exists():
            raise FileNotFoundError(self.path)
        if not allow_unvalidated and self.validation().get("status") != "passed":
            raise QueryError(
                "Database validation is not passed; use allow_unvalidated=True only for diagnostics"
            )

    def validation(self) -> dict[str, object]:
        with _connect(self.path) as con:
            row = con.execute("SELECT json_value FROM build_metadata WHERE key='validation'").fetchone()
        if row is None:
            raise QueryError("Database has no validation metadata")
        value = json.loads(row[0])
        if not isinstance(value, dict):
            raise QueryError("Database validation metadata is not an object")
        return value

    def sources(self, *, language: str = "ru") -> pd.DataFrame:
        if language not in {"ru", "en"}:
            raise ValueError("language must be 'ru' or 'en'")
        with _connect(self.path) as con:
            df = pd.read_sql_query(
                "SELECT source_id, source_revision_id, requested_url, resolved_url, registry_filename, sha256, bytes, acquired_at_utc FROM source_revisions ORDER BY source_id",
                con,
            )
        if df.empty:
            return df
        df["name_ru"] = df["source_id"].map(
            lambda sid: SOURCE_BY_ID[sid].name_ru if sid in SOURCE_BY_ID else str(sid)
        )
        df["name_en"] = df["source_id"].map(
            lambda sid: SOURCE_BY_ID[sid].name_en if sid in SOURCE_BY_ID else str(sid)
        )
        df.insert(1, "display_name", df["name_ru"] if language == "ru" else df["name_en"])
        return df

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
            cols = (
                ("name_ru", "label_ru_source", "label_ru_normalized")
                if language == "ru"
                else ("name_en", "name_ru", "label_ru_source")
            )
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

    def _dimension_members(self) -> list[dict[str, str]]:
        with _connect(self.path) as con:
            rows = con.execute(
                "SELECT dimension, classification, source_value_ru, name_ru, name_en FROM dimension_members"
            ).fetchall()
        return [dict(row) for row in rows]

    @staticmethod
    def _member(
        members: Sequence[Mapping[str, str]],
        key: str,
        raw_value: object,
        dims: Mapping[str, object],
    ) -> Mapping[str, str] | None:
        raw = str(raw_value)
        classification = str(dims.get("classification", ""))
        matches = [
            row for row in members
            if str(row.get("dimension", "")) == key
            and str(row.get("source_value_ru", "")) == raw
        ]
        exact = [row for row in matches if str(row.get("classification", "")) == classification]
        if exact:
            return exact[0]
        return matches[0] if len(matches) == 1 else None

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
            SELECT o.*, c.source_id AS concept_source_id, c.name_ru, c.name_en,
                   c.label_ru_source, c.translation_status, c.row_axis
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

        members = self._dimension_members()
        parsed_dims = df["dimensions_json"].map(json.loads)
        if dimensions:
            keep: list[bool] = []
            for dims in parsed_dims:
                row_ok = True
                for key, wanted in dimensions.items():
                    wanted_values = set(_as_list(wanted))
                    raw = str(dims.get(key, ""))
                    candidates = {raw}
                    member = self._member(members, key, raw, dims)
                    if member:
                        candidates.update(
                            str(member.get(field, ""))
                            for field in ("source_value_ru", "name_ru", "name_en")
                            if str(member.get(field, ""))
                        )
                    if not candidates.intersection(wanted_values):
                        row_ok = False
                        break
                keep.append(row_ok)
            df = df.loc[keep].copy()
            parsed_dims = parsed_dims.loc[keep]
        if df.empty:
            return df

        for key in sorted({key for dims in parsed_dims for key in dims}):
            values: list[str] = []
            for dims in parsed_dims:
                raw = str(dims.get(key, ""))
                member = self._member(members, key, raw, dims)
                if member:
                    raw = str(member.get("name_ru" if language == "ru" else "name_en", raw)) or raw
                values.append(raw)
            df[f"dim_{key}"] = values
        df.insert(0, "indicator", df["name_ru"] if language == "ru" else df["name_en"])
        df["value"] = df["value_exact"].map(Decimal) if decimal_values else pd.to_numeric(df["value_exact"], errors="raise")
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

        hidden_signature = [
            field for field in ("unit", "scale", "frequency", "period_role") if field not in keys
        ]
        if hidden_signature:
            group_cols = column_cols or ["source_concept_id"]
            for group_key, group in df.groupby(group_cols, dropna=False):
                signatures = group[hidden_signature].astype(str).drop_duplicates()
                if len(signatures) > 1:
                    raise QueryError(
                        "Pivot is semantically heterogeneous: one displayed series mixes "
                        f"{hidden_signature}. Narrow filters or expose the differing fields. "
                        f"Series={group_key!r}; signatures={signatures.head(8).to_dict('records')}"
                    )

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
                SELECT r.*, d.source_id AS disposition_source_id,
                       d.source_revision_id AS disposition_source_revision_id,
                       d.role AS disposition_role, d.reason AS disposition_reason
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
                SELECT o.*, o.source_id AS observation_source_id,
                       c.source_id AS concept_source_id, rc.source_id AS raw_source_id,
                       d.source_id AS disposition_source_id,
                       c.name_ru, c.name_en, r.requested_url, r.resolved_url, r.sha256,
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
