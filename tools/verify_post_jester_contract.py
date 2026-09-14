from __future__ import annotations

import argparse
import json
from pathlib import Path

from cbr_unified.query import UnifiedDatabase


def load_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("product_root")
    parser.add_argument("output")
    args = parser.parse_args()
    root = Path(args.product_root)

    build = load_json(root / "build_manifest.json")
    validation = load_json(root / "data" / "validation.json")
    manifest = load_json(root / "source_manifest.json")

    if validation.get("status") != "passed":
        raise AssertionError("Candidate validation is not passed")
    invariants = validation.get("invariants", {})
    for required in (
        "single_build_identity",
        "complete_registry_universe",
        "every_raw_cell_dispositioned",
        "every_observation_has_raw_lineage",
        "every_source_has_observations",
        "zero_unmapped_numeric",
        "no_conflicting_semantic_duplicates",
        "cross_owner_source_coherence",
        "bilingual_user_surface_complete",
    ):
        if not invariants.get(required):
            raise AssertionError(f"Required invariant is false: {required}")

    implementation_sha = str(build.get("implementation_sha256", ""))
    runtime = build.get("runtime_versions", {})
    if len(implementation_sha) != 64:
        raise AssertionError("Build manifest does not bind implementation SHA-256")
    for required in ("python", "requests", "openpyxl", "pandas"):
        if not isinstance(runtime, dict) or not str(runtime.get(required, "")):
            raise AssertionError(f"Build manifest lacks resolved runtime version: {required}")
    if validation.get("implementation_sha256") != implementation_sha:
        raise AssertionError("Validation and build manifest implementation fingerprints differ")
    if validation.get("runtime_versions") != runtime:
        raise AssertionError("Validation and build manifest runtime fingerprints differ")

    bad_trust = [
        row.get("source_id") for row in manifest
        if row.get("trust_status") != "cbr_domain_ooxml_validated"
    ]
    if bad_trust:
        raise AssertionError(f"Live source revisions lack CBR+OOXML trust admission: {bad_trust}")

    db = UnifiedDatabase(root / "data" / "cbr_unified.sqlite")
    sources_en = db.sources(language="en")
    if sources_en.empty or not sources_en["display_name"].astype(str).str.strip().all():
        raise AssertionError("English source catalog is incomplete")

    mortgage = db.observations(source_ids="mortgage_debt", language="en")
    if mortgage.empty or "dim_region" not in mortgage.columns:
        raise AssertionError("English regional query surface is unavailable")
    region_values = [str(value) for value in mortgage["dim_region"] if str(value).strip()]
    if not region_values:
        raise AssertionError("English dimension-member projection is empty")
    region_en = region_values[0]
    filtered = db.observations(
        source_ids="mortgage_debt",
        language="en",
        dimensions={"region": region_en},
    )
    if filtered.empty:
        raise AssertionError("English dimension-member filtering is not symmetric with display")

    observation_id = str(mortgage.iloc[0]["observation_id"])
    lineage = db.lineage(observation_id)
    for owner in (
        "observation_source_id",
        "concept_source_id",
        "raw_source_id",
        "disposition_source_id",
    ):
        if owner not in lineage:
            raise AssertionError(f"Lineage does not expose source owner: {owner}")
    if len({str(lineage[owner]) for owner in (
        "observation_source_id", "concept_source_id", "raw_source_id", "disposition_source_id"
    )}) != 1:
        raise AssertionError("Validated lineage exposes cross-owner source disagreement")

    report = {
        "status": "passed",
        "build_id": build.get("build_id"),
        "implementation_sha256": implementation_sha,
        "runtime_versions": runtime,
        "source_trust_count": len(manifest),
        "required_invariants": {key: bool(invariants.get(key)) for key in sorted(invariants)},
        "english_source_catalog_count": len(sources_en),
        "english_dimension_filter_sample": {
            "region": region_en,
            "rows": len(filtered),
        },
        "lineage_owner_sample": {
            key: lineage[key] for key in (
                "observation_source_id",
                "concept_source_id",
                "raw_source_id",
                "disposition_source_id",
            )
        },
    }
    output = Path(args.output)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps(report, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
