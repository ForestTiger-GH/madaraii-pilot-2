from __future__ import annotations

import hashlib
import json
import re
import tempfile
from collections import Counter, defaultdict
from contextlib import contextmanager
from pathlib import Path
from typing import Iterator, Mapping

from openpyxl import load_workbook
from openpyxl.utils.cell import coordinate_to_tuple

from .normalization import normalize_text, parse_decimal_text, stable_dimensions_json
from .registry import SourceSpec
from .semantic import SourceVariantError, discover_period_bindings, parse_source


def _is_numeric_raw(row: Mapping[str, object]) -> bool:
    lexical = str(row.get("value_lexical", ""))
    resolved = str(row.get("text_resolved", ""))
    if lexical and parse_decimal_text(lexical) is not None:
        return True
    if resolved and parse_decimal_text(resolved) is not None:
        return True
    return False


def _integer_year(value: object) -> int | None:
    if isinstance(value, bool):
        return None
    if isinstance(value, int) and 1900 <= value <= 2200:
        return value
    if isinstance(value, float) and value.is_integer() and 1900 <= int(value) <= 2200:
        return int(value)
    if isinstance(value, str) and re.fullmatch(r"\s*(19|20|21)\d{2}\s*", value):
        return int(value.strip())
    return None


def _prepare_exchange_semantic_view(wb) -> int:
    """Normalize only proven exchange-rate calendar presentations for parsing.

    The returned workbook is a semantic view only. Raw evidence always comes from
    the untouched source XLSX. Two current source presentations need explicit
    compatibility treatment:

    * quarterly headers use ``1 кварт.`` ... ``4 кварт.`` while the established
      exchange calendar parser expects the semantically equivalent ``1 кв`` form;
    * the annual ``Доли`` sheet stores the first year as a value and later years as
      formulas such as ``=B3+1``. For period binding only, this exact formula chain
      is materialized to explicit year strings.
    """
    changed = 0
    for ws in wb.worksheets:
        title = normalize_text(ws.title)
        if title == "ежеквартальные":
            quarter_cells = 0
            for cell in ws[3]:
                if not isinstance(cell.value, str):
                    continue
                m = re.fullmatch(r"\s*([1-4])\s*кварт\.\s*", cell.value, flags=re.I)
                if m:
                    cell.value = f"{m.group(1)} кв"
                    changed += 1
                    quarter_cells += 1
            if quarter_cells < 3:
                raise SourceVariantError(
                    "exchange_rate/Ежеквартальные: expected quarterly calendar labels 'N кварт.' were not found"
                )

        elif title == "доли":
            previous_year: int | None = None
            previous_coord: str | None = None
            annual_cells = 0
            for col in range(2, ws.max_column + 1):
                cell = ws.cell(3, col)
                value = cell.value
                if value is None:
                    continue
                year = _integer_year(value)
                if year is None and isinstance(value, str) and value.startswith("="):
                    if previous_year is None or previous_coord is None:
                        raise SourceVariantError(
                            f"exchange_rate/Доли: formula year {cell.coordinate} has no resolved predecessor"
                        )
                    formula = re.sub(r"\s+", "", value).upper()
                    expected = f"={previous_coord.upper()}+1"
                    if formula != expected:
                        raise SourceVariantError(
                            f"exchange_rate/Доли: unexpected year formula {cell.coordinate}={value!r}; expected {expected!r}"
                        )
                    year = previous_year + 1
                if year is None:
                    raise SourceVariantError(
                        f"exchange_rate/Доли: unsupported annual header {cell.coordinate}={value!r}"
                    )
                cell.value = str(year)
                previous_year = year
                previous_coord = cell.coordinate
                annual_cells += 1
                changed += 1
            if annual_cells < 3:
                raise SourceVariantError("exchange_rate/Доли: annual calendar is incomplete")
    return changed


@contextmanager
def _semantic_view(xlsx_path: str | Path, spec: SourceSpec) -> Iterator[Path]:
    source = Path(xlsx_path)
    if spec.source_id != "exchange_rate":
        yield source
        return

    wb = load_workbook(source, read_only=False, data_only=False, keep_links=True)
    temp_path: Path | None = None
    try:
        changed = _prepare_exchange_semantic_view(wb)
        if changed == 0:
            yield source
            return
        with tempfile.NamedTemporaryFile(prefix="cbr_exchange_semantic_", suffix=".xlsx", delete=False) as fh:
            temp_path = Path(fh.name)
        wb.save(temp_path)
    finally:
        wb.close()

    try:
        if temp_path is None:
            raise RuntimeError("Exchange semantic view was not created")
        yield temp_path
    finally:
        temp_path.unlink(missing_ok=True)


def _period_block_context(
    ws,
    *,
    header_row: int,
    first_period_col: int,
    previous_header_row: int | None,
) -> str:
    """Return the nearest source-visible semantic heading for one period block."""
    lower_bound = (previous_header_row + 1) if previous_header_row is not None else 1
    generic = {
        "дата",
        "отчетная дата",
        "отчётная дата",
        "период",
        "на дату",
        "date",
        "reporting date",
    }
    for row_no in range(header_row - 1, lower_bound - 1, -1):
        values: list[str] = []
        for col_no in range(1, first_period_col):
            value = ws.cell(row_no, col_no).value
            if not isinstance(value, str) or not value.strip():
                continue
            text = " ".join(value.split())
            if normalize_text(text) in generic:
                continue
            values.append(text)
        if values:
            return " | ".join(values)
    return ""


def _stub_values(ws, *, row_no: int, first_period_col: int, inherit_merged: bool) -> list[str]:
    values: list[str] = []
    seen: set[str] = set()
    merged_ranges = tuple(ws.merged_cells.ranges) if inherit_merged else ()
    for col_no in range(1, first_period_col):
        value = ws.cell(row_no, col_no).value
        if value is None and inherit_merged:
            for merged in merged_ranges:
                if (
                    merged.min_row <= row_no <= merged.max_row
                    and merged.min_col <= col_no <= merged.max_col
                ):
                    value = ws.cell(merged.min_row, merged.min_col).value
                    break
        if not isinstance(value, str) or not value.strip():
            continue
        text = " ".join(value.split())
        normalized = normalize_text(text)
        if normalized and normalized not in seen:
            values.append(text)
            seen.add(normalized)
    return values


def _stub_signature(ws, *, row_no: int, first_period_col: int) -> str:
    return normalize_text(
        " > ".join(
            _stub_values(
                ws,
                row_no=row_no,
                first_period_col=first_period_col,
                inherit_merged=False,
            )
        )
    )


def _frequency_ancestry_context(
    ws,
    *,
    row_no: int,
    first_period_col: int,
    header_row: int,
) -> str:
    """Infer a source-visible parent chain from repeated hierarchy signatures.

    In several CBR hierarchy tables the same children are repeated under sector
    parents, while the sectors themselves repeat under broader currency sections.
    Indentation and blank rows are not guaranteed. A strictly decreasing repetition
    count provides a conservative ancestry: frequent child -> rarer parent -> unique
    outer section. Physical row numbers never enter the resulting identity.
    """
    signatures: dict[int, str] = {}
    counts: Counter[str] = Counter()
    for candidate in range(header_row + 1, ws.max_row + 1):
        signature = _stub_signature(
            ws,
            row_no=candidate,
            first_period_col=first_period_col,
        )
        if not signature:
            continue
        signatures[candidate] = signature
        counts[signature] += 1

    current = signatures.get(row_no, "")
    if not current or counts[current] <= 1:
        return ""

    threshold = counts[current]
    ancestors: list[str] = []
    seen: set[str] = set()
    for candidate in range(row_no - 1, header_row, -1):
        signature = signatures.get(candidate, "")
        if not signature or signature in seen:
            continue
        count = counts[signature]
        if count >= threshold:
            continue
        values = _stub_values(
            ws,
            row_no=candidate,
            first_period_col=first_period_col,
            inherit_merged=False,
        )
        if not values:
            continue
        ancestors.append(" > ".join(values))
        seen.add(signature)
        threshold = count
        if threshold <= 1:
            break
    return " > ".join(reversed(ancestors))


def _blank_boundary_anchor_context(
    ws,
    *,
    row_no: int,
    first_period_col: int,
    header_row: int,
) -> str:
    for candidate in range(row_no - 1, header_row, -1):
        values = _stub_values(
            ws,
            row_no=candidate,
            first_period_col=first_period_col,
            inherit_merged=False,
        )
        if not values:
            continue
        previous_values = (
            _stub_values(
                ws,
                row_no=candidate - 1,
                first_period_col=first_period_col,
                inherit_merged=False,
            )
            if candidate - 1 > header_row
            else []
        )
        if not previous_values:
            return " > ".join(values)
    return ""


def _section_anchor_context(
    ws,
    *,
    row_no: int,
    first_period_col: int,
    header_row: int,
) -> str:
    """Find stable source-visible hierarchy ancestry without coordinate identity."""
    frequency_ancestry = _frequency_ancestry_context(
        ws,
        row_no=row_no,
        first_period_col=first_period_col,
        header_row=header_row,
    )
    if frequency_ancestry:
        return frequency_ancestry
    return _blank_boundary_anchor_context(
        ws,
        row_no=row_no,
        first_period_col=first_period_col,
        header_row=header_row,
    )


def _structural_currency_scope(
    ws,
    *,
    row_no: int,
    first_period_col: int,
    header_row: int,
) -> dict[str, str]:
    """Inherit only explicit currency scope headings from the source stub.

    The nearest explicit ruble / foreign-currency heading governs following child
    rows until another currency heading appears. Generic unit labels such as
    ``млн руб.`` never create a denomination dimension. Existing row/sheet
    dimensions retain precedence when this inherited scope is applied.
    """
    for candidate in range(row_no, header_row, -1):
        values = _stub_values(
            ws,
            row_no=candidate,
            first_period_col=first_period_col,
            inherit_merged=True,
        )
        if not values:
            continue
        raw_text = " > ".join(values)
        text = normalize_text(raw_text)
        if "инвалют" in text or ("иностран" in text and "валют" in text) or "в валюте" in text:
            dims = {"currency_category": "foreign_currency"}
            if "$" in raw_text or "доллар" in text:
                dims["measurement_currency"] = "USD"
            return dims
        if "в российских руб" in text or "в руб" in text or text.startswith("руб"):
            return {"currency_category": "rubles"}
    return {}


def _merged_stub_context(
    ws,
    *,
    row_no: int,
    first_period_col: int,
    header_row: int,
) -> str:
    """Resolve section + visible left-stub path, including inherited merged parents."""
    parts: list[str] = []
    section = _section_anchor_context(
        ws,
        row_no=row_no,
        first_period_col=first_period_col,
        header_row=header_row,
    )
    if section:
        parts.append(f"section={section}")
    stub = " > ".join(
        _stub_values(
            ws,
            row_no=row_no,
            first_period_col=first_period_col,
            inherit_merged=True,
        )
    )
    if stub:
        parts.append(f"row={stub}")
    return " | ".join(parts)


def _concept_id(source_id: str, local_key: str) -> str:
    payload = f"{source_id}\x1f{local_key}".encode("utf-8")
    return "sc_" + hashlib.sha256(payload).hexdigest()[:24]


def _split_repeated_block_concepts(
    observations: list[dict[str, object]],
    concepts: list[dict[str, str]],
    *,
    period_rows_by_sheet: Mapping[str, list[int]],
    first_period_col_by_sheet_header: Mapping[tuple[str, int], int],
    block_context_by_sheet_header: Mapping[tuple[str, int], str],
    stub_context_by_sheet_row: Mapping[tuple[str, int], str],
) -> tuple[list[dict[str, str]], int]:
    """Split repeated preliminary concepts only when source-visible context proves distinction.

    This operation is for concept-bearing row axes (indicator/hierarchy/mixed). Row
    dimensions such as region/activity are deliberately excluded by the caller:
    their row labels are dimension members, while the concept remains the measure.
    """
    concept_by_id = {str(row["source_concept_id"]): row for row in concepts}
    obs_context: dict[str, str] = {}
    contexts_by_concept: dict[str, set[str]] = defaultdict(set)

    for obs in observations:
        sheet = str(obs.get("sheet_exact", ""))
        try:
            source_row = int(obs.get("source_row", 0))
        except (TypeError, ValueError):
            continue
        headers = [row for row in period_rows_by_sheet.get(sheet, []) if row < source_row]
        if not headers:
            continue
        header_row = headers[-1]
        if (sheet, header_row) not in first_period_col_by_sheet_header:
            continue
        block = block_context_by_sheet_header.get((sheet, header_row), "").strip()
        stub = stub_context_by_sheet_row.get((sheet, source_row), "").strip()
        parts: list[str] = []
        if block:
            parts.append(f"block={block}")
        if stub:
            parts.append(f"stub={stub}")
        context = " | ".join(parts)
        normalized = normalize_text(context)
        if not normalized:
            continue
        observation_id = str(obs.get("observation_id", ""))
        concept_id = str(obs.get("source_concept_id", ""))
        obs_context[observation_id] = context
        contexts_by_concept[concept_id].add(normalized)

    affected = {
        concept_id
        for concept_id, contexts in contexts_by_concept.items()
        if len(contexts) > 1
    }
    if not affected:
        return concepts, 0

    rewritten: dict[str, dict[str, str]] = {
        concept_id: dict(row)
        for concept_id, row in concept_by_id.items()
        if concept_id not in affected
    }
    split_count = 0

    for obs in observations:
        old_id = str(obs.get("source_concept_id", ""))
        if old_id not in affected:
            continue
        observation_id = str(obs.get("observation_id", ""))
        context = obs_context.get(observation_id, "")
        if not context:
            raise SourceVariantError(
                f"{obs.get('source_id')}/{obs.get('sheet_exact')}: repeated concept {old_id} lacks semantic source context"
            )
        original = concept_by_id[old_id]
        local_key = (
            str(original.get("source_local_key", ""))
            + "|source_context|"
            + normalize_text(context)
        )
        source_id = str(original.get("source_id", obs.get("source_id", "")))
        new_id = _concept_id(source_id, local_key)
        candidate = dict(original)
        candidate["source_concept_id"] = new_id
        candidate["source_local_key"] = local_key
        prior_context = str(candidate.get("source_context", "")).strip()
        candidate["source_context"] = f"{prior_context} | {context}" if prior_context else context
        existing = rewritten.get(new_id)
        if existing is not None and existing != candidate:
            raise SourceVariantError(
                f"{source_id}: conflicting concept materialization for source context {context!r}"
            )
        rewritten[new_id] = candidate
        obs["source_concept_id"] = new_id
        split_count += 1

    return list(rewritten.values()), split_count


def parse_source_checked(
    xlsx_path: str | Path,
    *,
    spec: SourceSpec,
    source_revision_id: str,
    file_sha256: str,
    raw_cells: list[dict[str, object]],
):
    """Parse one source and close numeric-disposition gaps before admission."""
    with _semantic_view(xlsx_path, spec) as parse_path:
        observations, concepts, members, dispositions, diagnostics = parse_source(
            parse_path,
            spec=spec,
            source_revision_id=source_revision_id,
            file_sha256=file_sha256,
            raw_cells=raw_cells,
        )
        disp = {str(row["raw_cell_id"]): row for row in dispositions}
        raw_by_sheet: dict[str, list[dict[str, object]]] = defaultdict(list)
        for row in raw_cells:
            raw_by_sheet[str(row["sheet_exact"])].append(row)

        wb = load_workbook(parse_path, read_only=False, data_only=False, keep_links=True)
        period_rows_by_sheet: dict[str, list[int]] = {}
        first_period_col_by_sheet_header: dict[tuple[str, int], int] = {}
        block_context_by_sheet_header: dict[tuple[str, int], str] = {}
        stub_context_by_sheet_row: dict[tuple[str, int], str] = {}
        scope_dimensions_by_sheet_row: dict[tuple[str, int], dict[str, str]] = {}
        concept_row_axis = spec.row_axis not in {"region", "activity"}
        try:
            observations_by_sheet: dict[str, list[dict[str, object]]] = defaultdict(list)
            for obs in observations:
                observations_by_sheet[str(obs.get("sheet_exact", ""))].append(obs)

            for ws in wb.worksheets:
                bindings = discover_period_bindings(ws, spec.source_id)
                period_coords = {b.coordinate: b for b in bindings}
                period_rows = sorted({b.header_row for b in bindings})
                period_rows_by_sheet[ws.title] = period_rows
                first_period_col_by_row: dict[int, int] = {}
                for b in bindings:
                    first_period_col_by_row[b.header_row] = min(
                        b.column,
                        first_period_col_by_row.get(b.header_row, b.column),
                    )
                for index, header_row in enumerate(period_rows):
                    first_period_col = first_period_col_by_row[header_row]
                    first_period_col_by_sheet_header[(ws.title, header_row)] = first_period_col
                    previous_header = period_rows[index - 1] if index > 0 else None
                    block_context_by_sheet_header[(ws.title, header_row)] = _period_block_context(
                        ws,
                        header_row=header_row,
                        first_period_col=first_period_col,
                        previous_header_row=previous_header,
                    )

                if concept_row_axis:
                    for obs in observations_by_sheet.get(ws.title, []):
                        try:
                            source_row = int(obs.get("source_row", 0))
                        except (TypeError, ValueError):
                            continue
                        headers = [header for header in period_rows if header < source_row]
                        if not headers:
                            continue
                        header_row = headers[-1]
                        first_period_col = first_period_col_by_row.get(header_row)
                        if first_period_col is None:
                            continue
                        key = (ws.title, source_row)
                        if key not in stub_context_by_sheet_row:
                            stub_context_by_sheet_row[key] = _merged_stub_context(
                                ws,
                                row_no=source_row,
                                first_period_col=first_period_col,
                                header_row=header_row,
                            )
                            scope_dimensions_by_sheet_row[key] = _structural_currency_scope(
                                ws,
                                row_no=source_row,
                                first_period_col=first_period_col,
                                header_row=header_row,
                            )

                metadata_sheet = any(
                    token in normalize_text(ws.title)
                    for token in ("методолог", "metadata", "метадан")
                )

                for raw in raw_by_sheet.get(ws.title, []):
                    raw_id = str(raw["raw_cell_id"])
                    current = disp[raw_id]
                    if current.get("role") == "observation_value":
                        continue
                    coord = str(raw["cell_coordinate"])
                    if coord in period_coords:
                        current.update({"role": "period_key", "reason": period_coords[coord].representation})
                        continue
                    if not _is_numeric_raw(raw):
                        continue

                    row_no, col_no = coordinate_to_tuple(coord)
                    if metadata_sheet:
                        current.update({"role": "source_metadata_numeric", "reason": "metadata_sheet"})
                        continue

                    candidate_header_rows = [hr for hr in period_rows if hr < row_no]
                    nearest_header = candidate_header_rows[-1] if candidate_header_rows else None
                    first_period_col = first_period_col_by_row.get(nearest_header) if nearest_header is not None else None
                    if first_period_col is not None and col_no < first_period_col:
                        current.update({"role": "hierarchy_or_header_code", "reason": "numeric_before_period_axis"})
                        continue

                    if period_rows and row_no <= max(period_rows):
                        current.update({"role": "hierarchy_or_header_code", "reason": "numeric_period_header_structure"})
                        continue
                    if spec.parser == "exchange" and row_no <= 12:
                        current.update({"role": "hierarchy_or_header_code", "reason": "exchange_calendar_header"})
                        continue

                    if current.get("role") == "non_observation_numeric":
                        current.update({"role": "unmapped_numeric", "reason": "numeric_value_without_admitted_semantic_role"})

            structural_scope_updates = 0
            if concept_row_axis:
                for obs in observations:
                    try:
                        source_row = int(obs.get("source_row", 0))
                    except (TypeError, ValueError):
                        continue
                    key = (str(obs.get("sheet_exact", "")), source_row)
                    inherited = scope_dimensions_by_sheet_row.get(key, {})
                    if not inherited:
                        continue
                    try:
                        dims = json.loads(str(obs.get("dimensions_json", "{}")))
                    except json.JSONDecodeError as exc:
                        raise SourceVariantError(
                            f"{spec.source_id}: parser emitted invalid dimensions_json before structural scope"
                        ) from exc
                    if not isinstance(dims, dict):
                        raise SourceVariantError(
                            f"{spec.source_id}: parser emitted non-object dimensions_json before structural scope"
                        )
                    changed = False
                    for dimension, value in inherited.items():
                        if dimension not in dims:
                            dims[dimension] = value
                            changed = True
                    if changed:
                        obs["dimensions_json"] = stable_dimensions_json(dims)
                        structural_scope_updates += 1

                concepts, split_count = _split_repeated_block_concepts(
                    observations,
                    concepts,
                    period_rows_by_sheet=period_rows_by_sheet,
                    first_period_col_by_sheet_header=first_period_col_by_sheet_header,
                    block_context_by_sheet_header=block_context_by_sheet_header,
                    stub_context_by_sheet_row=stub_context_by_sheet_row,
                )
            else:
                split_count = 0
                structural_scope_updates = 0

            unresolved = sum(1 for row in dispositions if row.get("role") == "unmapped_numeric")
            diagnostics["unmapped_numeric_count"] = unresolved
            diagnostics["numeric_disposition_gate"] = "passed" if unresolved == 0 else "failed"
            diagnostics["semantic_view"] = "exchange_calendar_compatibility" if spec.source_id == "exchange_rate" else "source"
            diagnostics["period_block_concept_rewrites"] = split_count
            diagnostics["structural_scope_dimension_updates"] = structural_scope_updates
        finally:
            wb.close()
    return observations, concepts, members, dispositions, diagnostics
