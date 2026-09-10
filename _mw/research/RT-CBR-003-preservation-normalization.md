# RT-CBR-003 — Preservation, provenance and safe-normalization boundary

**Work kind:** `EXTERNAL_DESCRIPTIVE_RESEARCH` (`MADARAII-08`)  
**Research Topic:** `RT-CBR-003`  
**Baseline:** `RT-CBR-001`, `RT-CBR-002`; complete probe evidence at `140338646aef5a0cc5ab8db4abf04af3945b25c5`  
**Status:** established Research Result

## Central question

Which source variations can be normalized safely as presentation noise, which require source-family interpretation or explicit ambiguity, and what preservation/provenance model is sufficient to prove that source numbers survive processing without false semantic collapse?

## Main conclusion

The product needs **two coupled but separate representations**:

1. a lossless source-cell ledger that proves what the downloaded workbooks contained, independent of later interpretation; and
2. a semantic observation layer that references source cells and adds interpreted period/indicator/dimension meaning without destroying exact source identity.

This separation is necessary because the same physical Excel constructs can carry different meanings, while some source numbers (line codes, year headers, formula helpers) are numeric yet are not economic observations. “Preserve all source numbers” is therefore best satisfied at the raw-cell layer; semantic coverage is a separately auditable classification of those cells.

## Required preservation properties derived from the source universe

### Byte-level source revision identity

Every acquisition must retain at least:

- registry/source identity;
- requested and resolved URL;
- acquisition timestamp;
- file SHA-256;
- byte size;
- source revision/run identity.

A live CBR URL can change historical values through revisions. File hash therefore identifies the exact evidence used by a build.

### Exact cell provenance

Every material source value accepted by the system must be traceable to:

- file hash/source revision;
- exact worksheet title;
- Excel coordinate;
- stored value representation;
- formula expression and cached value when present;
- source cell type/style information where it materially affects interpretation, especially dates/percent/scale.

### Numeric lexical preservation

Excel/OOXML numeric values should be captured from worksheet XML as their stored lexical `<v>` representation, rather than first coercing all values to binary floating point. This avoids creating preservation differences solely through parser conversion. Semantic numeric operations may use `Decimal` or other typed values downstream, while the exact source lexical value remains available.

### Formula handling

The source universe contains formula cells, including seasonally adjusted monetary-series surfaces. The raw ledger should preserve both the formula and any stored cached value visible in OOXML. The product must not silently claim that a computed formula value was a literal source input.

### Missing/suppressed/non-numeric markers

Textual `-`, blanks and other source markers must remain distinguishable from numeric zero. Their semantic interpretation may be `missing/unavailable/not_published` only when the source contract justifies it; the raw carrier value remains unchanged.

## Raw-cell disposition model

Each non-empty source cell can receive a processing disposition without being deleted from evidence:

- `observation_value` — numeric published observation mapped into the semantic layer;
- `period_key` — date/year/month/quarter header;
- `indicator_or_dimension_label` — source semantic label;
- `unit_or_title_metadata` — title/unit/footnote framing;
- `hierarchy_code` — numeric-looking code such as `1.1` or classification code;
- `formula_observation` — formula cell whose cached value is a published observation;
- `source_metadata` — notes/update dates/methodological comments;
- `structural_helper` — merge/helper presentation cell with no independent statistical observation;
- `unclassified` — fail-closed residue requiring review.

The exact final vocabulary may be simplified in Target HOW, but the research requirement is that every source numeric cell is either represented as a semantic observation or has an explicit retained disposition explaining why it is not one.

## Safe normalization classes

### Presentation normalization

Safe operations, provided exact source text is retained:

- Unicode NFKC normalization;
- conversion of non-breaking spaces/zero-width artifacts;
- trimming and whitespace collapsing;
- controlled equivalence for date strings once the parser proves the date grammar and period semantics;
- case normalization for candidate lookup where case is not semantic;
- controlled sheet aliases scoped to a specific source specification.

These create search/dispatch keys, not global semantic identifiers.

### Source-specific structural normalization

After a source contract is established, the following may be normalized into common dimensions:

- sheet variants such as rubles / foreign currency / total;
- overdue/non-overdue status;
- acquired-rights treatment;
- seasonally adjusted/original status;
- nominal/market valuation;
- month/quarter frequency;
- regional hierarchy roles;
- known population/classification fields.

The mapping must be scoped to source/family semantics and asserted explicitly.

### Unsafe automatic normalization

Do not automatically:

- remove punctuation from canonical keys;
- fuzzy-merge similar row labels;
- infer cross-source equivalence from equal values;
- infer identity from equal structure;
- collapse historical/current classification regimes;
- combine total and subcomponents by arithmetic;
- recompute absent values;
- overwrite an earlier source revision with a later one;
- choose one of conflicting equivalent-mapped values without a visible policy/disposition.

## Robustness to drifting source presentation

The product can support presentation drift safely through a two-level contract:

1. **structural tolerance** accepts known-equivalent typography/whitespace/header placement variants where source semantics still validate;
2. **semantic guardrails** assert expected source properties such as required title concepts, period parsability, expected dimensional cues and non-empty numeric regions.

If a new workbook variant passes lexical normalization but violates semantic/structural invariants, the adapter should fail with an explicit `UnrecognizedSourceVariant`-type condition and leave the raw source available for inspection. Silent best-effort reshaping would make preservation unverifiable.

## Provenance model for normalized observations

A normalized observation should carry or resolve to:

- `observation_id` stable within a build;
- `source_id` and `source_revision_id`;
- `sheet_exact` and `cell_coordinate`;
- `value_exact` from source lexical representation;
- typed numeric value for filtering/pivoting when valid;
- `source_concept_id` (source-local semantic identity);
- optional `canonical_concept_id` only when an explicit mapping exists;
- exact Russian source label/path;
- unit and scale;
- period and period convention;
- structured dimensions plus their exact source values;
- mapping/translation status.

This is enough to move from a prepared 2D table back to the exact source cell.

## Duplicate/conflict disposition

The semantic layer should retain all source observations. A deduplicated/canonical query view may group equivalent observations only through explicit mappings.

For canonical-key collisions:

- identical values from explicitly equivalent sources may be marked `consistent_overlap` while preserving both provenance records;
- different values become `conflict_or_revision` and remain separate;
- a known historical/new-publication relationship can be represented as lineage/revision, not silent replacement;
- user-facing pivot should require a source/revision choice when multiple values remain materially valid.

## Evidence model for “all numbers preserved”

A defensible verification consists of machine reconciliation:

1. enumerate every stored numeric or formula-cached numeric source cell directly from OOXML for all 41 acquired workbooks;
2. enumerate raw-ledger numeric records keyed by source hash/sheet/cell;
3. require exact key/value/formula equality and zero missing/extra raw numeric records;
4. classify semantic-observation coverage separately and require every excluded numeric cell to carry an explicit non-observation disposition;
5. export/reload CSV using exact value strings and verify equality of keys/strings;
6. verify that a semantic observation resolves to one raw source record and that prepared views preserve this route.

This checks preservation rather than merely whether code ran.

## Local versus internet acquisition

The observed processing work depends on workbook bytes, not on HTTP itself. Therefore acquisition and processing can be separated cleanly: the internet path downloads exact registry sources and records hashes; a local path can ingest a directory/manifest of already downloaded files through the same downstream pipeline. Equivalence is verifiable when both paths use identical bytes/hashes.

This separation has independent value and is justified by the source universe rather than being optional aesthetic modularity.

## Failure policy

Fail closed for:

- unknown registry/source ID;
- file that is not valid OOXML/XLSX;
- duplicate local source bindings;
- required sheet/period/axis contract break;
- unparseable period where a semantic observation depends on it;
- ambiguous source-cell-to-observation mapping;
- canonical equivalence conflict where the query requests a single value;
- unsupported previously unseen source structural variant.

Still preserve the acquired/raw evidence where possible and report the exact failure locus.

## Residual uncertainty

Future CBR source revisions may introduce new structures. No static parser can prove forward compatibility. The appropriate product claim is deterministic processing of the bound/recognized source contracts plus fail-closed behavior and inspectable raw evidence for unseen variants.

The final implementation mechanism remains a Target HOW decision. This research establishes the preservation and semantic-normalization boundary only.
