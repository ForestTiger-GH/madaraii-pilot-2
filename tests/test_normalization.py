from cbr_unified.normalization import (
    infer_unit,
    normalize_text,
    parse_period,
    sheet_dimensions,
    stable_dimensions_json,
)


def test_conservative_normalization_preserves_punctuation_identity():
    assert normalize_text("  1.1  ") == "1.1"
    assert normalize_text("11") == "11"
    assert normalize_text("1.1") != normalize_text("11")


def test_period_and_unit_parsing():
    assert parse_period("Май 2026") == ("2026-05-01", "monthly", "month_year_text")
    assert parse_period("01.08.2026") == ("2026-08-01", "monthly_or_point", "date_string")
    assert infer_unit("Задолженность, млн руб.") == ("RUB", 1_000_000)
    assert infer_unit("Доля, %") == ("percent", 1)


def test_sheet_dimensions_keep_distinct_statistical_axes():
    dims = sheet_dimensions("Квартал (рыночная стоимость)")
    assert dims["valuation"] == "market"
    assert dims["frequency_sheet"] == "quarterly"
    assert dims["adjustment"] == "original"
    assert stable_dimensions_json({"b": "2", "a": "1"}) == '{"a":"1","b":"2"}'
