# RT-CBR-002 — Statistical identity, dimensions and semantic collisions

**Work kind:** `EXTERNAL_DESCRIPTIVE_RESEARCH` (`MADARAII-08`)  
**Research Topic:** `RT-CBR-002`  
**Baseline:** `RT-CBR-001` at commit `a2f0474f660c72fa69e12d47caa2797c4ca3c8db`; source evidence commit `140338646aef5a0cc5ab8db4abf04af3945b25c5`  
**External evidence:** Bank of Russia official methodology/publication surfaces only  
**Status:** established Research Result

## Central question

Across the observed source families, what makes two published numeric observations semantically identical, equivalent representations, distinct slices, or distinct statistics; which dimensions, units, temporal conventions and population definitions participate in identity; where can apparent duplicates or revisions conflict?

## Core finding

No single human-readable label is sufficient to identify a statistical observation across this source universe. A safe identity model is **contextual and compositional**. At minimum it must preserve the source statistical product, measure meaning, subject/population, period semantics, unit/valuation basis and every activated dimension that changes what the number denotes. Source revision/provenance identifies the published realization of that observation separately from semantic identity.

The source universe contains repeated labels and structurally identical workbooks whose meanings differ. Therefore equivalence must be **asserted through explicit semantic mapping** or exact source-family rules, not inferred by fuzzy text similarity or geometry.

## Distinctions that materially change statistical meaning

### Measure / statistical operation

Observed measure classes include:

- outstanding stock/debt/balance as of a reporting date;
- overdue portion of a stock;
- volume granted during a month;
- number of borrowers / number of loans;
- household transactions during a period;
- published growth rates;
- exchange-rate levels and derived exchange-rate indicators;
- debt-securities positions under different valuation bases;
- shares/percentages and ratios.

A number representing a stock at `01.08.2026` and a number representing flow **during July 2026** can both be published around the same calendar boundary while denoting different temporal objects. The normalized model therefore needs both a machine period representation and an explicit period/measure convention.

### Statistical subject / population

Observed populations include, among others:

- resident individuals;
- resident legal entities and individual entrepreneurs;
- SME entities;
- individual entrepreneurs as a distinct SME/borrower cut;
- households under national-accounts sector semantics;
- central bank, credit institutions/other depository corporations, government, financial/nonfinancial corporations and nonresidents;
- issuers/holders or debtors/creditors implicit in individual publications.

A row named `Кредиты и займы` under a household-sector financial balance does not become identical to a banking-sector credit row merely because the text overlaps. Population/institutional-sector meaning is part of identity.

### Classification regime / hierarchy path

The corporate files expose historical activity/use categories and current OKVED2 classes. The Bank of Russia current methodology ties current economic-activity publication to the Russian classification harmonized with NACE Rev. 2. Historical row taxonomies remain distinct unless a separately evidenced concordance establishes equivalence.

For coded hierarchical tables such as `obs_table_20s`, hierarchy path and line code are semantic. `1.1` and `11` are distinct even when punctuation-insensitive text normalization produces the same compact token.

### Currency denomination versus measurement unit

The sources use several different currency concepts:

- separate ruble/foreign-currency portfolios measured in **million rubles**;
- external debt denominated in national/foreign currency but reported in **million US dollars**;
- exchange rates measured in **rubles per unit of foreign currency**;
- some sheets containing total across denomination categories.

The data model must keep `denomination/currency_category` separate from `unit/currency_of_measurement`. A single `currency` column would be semantically ambiguous.

### Valuation basis

Debt securities explicitly distinguish nominal and market value. Notes also qualify accrued coupon treatment. Valuation basis is therefore part of semantic identity.

### Maturity concept

The source universe distinguishes original maturity from remaining maturity. Official Bank of Russia external-debt methodology defines short-term remaining maturity as original short-term liabilities plus portions of original long-term liabilities falling due within one year. These are related constructs, not aliases.

### Adjustment / transformation status

Household and monetary surfaces contain original and seasonally adjusted series. Published growth-rate sheets are source-provided derived series. Adjustment/transformation status must remain explicit rather than be treated as duplicate publication.

### Territory semantics

Regional matrices mix:

- national total;
- federal-district aggregates;
- constituent entities;
- autonomous okrugs reported as `в том числе`;
- parent-region rows explicitly excluding autonomous okrugs.

A territorial dimension therefore needs member type/scope/hierarchy, not only a standardized place name. The exact source label remains authoritative provenance.

### Frequency and period convention

Monthly and quarterly representations may coexist for the same broad subject. Frequency is part of the representation and, where values are separately published under different constructions, of identity. A `period_start/end/reference_date` surface alone is insufficient unless frequency and stock/flow convention are retained.

## Four identity layers

Research supports separating four concepts that are often conflated:

1. **Source cell identity** — exact workbook hash, worksheet and coordinate. This identifies the published carrier value.
2. **Source observation identity** — source statistical product + local row/hierarchy + local sheet semantics + period + exact unit and source classification context. This identifies what one source says without cross-source merging.
3. **Canonical concept identity** — a project concept that may link several source observations only after equivalence has been explicitly established.
4. **Presentation name** — Russian/English readable labels used by humans. These are mutable presentation surfaces and must never be primary identity keys.

This separation allows readable names to evolve without silently changing the data graph.

## Duplicate and overlap taxonomy

### Exact carrier duplicates

Same workbook hash + sheet + coordinate + raw value is the same carrier observation. Repeated ingestion should deduplicate operationally by source revision/cell identity.

### Same source concept, different published slice

Currency, overdue status, acquired-claims treatment, adjustment state, sector, maturity or valuation may create different slices of one broader concept. They should share a concept family only if explicit dimensions capture the distinction; their observation keys remain distinct.

### Cross-source overlap with materially different methodology

Examples include mortgage/household/banking-system credit and deposit concepts appearing in several publications. Similar economic subject does not establish duplication. Keep source concepts distinct until population, coverage, valuation, timing and methodological treatment are proven equivalent.

### Revision of the same live publication

Bank of Russia notes for monetary, debt-securities and external-debt statistics explicitly allow revisions. Re-downloading the same registry URL may therefore produce a new file hash with changed historical cells. A future acquisition must create a new **source revision**, compare against prior revisions when retained, and never overwrite provenance silently.

### Conflicting values

When two source observations map to the same asserted canonical concept key but carry different values, the system must surface a conflict/revision relation. It must not average, sum, pick the newest by default, or hide one source.

## Equivalence standard

Two observations may be assigned one canonical concept only when all material semantic components match or an explicit mapping establishes the relation:

- measure type and statistical operation;
- population/institutional scope;
- instrument/indicator meaning;
- classification regime and member;
- territory scope if applicable;
- currency denomination/category;
- unit and scale;
- valuation basis;
- maturity concept;
- overdue/acquired-rights/escrow/SME/IE or other activated cuts;
- adjustment/transformation state;
- frequency and period convention.

If one component is unresolved, the relation remains `candidate_equivalent`/UNKNOWN rather than becoming canonical equality.

## Source-family implications

### Mortgage / regional lending

Worksheet names reliably encode several dimensions inside one workbook, while A1 title confirms full measure semantics. Acquired claims and “with acquired claims” are separate states. Regional member path is part of identity.

### Corporate and SME

`A` and `C` files need distinct classification identifiers. SME versus all borrowers is a population distinction even when row geometry is identical. Debt and overdue debt are separate measure states; flow volume is a different measure type.

### Borrowings

Files for all funds, client funds, organization funds, corporate deposits, individual deposits, individual deposits excluding escrow, individual-entrepreneur deposits, escrow accounts and budgets are related but not interchangeable. “Excluding escrow” is a coverage dimension, not presentation wording.

### Households

Balance versus transaction and original versus seasonally adjusted are independent dimensions. Official methodology makes these constructs explicit.

### Monetary/financial surveys

Sector and instrument hierarchy, currency and source survey are fundamental. Similar row labels across central-bank, other-depository-corporation and consolidated surveys do not create duplicates because consolidation scope differs.

### External debt

Institutional sector, direct-investment relationship, denomination, original/remaining maturity and reporting regime all matter. Historical/current sheets can encode classification changes.

### `obs_table_20s`

Line code plus hierarchy plus sheet variant is the safest local source-concept key. Human label alone is inadequate.

### Exchange rates

Measure row + currency/basket + frequency + period identifies an observation. Missing marker `-` is not numeric zero.

## Countermodels rejected by evidence

- **Global normalized label key.** Rejected by repeated generic labels and `1.1`/`11` collision.
- **One source file = one indicator.** Rejected by multi-indicator workbooks such as households, monetary aggregates and `obs_table_20s`.
- **One sheet = one indicator.** Rejected by sheets containing nested sector/instrument or multiple measure blocks.
- **Same shape = same semantics.** Rejected by exact structural twins with different populations.
- **All time columns are equivalent monthly dates.** Rejected by stock dates, flow month labels, quarterly sheets and exchange-rate composite headers.
- **Newest source silently wins.** Rejected by provenance and revision requirements; newest is a revision ordering fact, not an automatic conflict-resolution rule.

## Research conclusion

The coherent common data system should normalize **representation mechanics** aggressively enough for usability while normalizing **statistical meaning** conservatively. Canonical equality is an explicit relation, not an output of string cleaning.

This result supplies the semantic boundary for preservation/normalization research and later Target WHAT/HOW. It does not prescribe a storage engine, Python module structure or final API.

## Evidence and reopen conditions

Primary source observations are traceable through `RT-CBR-001` evidence routes. Supplementary methodology used here is limited to Bank of Russia official current methodology for granted funds/borrowings, mortgages, household financial assets/liabilities, monetary/financial surveys and external debt.

Reopen if the registry changes, a source family changes its classification or method, a new cross-source equivalence is proposed, or implementation evidence reveals a source distinction absent from this model.
