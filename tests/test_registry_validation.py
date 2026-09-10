import json

import pytest

from cbr_unified.registry import SOURCES, SOURCE_BY_ID
from cbr_unified.validation import ValidationError, validate_bundle


def test_reviewed_registry_is_complete_and_unique():
    assert len(SOURCES) == 41
    assert len(SOURCE_BY_ID) == 41
    assert len({s.url for s in SOURCES}) == 41
    assert all(s.source_id and s.name_ru and s.name_en and s.row_axis for s in SOURCES)


def _minimal_bundle(conflicting=False):
    revision = "x@sha256:" + "a" * 64
    manifest = [{"source_id": "x", "source_revision_id": revision, "status": "ok"}]
    raw = []
    observations = []
    dispositions = []
    concepts = [{
        "source_concept_id": "sc_x",
        "source_id": "x",
        "source_local_key": "x",
        "name_ru": "X",
        "name_en": "X",
    }]
    for i, value in enumerate(("1", "2" if conflicting else "1"), start=1):
        rid = f"rc_{i}"
        raw.append({
            "raw_cell_id": rid,
            "source_id": "x",
            "source_revision_id": revision,
            "sheet_exact": "S",
            "cell_coordinate": f"B{i}",
            "ooxml_type": "n",
            "value_lexical": value,
            "formula": "",
        })
        observations.append({
            "observation_id": f"ob_{i}",
            "source_id": "x",
            "source_revision_id": revision,
            "source_concept_id": "sc_x",
            "period": "2026-01-01",
            "frequency": "monthly",
            "period_role": "stock",
            "value_exact": value,
            "unit": "RUB",
            "scale": "1",
            "dimensions_json": json.dumps({"region": "A"}, separators=(",", ":")),
            "sheet_exact": "S",
            "cell_coordinate": f"B{i}",
            "raw_cell_id": rid,
        })
        dispositions.append({
            "raw_cell_id": rid,
            "source_id": "x",
            "source_revision_id": revision,
            "role": "observation_value",
            "reason": "test",
        })
    return manifest, raw, concepts, observations, dispositions


def test_validation_reports_identical_repetition_without_dropping_it():
    manifest, raw, concepts, observations, dispositions = _minimal_bundle(False)
    result = validate_bundle(
        manifest=manifest,
        raw_cells=raw,
        concepts=concepts,
        dimension_members=[],
        observations=observations,
        dispositions=dispositions,
        diagnostics=[{"source_id": "x"}],
        require_complete=False,
    )
    assert result["status"] == "passed"
    assert len(result["identical_semantic_duplicate_groups"]) == 1
    assert result["observation_count"] == 2


def test_validation_fails_on_conflicting_semantic_duplicate():
    manifest, raw, concepts, observations, dispositions = _minimal_bundle(True)
    with pytest.raises(ValidationError, match="Conflicting semantic duplicates"):
        validate_bundle(
            manifest=manifest,
            raw_cells=raw,
            concepts=concepts,
            dimension_members=[],
            observations=observations,
            dispositions=dispositions,
            diagnostics=[{"source_id": "x"}],
            require_complete=False,
        )
