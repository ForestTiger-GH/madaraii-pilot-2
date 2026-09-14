import json
import sqlite3

import pytest

from cbr_unified.cli import main as cli_main
from cbr_unified.persistence import write_sqlite
from cbr_unified.query import QueryError, UnifiedDatabase


def _bundle(tmp_path, *, validation_status="passed"):
    source_id = "mortgage_debt"
    revision = source_id + "@sha256:" + "a" * 64
    manifest = [{
        "source_id": source_id,
        "source_revision_id": revision,
        "requested_url": "https://www.cbr.ru/test.xlsx",
        "resolved_url": "local",
        "registry_filename": "test.xlsx",
        "local_path": str(tmp_path / "test.xlsx"),
        "sha256": "a" * 64,
        "bytes": 1,
        "acquired_at_utc": "2026-09-15T00:00:00+00:00",
        "status": "ok",
    }]
    concepts = [{
        "source_concept_id": "sc_debt",
        "source_id": source_id,
        "source_local_key": "debt",
        "label_ru_source": "Задолженность",
        "label_ru_normalized": "задолженность",
        "name_ru": "Задолженность",
        "name_en": "Debt",
        "translation_status": "project_translation",
        "row_axis": "region",
        "source_context": "Test",
    }]
    members = [{
        "dimension_member_id": "dm_moscow",
        "dimension": "region",
        "classification": "",
        "source_value_ru": "Москва",
        "name_ru": "Москва",
        "name_en": "Moskva",
        "translation_status": "transliteration_only",
    }]
    raw = []
    observations = []
    dispositions = []
    for index, (period, value, unit) in enumerate(
        (("2026-01-01", "10", "RUB"), ("2026-02-01", "20", "USD")), start=1
    ):
        raw_id = f"rc_{index}"
        raw.append({
            "raw_cell_id": raw_id,
            "source_id": source_id,
            "source_revision_id": revision,
            "file_sha256": "a" * 64,
            "sheet_exact": "Data",
            "cell_coordinate": f"B{index + 2}",
            "ooxml_type": "n",
            "style_index": "0",
            "value_lexical": value,
            "text_resolved": "",
            "formula": "",
        })
        observations.append({
            "observation_id": f"ob_{index}",
            "build_id": "bld_test",
            "source_id": source_id,
            "source_revision_id": revision,
            "file_sha256": "a" * 64,
            "source_concept_id": "sc_debt",
            "period": period,
            "frequency": "monthly",
            "period_representation": "date_string",
            "period_role": "stock",
            "value_exact": value,
            "value_kind": "numeric",
            "unit": unit,
            "scale": 1,
            "dimensions_json": json.dumps({"region": "Москва"}, ensure_ascii=False, separators=(",", ":")),
            "sheet_exact": "Data",
            "cell_coordinate": f"B{index + 2}",
            "raw_cell_id": raw_id,
            "source_row": index + 2,
            "source_row_label": "Москва",
        })
        dispositions.append({
            "raw_cell_id": raw_id,
            "source_id": source_id,
            "source_revision_id": revision,
            "role": "observation_value",
            "reason": "test",
        })
    return manifest, raw, concepts, members, observations, dispositions, {"status": validation_status}


def _write(path, bundle):
    manifest, raw, concepts, members, observations, dispositions, validation = bundle
    return write_sqlite(
        path,
        manifest=manifest,
        raw_cells=raw,
        concepts=concepts,
        dimension_members=members,
        observations=observations,
        dispositions=dispositions,
        diagnostics=[{"source_id": "mortgage_debt"}],
        validation=validation,
    )


def test_bilingual_dimension_filter_source_catalog_and_lineage_owners(tmp_path):
    db_path = _write(tmp_path / "consumer.sqlite", _bundle(tmp_path))
    db = UnifiedDatabase(db_path)

    sources = db.sources(language="en")
    assert sources.iloc[0]["display_name"] == "Housing mortgage loan debt"
    frame = db.observations(language="en", dimensions={"region": "Moskva"})
    assert len(frame) == 2
    assert set(frame["dim_region"]) == {"Moskva"}

    lineage = db.lineage("ob_1")
    assert lineage["observation_source_id"] == "mortgage_debt"
    assert lineage["concept_source_id"] == "mortgage_debt"
    assert lineage["raw_source_id"] == "mortgage_debt"
    assert lineage["disposition_source_id"] == "mortgage_debt"


def test_indicator_discovery_uses_bilingual_dataset_context(tmp_path):
    db_path = _write(tmp_path / "discovery.sqlite", _bundle(tmp_path))
    db = UnifiedDatabase(db_path)

    # The source-local concept may correctly be generic (`Debt`) while the dataset
    # carries the domain qualifier (`Housing mortgage loan debt`). Discovery must
    # use both surfaces without changing concept identity.
    hits = db.indicators("mortgage", language="en", source_ids="mortgage_debt")
    assert len(hits) == 1
    assert hits.iloc[0]["source_concept_id"] == "sc_debt"


def test_pivot_rejects_hidden_unit_change(tmp_path):
    db = UnifiedDatabase(_write(tmp_path / "pivot.sqlite", _bundle(tmp_path)))
    with pytest.raises(QueryError, match="semantically heterogeneous"):
        db.pivot(language="en", dimensions={"region": "Moskva"})


def test_query_facade_fails_closed_on_failed_embedded_validation(tmp_path):
    path = _write(tmp_path / "failed.sqlite", _bundle(tmp_path, validation_status="failed"))
    with pytest.raises(QueryError, match="validation is not passed"):
        UnifiedDatabase(path)
    diagnostic = UnifiedDatabase(path, allow_unvalidated=True)
    assert diagnostic.validation()["status"] == "failed"
    assert len(diagnostic.observations()) == 2


def test_cli_validate_is_explicit_diagnostic_surface(tmp_path, capsys):
    path = _write(tmp_path / "failed-cli.sqlite", _bundle(tmp_path, validation_status="failed"))
    assert cli_main(["validate", "--db", str(path)]) == 0
    assert '"status": "failed"' in capsys.readouterr().out


def test_failed_direct_sqlite_replacement_keeps_previous_database(tmp_path):
    path = _write(tmp_path / "atomic.sqlite", _bundle(tmp_path))
    before = UnifiedDatabase(path).observations()
    assert len(before) == 2

    broken = list(_bundle(tmp_path))
    broken_observations = [dict(row) for row in broken[4]]
    broken_observations[0]["source_concept_id"] = "missing_concept"
    broken[4] = broken_observations

    with pytest.raises(sqlite3.IntegrityError):
        _write(path, tuple(broken))

    after = UnifiedDatabase(path).observations()
    assert len(after) == 2
    assert list(after["observation_id"]) == list(before["observation_id"])
