from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from urllib.parse import unquote, urlparse


@dataclass(frozen=True)
class SourceSpec:
    source_id: str
    url: str
    name_ru: str
    name_en: str
    family: str
    row_axis: str
    parser: str = "matrix"
    classification: str | None = None
    period_role: str = "source_defined"

    @property
    def filename(self) -> str:
        return unquote(Path(urlparse(self.url).path).name)


# This is the product-owned, reviewed Baseline copied only from the single permitted
# stratbox registry input. It intentionally contains no dependency on stratbox code.
SOURCES: tuple[SourceSpec, ...] = (
    SourceSpec("mortgage_debt_ind", "https://www.cbr.ru/vfs/statistics/BankSector/Mortgage/02_05_Debt_ind.xlsx", "Задолженность по кредитам физическим лицам", "Household loan debt", "mortgage", "region", period_role="stock"),
    SourceSpec("mortgage_debt", "https://www.cbr.ru/vfs/statistics/BankSector/Mortgage/02_14_Debt_mortgage.xlsx", "Задолженность по ипотечным жилищным кредитам", "Housing mortgage loan debt", "mortgage", "region", period_role="stock"),
    SourceSpec("mortgage_scpa_debt", "https://www.cbr.ru/vfs/statistics/BankSector/Mortgage/02_18_Debt_scpa_mortgage.xlsx", "Задолженность по ипотечным жилищным кредитам по ДДУ", "Housing mortgage loan debt under shared construction agreements", "mortgage", "region", period_role="stock"),
    SourceSpec("mortgage_ihc", "https://www.cbr.ru/vfs/statistics/banksector/mortgage/02_41_Mortgage_ihc.xlsx", "Ипотечные кредиты для индивидуального жилищного строительства", "Mortgage loans for individual housing construction", "mortgage", "indicator"),
    SourceSpec("mortgage_full", "https://www.cbr.ru/vfs/statistics/BankSector/Mortgage/02_02_Mortgage.xlsx", "Ипотечное жилищное кредитование", "Housing mortgage lending", "mortgage", "indicator"),
    SourceSpec("mortgage_scpa_full", "https://www.cbr.ru/vfs/statistics/BankSector/Mortgage/02_03_Scpa_mortgage.xlsx", "Ипотечное жилищное кредитование по ДДУ", "Housing mortgage lending under shared construction agreements", "mortgage", "indicator"),
    SourceSpec("corp_new_loans_a", "https://www.cbr.ru/vfs/statistics/BankSector/Loans_to_corporations/01_01_A_New_loans_corp_by_activity.xlsx", "Кредиты организациям и ИП по видам деятельности — историческая классификация", "Loans to corporations and individual entrepreneurs by activity — historical classification", "corporate_sme", "activity", classification="historical_activity", period_role="flow"),
    SourceSpec("corp_new_loans_c", "https://www.cbr.ru/vfs/statistics/BankSector/Loans_to_corporations/01_01_C_New_loans_corp_by_activity.xlsx", "Кредиты организациям и ИП по ОКВЭД2", "Loans to corporations and individual entrepreneurs by OKVED2", "corporate_sme", "activity", classification="OKVED2", period_role="flow"),
    SourceSpec("corp_debt_a", "https://www.cbr.ru/vfs/statistics/BankSector/Loans_to_corporations/01_02_A_Debt_corp_by_activity.xlsx", "Задолженность организаций и ИП по видам деятельности — историческая классификация", "Corporate and individual entrepreneur debt by activity — historical classification", "corporate_sme", "activity", classification="historical_activity", period_role="stock"),
    SourceSpec("corp_debt_c", "https://www.cbr.ru/vfs/statistics/BankSector/Loans_to_corporations/01_02_C_Debt_corp_by_activity.xlsx", "Задолженность организаций и ИП по ОКВЭД2", "Corporate and individual entrepreneur debt by OKVED2", "corporate_sme", "activity", classification="OKVED2", period_role="stock"),
    SourceSpec("sme_debt", "https://www.cbr.ru/vfs/statistics/BankSector/Loans_to_corporations/01_11_Debt_sme.xlsx", "Задолженность субъектов МСП", "SME debt", "corporate_sme", "indicator", period_role="stock"),
    SourceSpec("sme_debt_activity", "https://www.cbr.ru/vfs/statistics/BankSector/Loans_to_corporations/01_11_F_Debt_sme_by_activity.xlsx", "Задолженность субъектов МСП по ОКВЭД2", "SME debt by OKVED2", "corporate_sme", "activity", classification="OKVED2", period_role="stock"),
    SourceSpec("sme_debt_subj_f", "https://www.cbr.ru/vfs/statistics/BankSector/Loans_to_corporations/01_13_F_Debt_sme_subj.xlsx", "Задолженность субъектов МСП по регионам", "SME debt by region", "corporate_sme", "region", period_role="stock"),
    SourceSpec("sme_debt_subj_i", "https://www.cbr.ru/vfs/statistics/BankSector/Loans_to_corporations/01_13_I_Debt_sme_subj.xlsx", "Задолженность индивидуальных предпринимателей по регионам", "Individual entrepreneur debt by region", "corporate_sme", "region", period_role="stock"),
    SourceSpec("corp_debt_subj", "https://www.cbr.ru/vfs/statistics/BankSector/Loans_to_corporations/01_05_D_Debt_subj.xlsx", "Задолженность организаций и ИП по регионам", "Corporate and individual entrepreneur debt by region", "corporate_sme", "region", period_role="stock"),
    SourceSpec("debt_structure_benchmark_rate", "https://cbr.ru/vfs/statistics/BankSector/Loans_to_corporations/02_03_Debt_structure_by_benchmark_interest_rate_type.xlsx", "Структура задолженности по виду процентной ставки и базового компонента", "Debt structure by interest-rate type and benchmark component", "corporate_sme", "indicator", period_role="stock"),
    SourceSpec("sme_borrowers_info", "https://www.cbr.ru/vfs/statistics/banksector/loans_to_corporations/02_02_SME_Borrowers_info.xlsx", "Сведения о заемщиках МСП и выданных кредитах", "Information on SME borrowers and granted loans", "corporate_sme", "mixed", parser="mixed"),
    SourceSpec("sme_by_activity", "https://www.cbr.ru/vfs/statistics/BankSector/Loans_to_corporations/01_10_F_New_loans_sme_by_activity.xlsx", "Кредиты субъектам МСП по ОКВЭД2", "Loans granted to SMEs by OKVED2", "corporate_sme", "activity", classification="OKVED2", period_role="flow"),
    SourceSpec("debt_securities", "https://www.cbr.ru/vfs/statistics/debt_securities/66-debt_securities.xlsx", "Долговые ценные бумаги", "Debt securities", "debt_securities", "hierarchy", parser="hierarchy"),
    SourceSpec("funds_all", "https://www.cbr.ru/vfs/statistics/BankSector/Borrowings/02_01_Funds_all.xlsx", "Привлеченные средства", "Borrowings", "borrowings", "indicator", period_role="stock"),
    SourceSpec("funds_clients", "https://www.cbr.ru/vfs/statistics/BankSector/Borrowings/02_02_Funds_clients.xlsx", "Средства клиентов по регионам", "Client funds by region", "borrowings", "region", period_role="stock"),
    SourceSpec("funds_org", "https://www.cbr.ru/vfs/statistics/BankSector/Borrowings/02_04_Funds_org.xlsx", "Средства организаций по регионам", "Corporate funds by region", "borrowings", "region", period_role="stock"),
    SourceSpec("dep_corp", "https://www.cbr.ru/vfs/statistics/BankSector/Borrowings/02_05_Dep_corp.xlsx", "Депозиты организаций по регионам", "Corporate deposits by region", "borrowings", "region", period_role="stock"),
    SourceSpec("dep_ind", "https://www.cbr.ru/vfs/statistics/BankSector/Borrowings/02_06_Dep_ind.xlsx", "Вклады физических лиц по регионам", "Household deposits by region", "borrowings", "region", period_role="stock"),
    SourceSpec("dep_ind_no_escrow", "https://www.cbr.ru/vfs/statistics/banksector/borrowings/02_27_Dep_ind_excluding_escrow.xlsx", "Вклады физических лиц без счетов эскроу по регионам", "Household deposits excluding escrow accounts by region", "borrowings", "region", period_role="stock"),
    SourceSpec("dep_entrepreneur", "https://www.cbr.ru/vfs/statistics/BankSector/Borrowings/02_07_Dep_enterpreneur.xlsx", "Средства индивидуальных предпринимателей по регионам", "Individual entrepreneur funds by region", "borrowings", "region", period_role="stock"),
    SourceSpec("escrow_accounts", "https://www.cbr.ru/vfs/statistics/banksector/borrowings/02_28_Escrow_accounts.xlsx", "Счета эскроу физических лиц по регионам", "Household escrow accounts by region", "borrowings", "region", period_role="stock"),
    SourceSpec("budget_all", "https://www.cbr.ru/vfs/statistics/banksector/borrowings/02_29_Budget_all.xlsx", "Средства бюджетов", "Budget funds", "borrowings", "indicator", period_role="stock"),
    SourceSpec("households_bm", "https://cbr.ru/vfs/statistics/households/households_bm.xlsx", "Финансовые активы и обязательства домашних хозяйств — балансы", "Household financial assets and liabilities — balances", "households", "hierarchy", parser="hierarchy", period_role="stock"),
    SourceSpec("households_om", "https://cbr.ru/vfs/statistics/households/households_om.xlsx", "Финансовые активы и обязательства домашних хозяйств — операции", "Household financial assets and liabilities — transactions", "households", "hierarchy", parser="hierarchy", period_role="flow"),
    SourceSpec("monetary_agg", "https://www.cbr.ru/vfs/statistics/credit_statistics/monetary_agg.xlsx", "Денежные агрегаты", "Monetary aggregates", "monetary_financial", "hierarchy", parser="hierarchy"),
    SourceSpec("survey_cb", "https://www.cbr.ru/vfs/statistics/credit_statistics/survey/survey_cb.xlsx", "Обзор центрального банка", "Central Bank Survey", "monetary_financial", "hierarchy", parser="hierarchy", period_role="stock"),
    SourceSpec("balance_odc", "https://www.cbr.ru/vfs/statistics/credit_statistics/survey/balance_odc.xlsx", "Баланс кредитных организаций", "Balance of other depository corporations", "monetary_financial", "hierarchy", parser="hierarchy", period_role="stock"),
    SourceSpec("survey_odc", "https://www.cbr.ru/vfs/statistics/credit_statistics/survey/survey_odc.xlsx", "Обзор кредитных организаций", "Other Depository Corporations Survey", "monetary_financial", "hierarchy", parser="hierarchy", period_role="stock"),
    SourceSpec("survey_dc_new", "https://www.cbr.ru/vfs/statistics/credit_statistics/survey/survey_dc_new.xlsx", "Обзор банковской системы", "Depository Corporations Survey", "monetary_financial", "hierarchy", parser="hierarchy", period_role="stock"),
    SourceSpec("annex_survey_dc", "https://www.cbr.ru/vfs/statistics/credit_statistics/survey/annex_survey_dc.xlsx", "Приложение к обзору банковской системы", "Annex to Depository Corporations Survey", "monetary_financial", "hierarchy", parser="hierarchy"),
    SourceSpec("debt_new", "https://www.cbr.ru/vfs/statistics/credit_statistics/debt/debt_new.xlsx", "Внешний долг Российской Федерации", "External debt of the Russian Federation", "external_debt", "hierarchy", parser="hierarchy", period_role="stock"),
    SourceSpec("debt_maturity", "https://www.cbr.ru/vfs/statistics/credit_statistics/debt/debt_maturity.xlsx", "Внешний долг по срокам погашения и финансовым инструментам", "External debt by maturity and financial instrument", "external_debt", "hierarchy", parser="hierarchy", period_role="stock"),
    SourceSpec("debt_cur-mat_new", "https://www.cbr.ru/vfs/statistics/credit_statistics/debt/debt_cur-mat_new.xlsx", "Внешний долг в национальной и иностранной валютах", "External debt in national and foreign currencies", "external_debt", "hierarchy", parser="hierarchy", period_role="stock"),
    SourceSpec("obs_table_20s", "https://www.cbr.ru/Content/Document/File/115862/obs_tabl20%D1%81.xlsx", "Отдельные показатели деятельности кредитных организаций", "Selected indicators of credit institution activity", "other", "hierarchy", parser="hierarchy", period_role="stock"),
    SourceSpec("exchange_rate", "https://cbr.ru/vfs/statistics/credit_statistics/ex_rate_ind/exchange_rate.xlsx", "Показатели валютного курса", "Exchange-rate indicators", "exchange_rates", "hierarchy", parser="exchange"),
)

SOURCE_BY_ID = {s.source_id: s for s in SOURCES}
if len(SOURCE_BY_ID) != len(SOURCES):
    raise RuntimeError("Duplicate source_id in product registry")
if len({s.url for s in SOURCES}) != len(SOURCES):
    raise RuntimeError("Duplicate URL in product registry")


def get_source(source_id: str) -> SourceSpec:
    try:
        return SOURCE_BY_ID[source_id]
    except KeyError as exc:
        raise KeyError(f"Unknown source_id: {source_id}") from exc
