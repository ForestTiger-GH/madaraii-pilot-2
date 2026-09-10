from cbr_unified.normalization import sheet_dimensions


def test_acquired_claims_sheet_variants_are_distinct():
    ordinary = sheet_dimensions("в рублях", "mortgage_debt")
    acquired = sheet_dimensions("по приобр. правам в рублях", "mortgage_debt")
    included = sheet_dimensions("с учетом приобр. прав в рублях", "mortgage_debt")

    assert ordinary["currency_category"] == "rubles"
    assert "acquired_claims" not in ordinary
    assert acquired["currency_category"] == "rubles"
    assert acquired["acquired_claims"] == "acquired_only"
    assert included["currency_category"] == "rubles"
    assert included["acquired_claims"] == "included"


def test_acquired_claims_total_variant_keeps_total_currency_scope():
    dims = sheet_dimensions("с учетом приобр. прав итого", "mortgage_debt")
    assert dims["currency_category"] == "total"
    assert dims["acquired_claims"] == "included"
