from __future__ import annotations

import hashlib
import json
import shutil
import sys
from pathlib import Path

from cbr_unified import SOURCES, UnifiedDatabase, build_database


DETERMINISTIC_TABLES = (
    "raw_cells.csv",
    "source_concepts.csv",
    "dimension_members.csv",
    "observations.csv",
    "raw_cell_dispositions.csv",
)


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as fh:
        for chunk in iter(lambda: fh.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def load_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def main(argv: list[str] | None = None) -> int:
    argv = argv or sys.argv[1:]
    root = Path(argv[0]) if argv else Path("_verification")
    if root.exists():
        shutil.rmtree(root)
    root.mkdir(parents=True)
    live = root / "live"
    replay = root / "replay"

    live_result = build_database(live)
    replay_result = build_database(replay, input_dir=live / "sources")

    live_validation = load_json(live / "data" / "validation.json")
    replay_validation = load_json(replay / "data" / "validation.json")
    if live_validation.get("status") != "passed" or replay_validation.get("status") != "passed":
        raise AssertionError("Live or replay validation did not pass")
    if live_result.source_count != len(SOURCES) or replay_result.source_count != len(SOURCES):
        raise AssertionError(f"Expected {len(SOURCES)} sources in both builds")
    if live_result.raw_cell_count != replay_result.raw_cell_count:
        raise AssertionError("Raw-cell count differs between live and replay")
    if live_result.observation_count != replay_result.observation_count:
        raise AssertionError("Observation count differs between live and replay")

    live_manifest = {r["source_id"]: r for r in load_json(live / "source_manifest.json")}
    replay_manifest = {r["source_id"]: r for r in load_json(replay / "source_manifest.json")}
    if set(live_manifest) != set(replay_manifest):
        raise AssertionError("Source identity sets differ between live and replay")
    revision_mismatches = []
    for sid in sorted(live_manifest):
        if live_manifest[sid]["sha256"] != replay_manifest[sid]["sha256"]:
            revision_mismatches.append(sid)
        if live_manifest[sid]["source_revision_id"] != replay_manifest[sid]["source_revision_id"]:
            revision_mismatches.append(sid)
    if revision_mismatches:
        raise AssertionError(f"Replay revision mismatch: {sorted(set(revision_mismatches))}")

    table_hashes: dict[str, dict[str, str]] = {}
    for filename in DETERMINISTIC_TABLES:
        live_path = live / "data" / filename
        replay_path = replay / "data" / filename
        lhs = sha256(live_path)
        rhs = sha256(replay_path)
        table_hashes[filename] = {"live": lhs, "replay": rhs, "identical": lhs == rhs}
        if lhs != rhs:
            raise AssertionError(f"Deterministic table differs on replay: {filename}")

    db = UnifiedDatabase(live_result.sqlite_path)
    embedded_validation = db.validation()
    if embedded_validation.get("status") != "passed":
        raise AssertionError("SQLite embedded validation is not passed")
    sources_df = db.sources()
    if len(sources_df) != len(SOURCES):
        raise AssertionError("SQLite source count mismatch")
    sample = db.observations(source_ids="mortgage_debt", language="en")
    if sample.empty:
        raise AssertionError("Query smoke test returned no mortgage_debt observations")
    if "indicator" not in sample or "value_exact" not in sample:
        raise AssertionError("Query surface lacks required convenience columns")
    indicator_hits = db.indicators("mortgage", language="en", source_ids="mortgage_debt")
    if indicator_hits.empty:
        raise AssertionError("English indicator lookup returned no expected mortgage result")
    lineage = db.lineage(str(sample.iloc[0]["observation_id"]))
    for required in ("requested_url", "sha256", "sheet_exact", "cell_coordinate", "value_lexical", "disposition_role"):
        if required not in lineage:
            raise AssertionError(f"Lineage smoke test missing {required}")

    report = {
        "status": "passed",
        "registry_source_count": len(SOURCES),
        "live": {
            "raw_cell_count": live_result.raw_cell_count,
            "observation_count": live_result.observation_count,
            "source_concept_count": live_validation.get("source_concept_count"),
            "dimension_member_count": live_validation.get("dimension_member_count"),
            "formula_raw_cell_count": live_validation.get("formula_raw_cell_count"),
            "identical_semantic_duplicate_groups": len(live_validation.get("identical_semantic_duplicate_groups", [])),
        },
        "replay": {
            "raw_cell_count": replay_result.raw_cell_count,
            "observation_count": replay_result.observation_count,
        },
        "source_revisions_identical": True,
        "deterministic_table_hashes": table_hashes,
        "query_smoke": {
            "mortgage_rows": len(sample),
            "english_indicator_hits": len(indicator_hits),
            "sample_observation_id": str(sample.iloc[0]["observation_id"]),
            "sample_raw_cell_id": str(sample.iloc[0]["raw_cell_id"]),
        },
    }
    report_path = root / "full-build-report.json"
    report_path.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps(report, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
