from __future__ import annotations

import csv
import json
import sqlite3
from pathlib import Path
from typing import Mapping, Sequence


CSV_TABLES = (
    "source_revisions",
    "raw_cells",
    "source_concepts",
    "dimension_members",
    "observations",
    "raw_cell_dispositions",
)


def _write_csv(path: Path, rows: Sequence[Mapping[str, object]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        path.write_text("", encoding="utf-8-sig")
        return
    fields: list[str] = []
    seen: set[str] = set()
    for row in rows:
        for key in row:
            if key not in seen:
                fields.append(key)
                seen.add(key)
    with path.open("w", encoding="utf-8-sig", newline="") as fh:
        writer = csv.DictWriter(fh, fieldnames=fields, extrasaction="ignore")
        writer.writeheader()
        for row in rows:
            writer.writerow({k: "" if row.get(k) is None else row.get(k) for k in fields})


def _source_revision_rows(manifest: Sequence[Mapping[str, object]]) -> list[dict[str, object]]:
    fields = (
        "source_id",
        "source_revision_id",
        "requested_url",
        "resolved_url",
        "registry_filename",
        "local_path",
        "sha256",
        "bytes",
        "etag",
        "last_modified",
        "content_type",
        "acquired_at_utc",
        "status",
    )
    return [{k: row.get(k, "") for k in fields} for row in manifest]


def export_csv_bundle(
    output_dir: str | Path,
    *,
    manifest: Sequence[Mapping[str, object]],
    raw_cells: Sequence[Mapping[str, object]],
    concepts: Sequence[Mapping[str, object]],
    dimension_members: Sequence[Mapping[str, object]],
    observations: Sequence[Mapping[str, object]],
    dispositions: Sequence[Mapping[str, object]],
) -> dict[str, str]:
    root = Path(output_dir)
    root.mkdir(parents=True, exist_ok=True)
    tables: dict[str, Sequence[Mapping[str, object]]] = {
        "source_revisions": _source_revision_rows(manifest),
        "raw_cells": raw_cells,
        "source_concepts": concepts,
        "dimension_members": dimension_members,
        "observations": observations,
        "raw_cell_dispositions": dispositions,
    }
    paths: dict[str, str] = {}
    for name, rows in tables.items():
        path = root / f"{name}.csv"
        _write_csv(path, rows)
        paths[name] = str(path)
    return paths


def _json_text(value: object) -> str:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"))


def write_sqlite(
    path: str | Path,
    *,
    manifest: Sequence[Mapping[str, object]],
    raw_cells: Sequence[Mapping[str, object]],
    concepts: Sequence[Mapping[str, object]],
    dimension_members: Sequence[Mapping[str, object]],
    observations: Sequence[Mapping[str, object]],
    dispositions: Sequence[Mapping[str, object]],
    diagnostics: Mapping[str, object] | Sequence[Mapping[str, object]],
    validation: Mapping[str, object],
) -> Path:
    db = Path(path)
    db.parent.mkdir(parents=True, exist_ok=True)
    if db.exists():
        db.unlink()
    con = sqlite3.connect(db)
    try:
        con.execute("PRAGMA journal_mode=WAL")
        con.execute("PRAGMA synchronous=FULL")
        con.execute("PRAGMA foreign_keys=ON")
        con.executescript(
            """
            CREATE TABLE source_revisions (
                source_revision_id TEXT PRIMARY KEY,
                source_id TEXT NOT NULL,
                requested_url TEXT NOT NULL,
                resolved_url TEXT,
                registry_filename TEXT,
                local_path TEXT,
                sha256 TEXT NOT NULL,
                bytes INTEGER,
                etag TEXT,
                last_modified TEXT,
                content_type TEXT,
                acquired_at_utc TEXT,
                status TEXT NOT NULL
            );
            CREATE TABLE raw_cells (
                raw_cell_id TEXT PRIMARY KEY,
                source_id TEXT NOT NULL,
                source_revision_id TEXT NOT NULL REFERENCES source_revisions(source_revision_id),
                file_sha256 TEXT NOT NULL,
                sheet_exact TEXT NOT NULL,
                cell_coordinate TEXT NOT NULL,
                ooxml_type TEXT,
                style_index TEXT,
                value_lexical TEXT,
                text_resolved TEXT,
                formula TEXT,
                UNIQUE(source_revision_id, sheet_exact, cell_coordinate)
            );
            CREATE TABLE source_concepts (
                source_concept_id TEXT PRIMARY KEY,
                source_id TEXT NOT NULL,
                source_local_key TEXT NOT NULL,
                label_ru_source TEXT,
                label_ru_normalized TEXT,
                name_ru TEXT,
                name_en TEXT,
                translation_status TEXT,
                row_axis TEXT,
                source_context TEXT,
                UNIQUE(source_id, source_local_key)
            );
            CREATE TABLE dimension_members (
                dimension_member_id TEXT PRIMARY KEY,
                dimension TEXT NOT NULL,
                classification TEXT,
                source_value_ru TEXT NOT NULL,
                name_ru TEXT,
                name_en TEXT,
                translation_status TEXT
            );
            CREATE TABLE observations (
                observation_id TEXT PRIMARY KEY,
                source_id TEXT NOT NULL,
                source_revision_id TEXT NOT NULL REFERENCES source_revisions(source_revision_id),
                file_sha256 TEXT NOT NULL,
                source_concept_id TEXT NOT NULL REFERENCES source_concepts(source_concept_id),
                period TEXT NOT NULL,
                frequency TEXT NOT NULL,
                period_representation TEXT,
                period_role TEXT,
                value_exact TEXT NOT NULL,
                value_kind TEXT,
                unit TEXT,
                scale TEXT,
                dimensions_json TEXT NOT NULL,
                sheet_exact TEXT NOT NULL,
                cell_coordinate TEXT NOT NULL,
                raw_cell_id TEXT NOT NULL REFERENCES raw_cells(raw_cell_id),
                source_row INTEGER,
                source_row_label TEXT,
                UNIQUE(source_revision_id, sheet_exact, cell_coordinate)
            );
            CREATE TABLE raw_cell_dispositions (
                raw_cell_id TEXT PRIMARY KEY REFERENCES raw_cells(raw_cell_id),
                source_id TEXT NOT NULL,
                source_revision_id TEXT NOT NULL REFERENCES source_revisions(source_revision_id),
                role TEXT NOT NULL,
                reason TEXT NOT NULL
            );
            CREATE TABLE build_metadata (
                key TEXT PRIMARY KEY,
                json_value TEXT NOT NULL
            );

            CREATE INDEX idx_observations_source_period ON observations(source_id, period);
            CREATE INDEX idx_observations_concept_period ON observations(source_concept_id, period);
            CREATE INDEX idx_observations_frequency ON observations(frequency);
            CREATE INDEX idx_concepts_ru ON source_concepts(name_ru);
            CREATE INDEX idx_concepts_en ON source_concepts(name_en);
            CREATE INDEX idx_raw_source_sheet ON raw_cells(source_id, sheet_exact);
            CREATE INDEX idx_dispositions_role ON raw_cell_dispositions(role);
            """
        )

        revision_rows = _source_revision_rows(manifest)
        con.executemany(
            "INSERT INTO source_revisions VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?)",
            [
                (
                    r.get("source_revision_id", ""), r.get("source_id", ""), r.get("requested_url", ""),
                    r.get("resolved_url", ""), r.get("registry_filename", ""), r.get("local_path", ""),
                    r.get("sha256", ""), r.get("bytes") or None, r.get("etag", ""), r.get("last_modified", ""),
                    r.get("content_type", ""), r.get("acquired_at_utc", ""), r.get("status", ""),
                ) for r in revision_rows
            ],
        )
        con.executemany(
            "INSERT INTO raw_cells VALUES (?,?,?,?,?,?,?,?,?,?,?)",
            [tuple(r.get(k, "") for k in (
                "raw_cell_id","source_id","source_revision_id","file_sha256","sheet_exact","cell_coordinate",
                "ooxml_type","style_index","value_lexical","text_resolved","formula"
            )) for r in raw_cells],
        )
        con.executemany(
            "INSERT INTO source_concepts VALUES (?,?,?,?,?,?,?,?,?,?)",
            [tuple(r.get(k, "") for k in (
                "source_concept_id","source_id","source_local_key","label_ru_source","label_ru_normalized",
                "name_ru","name_en","translation_status","row_axis","source_context"
            )) for r in concepts],
        )
        con.executemany(
            "INSERT INTO dimension_members VALUES (?,?,?,?,?,?,?)",
            [tuple(r.get(k, "") for k in (
                "dimension_member_id","dimension","classification","source_value_ru","name_ru","name_en","translation_status"
            )) for r in dimension_members],
        )
        con.executemany(
            "INSERT INTO observations VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)",
            [tuple(r.get(k, "") for k in (
                "observation_id","source_id","source_revision_id","file_sha256","source_concept_id","period","frequency",
                "period_representation","period_role","value_exact","value_kind","unit","scale","dimensions_json",
                "sheet_exact","cell_coordinate","raw_cell_id","source_row","source_row_label"
            )) for r in observations],
        )
        con.executemany(
            "INSERT INTO raw_cell_dispositions VALUES (?,?,?,?,?)",
            [tuple(r.get(k, "") for k in ("raw_cell_id","source_id","source_revision_id","role","reason")) for r in dispositions],
        )
        con.executemany(
            "INSERT INTO build_metadata(key, json_value) VALUES (?,?)",
            (("diagnostics", _json_text(diagnostics)), ("validation", _json_text(validation))),
        )
        con.commit()
    finally:
        con.close()
    return db


def persist_bundle(
    output_dir: str | Path,
    *,
    manifest: Sequence[Mapping[str, object]],
    raw_cells: Sequence[Mapping[str, object]],
    concepts: Sequence[Mapping[str, object]],
    dimension_members: Sequence[Mapping[str, object]],
    observations: Sequence[Mapping[str, object]],
    dispositions: Sequence[Mapping[str, object]],
    diagnostics: Mapping[str, object] | Sequence[Mapping[str, object]],
    validation: Mapping[str, object],
) -> dict[str, str]:
    root = Path(output_dir)
    root.mkdir(parents=True, exist_ok=True)
    csv_paths = export_csv_bundle(
        root,
        manifest=manifest,
        raw_cells=raw_cells,
        concepts=concepts,
        dimension_members=dimension_members,
        observations=observations,
        dispositions=dispositions,
    )
    diagnostics_path = root / "diagnostics.json"
    diagnostics_path.write_text(json.dumps(diagnostics, ensure_ascii=False, indent=2), encoding="utf-8")
    validation_path = root / "validation.json"
    validation_path.write_text(json.dumps(validation, ensure_ascii=False, indent=2), encoding="utf-8")
    db_path = write_sqlite(
        root / "cbr_unified.sqlite",
        manifest=manifest,
        raw_cells=raw_cells,
        concepts=concepts,
        dimension_members=dimension_members,
        observations=observations,
        dispositions=dispositions,
        diagnostics=diagnostics,
        validation=validation,
    )
    return {**csv_paths, "diagnostics": str(diagnostics_path), "validation": str(validation_path), "sqlite": str(db_path)}
