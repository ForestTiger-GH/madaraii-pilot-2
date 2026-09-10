from cbr_unified.normalization import sheet_dimensions


def test_obs20_statement_currency_presentations_are_explicit():
    total = sheet_dimensions("Активы - всего", "obs_table_20s")
    rub = sheet_dimensions("Активы - рубли", "obs_table_20s")
    fx = sheet_dimensions("Активы - валюта", "obs_table_20s")
    fx_usd = sheet_dimensions("Активы - в ин. валюте $", "obs_table_20s")

    assert total["statement_side"] == "assets"
    assert total["currency_category"] == "total"
    assert rub["currency_category"] == "rubles"
    assert fx["currency_category"] == "foreign_currency"
    assert "measurement_currency" not in fx
    assert fx_usd["currency_category"] == "foreign_currency"
    assert fx_usd["measurement_currency"] == "USD"


def test_obs20_liability_side_is_separate_from_currency():
    dims = sheet_dimensions("Пассивы - рубли", "obs_table_20s")
    assert dims["statement_side"] == "liabilities"
    assert dims["currency_category"] == "rubles"
