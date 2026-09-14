from __future__ import annotations

import json
from collections import Counter, defaultdict
from datetime import date
from decimal import Decimal, InvalidOperation
from typing import Mapping, Sequence

from .normalization import parse_decimal_text
from .registry import SOURCES


class ValidationError(RuntimeError):
    pass


ALLOWED_TRANSLATION_STATUSES = {"cbr_official", "project_translation", "transliteration_only"}
ALLOWED_FREQUENCIES = {"monthly", "quarterly", "annual"}
ALLOWED_PERIOD_ROLES = {"stock", "flow", "published_change", "source_defined"}


def _unique(rows: Sequence[Mapping[str, object]], key: str, label: str) -> set[str]:
    values = [str(row.get(key, "")) for row in rows]
    missing = [i for i, value in enumerate(values) if not value]
    if missing:
        raise ValidationError(f"{label}: {key} missing in {len(missing)} rows")
    counts = Counter(values)
    duplicates = sorted(key_value for key_value, count in counts.items() if count > 1)
    if duplicates:
        raise ValidationError(f"{label}: duplicate {key}: {duplicates[:8]}")
    return set(values)


def _decimal(value: object) -> Decimal:
    try:
        return Decimal(str(value))
    except (InvalidOperation, ValueError) as exc:
        raise ValidationError(f"Observation value_exact is not decimal: {value!r}") from exc


def _validate_bilingual_rows(
    rows: Sequence[Mapping[str, object]],
    *,
    label: str,
    source_label_field: str,
) -> Counter[str]:
    required = (source_label_field, "name_ru", "name_en", "translation_status")
    missing: list[dict[str, object]] = []
    invalid_status: list[dict[str, object]] = []
    statuses: Counter[str] = Counter()
    for index, row in enumerate(rows):
        absent = [field for field in required if not str(row.get(field, "")).strip()]
        if absent:
            missing.append({"row": index, "fields": absent})
            continue
        status = str(row.get("translation_status", "")).strip()
        statuses[status] += 1
        if status not in ALLOWED_TRANSLATION_STATUSES:
            invalid_status.append({"row": index, "status": status})
    if missing:
        raise ValidationError(f"{label}: incomplete bilingual/source surface in {len(missing)} rows; sample={missing[:8]}")
    if invalid_status:
        raise ValidationError(f"{label}: invalid translation_status in {len(invalid_status)} rows; sample={invalid_status[:8]}")
    return statuses


def _canonical_dimensions(value: object, observation_id: object) -> str:
    try:
        parsed = json.loads(str(value or "{}"))
    except json.JSONDecodeError as exc:
        raise ValidationError(f"Invalid dimensions_json: {observation_id}") from exc
    if not isinstance(parsed, dict):
        raise ValidationError(f"dimensions_json must be an object: {observation_id}")
    if any(not str(key).strip() for key in parsed):
        raise ValidationError(f"dimensions_json contains an empty key: {observation_id}")
    return json.dumps(parsed, ensure_ascii=False, sort_keys=True, separators=(",", ":"))


def _validate_period(value: object, observation_id: object) -> str:
    period = str(value or "")
    try:
        parsed = date.fromisoformat(period)
    except ValueError as exc:
        raise ValidationError(f"Invalid ISO calendar period {period!r}: {observation_id}") from exc
    if parsed.isoformat() != period:
        raise ValidationError(f"Non-canonical ISO period anchor {period!r}: {observation_id}")
    return period


def _validate_scale(value: object, observation_id: object) -> None:
    if value in (None, ""):
        return
    try:
        parsed = Decimal(str(value))
    except (InvalidOperation, ValueError) as exc:
        raise ValidationError(f"Invalid scale {value!r}: {observation_id}") from exc
    if parsed <= 0 or parsed != parsed.to_integral_value():
        raise ValidationError(f"Scale must be a positive integer when present: {value!r}: {observation_id}")


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
    expected = {source.source_id for source in SOURCES}
    manifest_ids = [str(row.get("source_id", "")) for row in manifest]
    manifest_set = set(manifest_ids)
    if len(manifest_ids) != len(manifest_set):
        raise ValidationError("Manifest contains duplicate source_id")
    if require_complete and manifest_set != expected:
        raise ValidationError(
            f"Source universe mismatch: missing={sorted(expected-manifest_set)} extra={sorted(manifest_set-expected)}"
        )
    failed = [str(row.get("source_id")) for row in manifest if row.get("status") != "ok"]
    if failed:
        raise ValidationError(f"Failed source revisions present: {failed}")

    source_name_gaps = [
        source.source_id for source in SOURCES
        if not str(source.name_ru).strip() or not str(source.name_en).strip()
    ]
    if source_name_gaps:
        raise ValidationError(f"Registry sources missing bilingual dataset names: {source_name_gaps}")

    revision_ids = _unique(manifest, "source_revision_id", "manifest")
    raw_ids = _unique(raw_cells, "raw_cell_id", "raw_cells")
    concept_ids = _unique(concepts, "source_concept_id", "source_concepts")
    if dimension_members:
        _unique(dimension_members, "dimension_member_id", "dimension_members")
    obs_ids = _unique(observations, "observation_id", "observations")
    disposition_ids = _unique(dispositions, "raw_cell_id", "raw_cell_dispositions")

    concept_translation_statuses = _validate_bilingual_rows(
        concepts, label="source_concepts", source_label_field="label_ru_source"
    )
    member_translation_statuses = _validate_bilingual_rows(
        dimension_members, label="dimension_members", source_label_field="source_value_ru"
    )

    if raw_ids != disposition_ids:
        raise ValidationError(
            f"Raw-cell disposition coverage mismatch: without_disposition={len(raw_ids-disposition_ids)} "
            f"unknown_dispositions={len(disposition_ids-raw_ids)}"
        )

    manifest_by_source = {str(row["source_id"]): row for row in manifest}
    manifest_revision_by_source = {
        source_id: str(row["source_revision_id"]) for source_id, row in manifest_by_source.items()
    }
    raw_by_id = {str(row["raw_cell_id"]): row for row in raw_cells}
    concept_by_id = {str(row["source_concept_id"]): row for row in concepts}
    disp_by_id = {str(row["raw_cell_id"]): row for row in dispositions}

    for raw_id, raw in raw_by_id.items():
        sid = str(raw.get("source_id", ""))
        rev = str(raw.get("source_revision_id", ""))
        if sid not in manifest_set or manifest_revision_by_source.get(sid) != rev:
            raise ValidationError(f"Raw-cell source/revision ownership mismatch: {raw_id}: {sid}/{rev}")
        manifest_sha = str(manifest_by_source[sid].get("sha256", ""))
        raw_sha = str(raw.get("file_sha256", ""))
        if manifest_sha and raw_sha != manifest_sha:
            raise ValidationError(f"Raw-cell file hash mismatch: {raw_id}")
        disposition = disp_by_id[raw_id]
        if str(disposition.get("source_id", "")) != sid or str(disposition.get("source_revision_id", "")) != rev:
            raise ValidationError(f"Raw/disposition ownership mismatch: {raw_id}")

    for concept_id, concept in concept_by_id.items():
        if str(concept.get("source_id", "")) not in manifest_set:
            raise ValidationError(f"Concept references unknown source: {concept_id}")

    obs_source_counts: Counter[str] = Counter()
    semantic_keys: dict[tuple[str, ...], list[Mapping[str, object]]] = defaultdict(list)
    observation_raw_ids: list[str] = []
    source_periods: dict[str, set[str]] = defaultdict(set)
    source_frequencies: dict[str, set[str]] = defaultdict(set)
    build_ids: set[str] = set()

    for obs in observations:
        observation_id = obs.get("observation_id")
        build_id = str(obs.get("build_id", ""))
        if build_id:
            build_ids.add(build_id)
        elif require_complete:
            raise ValidationError(f"Observation lacks build_id: {observation_id}")

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
        if str(concept_by_id[concept_id].get("source_id", "")) != sid:
            raise ValidationError(f"Observation/concept source ownership mismatch: {observation_id}")

        raw = raw_by_id[raw_id]
        if str(raw.get("source_id", "")) != sid or str(raw.get("source_revision_id", "")) != rev:
            raise ValidationError(f"Observation/raw lineage mismatch: {observation_id}")
        if str(raw.get("sheet_exact", "")) != str(obs.get("sheet_exact", "")) or str(raw.get("cell_coordinate", "")) != str(obs.get("cell_coordinate", "")):
            raise ValidationError(f"Observation/raw locator mismatch: {observation_id}")
        if disp_by_id[raw_id].get("role") != "observation_value":
            raise ValidationError(f"Observed raw cell lacks observation_value disposition: {raw_id}")

        _decimal(obs.get("value_exact", ""))
        canonical_dims = _canonical_dimensions(obs.get("dimensions_json", "{}"), observation_id)
        period = _validate_period(obs.get("period", ""), observation_id)
        frequency = str(obs.get("frequency", "")).strip()
        period_role = str(obs.get("period_role", "")).strip()
        unit = str(obs.get("unit", "")).strip()
        if frequency not in ALLOWED_FREQUENCIES:
            raise ValidationError(f"Invalid frequency {frequency!r}: {observation_id}")
        if period_role not in ALLOWED_PERIOD_ROLES:
            raise ValidationError(f"Invalid period_role {period_role!r}: {observation_id}")
        if not unit:
            raise ValidationError(f"Observation unit is empty: {observation_id}")
        _validate_scale(obs.get("scale", ""), observation_id)

        observation_raw_ids.append(raw_id)
        obs_source_counts[sid] += 1
        source_periods[sid].add(period)
        source_frequencies[sid].add(frequency)
        key = (
            sid,
            concept_id,
            period,
            frequency,
            period_role,
            unit,
            str(obs.get("scale", "")),
            canonical_dims,
        )
        semantic_keys[key].append(obs)

    if len(set(observation_raw_ids)) != len(observation_raw_ids):
        counts = Counter(observation_raw_ids)
        duplicate_raw = [raw_id for raw_id, count in counts.items() if count > 1]
        raise ValidationError(f"Multiple observations reference the same raw cell: {duplicate_raw[:8]}")

    if require_complete:
        if len(build_ids) != 1:
            raise ValidationError(f"Complete build must contain exactly one build_id; found={sorted(build_ids)}")
        no_obs = sorted(source_id for source_id in expected if obs_source_counts[source_id] == 0)
        if no_obs:
            raise ValidationError(f"Sources with zero semantic observations: {no_obs}")

    duplicate_groups: list[dict[str, object]] = []
    conflicting_groups: list[dict[str, object]] = []
    for key, rows in semantic_keys.items():
        if len(rows) < 2:
            continue
        values = {str(row.get("value_exact", "")) for row in rows}
        item = {
            "source_id": key[0],
            "source_concept_id": key[1],
            "period": key[2],
            "count": len(rows),
            "values": sorted(values),
            "locators": [f"{row.get('sheet_exact')}!{row.get('cell_coordinate')}" for row in rows],
        }
        if len(values) > 1:
            conflicting_groups.append(item)
        else:
            duplicate_groups.append(item)
    if conflicting_groups:
        raise ValidationError(
            f"Conflicting semantic duplicates detected ({len(conflicting_groups)} groups); first={conflicting_groups[0]}"
        )

    numeric_raw = 0
    formula_raw = 0
    roles: Counter[str] = Counter()
    source_raw_counts: Counter[str] = Counter()
    source_observed_raw_counts: Counter[str] = Counter()
    unresolved_numeric: list[dict[str, str]] = []
    observation_raw_set = set(observation_raw_ids)
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
        if str(raw["raw_cell_id"]) in observation_raw_set:
            source_observed_raw_counts[sid] += 1

    if require_complete and unresolved_numeric:
        raise ValidationError(
            f"Unmapped numeric source cells block semantic completeness: count={len(unresolved_numeric)} sample={unresolved_numeric[:12]}"
        )

    diag_by_source = {str(diag.get("source_id")): diag for diag in diagnostics}
    missing_diag = sorted(manifest_set - set(diag_by_source))
    if missing_diag:
        raise ValidationError(f"Missing source diagnostics: {missing_diag}")

    invariants = {
        "single_build_identity": (len(build_ids) == 1) if require_complete and observations else len(build_ids) <= 1,
        "complete_registry_universe": (manifest_set == expected) if require_complete else True,
        "every_raw_cell_dispositioned": raw_ids == disposition_ids,
        "every_observation_has_raw_lineage": len(observation_raw_ids) == len(obs_ids),
        "every_source_has_observations": all(obs_source_counts[source_id] > 0 for source_id in manifest_set),
        "zero_unmapped_numeric": len(unresolved_numeric) == 0,
        "no_conflicting_semantic_duplicates": True,
        "cross_owner_source_coherence": True,
        "bilingual_user_surface_complete": (
            not source_name_gaps
            and len(concepts) == sum(concept_translation_statuses.values())
            and len(dimension_members) == sum(member_translation_statuses.values())
        ),
    }
    blocking_invariants = {
        "every_raw_cell_dispositioned",
        "every_observation_has_raw_lineage",
        "no_conflicting_semantic_duplicates",
        "cross_owner_source_coherence",
        "bilingual_user_surface_complete",
    }
    if require_complete:
        blocking_invariants.update({
            "single_build_identity",
            "complete_registry_universe",
            "every_source_has_observations",
            "zero_unmapped_numeric",
        })
    failed_invariants = [
        name for name in sorted(blocking_invariants) if not invariants[name]
    ]
    if failed_invariants:
        raise ValidationError(f"Blocking invariants are false: {failed_invariants}")

    return {
        "status": "passed",
        "build_ids": sorted(build_ids),
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
        "dataset_bilingual_count": len(SOURCES),
        "concept_bilingual_count": len(concepts),
        "dimension_member_bilingual_count": len(dimension_members),
        "concept_translation_statuses": dict(sorted(concept_translation_statuses.items())),
        "dimension_member_translation_statuses": dict(sorted(member_translation_statuses.items())),
        "raw_disposition_coverage": 1.0,
        "observation_raw_lineage_coverage": 1.0,
        "observation_sources": dict(sorted(obs_source_counts.items())),
        "raw_cells_by_source": dict(sorted(source_raw_counts.items())),
        "observed_raw_cells_by_source": dict(sorted(source_observed_raw_counts.items())),
        "period_count_by_source": {key: len(value) for key, value in sorted(source_periods.items())},
        "frequencies_by_source": {key: sorted(value) for key, value in sorted(source_frequencies.items())},
        "disposition_roles": dict(sorted(roles.items())),
        "identical_semantic_duplicate_groups": duplicate_groups,
        "conflicting_semantic_duplicate_groups": [],
        "invariants": invariants,
    }
