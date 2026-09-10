# TS-CBR-ID — Statistical identity, dimensions and overlap

**Work kind:** `THEMATIC_RESEARCH_SYNTHESIS` (`MADARAII-12`)  
**Theme:** `T-CBR-ID`  
**Corpus Baseline:** `RC-CBR-001`  
**Status:** established thematic synthesis

## Current bounded answer

An observation in this source universe is identified by **meaning in context**, not by its visible label. The minimum reusable identity model separates source carrier identity, source-local statistical concept and optional cross-source canonical concept.

The source-local concept combines measure, statistical subject/population, instrument/classification/hierarchy, period convention, unit/scale and every activated dimension that changes what the number denotes. Typical activated dimensions include territory scope, denomination, overdue status, acquired-rights treatment, SME/IE status, valuation, maturity, institutional sector, seasonal adjustment and frequency.

Cross-source canonical equality is a separately asserted relation. It cannot be inferred from text similarity, equal values, equal geometry or common economic topic.

## Cross-source definition model

### Source carrier

`source revision + exact sheet + exact cell` identifies where the published value came from. This is provenance identity.

### Source concept

`dataset/source contract + hierarchy path + local semantic dimensions` identifies the statistic the source publishes. This is the default safe level for all data.

### Canonical concept

A higher-level project concept may group source concepts only when their population, measure, classification, timing, unit/valuation and other material dimensions are demonstrated equivalent. A candidate mapping can remain unresolved without blocking preservation of source data.

### Human name

Readable Russian/English names are display aliases over stable IDs. Same alias may resolve to several concepts and must carry context.

## Reconciled dimension distinctions

- **Measure:** stock, overdue stock, flow/volume, count, transaction, growth rate, exchange-rate measure, ratio/share.
- **Population:** resident individuals, all resident legal entities/IE, SME, IE, households, institutional sectors and source-specific populations.
- **Classification:** historical activity/use taxonomy and OKVED2 are separate regimes.
- **Territory:** national/federal district/constituent entity/`including`/`excluding` territorial aggregates.
- **Denomination:** rubles, foreign currency, total, national/foreign currency; distinct from measurement unit.
- **Unit/scale:** million rubles, billion rubles, million US dollars, units, percent, rubles per currency unit and others present in titles/rows.
- **Valuation:** nominal versus market value.
- **Maturity:** original versus remaining maturity.
- **Adjustment:** original versus seasonally adjusted; other published transformation types remain explicit.
- **Frequency/period:** monthly/quarterly and stock-date/flow-period convention.
- **Coverage modifiers:** acquired claims, escrow exclusion, direct-investment relation and similar source-specific qualifiers.

## Duplicate and revision model

The corpus supports four materially different relations:

1. repeated ingestion of the same source revision/cell — operational duplicate;
2. distinct slices of one source concept family — shared concept family, distinct observations;
3. cross-source overlap — separate until explicit equivalence is established;
4. live-publication revision — new file revision that may alter historical values and must remain traceable.

If explicitly equivalent source concepts disagree at the same semantic key, the correct state is visible conflict/revision, not silent winner selection.

## Strongest challenge

A broad canonical taxonomy would make querying simpler. The source evidence shows that the cost of premature canonicalization is semantic corruption: generic labels recur in unrelated contexts; structural twins have different populations; historical/current classification regimes differ; and currency/valuation/maturity concepts cross-cut each other. Therefore source-local identity is the conservative universal floor, while canonical mappings can grow incrementally.

## Applicability and limitations

This model establishes semantics for the bound source universe and safe behavior for future variants. It does not claim that every possible Bank of Russia statistical publication follows the same dimensions. It also does not prove specific cross-source equivalence pairs beyond exact source-local relationships.

## Downstream implications

- data storage/query must retain source-local IDs and dimensions;
- canonical mapping is optional and explicit;
- pivots must reject ambiguous duplicate keys by default;
- a simple `indicator + date + region + value` schema is insufficient;
- source revisions require hash-based provenance and visible lineage.

## Reopen

Reopen on a proposed new canonical equivalence, changed CBR methodology/classification, a new dimension encountered by implementation, or evidence that an existing dimension has different semantics than recorded.
