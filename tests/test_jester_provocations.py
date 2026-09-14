from __future__ import annotations

import json
from decimal import Decimal

import pytest
from openpyxl import Workbook

from cbr_unified.normalization import parse_decimal_text, parse_period
from cbr_unified.persistence import write_sqlite
from cbr_unified.query import QueryError, UnifiedDatabase
from cbr_unified.semantic import _dimension_member, discover_period_bindings


def _precision_db(tmp_path, values=("0.12345678901234567890123456789",)):
    revision = "precision@sha256:" + "a" * 64
    manifest = [{
        "source_id": "precision",
        "source_revision_id": revision,
        "requested_url": "https://example.invalid/precision.xlsx",
        "resolved_url": "local",
        "registry_filename": "precision.xlsx",
        "local_path": str(tmp_path / "precision.xlsx"),
        "sha256": "a" * 64,
        "bytes": 1,
        "acquired_at_utc": "2026-09-14T20:30:00+00:00",
        "status": "ok",
    }]
    concepts = [{
        "source_concept_id": "sc_precision",
        "source_id": "precision",
        "source_local_key": "measure",
        "label_ru_source": "Неприлично точный показатель",
        "label_ru_normalized": "неприлично точный показатель",
        "name_ru": "Неприлично точный показатель",
        "name_en": "Indecently precise indicator",
        "translation_status": "project_translation",
        "row_axis": "indicator",
        "source_context": "Jester fixture",
    }]
    raw, obs, dispositions = [], [], []
    for i, value in enumerate(values, start=1):
        raw_id = f"rc_{i}"
        raw.append({
            "raw_cell_id": raw_id,
            "source_id": "precision",
            "source_revision_id": revision,
            "file_sha256": "a" * 64,
            "sheet_exact": "Data",
            "cell_coordinate": f"B{i+2}",
            "ooxml_type": "n",
            "style_index": "0",
            "value_lexical": value,
            "text_resolved": "",
            "formula": "",
        })
        obs.append({
            "observation_id": f"ob_{i}",
            "source_id": "precision",
            "source_revision_id": revision,
            "file_sha256": "a" * 64,
            "source_concept_id": "sc_precision",
            "period": f"2026-0{i}-01",
            "frequency": "monthly",
            "period_representation": "date_string",
            "period_role": "stock",
            "value_exact": value,
            "value_kind": "numeric",
            "unit": "RUB",
            "scale": 1,
            "dimensions_json": json.dumps({"region": "A"}, ensure_ascii=False, separators=(",", ":")),
            "sheet_exact": "Data",
            "cell_coordinate": f"B{i+2}",
            "raw_cell_id": raw_id,
            "source_row": i + 2,
            "source_row_label": "A",
        })
        dispositions.append({
            "raw_cell_id": raw_id,
            "source_id": "precision",
            "source_revision_id": revision,
            "role": "observation_value",
            "reason": "jester_precision_fixture",
        })
    path = tmp_path / "jester.sqlite"
    write_sqlite(
        path,
        manifest=manifest,
        raw_cells=raw,
        concepts=concepts,
        dimension_members=[],
        observations=obs,
        dispositions=dispositions,
        diagnostics=[{"source_id": "precision"}],
        validation={"status": "jester_fixture"},
    )
    return UnifiedDatabase(path)


def test_jester_adaptive_trajectory(tmp_path):
    print("\n[JST-P01] precision stripper: let the convenient numeric surface wear the raw ledger's suit")
    exact = Decimal("0.12345678901234567890123456789")
    db = _precision_db(tmp_path)
    frame = db.observations(source_ids="precision")
    convenient = frame.iloc[0]["value"]
    exact_text = frame.iloc[0]["value_exact"]
    print("value_exact=", exact_text)
    print("value(repr)=", repr(convenient))
    print("decimal(str(value))=", Decimal(str(convenient)))
    print("precision_preserved_on_convenience_surface=", Decimal(str(convenient)) == exact)

    print("\n[JST-P02] pivot in a tuxedo: does the default 2D view inherit that precision laundering?")
    pivot = db.pivot(source_ids="precision")
    pivot_value = pivot.iloc[0, 0]
    print("pivot_value(repr)=", repr(pivot_value))
    print("pivot_exact_after_roundtrip=", Decimal(str(pivot_value)) == exact)

    print("\n[JST-P03] passport office from hell: same regional label in two regimes asks for two identities")
    regime_a = _dimension_member("region", "Москва")
    regime_b = _dimension_member("region", "Москва")
    print("member_a=", regime_a["dimension_member_id"])
    print("member_b=", regime_b["dimension_member_id"])
    print("source_or_regime_scoped=", regime_a["dimension_member_id"] != regime_b["dimension_member_id"])

    print("\n[JST-P04] calendar bureaucrat: the parser knows 2026, discovery pretends an integer 2026 is furniture")
    wb = Workbook()
    ws = wb.active
    ws.append(["Region", 2024, 2025, 2026])
    ws.append(["A", 1, 2, 3])
    bindings = discover_period_bindings(ws, "jester_years")
    print("parse_period_string_2026=", parse_period("2026"))
    print("discovered_integer_year_bindings=", [(b.coordinate, b.period, b.frequency) for b in bindings])

    print("\n[JST-P05] dash cult: ask whether punctuation can be promoted to money")
    print("dash_decimal=", parse_decimal_text("-"))
    print("em_dash_decimal=", parse_decimal_text("—"))

    print("\n[JST-P06] identical-name masquerade: two values demand one pivot cell")
    revision = "mask@sha256:" + "b" * 64
    manifest = [{
        "source_id": "mask", "source_revision_id": revision,
        "requested_url": "https://example.invalid/mask.xlsx", "resolved_url": "local",
        "registry_filename": "mask.xlsx", "local_path": str(tmp_path / "mask.xlsx"),
        "sha256": "b" * 64, "bytes": 1, "acquired_at_utc": "2026-09-14T20:30:00+00:00", "status": "ok",
    }]
    concepts = [
        {"source_concept_id":"sc_a","source_id":"mask","source_local_key":"a","label_ru_source":"A","label_ru_normalized":"a","name_ru":"Одинаково","name_en":"Same","translation_status":"project_translation","row_axis":"indicator","source_context":"Jester"},
        {"source_concept_id":"sc_b","source_id":"mask","source_local_key":"b","label_ru_source":"B","label_ru_normalized":"b","name_ru":"Одинаково","name_en":"Same","translation_status":"project_translation","row_axis":"indicator","source_context":"Jester"},
    ]
    raw, obs, dispositions = [], [], []
    for i, concept in enumerate(("sc_a", "sc_b"), start=1):
        rid = f"mask_rc_{i}"
        raw.append({"raw_cell_id":rid,"source_id":"mask","source_revision_id":revision,"file_sha256":"b"*64,"sheet_exact":"Data","cell_coordinate":f"B{i+2}","ooxml_type":"n","style_index":"0","value_lexical":str(i),"text_resolved":"","formula":""})
        obs.append({"observation_id":f"mask_ob_{i}","source_id":"mask","source_revision_id":revision,"file_sha256":"b"*64,"source_concept_id":concept,"period":"2026-01-01","frequency":"monthly","period_representation":"date_string","period_role":"stock","value_exact":str(i),"value_kind":"numeric","unit":"RUB","scale":1,"dimensions_json":"{}","sheet_exact":"Data","cell_coordinate":f"B{i+2}","raw_cell_id":rid,"source_row":i+2,"source_row_label":concept})
        dispositions.append({"raw_cell_id":rid,"source_id":"mask","source_revision_id":revision,"role":"observation_value","reason":"jester_mask_fixture"})
    mask_path = tmp_path / "mask.sqlite"
    write_sqlite(mask_path, manifest=manifest, raw_cells=raw, concepts=concepts, dimension_members=[], observations=obs, dispositions=dispositions, diagnostics=[{"source_id":"mask"}], validation={"status":"jester_fixture"})
    mask_db = UnifiedDatabase(mask_path)
    try:
        mask_db.pivot(source_ids="mask", language="en")
        print("ambiguous_pivot= SILENTLY_ACCEPTED")
    except QueryError as exc:
        print("ambiguous_pivot= FAIL_CLOSED")
        print("error_prefix=", str(exc).split("Sample=")[0].strip())

    # Jester Report owns interpretation; this probe records behavior only.
    assert True
