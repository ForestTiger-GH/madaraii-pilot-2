import json

import pytest

from cbr_unified.persistence import write_sqlite
from cbr_unified.query import QueryError, UnifiedDatabase


def _bundle(tmp_path):
    revision = "x@sha256:" + "a" * 64
    manifest = [{
        "source_id": "x",
        "source_revision_id": revision,
        "requested_url": "https://example.invalid/x.xlsx",
        "resolved_url": "local",
        "registry_filename": "x.xlsx",
        "local_path": str(tmp_path / "x.xlsx"),
        "sha256": "a" * 64,
        "bytes": 1,
        "acquired_at_utc": "2026-09-11T00:00:00+00:00",
        "status": "ok",
    }]
    concepts = [{
        "source_concept_id": "sc_x",
        "source_id": "x",
        "source_local_key": "measure",
        "label_ru_source": "Показатель",
        "label_ru_normalized": "показатель",
        "name_ru": "Показатель",
        "name_en": "Indicator",
        "translation_status": "project_translation",
        "row_axis": "indicator",
        "source_context": "Тест",
    }]
    raw = []
    obs = []
    dispositions = []
    for i, (coord, value, region) in enumerate((("B3", "10.5", "A"), ("B4", "20.5", "B")), start=1):
        raw_id = f"rc_{i}"
        raw.append({
            "raw_cell_id": raw_id,
            "source_id": "x",
            "source_revision_id": revision,
            "file_sha256": "a" * 64,
            "sheet_exact": "Data",
            "cell_coordinate": coord,
            "ooxml_type": "n",
            "style_index": "0",
            "value_lexical": value,
            "text_resolved": "",
            "formula": "",
        })
        obs.append({
            "observation_id": f"ob_{i}",
            "source_id": "x",
            "source_revision_id": revision,
            "file_sha256": "a" * 64,
            "source_concept_id": "sc_x",
            "period": "2026-08-01",
            "frequency": "monthly",
            "period_representation": "date_string",
            "period_role": "stock",
            "value_exact": value,
            "value_kind": "numeric",
            "unit": "RUB",
            "scale": 1,
            "dimensions_json": json.dumps({"region": region}, ensure_ascii=False, separators=(",", ":")),
            "sheet_exact": "Data",
            "cell_coordinate": coord,
            "raw_cell_id": raw_id,
            "source_row": i + 2,
            "source_row_label": region,
        })
        dispositions.append({
            "raw_cell_id": raw_id,
            "source_id": "x",
            "source_revision_id": revision,
            "role": "observation_value",
            "reason": "period_bound_numeric_value",
        })
    return manifest, raw, concepts, obs, dispositions


def test_sqlite_query_lineage_and_fail_closed_pivot(tmp_path):
    manifest, raw, concepts, observations, dispositions = _bundle(tmp_path)
    db_path = tmp_path / "test.sqlite"
    write_sqlite(
        db_path,
        manifest=manifest,
        raw_cells=raw,
        concepts=concepts,
        dimension_members=[],
        observations=observations,
        dispositions=dispositions,
        diagnostics=[{"source_id": "x"}],
        validation={"status": "passed"},
    )
    db = UnifiedDatabase(db_path)
    df = db.observations(source_ids="x", dimensions={"region": "A"}, language="en")
    assert len(df) == 1
    assert df.iloc[0]["indicator"] == "Indicator"
    assert df.iloc[0]["value_exact"] == "10.5"
    lineage = db.lineage("ob_1")
    assert lineage["value_lexical"] == "10.5"
    assert lineage["dimensions"] == {"region": "A"}

    with pytest.raises(QueryError, match="Pivot is ambiguous"):
        db.pivot(source_ids="x", language="en")

    pivot = db.pivot(source_ids="x", dimensions={"region": "A"}, language="en")
    assert float(pivot.iloc[0, 0]) == 10.5
