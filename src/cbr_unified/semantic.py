from __future__ import annotations

import hashlib
import re
from collections import defaultdict
from dataclasses import dataclass
from datetime import date, datetime
from decimal import Decimal
from pathlib import Path
from typing import Any, Iterable

from openpyxl import load_workbook
from openpyxl.cell.cell import Cell
from openpyxl.utils.cell import coordinate_to_tuple

from .normalization import (
    EN_MONTHS,
    RU_MONTHS,
    infer_unit,
    normalize_text,
    parse_decimal_text,
    parse_period,
    sheet_dimensions,
    stable_dimensions_json,
    territory_type,
    transliterate_ru,
)
from .raw import raw_index
from .registry import SourceSpec


class SourceVariantError(RuntimeError):
    pass


@dataclass(frozen=True)
class PeriodBinding:
    header_row: int
    column: int
    period: str
    frequency: str
    representation: str
    coordinate: str


def _stable_id(prefix: str, *parts: object) -> str:
    payload = "\x1f".join(str(p) for p in parts).encode("utf-8")
    return prefix + hashlib.sha256(payload).hexdigest()[:24]


def _cell_text(cell: Cell) -> str:
    value = cell.value
    if value is None:
        return ""
    if isinstance(value, (datetime, date)):
        return value.isoformat()
    return str(value).strip()


def _is_period_candidate_value(value: Any) -> bool:
    # Generic discovery intentionally avoids naked numeric years; those occur in data too.
    return isinstance(value, (str, datetime, date))


def discover_period_bindings(ws, source_id: str) -> list[PeriodBinding]:
    by_row: dict[int, list[PeriodBinding]] = defaultdict(list)
    for row in ws.iter_rows():
        for cell in row:
            if cell.value is None or not _is_period_candidate_value(cell.value):
                continue
            parsed = parse_period(cell.value)
            if parsed:
                period, freq, rep = parsed
                by_row[cell.row].append(PeriodBinding(cell.row, cell.column, period, freq, rep, cell.coordinate))

    accepted: list[PeriodBinding] = []
    for row_no, bindings in by_row.items():
        # Three columns is enough for the smallest current statistical matrices.
        if len(bindings) >= 3:
            accepted.extend(bindings)

    if source_id == "exchange_rate":
        accepted.extend(_discover_exchange_periods(ws))

    # Deduplicate same cell; specialized exchange binding wins where generic is absent.
    uniq: dict[tuple[int, int], PeriodBinding] = {}
    for b in accepted:
        uniq[(b.header_row, b.column)] = b
    return sorted(uniq.values(), key=lambda b: (b.header_row, b.column))


def _discover_exchange_periods(ws) -> list[PeriodBinding]:
    max_header = min(ws.max_row, 12)
    max_col = ws.max_column
    years_by_row: dict[int, dict[int, int]] = {}

    for r in range(1, max_header + 1):
        years: dict[int, int] = {}
        current: int | None = None
        for c in range(1, max_col + 1):
            v = ws.cell(r, c).value
            y: int | None = None
            if isinstance(v, int) and 1900 <= v <= 2200:
                y = v
            elif isinstance(v, float) and v.is_integer() and 1900 <= v <= 2200:
                y = int(v)
            elif isinstance(v, str) and re.fullmatch(r"\s*(19|20|21)\d{2}\s*", v):
                y = int(v.strip())
            if y:
                current = y
            if current:
                years[c] = current
        if years:
            years_by_row[r] = years

    out: list[PeriodBinding] = []
    for r in range(1, max_header + 1):
        month_or_quarter: list[tuple[int, str, int | None, str]] = []
        for c in range(1, max_col + 1):
            v = ws.cell(r, c).value
            if not isinstance(v, str):
                continue
            token = normalize_text(v).replace(".", "").strip()
            mo = RU_MONTHS.get(token) or EN_MONTHS.get(token)
            if mo:
                month_or_quarter.append((c, "monthly", mo, "exchange_composite"))
                continue
            m = re.fullmatch(r"(?:([iv]+)|([1-4]))\s*(?:кв(?:арт(?:ал)?)?|q)", token)
            if m:
                roman, digit = m.groups()
                q = int(digit) if digit else {"i":1,"ii":2,"iii":3,"iv":4}.get(roman)
                if q:
                    month_or_quarter.append((c, "quarterly", q, "exchange_composite"))
        if len(month_or_quarter) < 3:
            continue
        prior_year_rows = [yr for rr, yr in years_by_row.items() if rr < r]
        if not prior_year_rows:
            continue
        years = prior_year_rows[-1]
        for c, freq, token_num, rep in month_or_quarter:
            y = years.get(c)
            if not y:
                continue
            if freq == "monthly":
                p = date(y, int(token_num), 1).isoformat()
            else:
                p = date(y, 1 + 3 * (int(token_num) - 1), 1).isoformat()
            out.append(PeriodBinding(r, c, p, freq, rep, ws.cell(r, c).coordinate))
    return out


def _raw_decimal(raw: dict[str, object], openpyxl_value: Any) -> Decimal | None:
    # Prefer exact source lexical representation for numeric cells/formula cached values.
    raw_type = str(raw.get("ooxml_type", ""))
    lexical = str(raw.get("value_lexical", ""))
    resolved = str(raw.get("text_resolved", ""))
    if raw_type in {"n", "str"} and lexical:
        d = parse_decimal_text(lexical)
        if d is not None:
            return d
    if raw_type in {"s", "inlineStr"} and resolved:
        d = parse_decimal_text(resolved)
        if d is not None:
            return d
    # Formula cells usually use type n with a cached <v>; fallback only if needed.
    return parse_decimal_text(openpyxl_value)


def _raw_value_exact(raw: dict[str, object], openpyxl_value: Any) -> str:
    lexical = str(raw.get("value_lexical", ""))
    if lexical != "":
        return lexical
    resolved = str(raw.get("text_resolved", ""))
    if resolved != "":
        return resolved
    return "" if openpyxl_value is None else str(openpyxl_value)


def _first_title(ws) -> str:
    for r in range(1, min(ws.max_row, 8) + 1):
        for c in range(1, min(ws.max_column, 8) + 1):
            v = ws.cell(r, c).value
            if isinstance(v, str) and v.strip():
                text = " ".join(v.split())
                if len(text) >= 12:
                    return text
    return ws.title


def _row_side_values(ws, row: int, first_period_col: int) -> list[str]:
    values: list[str] = []
    for c in range(1, first_period_col):
        v = ws.cell(row, c).value
        if v is None:
            continue
        if isinstance(v, (datetime, date)):
            continue
        text = " ".join(str(v).split())
        if text:
            values.append(text)
    return values


def _row_label(ws, row: int, first_period_col: int) -> str:
    vals = _row_side_values(ws, row, first_period_col)
    if not vals:
        return f"Строка {row}"
    # Preserve all row-side code/context columns without flattening punctuation semantics.
    return " | ".join(vals)


def _readable_ru(label: str) -> str:
    s = " ".join(label.split())
    # Remove only an explicit trailing unit phrase; unit remains a structured field.
    s = re.sub(r",?\s*(?:млн|млрд|тыс)\.?\s*руб\.?\s*$", "", s, flags=re.I)
    s = re.sub(r",?\s*%\s*$", "", s)
    return s.strip(" ,;:") or label


_COMMON_EN = [
    (r"^итого$", "Total"),
    (r"^всего:?$", "Total"),
    (r"просроченн(?:ая|ой) задолженность", "Overdue debt"),
    (r"задолженность", "Debt"),
    (r"объем кредитов", "Loan volume"),
    (r"количество кредитов", "Number of loans"),
    (r"количество заемщиков", "Number of borrowers"),
    (r"финансовые активы", "Financial assets"),
    (r"обязательства", "Liabilities"),
    (r"денежн(?:ая|ые) масса|денежные агрегаты", "Monetary aggregates"),
    (r"депозиты", "Deposits"),
    (r"кредиты и займы", "Loans"),
    (r"кредиты", "Loans"),
    (r"наличная валюта", "Currency"),
    (r"иностранн(?:ая|ой) валюта", "Foreign currency"),
    (r"национальн(?:ая|ой) валюта", "National currency"),
    (r"долговые ценные бумаги", "Debt securities"),
    (r"краткосрочн", "Short-term"),
    (r"долгосрочн", "Long-term"),
]


def _project_english(label: str, fallback_context: str) -> tuple[str, str]:
    s = normalize_text(label)
    for pattern, english in _COMMON_EN:
        if re.search(pattern, s, re.I):
            # Add a transliterated differentiator when the source label contains more detail.
            translit = transliterate_ru(_readable_ru(label))
            if len(translit) > len(english) + 12:
                return f"{english} — {translit}", "project_translation"
            return english, "project_translation"
    # Transparent project surface: English context + source-label transliteration.
    # This never pretends to be official translation and identity remains source-local.
    return f"{fallback_context}: {transliterate_ru(_readable_ru(label))}", "project_translation"


def _embedded_dimensions(label: str, source_id: str) -> dict[str, str]:
    s = normalize_text(label)
    dims: dict[str, str] = {}
    if "иностранн" in s and "валют" in s:
        dims["currency_category"] = "foreign_currency"
    elif "национальн" in s and "валют" in s:
        dims["currency_category"] = "national_currency"
    elif "в рублях" in s or "рублев" in s:
        dims["currency_category"] = "rubles"
    if "просроч" in s:
        dims["overdue"] = "true"
    if "до 1 года" in s or "до одного года" in s:
        dims["maturity_bucket"] = "up_to_1_year"
    elif "свыше 1 года" in s or "более 1 года" in s:
        dims["maturity_bucket"] = "over_1_year"
    if "остаточн" in s and "срок" in s:
        dims["maturity_basis"] = "remaining"
    elif "первоначальн" in s and "срок" in s:
        dims["maturity_basis"] = "original"
    if source_id.startswith("sme_"):
        dims["sme_scope"] = "sme"
    if source_id == "sme_debt_subj_i":
        dims["entrepreneur_scope"] = "individual_entrepreneurs"
    if source_id == "dep_ind_no_escrow":
        dims["escrow_coverage"] = "excluded"
    if source_id == "escrow_accounts":
        dims["escrow_coverage"] = "escrow_only"
    return dims


def _period_role(spec: SourceSpec, label: str, sheet: str) -> str:
    s = normalize_text(label + " " + sheet)
    if "темп прироста" in s or "прирост" in s or "изменение" in s:
        return "published_change"
    if "за месяц" in s or "за отчетный период" in s or "операци" in s or "объем кредитов, предоставленных" in s:
        return "flow"
    if "задолж" in s or "остат" in s or "баланс" in s or "по состоянию" in s:
        return "stock"
    return spec.period_role


def _activity_code(label: str) -> str:
    m = re.match(r"\s*([A-ZА-Я]?\d{1,2}(?:\.\d+)*)\b", label)
    return m.group(1) if m else ""


def _concept(
    spec: SourceSpec,
    *,
    sheet: str,
    row: int,
    label: str,
    title: str,
    row_axis: str,
) -> dict[str, str]:
    if row_axis in {"region", "activity"}:
        local_key = "dataset_measure"
        label_source = title
        name_ru = spec.name_ru
        name_en = spec.name_en
        translation_status = "project_translation"
    else:
        local_key = f"{sheet}|row:{row}|{label}"
        label_source = label
        name_ru = _readable_ru(label)
        name_en, translation_status = _project_english(label, spec.name_en)
    concept_id = _stable_id("sc_", spec.source_id, local_key)
    return {
        "source_concept_id": concept_id,
        "source_id": spec.source_id,
        "source_local_key": local_key,
        "label_ru_source": label_source,
        "label_ru_normalized": normalize_text(label_source),
        "name_ru": name_ru,
        "name_en": name_en,
        "translation_status": translation_status,
        "row_axis": row_axis,
        "source_context": title,
    }


def _dimension_member(dimension: str, source_value: str, *, classification: str | None = None) -> dict[str, str]:
    norm = normalize_text(source_value)
    member_id = _stable_id("dm_", dimension, classification or "", norm)
    if dimension == "region":
        en = transliterate_ru(source_value)
        status = "transliteration_only"
    elif dimension == "activity":
        code = _activity_code(source_value)
        prefix = classification or "activity"
        en = f"{prefix} {code}: {transliterate_ru(source_value)}" if code else f"{prefix}: {transliterate_ru(source_value)}"
        status = "project_translation"
    else:
        en = source_value
        status = "project_translation"
    return {
        "dimension_member_id": member_id,
        "dimension": dimension,
        "classification": classification or "",
        "source_value_ru": source_value,
        "name_ru": source_value,
        "name_en": en,
        "translation_status": status,
    }


def parse_source(
    xlsx_path: str | Path,
    *,
    spec: SourceSpec,
    source_revision_id: str,
    file_sha256: str,
    raw_cells: list[dict[str, object]],
) -> tuple[list[dict[str, object]], list[dict[str, str]], list[dict[str, str]], list[dict[str, str]], dict[str, object]]:
    """Return observations, concepts, dimension members, dispositions, source diagnostics."""
    wb = load_workbook(xlsx_path, read_only=False, data_only=False, keep_links=True)
    rindex = raw_index(raw_cells)
    dispositions: dict[str, dict[str, str]] = {
        str(r["raw_cell_id"]): {
            "raw_cell_id": str(r["raw_cell_id"]),
            "source_id": spec.source_id,
            "source_revision_id": source_revision_id,
            "role": "source_cell",
            "reason": "retained_nonempty_source_cell",
        }
        for r in raw_cells
    }
    observations: list[dict[str, object]] = []
    concepts: dict[str, dict[str, str]] = {}
    members: dict[str, dict[str, str]] = {}
    sheet_diags: list[dict[str, object]] = []

    for ws in wb.worksheets:
        title = _first_title(ws)
        bindings = discover_period_bindings(ws, spec.source_id)
        by_header: dict[int, dict[int, PeriodBinding]] = defaultdict(dict)
        for b in bindings:
            by_header[b.header_row][b.column] = b
            raw = rindex.get((ws.title, b.coordinate))
            if raw:
                dispositions[str(raw["raw_cell_id"])].update({"role": "period_key", "reason": b.representation})

        header_rows = sorted(by_header)
        sheet_dims = sheet_dimensions(ws.title, spec.source_id)
        metadata_sheet = any(token in normalize_text(ws.title) for token in ("методолог", "metadata", "метадан"))
        obs_before = len(observations)
        numeric_candidates = 0
        numeric_observed = 0

        # Fast row/column lookup of raw source cells.
        raw_by_coord = {coord: row for (sheet, coord), row in rindex.items() if sheet == ws.title}

        for coord, raw in raw_by_coord.items():
            row_no, col_no = coordinate_to_tuple(coord)
            open_value = ws[coord].value
            dec = _raw_decimal(raw, open_value)
            if dec is None:
                continue
            numeric_candidates += 1

            # Find nearest preceding period-header block containing this column.
            candidate_headers = [hr for hr in header_rows if hr < row_no and col_no in by_header[hr]]
            if not candidate_headers:
                # Numeric years used by exchange composite headers or source hierarchy codes are not observations.
                role = "non_observation_numeric"
                reason = "no_period_binding"
                if col_no <= 5:
                    role, reason = "hierarchy_or_header_code", "numeric_before_period_axis"
                dispositions[str(raw["raw_cell_id"])].update({"role": role, "reason": reason})
                continue
            header_row = candidate_headers[-1]
            binding = by_header[header_row][col_no]
            first_period_col = min(by_header[header_row])
            if row_no <= header_row:
                continue

            row_label = _row_label(ws, row_no, first_period_col)
            # Avoid treating the exact header row or obvious note/source rows as observations.
            if row_label.startswith("Строка ") and metadata_sheet:
                dispositions[str(raw["raw_cell_id"])].update({"role": "source_metadata_numeric", "reason": "metadata_sheet"})
                continue

            dims: dict[str, str] = dict(sheet_dims)
            dims.update(_embedded_dimensions(row_label, spec.source_id))
            if spec.row_axis == "region":
                dims["region"] = row_label
                dims["region_type"] = territory_type(row_label)
                member = _dimension_member("region", row_label)
                members[member["dimension_member_id"]] = member
            elif spec.row_axis == "activity":
                dims["activity"] = row_label
                dims["classification"] = spec.classification or "source_activity"
                code = _activity_code(row_label)
                if code:
                    dims["activity_code"] = code
                member = _dimension_member("activity", row_label, classification=spec.classification)
                members[member["dimension_member_id"]] = member

            concept = _concept(spec, sheet=ws.title, row=row_no, label=row_label, title=title, row_axis=spec.row_axis)
            concepts[concept["source_concept_id"]] = concept
            unit, scale = infer_unit(row_label, title)
            obs_id = _stable_id("ob_", source_revision_id, ws.title, coord)
            observations.append({
                "observation_id": obs_id,
                "source_id": spec.source_id,
                "source_revision_id": source_revision_id,
                "file_sha256": file_sha256,
                "source_concept_id": concept["source_concept_id"],
                "period": binding.period,
                "frequency": "monthly" if binding.frequency == "monthly_or_point" else binding.frequency,
                "period_representation": binding.representation,
                "period_role": _period_role(spec, row_label, ws.title),
                "value_exact": _raw_value_exact(raw, open_value),
                "value_kind": "formula_cached" if str(raw.get("formula", "")) else ("numeric_text" if str(raw.get("ooxml_type")) in {"s", "inlineStr", "str"} else "numeric"),
                "unit": unit or "source_defined",
                "scale": scale if scale is not None else "",
                "dimensions_json": stable_dimensions_json(dims),
                "sheet_exact": ws.title,
                "cell_coordinate": coord,
                "raw_cell_id": str(raw["raw_cell_id"]),
                "source_row": row_no,
                "source_row_label": row_label,
            })
            numeric_observed += 1
            dispositions[str(raw["raw_cell_id"])].update({"role": "observation_value", "reason": "period_bound_numeric_value"})

        obs_count = len(observations) - obs_before
        sheet_diags.append({
            "sheet": ws.title,
            "title": title,
            "metadata_sheet": metadata_sheet,
            "period_bindings": len(bindings),
            "period_header_rows": header_rows,
            "numeric_candidates": numeric_candidates,
            "observations": obs_count,
        })
        if numeric_candidates >= 10 and not metadata_sheet and obs_count == 0:
            wb.close()
            raise SourceVariantError(
                f"{spec.source_id}/{ws.title}: {numeric_candidates} numeric candidates but no semantic observations; period/header contract unrecognized"
            )

    wb.close()
    return observations, list(concepts.values()), list(members.values()), list(dispositions.values()), {
        "source_id": spec.source_id,
        "source_revision_id": source_revision_id,
        "sheets": sheet_diags,
        "observation_count": len(observations),
        "concept_count": len(concepts),
        "dimension_member_count": len(members),
    }
