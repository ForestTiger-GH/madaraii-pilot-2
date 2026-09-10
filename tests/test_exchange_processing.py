from openpyxl import Workbook

from cbr_unified.processing import parse_source_checked
from cbr_unified.raw import extract_raw_cells, workbook_sha256
from cbr_unified.registry import get_source


def test_exchange_quarterly_and_formula_annual_calendars(tmp_path):
    path = tmp_path / "exchange.xlsx"
    wb = Workbook()
    q = wb.active
    q.title = "Ежеквартальные"
    q["B1"] = "Основные производные показатели динамики обменного курса рубля"
    for cell, year in (("B2", 2025), ("C2", 2025), ("D2", 2025), ("E2", 2025)):
        q[cell] = year
    for cell, label in (("B3", "1 кварт."), ("C3", "2 кварт."), ("D3", "3 кварт."), ("E3", "4 кварт.")):
        q[cell] = label
    q["A5"] = "Номинальный курс доллара США к рублю на конец периода"
    q["B5"] = 90.1
    q["C5"] = 91.2
    q["D5"] = 92.3
    q["E5"] = 93.4

    annual = wb.create_sheet("Доли")
    annual["B1"] = "Доли торгового оборота"
    annual["A2"] = "Страны"
    annual["B2"] = "Доли"
    annual["B3"] = 2024
    annual["C3"] = "=B3+1"
    annual["D3"] = "=C3+1"
    annual["A4"] = "Австрия"
    annual["B4"] = 1.1
    annual["C4"] = 1.2
    annual["D4"] = 1.3
    wb.save(path)

    sha = workbook_sha256(path)
    revision = f"exchange_rate@sha256:{sha}"
    raw = extract_raw_cells(path, source_id="exchange_rate", source_revision_id=revision, file_sha256=sha)
    observations, _, _, dispositions, diagnostics = parse_source_checked(
        path,
        spec=get_source("exchange_rate"),
        source_revision_id=revision,
        file_sha256=sha,
        raw_cells=raw,
    )

    quarterly = [o for o in observations if o["sheet_exact"] == "Ежеквартальные"]
    assert [o["period"] for o in quarterly] == ["2025-01-01", "2025-04-01", "2025-07-01", "2025-10-01"]
    assert {o["frequency"] for o in quarterly} == {"quarterly"}

    shares = [o for o in observations if o["sheet_exact"] == "Доли"]
    assert [o["period"] for o in shares] == ["2024-01-01", "2025-01-01", "2026-01-01"]
    assert {o["frequency"] for o in shares} == {"annual"}

    raw_by_coord = {(r["sheet_exact"], r["cell_coordinate"]): r for r in raw}
    disp = {d["raw_cell_id"]: d for d in dispositions}
    assert disp[raw_by_coord[("Ежеквартальные", "B3")]["raw_cell_id"]]["role"] == "period_key"
    assert disp[raw_by_coord[("Доли", "B3")]["raw_cell_id"]]["role"] == "period_key"
    assert disp[raw_by_coord[("Доли", "C3")]["raw_cell_id"]]["role"] == "period_key"
    assert diagnostics["unmapped_numeric_count"] == 0
