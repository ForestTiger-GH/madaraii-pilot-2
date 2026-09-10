# TARGET-WHAT-CBR-001 — Target Product Definition

**Work kind:** `TARGET_WHAT_ASSEMBLY` (`MADARAII-17`)  
**Product:** CBR Unified Statistics  
**Baseline:** `TW-CBR-1`  
**Status:** accepted under the active user Commission  
**Inputs:** developed actor intent `RES-ACTOR-001`; admitted Scientific Knowledge `KNOWLEDGE-CBR-001`

## Product purpose and beneficiaries

CBR Unified Statistics is a reusable Python product that acquires the complete registry-defined Bank of Russia Excel source universe, preserves the published source values and provenance, interprets recognized statistical structures into a coherent queryable system, and lets notebook users or external Python systems export the unified data and obtain meaningful two-dimensional tables in Russian or English.

Primary beneficiaries are analysts working in Google Colab/Jupyter and software systems that need the same prepared statistics through callable operations.

## Concrete target subject

For the bound registry universe the Product contains:

- a registry/source catalog covering every declared CBR file;
- source-revision records for downloaded or locally supplied workbooks;
- a lossless raw-cell dataset retaining all source numeric/formula-cached values plus interpretation-relevant text/metadata provenance;
- source specifications for every current workbook family/source;
- a semantic concept/dimension catalog;
- normalized long-form observations referring back to source cells;
- Russian and English display surfaces for user-exposed semantic entities, with exact Russian CBR labels and translation status retained;
- validation/evidence reports;
- CSV exports;
- programmatic catalog/filter/pivot operations;
- a notebook-facing example/entry point using the same reusable package operations.

The exact bound source set is the 41 URLs from registry revision `b7af2c380a028984ec4b465250ac44a0f05efab6`; a later registry revision is a new target/source Baseline transition.

## Observable obligations

### TW-01 — Complete source acquisition

The internet workflow obtains every bound registry source and records its exact source identity, URL and source-revision hash. Any acquisition failure is visible and prevents a claim of complete build.

### TW-02 — Local-source path

The same processing workflow can operate on a local directory containing source files bound to registry source IDs. For identical workbook bytes, internet and local processing produce equivalent downstream source-revision/raw content.

### TW-03 — Lossless numeric preservation

Every stored numeric or formula-cached numeric source value in every accepted workbook revision is retained in a raw ledger under exact source-hash/sheet/cell provenance. Numeric lexical values are preserved without mandatory binary-float rewriting.

### TW-04 — Semantic disposition completeness

Every source numeric cell receives an auditable disposition. Published observations are mapped into the semantic observation layer; numeric headers/codes/helpers or other non-observation values remain present with an explicit non-observation disposition. Unclassified residue is visible and blocks a “semantic coverage complete” claim for that source contract.

### TW-05 — Statistical meaning preservation

Normalized observations preserve the distinctions required by their source semantics: measure/population, period convention, unit/scale, hierarchy/classification and all activated dimensions such as territory, denomination, overdue/acquired-rights/SME/IE status, valuation, maturity, institutional sector and adjustment.

### TW-06 — No false semantic unification

Text similarity, punctuation/whitespace normalization, equal values, equal worksheet names or equal workbook geometry never by themselves merge two source concepts. Cross-source canonical equality exists only through explicit mapping.

### TW-07 — Revision and conflict visibility

Changed file bytes at the same source URL create a new source revision. Multiple source observations that overlap or conflict remain traceable. A request that requires one value from an unresolved multi-value canonical key fails visibly rather than choosing a silent winner.

### TW-08 — Presentation-variation robustness

Known presentation-level differences in whitespace, Unicode and source-scoped worksheet/label variants are tolerated when semantic invariants remain satisfied. A materially new unrecognized source variant fails closed with a diagnostic and preserved raw evidence.

### TW-09 — Bilingual semantics

Every user-exposed dataset, concept and dimension member has a Russian and English display surface. Exact CBR Russian source text remains available. English terms distinguish `cbr_official`, `project_translation` and, only for proper-name/technical fallback where semantically safe, transparent transliteration status.

### TW-10 — Readable naming

Working names are shorter where qualifiers have been factored into explicit dimensions. A short name may never erase a distinction required to interpret the statistic.

### TW-11 — Query and 2D views

Users can discover concepts/dimensions, filter normalized observations by meaningful parameters, and pivot a selected subset into a two-dimensional table. The default pivot performs no aggregation or new economic calculation. Multi-value output-cell ambiguity is an explicit error unless the caller has narrowed the selection sufficiently.

### TW-12 — Export

At minimum, the Product exports raw ledger, normalized observations, catalogs and requested prepared views to CSV with stable identifiers and provenance-preserving fields/sidecars sufficient for trace-back.

### TW-13 — Reusable operations

Acquisition, local binding, raw extraction, semantic parsing, validation, catalog/query, pivot and export are independently callable operations. A notebook orchestrates them but does not own their implementation.

### TW-14 — Runtime

The Product is practically runnable in Python in Google Colab or Jupyter Notebook with internet access. Installation from the repository plus declared Python dependencies is sufficient; no private service or API key is required for the core build.

### TW-15 — Reproducible evidence

A complete build emits a machine-readable report that identifies the source revisions processed, parser/specification versions, counts/dispositions, preservation reconciliation and any warnings/failures.

## Core product entities and invariants

- **Source** — stable registry item.
- **SourceRevision** — exact acquired workbook bytes/hash.
- **RawCell** — exact source cell value/provenance; immutable for a source revision.
- **SourceConcept** — source-local statistical meaning/hierarchy.
- **Dimension / Member** — typed semantic qualifier; exact source label retained.
- **Observation** — one published source value under one source concept, period and dimensions, linked to one RawCell.
- **CanonicalConceptRelation** — optional explicit cross-source relation; absence is valid.
- **Translation/Name** — mutable presentation surface over stable identity.
- **Build** — reproducible set of source revisions plus processing/spec version and evidence.

No display name is an identity key. No semantic observation exists without a source-cell provenance link. No canonical relation deletes its member source observations.

## Supported query semantics

Core selectors include source/dataset, concept, time/frequency, unit, language and structured dimensions discovered in the sources. Common dimensions such as region, currency category, overdue status, SME/IE scope, valuation and maturity are first-class where they exist; sources may expose additional dimensions without forcing null-filled global columns.

## Unacceptable outcomes

- dropped source numeric cells without explicit disposition;
- silently recomputed/reformatted source numbers as the only preserved form;
- fuzzy-merging distinct indicators;
- treating `-` as zero;
- merging nominal/market, original/seasonally adjusted, stock/flow or original/remaining maturity;
- flattening territorial/classification regimes so distinct source members collide;
- hiding source revisions/conflicting overlapping values;
- implicit aggregation in a standard 2D view;
- bilingual names that replace or obscure exact source meaning;
- a notebook-only monolith that prevents reuse from external Python code.

## Non-goals

- calculating new economic indicators absent from source files;
- creating a universal ontology for all Bank of Russia statistics;
- guaranteeing automatic interpretation of arbitrary future workbook layouts;
- declaring every similar cross-publication statistic equivalent;
- providing a server/database service deployment;
- using other `stratbox` code or external project architectures.

## Correctness and completion

Target completion requires evidence for all 41 bound sources that raw numeric preservation is exact, semantic dispositions are complete under recognized source contracts, all current structural variants are handled, bilingual/query/export surfaces work, internet/local paths are reproducible, unknown variants fail closed, and documentation matches implementation.

## HOW handoff

`TW-CBR-1` is complete for mechanism formation. HOW may choose package layout, storage representation and adapter implementation provided every obligation above remains protected. A HOW discovery that cannot satisfy a commitment reopens this WHAT owner rather than weakening the obligation silently.
