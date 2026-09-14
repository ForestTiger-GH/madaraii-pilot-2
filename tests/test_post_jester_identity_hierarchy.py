from openpyxl import Workbook

from cbr_unified.semantic import _concept, _row_hierarchy_context
from cbr_unified.registry import SourceSpec


def _spec():
    return SourceSpec(
        source_id="synthetic",
        url="https://cbr.ru/test.xlsx",
        name_ru="Тест",
        name_en="Test",
        family="test",
        row_axis="indicator",
        period_role="stock",
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
    # Mirrors a real-source presentation typo: identical child label in another section.
    ws["A8"] = "  на приобретение объектов, единиц"

    first_context = _row_hierarchy_context(ws, 5, 2, 2)
    second_context = _row_hierarchy_context(ws, 8, 2, 2)
    assert first_context == "Количество кредитов, единиц, в том числе"
    assert second_context == "Объем кредитов, млн руб., в том числе"

    first = _concept(
        _spec(),
        sheet="Data",
        row=5,
        label="на приобретение объектов, единиц",
        title="Ипотечные кредиты",
        row_axis="indicator",
        unit="count",
        scale=1,
        identity_context=first_context,
    )
    second = _concept(
        _spec(),
        sheet="Data",
        row=8,
        label="на приобретение объектов, единиц",
        title="Ипотечные кредиты",
        row_axis="indicator",
        unit="count",
        scale=1,
        identity_context=second_context,
    )
    moved = _concept(
        _spec(),
        sheet="Data",
        row=50,
        label="на приобретение объектов, единиц",
        title="Ипотечные кредиты",
        row_axis="indicator",
        unit="count",
        scale=1,
        identity_context=first_context,
    )
    assert first["source_concept_id"] != second["source_concept_id"]
    assert first["source_concept_id"] == moved["source_concept_id"]
    wb.close()
