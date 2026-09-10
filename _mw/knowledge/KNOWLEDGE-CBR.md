# KNOWLEDGE-CBR-001 — Current Scientific Knowledge

**Work kind:** `SCIENTIFIC_KNOWLEDGE_CORPUS_ASSEMBLY` (`MADARAII-16`)  
**Scientific scope:** Bank of Russia source semantics and engineering facts required to construct a trustworthy unified statistics product for the bound registry universe  
**Baseline:** `RC-CBR-001`, `TM-CBR-001`, thematic syntheses `TS-CBR-*`, cross-theme synthesis `RS-CBR-001`  
**Owner status:** current/admitted for `WORK-CBR-001`

## Orientation

The bound source universe contains 41 live Bank of Russia XLSX workbooks and 162 worksheets. The files are heterogeneous statistical publications rather than instances of one universal spreadsheet schema. They nevertheless share enough matrix mechanics to support a common software product when source preservation, structural parsing and statistical identity are separated.

The trustworthy model has three scientific layers:

1. **Source evidence** — exact workbook revision and exact cell content.
2. **Source-local statistical semantics** — what each published value denotes under its own table, hierarchy, dimensions, period and methodology.
3. **Optional cross-source relations** — explicit equivalence/overlap/revision mappings; never inferred from fuzzy naming.

Readable Russian/English labels and 2D tables are views over these layers.

## K-CBR-01 — Source universe and structural model

### Current claim

Every one of the 41 registry sources was acquired and inspected successfully in the research baseline; 162 worksheets and 36,161 text cells were structurally indexed. Exact workbook hashes and source routes exist in the research evidence.

The observed structures reduce to reusable matrix families plus outliers: regional matrices, classification matrices, indicator matrices, hierarchical financial-statistics matrices, multi-block matrices, composite-calendar matrices and methodology/metadata sheets.

### WHY / BASIS

The complete mechanical census and per-source evidence establish the empirical universe. Exact structural twins occur across semantically different datasets, proving that structural reuse is justified while semantic reuse needs separate contracts.

### Limits

This is bounded to the acquired revisions. Future live URLs may change. Forward compatibility therefore means detection and controlled adaptation, not guaranteed automatic interpretation.

## K-CBR-02 — Statistical observation identity

### Current claim

A safe observation identity is compositional. At source level it includes the source statistical product, measure meaning, population/sector, indicator or hierarchy member, period convention, unit/scale and every activated semantic dimension.

Material observed dimensions include:

- territory and territory scope/type;
- activity/classification regime and member;
- denomination/currency category;
- overdue status;
- acquired-rights treatment;
- SME/IE/population scope;
- valuation basis;
- original/remaining maturity;
- financial instrument and institutional sector;
- balance/transaction/growth or other measure form;
- original/seasonally adjusted state;
- frequency and period convention;
- source-specific coverage qualifiers such as escrow exclusion.

`currency denomination` and `unit/currency of measurement` are distinct. External debt can be denominated in national/foreign currency while measured in USD; many bank-sector currency slices are measured in million rubles.

### WHY / BASIS

Generic labels recur across unrelated hierarchies. Punctuation-insensitive matching creates demonstrable collisions such as `1.1` and `11`. Equal workbook geometry occurs across SME and non-SME populations. Official CBR methodology separately defines maturity, sector, activity, stock/transaction and adjustment concepts.

### Consequence

Global normalized label equality is scientifically invalid as a canonical key. Canonical concepts can link source concepts only through explicit mappings whose semantic components have been checked.

## K-CBR-03 — Period model

### Current claim

The source universe includes several physical encodings of time and several statistical time meanings.

Physical encodings include Excel dates, date strings, Russian month-year labels, quarterly date columns and composite year/month headers. Statistical meanings include stock at reporting date, monthly/quarterly flow, published growth/change and other transformed series.

### Consequence

The product needs a normalized machine period plus explicit frequency and `period_role`/measure convention. Formatting a date is insufficient to establish temporal equivalence.

## K-CBR-04 — Classification and territorial regimes

### Current claim

Historical activity/use rows and current OKVED2 classes are different classification regimes. Territorial tables mix national totals, federal-district aggregates, constituent entities, `including` autonomous okrugs and explicit parent-region-excluding-subregion rows.

### Consequence

Classification and territory require stable member identity plus exact source label/path/type. Fuzzy conversion to a single modern classification or flat region list risks false aggregation.

## K-CBR-05 — Valuation, maturity, adjustment and published transformations

### Current claim

Nominal versus market debt-securities valuation, original versus remaining maturity, original versus seasonally adjusted series, balance versus transaction, and published growth-rate series are materially different statistical representations.

The product is expected to preserve source-published transformations but is not required to calculate new economic indicators itself.

## K-CBR-06 — Revisions, overlaps and duplicates

### Current claim

The same live CBR URL may be revised. A changed file hash is a new source revision. Cross-source subject overlap is common, but overlap is not duplicate identity until measure, population, timing, classification, unit/valuation and dimensions are shown equivalent.

Four relations must stay distinct:

- same source cell re-ingested;
- different slices of one source concept family;
- cross-source overlap/equivalence candidate;
- revised publication of the same source.

Conflicting values under an asserted canonical key remain visible and require explicit disposition.

## K-CBR-07 — Preservation model

### Current claim

“All numbers preserved” is best verified through a raw OOXML cell ledger beneath semantic parsing.

A raw record needs source revision/hash, exact worksheet and coordinate, exact stored lexical value, cell type/style information sufficient for interpretation, and formula/cached value when present. Semantic observations reference these raw records.

Every numeric/formula-cached cell must be machine-reconciled between source OOXML and the raw ledger. Each numeric cell should additionally have a semantic disposition: observation, period/header/code/metadata/helper or explicit unclassified residue.

### Consequence

The system can prove source-value completeness even when a future unknown table cannot yet be semantically normalized.

## K-CBR-08 — Safe normalization and source drift

### Current claim

Unicode normalization, whitespace cleanup and source-scoped aliases are safe for discovery/dispatch when exact text is retained. Aggressive punctuation removal and fuzzy label merging are unsafe identity operations.

Recognized source specifications may tolerate presentation drift while validating semantic anchors. An unrecognized variant should fail closed after raw acquisition and expose the exact structural difference.

## K-CBR-09 — Bilingual semantic surfaces

### Current claim

Language is presentation over stable IDs. The maintained semantic catalog should distinguish exact CBR Russian source text, conservative normalized text, readable Russian name, English name and translation status/provenance.

Official CBR English terminology is preferred where clearly corresponding. Remaining translations are project translations and must be marked as such. Equal display names never imply concept equality.

Every user-exposed semantic concept should have both Russian and English display names; raw notes/presentation cells need not all be translated.

## K-CBR-10 — Safe 2D analytical views

### Current claim

A common long-form observation system can expose heterogeneous sources while preserving open dimensions. A 2D table is a deterministic filter/pivot projection. It should perform no implicit economic aggregation.

If several valid observations would occupy one pivot cell, the operation is ambiguous and should require narrower filters or an explicit resolution choice. Language selection changes labels only.

## K-CBR-11 — Acquisition and processing separation

### Current claim

Source acquisition can be separated from downstream processing because semantic processing consumes workbook bytes plus source identity. The required internet path can download every registry URL and record hashes; a local path can bind already downloaded files to the same source IDs and run the identical raw/semantic pipeline.

Byte/hash equality provides a direct verification of internet/local processing equivalence.

## K-CBR-12 — Product correctness boundary

A trustworthy product can claim:

- complete processing of the recognized 41-source baseline;
- exact raw numeric preservation and provenance;
- explicit semantic interpretation under source specifications;
- safe query/export of source-local observations;
- explicit, sparse canonical mappings where supported;
- bilingual display catalog;
- controlled failure on unknown variants.

It cannot claim:

- a complete universal Bank of Russia ontology;
- automatic semantic interpretation of arbitrary future Excel layouts;
- automatic equivalence of similar statistics across publications;
- official English wording for every project translation;
- calculated new economic indicators.

## Source registry and study route

Primary research/evidence routes are owned by `RC-CBR-001`. Ordinary engineering study should use this Scientific owner first. For deep challenge:

1. `RT-CBR-001` and source probe for exact workbook structure;
2. `RT-CBR-002` for identity and collision evidence;
3. `RT-CBR-003` for preservation/evidence logic;
4. `RT-CBR-004` for bilingual semantics;
5. thematic and cross-theme syntheses for reconciliation lineage.

Official Bank of Russia methodology is used as definitional BASIS in the Research Results; it remains external evidence rather than project Product Authority.

## Relations to downstream owners

This Scientific Knowledge supports and constrains Target WHAT/HOW but makes no Product commitments. In particular, K-CBR-07/08 constrain preservation and forward-compatibility claims; K-CBR-02..06 constrain data identity; K-CBR-09/10 constrain user/query surfaces.

## Completeness and research amputation

For the current engineering job, ordinary target/design work can proceed from this Knowledge owner without reconstructing meaning from raw Research. The complete source census remains available for implementation-specific adapter work and verification. The Scientific scope is bounded to the registry universe and current methodology required to interpret it.

## UNKNOWNs and reopen triggers

- future source-revision structural changes;
- specific cross-source canonical equivalence pairs beyond explicit source-local semantics;
- future methodology/classification changes;
- maintenance of project translations.

Reopen Scientific Knowledge when these materially affect active Product claims or source interpretation.
