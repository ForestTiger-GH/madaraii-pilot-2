from openpyxl import Workbook

from cbr_unified.processing import parse_source_checked
from cbr_unified.raw import extract_raw_cells, workbook_sha256
from cbr_unified.semantic import _concept, _row_hierarchy_context
from cbr_unified.registry import SourceSpec


def _spec(row_axis="indicator", parser="matrix"):
    return SourceSpec(
        source_id="synthetic",
        url="https://cbr.ru/test.xlsx",
        name_ru="Тест",
        name_en="Test",
        family="test",
        row_axis=row_axis,
        parser=parser,
        period_role="stock",
    )


def _parse(path, spec):
    sha = workbook_sha256(path)
    revision = "synthetic@sha256:" + sha
    raw = extract_raw_cells(
        path,
        source_id="synthetic",
        source_revision_id=revision,
        file_sha256=sha,
    )
    return parse_source_checked(
        path,
        spec=spec,
        source_revision_id=revision,
        file_sha256=sha,
        raw_cells=raw,
    )


def test_repeated_child_labels_are_disambiguated_by_semantic_parent_not_row_number():
    wb = Workbook()
    ws = wb.active
    ws["A2"] = "Отчетная дата"
    ws["A3"] = "Количество кредитов, единиц, в том числе"
    ws["A4"] = "  на создание объектов, единиц"
    ws["A5"] = "  на приобретение объектов, единиц"
    ws["A6"] = "Объем кредитов, млн руб., в том числе"
    ws["A7"] = "  на создание объектов, млн руб."
    ws["A8"] = "  на приобретение объектов, единиц"

    first_context = _row_hierarchy_context(ws, 5, 2, 2)
    second_context = _row_hierarchy_context(ws, 8, 2, 2)
    assert first_context == "Количество кредитов, единиц, в том числе"
    assert second_context == "Объем кредитов, млн руб., в том числе"

    first = _concept(
        _spec(), sheet="Data", row=5, label="на приобретение объектов, единиц",
        title="Ипотечные кредиты", row_axis="indicator", unit="count", scale=1,
        identity_context=first_context,
    )
    second = _concept(
        _spec(), sheet="Data", row=8, label="на приобретение объектов, единиц",
        title="Ипотечные кредиты", row_axis="indicator", unit="count", scale=1,
        identity_context=second_context,
    )
    moved = _concept(
        _spec(), sheet="Data", row=50, label="на приобретение объектов, единиц",
        title="Ипотечные кредиты", row_axis="indicator", unit="count", scale=1,
        identity_context=first_context,
    )
    assert first["source_concept_id"] != second["source_concept_id"]
    assert first["source_concept_id"] == moved["source_concept_id"]
    wb.close()


def test_mixed_repeated_blocks_use_source_heading_not_physical_row(tmp_path):
    path = tmp_path / "mixed.xlsx"
    wb = Workbook()
    ws = wb.active
    ws.title = "Data"
    ws["A1"] = "Сведения о заемщиках МСП"

    ws["A2"] = "Количество заемщиков, единиц"
    ws["B3"], ws["C3"], ws["D3"] = "01.01.2024", "01.02.2024", "01.03.2024"
    ws["A4"] = "Всего"
    ws["B4"], ws["C4"], ws["D4"] = 10, 11, 12

    ws["A6"] = "Объем кредитов, млн руб."
    ws["B7"], ws["C7"], ws["D7"] = "01.01.2024", "01.02.2024", "01.03.2024"
    ws["A8"] = "Всего"
    ws["B8"], ws["C8"], ws["D8"] = 20, 21, 22
    wb.save(path)
    wb.close()

    observations, concepts, _, _, diagnostics = _parse(path, _spec("mixed", "mixed"))
    first_ids = {row["source_concept_id"] for row in observations if row["source_row"] == 4}
    second_ids = {row["source_concept_id"] for row in observations if row["source_row"] == 8}
    assert len(first_ids) == 1
    assert len(second_ids) == 1
    assert first_ids != second_ids
    assert diagnostics["period_block_concept_rewrites"] == 6
    assert len(concepts) == 2
    assert all("source_context" in row["source_local_key"] for row in concepts)


def test_vertical_merged_parent_is_part_of_semantic_stub_identity(tmp_path):
    path = tmp_path / "merged-hierarchy.xlsx"
    wb = Workbook()
    ws = wb.active
    ws.title = "Data"
    ws["A1"] = "Количество субъектов МСП"
    ws["C3"], ws["D3"], ws["E3"] = "01.01.2024", "01.02.2024", "01.03.2024"

    ws.merge_cells("A4:A6")
    ws["A4"] = "Субъекты МСП - юридические лица"
    ws["B4"], ws["B5"], ws["B6"] = "Микропредприятие", "Малое предприятие", "Среднее предприятие"
    for row_no, base in ((4, 10), (5, 20), (6, 30)):
        ws.cell(row_no, 3).value = base
        ws.cell(row_no, 4).value = base + 1
        ws.cell(row_no, 5).value = base + 2

    ws.merge_cells("A7:A9")
    ws["A7"] = "Субъекты МСП - индивидуальные предприниматели"
    ws["B7"], ws["B8"], ws["B9"] = "Микропредприятие", "Малое предприятие", "Среднее предприятие"
    for row_no, base in ((7, 40), (8, 50), (9, 60)):
        ws.cell(row_no, 3).value = base
        ws.cell(row_no, 4).value = base + 1
        ws.cell(row_no, 5).value = base + 2

    wb.save(path)
    wb.close()

    observations, concepts, _, _, diagnostics = _parse(path, _spec("mixed", "mixed"))
    legal_small = {row["source_concept_id"] for row in observations if row["source_row"] == 5}
    entrepreneur_small = {row["source_concept_id"] for row in observations if row["source_row"] == 8}
    assert len(legal_small) == 1
    assert len(entrepreneur_small) == 1
    assert legal_small != entrepreneur_small
    assert diagnostics["period_block_concept_rewrites"] == 12
    assert len(concepts) == 6
    contexts = "\n".join(row["source_context"] for row in concepts)
    assert "юридические лица" in contexts
    assert "индивидуальные предприниматели" in contexts


def test_region_rows_remain_dimension_members_of_one_measure_concept(tmp_path):
    path = tmp_path / "regions.xlsx"
    wb = Workbook()
    ws = wb.active
    ws.title = "Данные"
    ws["A1"] = "Задолженность по кредитам, млн руб."
    ws["B3"], ws["C3"], ws["D3"] = "01.01.2024", "01.02.2024", "01.03.2024"
    for row_no, (region, base) in enumerate((("Москва", 10), ("Татарстан", 20)), start=4):
        ws.cell(row_no, 1).value = region
        ws.cell(row_no, 2).value = base
        ws.cell(row_no, 3).value = base + 1
        ws.cell(row_no, 4).value = base + 2
    wb.save(path)
    wb.close()

    observations, concepts, members, _, diagnostics = _parse(path, _spec("region"))
    assert len(observations) == 6
    assert len(concepts) == 1
    assert len(members) == 2
    assert diagnostics["period_block_concept_rewrites"] == 0
    assert {row["source_concept_id"] for row in observations} == {concepts[0]["source_concept_id"]}


def test_hierarchy_repeated_tree_is_disambiguated_by_section_anchor(tmp_path):
    path = tmp_path / "hierarchy-sections.xlsx"
    wb = Workbook()
    ws = wb.active
    ws.title = "Квартал"
    ws["A1"] = "Долговые ценные бумаги, млн руб."
    ws["B3"], ws["C3"], ws["D3"] = "01.01.2024", "01.04.2024", "01.07.2024"

    for start, section, base in (
        (4, "Выпущенные долговые ценные бумаги - Итого", 100),
        (8, "Выпущенные долговые ценные бумаги в рублях", 200),
        (12, "Выпущенные долговые ценные бумаги в иностранной валюте", 300),
    ):
        ws.cell(start, 1).value = section
        ws.cell(start + 1, 1).value = "  Итого"
        for offset, value in enumerate((base, base + 1, base + 2), start=2):
            ws.cell(start + 1, offset).value = value

    wb.save(path)
    wb.close()

    observations, concepts, _, _, diagnostics = _parse(path, _spec("hierarchy", "hierarchy"))
    total_ids = {
        next(row["source_concept_id"] for row in observations if row["source_row"] == source_row)
        for source_row in (5, 9, 13)
    }
    assert len(total_ids) == 3
    assert diagnostics["period_block_concept_rewrites"] == 9
    assert len(concepts) == 3
    contexts = "\n".join(row["source_context"] for row in concepts)
    assert "в рублях" in contexts
    assert "в иностранной валюте" in contexts


def test_nested_hierarchy_uses_rarity_ancestry_for_repeated_children(tmp_path):
    path = tmp_path / "nested-hierarchy.xlsx"
    wb = Workbook()
    ws = wb.active
    ws.title = "Квартал (номинальная стоимость)"
    ws["A1"] = "Выпущенные долговые ценные бумаги по номинальной стоимости"
    ws["B3"], ws["C3"], ws["D3"] = "01.01.2024", "01.04.2024", "01.07.2024"

    rows = [
        (4, "Выпущенные долговые ценные бумаги - Итого", None),
        (5, "Итого", None),
        (6, "краткосрочные", 10),
        (7, "Центральный банк", None),
        (8, "краткосрочные", 20),
        (9, "Кредитные организации", None),
        (10, "краткосрочные", 30),
        (12, "Выпущенные долговые ценные бумаги в рублях", None),
        (13, "Итого", None),
        (14, "краткосрочные", 40),
        (15, "Центральный банк", None),
        (16, "краткосрочные", 50),
        (17, "Кредитные организации", None),
        (18, "краткосрочные", 60),
    ]
    for row_no, label, base in rows:
        ws.cell(row_no, 1).value = label
        if base is not None:
            ws.cell(row_no, 2).value = base
            ws.cell(row_no, 3).value = base + 1
            ws.cell(row_no, 4).value = base + 2

    wb.save(path)
    wb.close()

    observations, concepts, _, _, diagnostics = _parse(path, _spec("hierarchy", "hierarchy"))
    child_rows = (6, 8, 10, 14, 16, 18)
    child_ids = {
        next(row["source_concept_id"] for row in observations if row["source_row"] == source_row)
        for source_row in child_rows
    }
    assert len(child_ids) == len(child_rows)
    assert diagnostics["period_block_concept_rewrites"] == 18
    assert len(concepts) == len(child_rows)
    contexts = "\n".join(row["source_context"] for row in concepts)
    assert "Центральный банк" in contexts
    assert "Кредитные организации" in contexts
    assert "в рублях" in contexts
