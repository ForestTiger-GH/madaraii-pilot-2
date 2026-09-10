from cbr_unified.normalization import sheet_dimensions


def test_full_and_abbreviated_overdue_labels_are_equivalent_dimensions():
    full = sheet_dimensions("в т.ч. просроч. в рублях", "corp_debt_c")
    abbreviated = sheet_dimensions("МСП в т.ч. проср. в рублях", "sme_debt_subj_f")
    short_no_dot = sheet_dimensions("ИП в т.ч проср в инвалюте", "sme_debt_subj_i")

    assert full["overdue"] == "true"
    assert abbreviated["overdue"] == "true"
    assert short_no_dot["overdue"] == "true"
    assert abbreviated["currency_category"] == "rubles"
    assert short_no_dot["currency_category"] == "foreign_currency"
