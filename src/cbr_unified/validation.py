from __future__ import annotations

import json
from collections import Counter, defaultdict
from decimal import Decimal, InvalidOperation
from typing import Mapping, Sequence

from .normalization import parse_decimal_text
from .registry import SOURCES


class ValidationError(RuntimeError):
    pass


def _unique(rows: Sequence[Mapping[str, object]], key: str, label: str) -> set[str]:
    values = [str(r.get(key, "")) for r in rows]
    missing = [i for i, v in enumerate(values) if not v]
    if missing:
        raise ValidationError(f"{label}: {key} missing in {len(missing)} rows")
    counts = Counter(values)
    dup = sorted(k for k, n in counts.items() if n > 1)
    if dup:
        raise ValidationError(f"{label}: duplicate {key}: {dup[:8]}")
    return set(values)


def _decimal(value: object) -> Decimal:
    try:
        return Decimal(str(value))
    except (InvalidOperation, ValueError) as exc:
        raise ValidationError(f"Observation value_exact is not decimal: {value!r}") from exc


def validate_bundle(
    *,
    manifest: Sequence[Mapping[str, object]],
    raw_cells: Sequence[Mapping[str, object]],
    concepts: Sequence[Mapping[str, object]],
    dimension_members: Sequence[Mapping[str, object]],
    observations: Sequence[Mapping[str, object]],
    dispositions: Sequence[Mapping[str, object]],
    diagnostics: Sequence[Mapping[str, object]],
    require_complete: bool = True,
) -> dict[str, object]:
    expected = {s.source_id for s in SOURCES}
    manifest_ids = [str(r.get("source_id", "")) for r in manifest]
    manifest_set = set(manifest_ids)
    if len(manifest_ids) != len(manifest_set):
        raise ValidationError("Manifest contains duplicate source_id")
    if require_complete and manifest_set != expected:
        raise ValidationError(
            f"Source universe mismatch: missing={sorted(expected-manifest_set)} extra={sorted(manifest_set-expected)}"
        )
    failed = [str(r.get("source_id")) for r in manifest if r.get("status") != "ok"]
    if failed:
        raise ValidationError(f"Failed source revisions present: {failed}")

    revision_ids = _unique(manifest, "source_revision_id", "manifest")
    raw_ids = _unique(raw_cells, "raw_cell_id", "raw_cells")
    concept_ids = _unique(concepts, "source_concept_id", "source_concepts")
    _unique(dimension_members, "dimension_member_id", "dimension_members") if dimension_members else set()
    obs_ids = _unique(observations, "observation_id", "observations")
    disposition_ids = _unique(dispositions, "raw_cell_id", "raw_cell_dispositions")

    if raw_ids != disposition_ids:
        raise ValidationError(
            f"Raw-cell disposition coverage mismatch: without_disposition={len(raw_ids-disposition_ids)} "
            f"unknown_dispositions={len(disposition_ids-raw_ids)}"
        )

    manifest_revision_by_source = {str(r["source_id"]): str(r["source_revision_id"]) for r in manifest}
    raw_by_id = {str(r["raw_cell_id"]): r for r in raw_cells}
    concept_by_id = {str(r["source_concept_id"]): r for r in concepts}
    disp_by_id = {str(r["raw_cell_id"]): r for r in dispositions}

    obs_source_counts: Counter[str] = Counter()
    semantic_keys: dict[tuple[str, ...], list[Mapping[str, object]]] = defaultdict(list)
    observation_raw_ids: set[str] = set()
    source_periods: dict[str, set[str]] = defaultdict(set)
    source_frequencies: dict[str, set[str]] = defaultdict(set)

    for obs in observations:
        sid = str(obs.get("source_id", ""))
        rev = str(obs.get("source_revision_id", ""))
        raw_id = str(obs.get("raw_cell_id", ""))
        concept_id = str(obs.get("source_concept_id", ""))
        if sid not in manifest_set:
            raise ValidationError(f"Observation references unknown source: {sid}")
        if rev not in revision_ids or manifest_revision_by_source.get(sid) != rev:
            raise ValidationError(f"Observation revision mismatch: {sid} / {rev}")
        if raw_id not in raw_by_id:
            raise ValidationError(f"Observation references unknown raw cell: {raw_id}")
        if concept_id not in concept_by_id:
            raise ValidationError(f"Observation references unknown concept: {concept_id}")
        raw = raw_by_id[raw_id]
        if str(raw.get("source_id")) != sid or str(raw.get("source_revision_id")) != rev:
            raise ValidationError(f"Observation/raw lineage mismatch: {obs.get('observation_id')}")
        if str(raw.get("sheet_exact")) != str(obs.get("sheet_exact")) or str(raw.get("cell_coordinate")) != str(obs.get("cell_coordinate")):
            raise ValidationError(f"Observation/raw locator mismatch: {obs.get('observation_id')}")
        if disp_by_id[raw_id].get("role") != "observation_value":
            raise ValidationError(f"Observed raw cell lacks observation_value disposition: {raw_id}")
        _decimal(obs.get("value_exact", ""))
        try:
            dims = json.loads(str(obs.get("dimensions_json", "{}")))
        except json.JSONDecodeError as exc:
            raise ValidationError(f"Invalid dimensions_json: {obs.get('observation_id')}") from exc
        if not isinstance(dims, dict):
            raise ValidationError(f"dimensions_json must be an object: {obs.get('observation_id')}")
        period = str(obs.get("period", ""))
        if len(period) != 10 or period[4:5] != "-" or period[7:8] != "-":
            raise ValidationError(f"Non-ISO period anchor: {period!r}")

        observation_raw_ids.add(raw_id)
        obs_source_counts[sid] += 1
        source_periods[sid].add(period)
        source_frequencies[sid].add(str(obs.get("frequency", "")))
        key = (
            sid,
            concept_id,
            period,
            str(obs.get("frequency", "")),
            str(obs.get("period_role", "")),
            str(obs.get("unit", "")),
            str(obs.get("scale", "")),
            str(obs.get("dimensions_json", "")),
        )
        semantic_keys[key].append(obs)

    if require_complete:
        no_obs = sorted(s for s in expected if obs_source_counts[s] == 0)
        if no_obs:
            raise ValidationError(f"Sources with zero semantic observations: {no_obs}")

    duplicate_groups: list[dict[str, object]] = []
    conflicting_groups: list[dict[str, object]] = []
    for key, rows in semantic_keys.items():
        if len(rows) < 2:
            continue
        values = {str(r.get("value_exact", "")) for r in rows}
        item = {
            "source_id": key[0],
            "source_concept_id": key[1],
            "period": key[2],
            "count": len(rows),
            "values": sorted(values),
            "locators": [f"{r.get('sheet_exact')}!{r.get('cell_coordinate')}" for r in rows],
        }
        if len(values) > 1:
            conflicting_groups.append(item)
        else:
            duplicate_groups.append(item)
    if conflicting_groups:
        first = conflicting_groups[0]
        raise ValidationError(
            f"Conflicting semantic duplicates detected ({len(conflicting_groups)} groups); first={first}"
        )

    numeric_raw = 0
    formula_raw = 0
    roles: Counter[str] = Counter()
    source_raw_counts: Counter[str] = Counter()
    source_observed_raw_counts: Counter[str] = Counter()
    unresolved_numeric: list[dict[str, str]] = []
    for raw in raw_cells:
        sid = str(raw.get("source_id", ""))
        source_raw_counts[sid] += 1
        lexical = str(raw.get("value_lexical", ""))
        resolved = str(raw.get("text_resolved", ""))
        if parse_decimal_text(lexical) is not None or parse_decimal_text(resolved) is not None:
            numeric_raw += 1
        if str(raw.get("formula", "")):
            formula_raw += 1
        role = str(disp_by_id[str(raw["raw_cell_id"])].get("role", ""))
        roles[role] += 1
        if role == "unmapped_numeric":
            unresolved_numeric.append({
                "source_id": sid,
                "sheet": str(raw.get("sheet_exact", "")),
                "cell": str(raw.get("cell_coordinate", "")),
                "value": lexical or resolved,
            })
        if str(raw["raw_cell_id"]) in observation_raw_ids:
            source_observed_raw_counts[sid] += 1

    if require_complete and unresolved_numeric:
        raise ValidationError(
            f"Unmapped numeric source cells block semantic completeness: count={len(unresolved_numeric)} "
            f"sample={unresolved_numeric[:12]}"
        )

    diag_by_source = {str(d.get("source_id")): d for d in diagnostics}
    missing_diag = sorted(manifest_set - set(diag_by_source))
    if missing_diag:
        raise ValidationError(f"Missing source diagnostics: {missing_diag}")

    return {
        "status": "passed",
        "source_count": len(manifest),
        "raw_cell_count": len(raw_cells),
        "numeric_raw_cell_count": numeric_raw,
        "formula_raw_cell_count": formula_raw,
        "observation_count": len(observations),
        "source_concept_count": len(concepts),
        "dimension_member_count": len(dimension_members),
        "disposition_count": len(dispositions),
        "unmapped_numeric_count": len(unresolved_numeric),
        "unmapped_numeric_sample": unresolved_numeric[:50],
        "raw_disposition_coverage": 1.0 if raw_cells else 1.0,
        "observation_raw_lineage_coverage": 1.0 if observations else 1.0,
        "observation_sources": dict(sorted(obs_source_counts.items())),
        "raw_cells_by_source": dict(sorted(source_raw_counts.items())),
        "observed_raw_cells_by_source": dict(sorted(source_observed_raw_counts.items())),
        "period_count_by_source": {k: len(v) for k, v in sorted(source_periods.items())},
        "frequencies_by_source": {k: sorted(v) for k, v in sorted(source_frequencies.items())},
        "disposition_roles": dict(sorted(roles.items())),
        "identical_semantic_duplicate_groups": duplicate_groups,
        "conflicting_semantic_duplicate_groups": [],
        "invariants": {
            "complete_registry_universe": manifest_set == expected,
            "every_raw_cell_dispositioned": raw_ids == disposition_ids,
            "every_observation_has_raw_lineage": len(observation_raw_ids) == len(obs_ids),
            "every_source_has_observations": all(obs_source_counts[s] > 0 for s in manifest_set),
            "zero_unmapped_numeric": len(unresolved_numeric) == 0,
            "no_conflicting_semantic_duplicates": True,
        },
    }
