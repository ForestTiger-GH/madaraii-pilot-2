from __future__ import annotations

import hashlib
import json
from collections import defaultdict
from pathlib import Path

from openpyxl import load_workbook

from . import processing_core as _core
from .normalization import normalize_text, sheet_dimensions, stable_dimensions_json
from .registry import SourceSpec
from .semantic import SourceVariantError, discover_period_bindings
from .processing_core import *  # noqa: F401,F403 - preserve the established lower-level module surface


def _stable_concept_id(source_id: str, local_key: str) -> str:
    payload = f"{source_id}\x1f{local_key}".encode("utf-8")
    return "sc_" + hashlib.sha256(payload).hexdigest()[:24]


def _pre_context_local_key(concept: dict[str, str]) -> str:
    """Recover the preliminary semantic identity before source-context splitting."""
    return str(concept.get("source_local_key", "")).split("|source_context|", 1)[0]


def _header_layout(ws, source_id: str) -> tuple[list[int], dict[int, int]]:
    bindings = discover_period_bindings(ws, source_id)
    period_rows = sorted({binding.header_row for binding in bindings})
    first_period_col_by_row: dict[int, int] = {}
    for binding in bindings:
        first_period_col_by_row[binding.header_row] = min(
            binding.column,
            first_period_col_by_row.get(binding.header_row, binding.column),
        )
    return period_rows, first_period_col_by_row


def _nearest_header(
    source_row: int,
    period_rows: list[int],
    first_period_col_by_row: dict[int, int],
) -> tuple[int, int] | None:
    headers = [header for header in period_rows if header < source_row]
    if not headers:
        return None
    header_row = headers[-1]
    first_period_col = first_period_col_by_row.get(header_row)
    if first_period_col is None:
        return None
    return header_row, first_period_col


def _correct_structural_currency_leakage(
    parse_path: str | Path,
    *,
    spec: SourceSpec,
    observations: list[dict[str, object]],
    concepts: list[dict[str, str]],
) -> int:
    """Keep inherited currency scope on repeated branch children, not later unique totals.

    Structural currency headings describe a subtree. A repeated preliminary concept
    under multiple explicit currency branches is safely scoped by the inherited
    heading. A unique row appearing after one such branch may instead be a broader
    aggregate, so inherited scope is removed unless the current row itself is an
    explicit currency heading. Sheet-level dimensions keep precedence.
    """
    concept_by_id = {str(row["source_concept_id"]): row for row in concepts}
    base_key_by_concept = {
        concept_id: _pre_context_local_key(concept)
        for concept_id, concept in concept_by_id.items()
    }
    source_rows_by_base: dict[str, set[tuple[str, int]]] = defaultdict(set)
    for obs in observations:
        concept_id = str(obs.get("source_concept_id", ""))
        base_key = base_key_by_concept.get(concept_id, "")
        if not base_key:
            continue
        try:
            source_row = int(obs.get("source_row", 0))
        except (TypeError, ValueError):
            continue
        source_rows_by_base[base_key].add((str(obs.get("sheet_exact", "")), source_row))

    removals = 0
    wb = load_workbook(parse_path, read_only=False, data_only=False, keep_links=True)
    try:
        observations_by_sheet: dict[str, list[dict[str, object]]] = defaultdict(list)
        for obs in observations:
            observations_by_sheet[str(obs.get("sheet_exact", ""))].append(obs)

        for ws in wb.worksheets:
            period_rows, first_period_col_by_row = _header_layout(ws, spec.source_id)
            source_sheet_dims = sheet_dimensions(ws.title, spec.source_id)
            for obs in observations_by_sheet.get(ws.title, []):
                try:
                    source_row = int(obs.get("source_row", 0))
                except (TypeError, ValueError):
                    continue
                layout = _nearest_header(source_row, period_rows, first_period_col_by_row)
                if layout is None:
                    continue
                header_row, first_period_col = layout
                inherited = _core._structural_currency_scope(
                    ws,
                    row_no=source_row,
                    first_period_col=first_period_col,
                    header_row=header_row,
                )
                if not inherited:
                    continue

                concept_id = str(obs.get("source_concept_id", ""))
                base_key = base_key_by_concept.get(concept_id, "")
                repeated_source_rows = len(source_rows_by_base.get(base_key, set())) > 1
                explicit_current_row = _core._structural_currency_scope(
                    ws,
                    row_no=source_row,
                    first_period_col=first_period_col,
                    header_row=source_row - 1,
                )
                if repeated_source_rows or explicit_current_row:
                    continue

                try:
                    dims = json.loads(str(obs.get("dimensions_json", "{}")))
                except json.JSONDecodeError as exc:
                    raise SourceVariantError(
                        f"{spec.source_id}: invalid dimensions_json during currency-scope reconciliation"
                    ) from exc
                if not isinstance(dims, dict):
                    raise SourceVariantError(
                        f"{spec.source_id}: non-object dimensions_json during currency-scope reconciliation"
                    )

                changed = False
                for dimension, value in inherited.items():
                    if dimension in source_sheet_dims:
                        continue
                    if dims.get(dimension) == value:
                        dims.pop(dimension)
                        changed = True
                if changed:
                    obs["dimensions_json"] = stable_dimensions_json(dims)
                    removals += 1
    finally:
        wb.close()
    return removals


def _exchange_measure_heading_context(
    ws,
    *,
    row_no: int,
    first_period_col: int,
    header_row: int,
) -> str:
    """Return the exact exchange-index measure heading carried on the time axis.

    The CBR exchange workbook repeats identical indicator labels under three
    source-visible definitions: growth versus previous December, previous period,
    and the corresponding period of the previous year. Those headings are anchored
    in the first period column rather than the left stub, so they require an
    explicit source adapter.
    """
    for candidate in range(row_no - 1, header_row, -1):
        value = ws.cell(candidate, first_period_col).value
        if not isinstance(value, str) or not value.strip():
            continue
        text = " ".join(value.split())
        if normalize_text(text).startswith("индексы обменного курса рубля"):
            return text
    return ""


def _split_exchange_measure_contexts(
    parse_path: str | Path,
    *,
    spec: SourceSpec,
    observations: list[dict[str, object]],
    concepts: list[dict[str, str]],
) -> tuple[list[dict[str, str]], int]:
    if spec.source_id != "exchange_rate":
        return concepts, 0

    concept_by_id = {str(row["source_concept_id"]): row for row in concepts}
    context_by_observation: dict[str, str] = {}
    contexts_by_concept: dict[str, set[str]] = defaultdict(set)

    wb = load_workbook(parse_path, read_only=False, data_only=False, keep_links=True)
    try:
        observations_by_sheet: dict[str, list[dict[str, object]]] = defaultdict(list)
        for obs in observations:
            observations_by_sheet[str(obs.get("sheet_exact", ""))].append(obs)

        for ws in wb.worksheets:
            period_rows, first_period_col_by_row = _header_layout(ws, spec.source_id)
            for obs in observations_by_sheet.get(ws.title, []):
                try:
                    source_row = int(obs.get("source_row", 0))
                except (TypeError, ValueError):
                    continue
                layout = _nearest_header(source_row, period_rows, first_period_col_by_row)
                if layout is None:
                    continue
                header_row, first_period_col = layout
                context = _exchange_measure_heading_context(
                    ws,
                    row_no=source_row,
                    first_period_col=first_period_col,
                    header_row=header_row,
                )
                if not context:
                    continue
                observation_id = str(obs.get("observation_id", ""))
                concept_id = str(obs.get("source_concept_id", ""))
                context_by_observation[observation_id] = context
                contexts_by_concept[concept_id].add(normalize_text(context))
    finally:
        wb.close()

    affected = {
        concept_id
        for concept_id, contexts in contexts_by_concept.items()
        if len(contexts) > 1
    }
    if not affected:
        return concepts, 0

    rewritten: dict[str, dict[str, str]] = {
        concept_id: dict(concept)
        for concept_id, concept in concept_by_id.items()
        if concept_id not in affected
    }
    rewrite_count = 0
    for obs in observations:
        old_id = str(obs.get("source_concept_id", ""))
        if old_id not in affected:
            continue
        observation_id = str(obs.get("observation_id", ""))
        context = context_by_observation.get(observation_id, "")
        if not context:
            raise SourceVariantError(
                f"exchange_rate/{obs.get('sheet_exact')}: repeated exchange concept {old_id} lacks measure heading"
            )
        original = concept_by_id[old_id]
        local_key = (
            str(original.get("source_local_key", ""))
            + "|exchange_measure_context|"
            + normalize_text(context)
        )
        source_id = str(original.get("source_id", spec.source_id))
        new_id = _stable_concept_id(source_id, local_key)
        candidate = dict(original)
        candidate["source_concept_id"] = new_id
        candidate["source_local_key"] = local_key
        prior_context = str(candidate.get("source_context", "")).strip()
        addition = f"exchange_measure={context}"
        candidate["source_context"] = f"{prior_context} | {addition}" if prior_context else addition
        existing = rewritten.get(new_id)
        if existing is not None and existing != candidate:
            raise SourceVariantError(
                f"exchange_rate: conflicting concept materialization for {context!r}"
            )
        rewritten[new_id] = candidate
        obs["source_concept_id"] = new_id
        rewrite_count += 1

    return list(rewritten.values()), rewrite_count


def parse_source_checked(
    xlsx_path: str | Path,
    *,
    spec: SourceSpec,
    source_revision_id: str,
    file_sha256: str,
    raw_cells: list[dict[str, object]],
):
    """Parse one source and apply post-Jester source-context reconciliation."""
    observations, concepts, members, dispositions, diagnostics = _core.parse_source_checked(
        xlsx_path,
        spec=spec,
        source_revision_id=source_revision_id,
        file_sha256=file_sha256,
        raw_cells=raw_cells,
    )

    if spec.row_axis not in {"region", "activity"}:
        with _core._semantic_view(xlsx_path, spec) as parse_path:
            removals = _correct_structural_currency_leakage(
                parse_path,
                spec=spec,
                observations=observations,
                concepts=concepts,
            )
            concepts, exchange_rewrites = _split_exchange_measure_contexts(
                parse_path,
                spec=spec,
                observations=observations,
                concepts=concepts,
            )
    else:
        removals = 0
        exchange_rewrites = 0

    diagnostics["structural_scope_dimension_removals"] = removals
    diagnostics["exchange_measure_context_rewrites"] = exchange_rewrites
    diagnostics["period_block_concept_rewrites"] = int(
        diagnostics.get("period_block_concept_rewrites", 0)
    ) + exchange_rewrites
    return observations, concepts, members, dispositions, diagnostics
