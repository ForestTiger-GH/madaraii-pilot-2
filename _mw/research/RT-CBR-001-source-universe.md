# RT-CBR-001 — Complete CBR source-universe census and structural classification

**Work kind:** `EXTERNAL_DESCRIPTIVE_RESEARCH` (`MADARAII-08`)  
**Research Topic:** `RT-CBR-001` from `RES-RESEARCH-QUAL-001`  
**Registry Baseline:** `ForestTiger-GH/stratbox/src/stratbox/macrobanks/cbr_file_collector/registry.py@b7af2c380a028984ec4b465250ac44a0f05efab6`  
**Evidence acquisition commit:** `140338646aef5a0cc5ab8db4abf04af3945b25c5`  
**Readable evidence commit:** `4782c08fc86b0d6e481103970499b3559d73062a`  
**Status:** established Research Result

## Research question and boundary

What files, sheets, table geometries, label patterns, numeric regions, units, periods, regions/classifications, revisions and structural variants actually exist across every URL declared by the permitted registry, and which differences are clearly presentation-level versus candidates for semantic distinction?

The research universe is exactly the 41 Bank of Russia URLs declared by the bound registry. No other `stratbox` content was inspected. Primary evidence is the downloaded workbook content itself. Bank of Russia methodological/publication pages are supplementary interpretation evidence only.

## Complete source accounting

A reproducible internet-enabled probe acquired **41 of 41** registry workbooks with **0 acquisition/inspection failures**. The probe inspected **162 worksheets**, indexed **36,161 text cells**, recorded workbook byte size and SHA-256 for every source, and retained per-sheet bounds, cell-type counts, merges, number formats, formulas, exact text labels and representative date/numeric anchors.

Authoritative evidence routes:

- `_mw/research/evidence/source-probe/MANIFEST.json` — exact URL, HTTP disposition and SHA-256 for every workbook;
- `_mw/research/evidence/source-probe/SHEET_INDEX.csv` — all 162 sheets with geometry/type counts;
- `_mw/research/evidence/source-probe/LABEL_INDEX.csv` — every indexed source text cell with coordinate and conservative normalization candidates;
- `_mw/research/evidence/source-probe/<source_id>.json` — per-workbook evidence;
- `_mw/research/evidence/research-pack/FAMILY-*.md` — readable family evidence;
- `_mw/research/evidence/research-pack/STRUCTURAL-CLUSTERS.md` and `PRESENTATION-COLLISIONS.md` — discovery aids only, never semantic identity authorities.

The manifest is a full census, rather than a representative sample. Structural classification below uses all sources while interpreting representative members and outliers in detail.

## Observed source families and structural forms

### 1. Regional/date matrices for mortgage and banking-sector statistics

Several mortgage, corporate-credit and borrowings workbooks use a wide time axis with one source row axis and sheet-level dimensions.

Observed variants include:

- mortgage debt of resident individuals by territory, with separate worksheets for rubles, foreign currency, totals and overdue debt;
- mortgage debt variants additionally separating acquired claims and debt including acquired claims;
- corporate/SME debt by activity or territory, with currency and overdue status carried by worksheet;
- attracted-funds workbooks with currency carried by worksheet and territorial/aggregate rows in the table.

The same visible worksheet names (`в рублях`, `в инвалюте`, `итого`, overdue variants) recur across many workbooks. They are therefore useful **local sheet dimensions**, not global indicator identities.

Regional tables contain several territorial semantic levels in the same axis: Russian Federation, federal districts, constituent entities, autonomous okrug inclusions and explicit “region excluding autonomous okrug(s)” rows. A universal `region_name -> region_id` mapping that erases these distinctions would lose source meaning. The model must preserve a territorial member's exact published scope and hierarchy/type.

Period cells vary in physical representation. Some workbooks store Excel dates; many banking-sector files store visually identical dates as strings such as `01.02.2012`; corporate flow tables may use Russian month-year strings such as `Январь 2018`. This is a presentation variation around a potentially shared monthly period concept, provided the statistical meaning of the date is also preserved (stock date versus flow month).

### 2. Activity-classification matrices

Corporate and SME loan files demonstrate at least two classification regimes.

- `corp_*_a` files describe economic activities and specific uses through a compact historical row taxonomy.
- `corp_*_c` files explicitly state `Класс ОКВЭД2` and contain a materially larger class axis.

The Bank of Russia current summary methodology states that borrower activities correspond to the Russian Classification of Economic Activities harmonized with NACE Rev. 2 for the current publication surface. That does not retroactively make historical `A` rows identical to `C` rows. Classification regime/vintage is therefore part of source semantics.

The exact structural signature of `corp_debt_c` equals `sme_debt_activity`; likewise `corp_new_loans_c` equals `sme_by_activity`. This is strong evidence for reusable parsing geometry and equally strong counterevidence against treating geometry as semantic identity: the population differs (all resident legal entities/individual entrepreneurs versus SME).

### 3. One-sheet indicator/date matrices with nested row semantics

`debt_structure_benchmark_rate` and `sme_borrowers_info` are one-sheet files but their rows encode materially different statistical concepts.

The benchmark-rate file separates total debt, fixed-rate debt, floating/variable-rate debt and individual benchmark components such as the Bank of Russia key rate, MosPrime and RUONIA. These are indicator hierarchy members, not presentation aliases.

The SME borrowers workbook contains multiple titled blocks such as counts of SME subjects with debt, counts receiving loans and related measures. Units and population semantics change between blocks, while periods appear in shared columns. A parser must retain block context; row text alone may be insufficient.

### 4. Debt securities: frequency, valuation and maturity as independent distinctions

The debt-securities workbook contains four sheets:

- quarter / nominal value;
- month / nominal value;
- quarter / market value;
- month / market value.

Inside each sheet the row hierarchy distinguishes economic sector, ruble/foreign-currency denomination and both original and remaining maturity concepts. Notes state that from 2019 long-term securities are split by remaining maturity and that data may be revised. The quarterly/monthly and nominal/market sheets are therefore distinct statistical representations, not duplicates.

This source demonstrates a critical general rule: **frequency**, **valuation basis**, **currency denomination**, **unit of measure**, **institutional sector**, **original maturity** and **remaining maturity** are orthogonal semantic dimensions where present. They cannot be inferred from a single global `indicator` string.

### 5. Household financial assets/liabilities: balances, transactions, seasonal adjustment, metadata

The two household workbooks each contain dedicated methodological and metadata sheets plus statistical surfaces.

`households_bm` contains balances and seasonally adjusted balances; `households_om` contains transactions and seasonally adjusted transactions. The Bank of Russia methodological notes distinguish stocks at a point in time from transactions and explain monthly data as estimates for selected instruments; seasonal adjustment is a methodological transformation using X-13 ARIMA/SEATS.

Consequently:

- balances and transactions are different measure semantics;
- original and seasonally adjusted series are different representation states;
- embedded metadata/methodological text is part of interpretation provenance but not numeric observations;
- overlap with banking-sector deposit/loan files cannot be assumed to be duplication because institutional scope, methodology and measure construction can differ.

### 6. Monetary and financial statistics: sector/instrument hierarchies and derived published series

The monetary-statistics source set includes monetary aggregates, a central-bank survey, other-depository-corporation balance/survey, depository-corporation survey and an annex.

Observed surfaces include:

- monetary aggregate levels;
- sector decomposition;
- annual growth, growth from beginning of year and monthly growth as separately published series;
- balance/survey rows broken down by financial instrument and economic sector;
- original and seasonally adjusted annex series.

The Bank of Russia methodological notes state that surveys follow international monetary/financial-statistics standards, publish breakdowns by instrument and sector in rubles and foreign currency, and may be revised. Published growth-rate sheets are therefore **source statistics to preserve**, even though the commissioned product itself must not calculate new economic indicators.

Formula cells occur in the seasonally adjusted annex. Formula presence is source provenance: the product must preserve formula/cached-value origin in the raw layer rather than silently converting the workbook into an unexplained value-only file.

### 7. External debt: method/regime boundaries embedded in workbook structure

External-debt files use quarterly date axes and nested row hierarchies. The observed semantics include:

- institutional sector;
- instrument;
- national versus foreign currency denomination;
- short/long original maturity;
- short-term remaining maturity in the dedicated publication;
- direct-investment debt relationships;
- measurement in millions of US dollars.

The current and historical sheets are not structurally interchangeable. In `debt_cur-mat_new`, an older sheet separates central bank and banks, while the current surface combines “central bank and banks” for some rows. The source notes also state that external-debt data may be revised and that totals may differ from component sums because of rounding. Classification/regime and revision provenance must therefore survive normalization.

### 8. `obs_table_20s`: coded hierarchical banking-sector statements

This workbook is a structural outlier with ten sheets: asset variants, liability variants, and corporate/household loan maturity tables.

The asset/liability sheets use explicit hierarchical line codes (`1`, `1.1`, `1.4.1`, etc.) alongside nested textual labels. The same generic labels, such as `Прочие` or `Просроченная задолженность`, appear at different hierarchy locations. The line code and hierarchy path are part of indicator identity.

A punctuation-insensitive normalization would collapse semantically different codes such as `1.1` and `11`. This is observed counterevidence against punctuation stripping as a canonical identifier strategy.

### 9. Exchange-rate workbook: multi-row calendar and heterogeneous measure rows

The exchange-rate workbook contains monthly, quarterly and share/weight-type surfaces. In monthly data, period semantics are split across repeated month labels and year/header context rather than stored as ordinary Excel date cells. Rows include different measures and different decimal formats. Missing/unavailable observations may be represented by text `-` rather than numeric zero.

This source requires a dedicated calendar/header interpreter. A generic “all columns after A are dates” rule is insufficient.

## Presentation variation versus semantic variation

### Safe discovery-level presentation normalizations observed

The evidence supports conservative transformations for **matching candidates**:

- Unicode normalization;
- non-breaking/zero-width space cleanup;
- trimming and collapsing runs of whitespace;
- case-folding where case is demonstrably not meaningful;
- controlled normalization of known typographic dash variants in human labels.

These operations may improve candidate matching while retaining the exact source text alongside the candidate key.

### Unsafe global normalizations

The following are explicitly unsafe as global identity rules:

- deleting all punctuation (`1.1` versus `11` collision);
- equating all case/punctuation-normalized `Всего`, `Прочие`, `Кредиты и займы`, `Просроченная задолженность` labels;
- treating equal sheet titles as equal measures across workbooks;
- treating equal workbook geometry as semantic equivalence;
- equating ruble/foreign-currency denomination with measurement currency;
- equating monthly stock dates with monthly flow periods;
- equating original and seasonally adjusted series;
- equating nominal and market valuations;
- equating original maturity with remaining maturity;
- collapsing historical/current classification regimes by fuzzy label similarity.

## Source-universe implications

The empirical source space does **not** support one universal positional parser or a single denormalized table whose columns are guessed from visible labels. It does support a layered approach:

1. exact source acquisition and immutable provenance;
2. a lossless raw-cell representation independent of source semantics;
3. a finite set of reusable structural parsing mechanisms;
4. explicit per-source/per-family semantic contracts binding those mechanisms to correct measure/dimension meanings;
5. a common observation model that preserves source-specific dimensions and refuses unknown semantic collisions.

This is a research implication, not yet an accepted Target HOW.

## Remaining uncertainty after census

The complete structural universe is known for the bound file revisions. Further research is still required for:

- exact cross-source indicator equivalence and overlap;
- revision identity across future downloads of the same URL;
- precise semantic identity keys for every family;
- safe bilingual/readable naming;
- which data cells should be exposed as semantic observations versus retained only in the raw provenance ledger (for example source helper/formula cells or numeric line codes).

These are routed to `RT-CBR-002..004` rather than resolved by source geometry alone.

## Coverage and limitations

All 41 registry sources have explicit successful dispositions. All 162 sheets are present in mechanical evidence. Detailed human interpretation focused on every structural family and material outlier rather than narrating every repeated sheet separately. Exact labels and geometry for all repeated sheets remain navigable in the evidence pack.

The evidence is a snapshot of the live CBR files acquired on 2026-09-11 project time. A changed workbook hash or registry source set reopens source census and downstream semantic validation.
