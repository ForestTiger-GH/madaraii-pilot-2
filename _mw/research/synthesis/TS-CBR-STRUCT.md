# TS-CBR-STRUCT — Source structure and interpretation boundary

**Work kind:** `THEMATIC_RESEARCH_SYNTHESIS` (`MADARAII-12`)  
**Theme:** `T-CBR-STRUCT` from `TM-CBR-001`  
**Corpus Baseline:** `RC-CBR-001`; evidence commit `140338646aef5a0cc5ab8db4abf04af3945b25c5`  
**Status:** established thematic synthesis

## Current bounded answer

The 41 CBR workbooks form a finite but heterogeneous set of **wide statistical matrices** plus metadata/methodology sheets. Most statistical sheets place time on columns and one semantic axis on rows, while the row axis can represent territory, activity/classification, indicator hierarchy, sector/instrument hierarchy or multiple block-specific measures. Sheet titles frequently encode additional dimensions such as currency, overdue status, acquired-right treatment, valuation, frequency or adjustment.

The evidence supports reusable structural mechanisms, but no universal position-only parser. A structural parser may discover periods, row paths, numeric rectangles and sheet dimensions; a source semantic contract must still validate what those structures mean.

## Structural families

1. **Regional wide matrices** — one row per territorial member, period columns, sheet-level currency/status; mortgage debt, regional corporate/SME debt and several borrowings sources.
2. **Classification wide matrices** — activity/OKVED2 rows, monthly period columns and sheet-level currency/status; corporate/SME flow/debt.
3. **Indicator wide matrices** — a compact or nested indicator row axis, periods on columns; mortgage full/IHC, benchmark-rate debt, monetary aggregates.
4. **Hierarchical financial statements/surveys** — nested sector/instrument/measure rows, periods on columns; households, monetary surveys, debt securities, external debt and `obs_table_20s`.
5. **Block matrix** — several semantically distinct row blocks sharing one period axis; SME borrower information.
6. **Composite-calendar matrix** — period semantics distributed across year/month/quarter header rows; exchange-rate workbook.
7. **Metadata/methodology sheets** — non-observation content that is materially relevant to interpretation and lineage.

These families overlap in physical mechanism. One source can use the same matrix reader as another while binding different semantic axes.

## Period discovery

Observed period carriers include real Excel date cells, date-like strings, Russian month-year strings, quarter date axes and composite year/month headers. A valid common period parser therefore needs several explicit grammars and source-level period conventions. It must preserve whether the published datum is a stock at a date, a flow during a month/quarter or another published transformation.

## Presentation tolerance

Whitespace, Unicode and some sheet-label typography can be normalized for dispatch. Broad punctuation removal is unsafe: coded hierarchy entries demonstrate collisions (`1.1` versus `11`). Equal sheet labels across different sources also do not establish equal semantics.

## Failure model

The safest forward-compatibility posture is **recognized variants + fail closed**. A future source can move titles, alter header depth, add a sheet or change classification. If required semantic anchors cannot be validated, the system should retain raw source evidence and report the changed structure instead of guessing.

## Counterarguments and limits

A fully generic table-inference system could theoretically infer more unknown variants, but the source universe contains enough semantic reuse and label ambiguity that unsupervised inference would make correctness difficult to verify. Conversely, one hard-coded parser per sheet would duplicate mechanics and make maintenance brittle. The evidence favors shared structural readers plus explicit source specifications.

## Implications

- raw acquisition/preservation can be uniform across all files;
- semantic parsing should be adapter/specification driven;
- structural reuse and semantic identity must remain separate;
- source specifications should state expected sheets/period grammar/axes and fail on material deviation;
- verification should cover all recognized source contracts and at least one synthetic unknown-variant failure.

These are evidence-derived constraints, not final implementation commitments.

## Coverage and reopen

All 41 files and 162 sheets are represented in source evidence; every observed structural form is covered by a family or explicit outlier. Reopen on new registry source, changed workbook structure/hash with new geometry, or a parser failure revealing an unmodelled structural class.
