# PRODUCT-ARCH-CBR-001 — Engineering Product Architecture

**Work kind:** `ENGINEERING_PRODUCT_ARCHITECTURE_FORMATION` (`MADARAII-24`)  
**Inputs:** `TW-CBR-1`, `TH-CBR-1`  
**Status:** accepted; separate architecture is justified by independently reusable units and cross-boundary correctness contracts

## Independent value

The Product must be reusable from notebooks and external systems while making raw preservation, semantic interpretation, validation and query behavior independently testable. A separate allocation view therefore has lifecycle value beyond the mechanism prose in Target HOW.

## Realization units and responsibilities

| Unit | Exclusive responsibility | Material interfaces |
| --- | --- | --- |
| Registry/specification | stable source IDs/URLs, source profiles, bilingual dataset metadata | acquisition; semantic adapters; validation |
| Acquisition | internet download/local binding, source revision hashes and manifest | registry → manifest/files |
| OOXML raw extractor | lossless non-empty cell ledger, exact lexical values/formulas/provenance | manifest/files → raw cells |
| Period interpreter | parse supported source period carriers without assigning unsupported measure semantics | workbook/profile → period bindings |
| Structural matrix extractor | period-block/data-cell geometry and row-side context | workbook + periods → source cell candidates |
| Semantic adapters | source-local concept/dimension interpretation and observation admission | candidates + specs + raw cells → observations/catalog |
| Translation/catalog | stable concept/member IDs and RU/EN presentation surfaces | semantic output → catalogs |
| Validation/evidence | preservation reconciliation, semantic dispositions, bilingual/provenance/coverage claims | all prior outputs → validation report |
| Persistence | deterministic CSV + SQLite projections | validated records → output directory |
| Query/view | discovery, filtering, non-aggregating pivot, CSV view export | persisted catalogs/observations |
| Orchestrator | ordered build transaction, staging/promotion and user-facing build API | coordinates units; owns no source semantics |

## State ownership

- source bytes and manifest own SourceRevision facts;
- raw ledger owns exact source-cell facts;
- source specs/adapters own semantic interpretation logic;
- observations/catalog own current build semantic projection;
- validation owns evidence/verdicts, not source truth;
- CSV/SQLite files are generated build outputs and remain mutually reconstructable projections;
- notebook owns no persistent Product logic.

## Dependency direction

`registry → acquisition → raw extraction` is independent of semantic parsing.  
`registry/specs + acquired workbook → period/structural extraction → semantic adapters`.  
`raw extraction + semantic output → dispositions/validation`.  
`validated semantic output → persistence → query/view`.

No downstream display/query layer may mutate semantic identity. No semantic adapter may discard a raw source record.

## Cross-cutting allocations

### Preservation

OOXML extractor owns lexical source capture. Validation independently reconciles source XML against the ledger. Semantic adapters reference, rather than recreate, raw values.

### Semantic safety

Registry/specification owns expected source profile. Adapter owns interpretation only inside that profile. Unknown variant handling is a shared contract: extractor preserves; adapter rejects; validation reports.

### Revision

Acquisition owns source hash/revision identity. Persistence includes it on every raw/semantic record. Query exposes revision/source filters.

### Bilingual presentation

Catalog owns names and translation status. Stable IDs remain outside language surfaces.

### Ambiguity

Semantic layer preserves all observations. Query/pivot owns refusal to collapse duplicate output keys without caller action.

## Failure containment

- one HTTP failure prevents complete-build admission but preserves other diagnostic downloads;
- one malformed XLSX cannot corrupt already acquired source files;
- semantic failure for one source does not destroy its raw ledger;
- validation failure prevents staging promotion;
- SQLite generation failure leaves CSV staging evidence and prevents promotion until projections agree;
- query ambiguity is local to the requested view and never changes stored observations.

## Compatibility and evolution

Source profiles are versioned with Product code. A source hash change alone is a normal SourceRevision; a structural invariant change that breaks parsing reopens the affected source profile and verification. Schema evolution keeps stable identity/provenance columns compatible or supplies an explicit migration.

## Architecture choices

**FIXED:** responsibility boundaries above; raw semantics separation; manifest convergence for internet/local paths; query cannot aggregate implicitly; validation gates final build promotion.

**BOUNDED_OPEN:** exact module filenames, internal dataframe/iterator use, SQLite indexing, output partitioning and caching.

**UNRESOLVED_BLOCKING:** none.

## Verification points

- registry ↔ manifest exact source coverage;
- workbook XML ↔ raw ledger exact cell reconciliation;
- raw cell ↔ observation provenance foreign-key reconciliation;
- source profile ↔ observed sheet/period contract checks;
- semantic observation ↔ raw disposition coverage;
- catalog bilingual completeness;
- CSV ↔ SQLite record-count/key equivalence;
- query pivot ambiguity tests;
- full internet build and local replay.

## Implementation handoff

Implementation may organize files for maintainability but may not move semantic Authority into notebook code or merge the responsibility boundaries above. Any discovery that requires weakening a protected WHAT/HOW claim reopens the relevant owner before admission.
