from __future__ import annotations

import re
import tempfile
from collections import defaultdict
from contextlib import contextmanager
from pathlib import Path
from typing import Iterator, Mapping

from openpyxl import load_workbook
from openpyxl.utils.cell import coordinate_to_tuple

from .normalization import normalize_text, parse_decimal_text
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


def parse_source_checked(
    xlsx_path: str | Path,
    *,
    spec: SourceSpec,
    source_revision_id: str,
    file_sha256: str,
    raw_cells: list[dict[str, object]],
):
    """Parse one source and close numeric-disposition gaps before admission.

    ``semantic.parse_source`` owns observation extraction. This gate independently
    rebinds period/header/metadata roles from workbook structure and converts any
    remaining unexplained numeric candidate into ``unmapped_numeric``. Complete
    validation can therefore fail closed instead of accepting a number merely
    because no period binding happened to be found for it.
    """
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
        try:
            for ws in wb.worksheets:
                bindings = discover_period_bindings(ws, spec.source_id)
                period_coords = {b.coordinate: b for b in bindings}
                period_rows = sorted({b.header_row for b in bindings})
                first_period_col_by_row: dict[int, int] = {}
                for b in bindings:
                    first_period_col_by_row[b.header_row] = min(
                        b.column,
                        first_period_col_by_row.get(b.header_row, b.column),
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

                    # Numeric cells in the left semantic stub are hierarchy/classification
                    # codes or source-side header material, not time-series observations.
                    candidate_header_rows = [hr for hr in period_rows if hr < row_no]
                    nearest_header = candidate_header_rows[-1] if candidate_header_rows else None
                    first_period_col = first_period_col_by_row.get(nearest_header) if nearest_header is not None else None
                    if first_period_col is not None and col_no < first_period_col:
                        current.update({"role": "hierarchy_or_header_code", "reason": "numeric_before_period_axis"})
                        continue

                    # Calendar/header numerics above the first data block are explicit
                    # source structure. Exchange-rate workbooks use numeric year bands.
                    if period_rows and row_no <= max(period_rows):
                        current.update({"role": "hierarchy_or_header_code", "reason": "numeric_period_header_structure"})
                        continue
                    if spec.parser == "exchange" and row_no <= 12:
                        current.update({"role": "hierarchy_or_header_code", "reason": "exchange_calendar_header"})
                        continue

                    # Preserve existing specific classifications; generic
                    # non_observation_numeric means the value is still unexplained.
                    if current.get("role") == "non_observation_numeric":
                        current.update({"role": "unmapped_numeric", "reason": "numeric_value_without_admitted_semantic_role"})

            unresolved = sum(1 for row in dispositions if row.get("role") == "unmapped_numeric")
            diagnostics["unmapped_numeric_count"] = unresolved
            diagnostics["numeric_disposition_gate"] = "passed" if unresolved == 0 else "failed"
            diagnostics["semantic_view"] = "exchange_calendar_compatibility" if spec.source_id == "exchange_rate" else "source"
        finally:
            wb.close()
    return observations, concepts, members, dispositions, diagnostics
