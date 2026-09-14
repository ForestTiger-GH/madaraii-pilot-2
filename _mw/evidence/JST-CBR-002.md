# JST-CBR-002 — Semantic-inference Jester evidence

**Owner:** `JST-CBR-002`  
**Work:** `WORK-JESTER-0002`  
**Method:** `MADARAII-40`  
**Product baseline under provocation:** `4ee8583b3feff7775a956c51812232fa0d0516d2`  
**Experimental branch:** `jester/jst-0002`  
**Governing MADARAII baseline:** `ForestTiger-GH/MADARAII@721a199352b5c5282b1478cd6a5eb36a9872fb34`  
**Evidence state:** CAPTURED; restoration verification pending at initial write

## Control shell

All executable provocations ran on the derived branch created from the exact admitted Product revision. The canonical Product code on `main` was outside the experiment surface.

The branch-only GitHub Actions workflow performed repository checkout, Python 3.12 setup, editable package installation with test dependencies, and `pytest -q`. Its token had `contents: read`. No live Bank of Russia acquisition, release, deployment, source-system write, secret use, or customer-data operation formed part of this Work.

## Experiment trajectory

| Wave | Experimental commit | CI run | Outcome | Meaning |
|---|---|---:|---|---|
| Harness | `4c311b7fe8375459c986d1497934d7cc6d355f2c` | `34894626350` | PASS | isolated branch-only test harness |
| Inference wave | `bf901a664a233c5bc276bce0557d8135a9cd114c` | `34894678755` | EXPECTED PROBE FAILURE | one Jester assertion used a phrase that did not activate the tested rule; evidence preserved and trajectory adapted |
| Sharpened inference | `223f09f65de61d809f268e0c2026adf5fd3f6179` | `34894764636` | PASS | sharpened the negation phrase to the exact recognized lexical form |
| Variant-drift wave | `ebcbd7767519321a7de6330c4ea1c5e34dd27dd9` | `34894854255` | PASS | final two source-variant provocations; budget reached |

The failed run `34894678755` is retained as a blocked/failed provocation record rather than erased. It showed that `"Без прав требования"` did not activate `acquired_claims`; the adaptive next step changed the phrase to `"Без права требования"`, which did activate `acquired_claims=acquired_only` despite the negation. The final CI run completed the ordinary suite plus all disposable Jester-2 reproducers successfully.

## Provocation ledger

### JST2-P01 — «Negation shredder»

**Tried:** place explicit negation around familiar qualifier words.

**Observed:** `_embedded_dimensions("Непросроченная задолженность", ...)` yields `overdue=true`; `sheet_dimensions("Без просроченной задолженности")` also yields `overdue=true`; `sheet_dimensions("Без права требования")` yields `acquired_claims=acquired_only`; `sheet_dimensions("Несезонно скорректированные данные")` yields `adjustment=seasonally_adjusted`.

**Evidence:** `tests/test_jester_inference_provocations.py`; runs `34894678755` and `34894764636`.

### JST2-P02 — «Money perfume»

**Tried:** give a row an explicit percent or count meaning while the broader table title says `млн руб.`.

**Observed:** `infer_unit("Темп прироста, %", "Показатели, млн руб.")` and `infer_unit("Количество заемщиков, единиц", "Показатели, млн руб.")` both resolve to `RUB`, scale `1_000_000`.

### JST2-P03 — «Methodology word hijack»

**Tried:** put the word `изменение` in methodological or negated context around a stock measure.

**Observed:** `_period_role` returns `published_change` for both `sheet="Изменение методологии"` with label `Задолженность` and label `Изменение отсутствует — задолженность`.

### JST2-P04 — «Country total with amputated limb»

**Tried:** label a national total while explicitly excluding part of the territory.

**Observed:** `territory_type("Российская Федерация без данных по отдельной территории")` resolves to `country_total`; the exclusion meaning is outside that type result.

### JST2-P05 — «Methodology calendar cosplay»

**Tried:** make three methodology-revision dates look geometrically like a period header and put technical control values beneath them.

**Observed:** real workbook parsing materializes the control values as three semantic observations for those dates; their dispositions become `observation_value`, and the numeric disposition gate reports `passed`.

### JST2-P06 — «Nine angels, ten demons»

**Tried:** feed a workbook unknown numerics without a recognized period axis and vary only the count.

**Observed:** nine numerics can yield zero observations with the numeric gate `passed`; ten numerics in the same pattern trigger `SourceVariantError` for numeric candidates without semantic observations. The semantic posture changes discontinuously at that count boundary.

### JST2-P07 — «Two maturity buckets enter, one leaves»

**Tried:** give one label a combined scope: `Итого: до 1 года и свыше 1 года`.

**Observed:** `_embedded_dimensions` resolves only `maturity_bucket=up_to_1_year` because the first matching branch wins.

### JST2-P08 — «Calendar type caste system»

**Tried:** express the same year headers as numeric Excel values and as text.

**Observed:** generic period discovery ignores integer `2024/2025/2026`; the same values as strings become annual periods. This is a type-sensitive source-variant boundary.

### JST2-P09 — «One regional concept, two incompatible careers»

**Tried:** create one region-axis workbook with two sheets: debt in `млн руб.` and loan count in `единиц`, both for Moscow and the same periods.

**Observed:** parsing produces six observations with two different units but only one `source_concept_id` / one concept because a region-axis concept uses the source-level `dataset_measure` local key. The numeric disposition gate reports `passed`.

**Evidence:** `tests/test_jester_inference_wave2.py`; commit `ebcbd7767519321a7de6330c4ea1c5e34dd27dd9`; CI `34894854255`.

### JST2-P10 — «Accounting parentheses invisibility cloak»

**Tried:** use `(10)`, `(20)`, `(30)` as number-like source values in an otherwise recognized matrix.

**Observed:** parsing produces zero observations, `unmapped_numeric_count=0`, and `numeric_disposition_gate=passed`; no value is classified `unmapped_numeric`. These lexical forms are outside the current numeric parser and therefore outside the numeric-completeness gate.

**Evidence:** `tests/test_jester_inference_wave2.py`; commit `ebcbd7767519321a7de6330c4ea1c5e34dd27dd9`; CI `34894854255`.

## Session boundary

The fixed budget of ten materially different provocations was reached. The second pass continued to produce distinct semantic-inference signals through the last wave, so the session ended because its authorized budget was exhausted rather than because the final experiments were empty.

This evidence establishes observed behavior only. It assigns no defect status, severity, root cause, priority, Product requirement, or repair. Those dispositions belong to the mandatory non-Jester continuation after restoration.
