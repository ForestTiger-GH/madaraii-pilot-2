from __future__ import annotations

import json
import re
import unicodedata
from datetime import date, datetime
from decimal import Decimal, InvalidOperation
from typing import Any

RU_MONTHS = {
    "январь": 1, "января": 1, "янв": 1,
    "февраль": 2, "февраля": 2, "фев": 2,
    "март": 3, "марта": 3, "мар": 3,
    "апрель": 4, "апреля": 4, "апр": 4,
    "май": 5, "мая": 5,
    "июнь": 6, "июня": 6, "июн": 6,
    "июль": 7, "июля": 7, "июл": 7,
    "август": 8, "августа": 8, "авг": 8,
    "сентябрь": 9, "сентября": 9, "сен": 9, "сент": 9,
    "октябрь": 10, "октября": 10, "окт": 10,
    "ноябрь": 11, "ноября": 11, "ноя": 11,
    "декабрь": 12, "декабря": 12, "дек": 12,
}

EN_MONTHS = {
    "january": 1, "jan": 1, "february": 2, "feb": 2, "march": 3, "mar": 3,
    "april": 4, "apr": 4, "may": 5, "june": 6, "jun": 6, "july": 7, "jul": 7,
    "august": 8, "aug": 8, "september": 9, "sep": 9, "october": 10, "oct": 10,
    "november": 11, "nov": 11, "december": 12, "dec": 12,
}

_TRANSLIT = str.maketrans({
    "а":"a","б":"b","в":"v","г":"g","д":"d","е":"e","ё":"yo","ж":"zh","з":"z","и":"i","й":"y",
    "к":"k","л":"l","м":"m","н":"n","о":"o","п":"p","р":"r","с":"s","т":"t","у":"u","ф":"f",
    "х":"kh","ц":"ts","ч":"ch","ш":"sh","щ":"shch","ъ":"","ы":"y","ь":"","э":"e","ю":"yu","я":"ya",
    "А":"A","Б":"B","В":"V","Г":"G","Д":"D","Е":"E","Ё":"Yo","Ж":"Zh","З":"Z","И":"I","Й":"Y",
    "К":"K","Л":"L","М":"M","Н":"N","О":"O","П":"P","Р":"R","С":"S","Т":"T","У":"U","Ф":"F",
    "Х":"Kh","Ц":"Ts","Ч":"Ch","Ш":"Sh","Щ":"Shch","Ъ":"","Ы":"Y","Ь":"","Э":"E","Ю":"Yu","Я":"Ya",
})


def normalize_text(value: Any) -> str:
    """Conservative search normalization. Never use as semantic identity by itself."""
    if value is None:
        return ""
    s = unicodedata.normalize("NFKC", str(value)).replace("\u00a0", " ").replace("\u200b", "")
    s = re.sub(r"\s+", " ", s).strip()
    return s.casefold()


def normalize_sheet_dispatch(value: str) -> str:
    """A source-scoped dispatch key; punctuation is retained except typographic dash variants."""
    s = normalize_text(value)
    s = s.replace("–", "-").replace("—", "-").replace("−", "-")
    return s


def transliterate_ru(value: str) -> str:
    return str(value).translate(_TRANSLIT)


def parse_decimal_text(value: Any) -> Decimal | None:
    if isinstance(value, bool) or value is None:
        return None
    if isinstance(value, Decimal):
        return value
    if isinstance(value, int):
        return Decimal(value)
    if isinstance(value, float):
        return Decimal(str(value))
    if not isinstance(value, str):
        return None
    s = unicodedata.normalize("NFKC", value).strip().replace("\u00a0", " ")
    if not s or s in {"-", "—", "–", "…", "..", "."}:
        return None
    # Thousands spaces and decimal comma are common in spreadsheet text values.
    s = re.sub(r"(?<=\d)[ \u202f](?=\d{3}(?:\D|$))", "", s)
    if re.fullmatch(r"[+-]?(?:\d+(?:[.,]\d+)?|[.,]\d+)", s):
        try:
            return Decimal(s.replace(",", "."))
        except InvalidOperation:
            return None
    return None


def parse_period(value: Any) -> tuple[str, str, str] | None:
    """Return ISO period anchor, frequency, source representation kind."""
    if isinstance(value, datetime):
        return value.date().isoformat(), "monthly_or_point", "excel_date"
    if isinstance(value, date):
        return value.isoformat(), "monthly_or_point", "excel_date"
    if value is None:
        return None
    s0 = unicodedata.normalize("NFKC", str(value)).replace("\u00a0", " ").strip()
    if not s0:
        return None
    s = s0.casefold().replace("–", "-").replace("—", "-")

    m = re.fullmatch(r"(\d{1,2})[.\-/](\d{1,2})[.\-/](\d{4})", s)
    if m:
        d, mo, y = map(int, m.groups())
        try:
            return date(y, mo, d).isoformat(), "monthly_or_point", "date_string"
        except ValueError:
            return None

    m = re.fullmatch(r"(\d{4})-(\d{1,2})-(\d{1,2})", s)
    if m:
        y, mo, d = map(int, m.groups())
        try:
            return date(y, mo, d).isoformat(), "monthly_or_point", "iso_date_string"
        except ValueError:
            return None

    m = re.fullmatch(r"([а-яёa-z]+)[\s.-]+(\d{4})", s)
    if m:
        month_token, y = m.groups()
        mo = RU_MONTHS.get(month_token) or EN_MONTHS.get(month_token)
        if mo:
            return date(int(y), mo, 1).isoformat(), "monthly", "month_year_text"

    m = re.fullmatch(r"(?:([ivx]+)|([1-4]))\s*(?:кв(?:арт(?:ал)?)?\.?|q)\s*(\d{4})", s)
    if m:
        roman, digit, y = m.groups()
        q = int(digit) if digit else {"i":1, "ii":2, "iii":3, "iv":4}.get(roman)
        if q:
            return date(int(y), 1 + 3 * (q - 1), 1).isoformat(), "quarterly", "quarter_text"

    m = re.fullmatch(r"(\d{4})", s)
    if m:
        return date(int(m.group(1)), 1, 1).isoformat(), "annual", "year_text"
    return None


def infer_unit(*texts: str) -> tuple[str | None, int | None]:
    text = " ".join(normalize_text(t) for t in texts if t)
    if re.search(r"млрд\.?\s*руб", text):
        return "RUB", 1_000_000_000
    if re.search(r"млн\.?\s*руб", text):
        return "RUB", 1_000_000
    if re.search(r"тыс\.?\s*руб", text):
        return "RUB", 1_000
    if re.search(r"млн\.?\s*(?:долл|usd)", text):
        return "USD", 1_000_000
    if re.search(r"млрд\.?\s*(?:долл|usd)", text):
        return "USD", 1_000_000_000
    if "%" in text or "процент" in text:
        return "percent", 1
    if re.search(r"\bединиц(?:а|ы)?\b|\bед\.\b", text):
        return "count", 1
    if "рублей за единицу" in text or "руб. за единицу" in text or "рублей за 1" in text:
        return "RUB_per_currency_unit", 1
    return None, None


def sheet_dimensions(sheet: str, source_id: str = "") -> dict[str, str]:
    s = normalize_sheet_dispatch(sheet)
    dims: dict[str, str] = {}

    if "инвалют" in s or "иностран" in s or "в валюте" in s:
        dims["currency_category"] = "foreign_currency"
    elif "в руб" in s or s.startswith("руб"):
        dims["currency_category"] = "rubles"
    elif s in {"итого", "всего"} or " итого" in s:
        dims["currency_category"] = "total"

    if "просроч" in s:
        dims["overdue"] = "true"

    # CBR mortgage sheets use abbreviated wording: "по приобр. правам" means
    # acquired claims only, while "с учетом приобр. прав" means the measure
    # including acquired claims. These are distinct statistical populations.
    if "с учетом приобр" in s and "прав" in s:
        dims["acquired_claims"] = "included"
    elif "по приобр" in s and "прав" in s:
        dims["acquired_claims"] = "acquired_only"
    elif "с правами требования" in s or "включая права требования" in s:
        dims["acquired_claims"] = "included"
    elif "права требования" in s:
        dims["acquired_claims"] = "acquired_only"

    if "(с.к" in s or "с.к." in s or "сезон" in s:
        dims["adjustment"] = "seasonally_adjusted"
    else:
        dims["adjustment"] = "original"

    if "номин" in s:
        dims["valuation"] = "nominal"
    elif "рыноч" in s:
        dims["valuation"] = "market"
    if "кварт" in s:
        dims["frequency_sheet"] = "quarterly"
    elif "месяц" in s:
        dims["frequency_sheet"] = "monthly"

    if source_id == "obs_table_20s":
        if "актив" in s:
            dims["statement_side"] = "assets"
        elif "пассив" in s:
            dims["statement_side"] = "liabilities"

        # This workbook publishes the same statement geometry in four explicit
        # currency presentations. "валюта" and "в ин. валюте $" are both foreign-
        # currency denomination; the latter additionally changes the measurement
        # currency to USD. Denomination and measurement currency remain separate.
        if s.endswith("- всего"):
            dims["currency_category"] = "total"
        elif s.endswith("- рубли"):
            dims["currency_category"] = "rubles"
        elif s.endswith("- валюта") or "в ин. валюте" in s:
            dims["currency_category"] = "foreign_currency"
        if "доллар" in s or "$" in s:
            dims["measurement_currency"] = "USD"

    return dims


def territory_type(label: str) -> str:
    s = normalize_text(label)
    if s == "российская федерация" or s.startswith("российская федерация "):
        return "country_total"
    if "федеральный округ" in s:
        return "federal_district"
    if s.startswith("в том числе"):
        return "included_subregion"
    if " без " in f" {s} ":
        return "excluding_subregion_aggregate"
    return "region_or_subject"


def stable_dimensions_json(dims: dict[str, Any]) -> str:
    return json.dumps({k: dims[k] for k in sorted(dims) if dims[k] not in (None, "")}, ensure_ascii=False, separators=(",", ":"))
