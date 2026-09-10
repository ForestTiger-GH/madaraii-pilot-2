import pytest

from cbr_unified.registry import SOURCES
from cbr_unified.validation import ValidationError, _validate_bilingual_rows


def test_registry_sources_have_bilingual_dataset_names():
    assert len(SOURCES) == 41
    assert all(source.name_ru.strip() and source.name_en.strip() for source in SOURCES)


def test_bilingual_row_gate_accepts_complete_project_translation():
    statuses = _validate_bilingual_rows(
        [
            {
                "label_ru_source": "Задолженность",
                "name_ru": "Задолженность",
                "name_en": "Debt",
                "translation_status": "project_translation",
            }
        ],
        label="source_concepts",
        source_label_field="label_ru_source",
    )
    assert statuses == {"project_translation": 1}


def test_bilingual_row_gate_rejects_missing_english_name():
    with pytest.raises(ValidationError, match="incomplete bilingual/source surface"):
        _validate_bilingual_rows(
            [
                {
                    "label_ru_source": "Задолженность",
                    "name_ru": "Задолженность",
                    "name_en": "",
                    "translation_status": "project_translation",
                }
            ],
            label="source_concepts",
            source_label_field="label_ru_source",
        )


def test_bilingual_row_gate_rejects_unknown_translation_status():
    with pytest.raises(ValidationError, match="invalid translation_status"):
        _validate_bilingual_rows(
            [
                {
                    "source_value_ru": "Москва",
                    "name_ru": "Москва",
                    "name_en": "Moskva",
                    "translation_status": "guessed",
                }
            ],
            label="dimension_members",
            source_label_field="source_value_ru",
        )
