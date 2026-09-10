# TARGET-HOW-CBR-001 — Target Mechanism Model

**Work kind:** `TARGET_HOW_FORMATION` (`MADARAII-23`)  
**Target WHAT:** `TW-CBR-1` at `_mw/knowledge/TARGET-WHAT.md`  
**Target HOW Baseline:** `TH-CBR-1`  
**Status:** accepted under the active Commission  
**Environment:** Python 3.10+; Google Colab/Jupyter-class runtime; ordinary internet access for acquisition

## Mechanism overview

The Product is realized as an installable Python package plus thin notebook/example orchestration. Processing is a deterministic pipeline over an explicit source registry:

`registry → acquisition/local binding → source revisions → lossless OOXML ledger → semantic source adapters → catalogs/observations → validation → CSV/SQLite exports → query/pivot views`.

The raw ledger and semantic observation layer are separate owners of different claims. Raw preservation never depends on semantic adapter success.

## HOW-R — realization

### H-01 Registry and source specification

A package-owned registry declares the exact 41 source IDs/URLs and source-level metadata required for the accepted Baseline. Each source has a semantic profile specifying its row-axis role (`region`, `activity`, `indicator`, `hierarchy`, `mixed`) and any specialized parser behavior.

**FIXED:** source IDs and URLs for this Baseline; source-local parser binding.  
**BOUNDED_OPEN:** internal representation of specifications may evolve if stable IDs/behavior remain compatible.

### H-02 Acquisition and local binding

`download_sources()` downloads each source independently with retry/timeouts, records HTTP metadata and SHA-256, and writes a manifest binding `source_id → local file → hash`.

`bind_local_sources()` resolves files by stable source ID/expected filename or explicit mapping, hashes them, and emits the same manifest shape. Downstream code accepts only the manifest, so internet and local paths converge immediately.

Partial acquisition is retained diagnostically but a complete-build claim requires every registry source.

### H-03 Lossless OOXML extraction

A standard-library OOXML reader opens the XLSX ZIP, resolves workbook sheet relationships/shared strings, and emits one raw record for every non-empty cell. It retains:

- source/revision ID and SHA-256;
- exact sheet title and coordinate;
- cell OOXML type/style index;
- exact lexical `<v>` value when present;
- inline/shared string resolved text while retaining storage type;
- formula text and cached value where present.

Native numerics, formula-cached numerics and numeric-looking text are never discarded. Source date serials remain exact in the raw record even when a semantic date is also interpreted.

**FIXED:** raw provenance key and exact lexical preservation behavior.

### H-04 Period discovery

A period interpreter scans worksheets for repeated period header rows rather than assuming one fixed header. Supported grammars for the current universe include:

- Excel date/datetime cells;
- `dd.mm.yyyy` strings;
- Russian month + year strings;
- quarterly/annual date headers;
- exchange-rate composite year + month/quarter headers through a dedicated adapter.

Each parsed period carries `period`, `frequency` and source representation. Stock/flow/derived semantics remain source-concept attributes rather than inferred solely from the calendar token.

Unknown required period grammar fails the semantic source contract.

### H-05 Shared matrix extractor

For each identified period block, the extractor maps data cells beneath/along the period columns. It collects exact row-side labels/codes before the period axis and links each observation to its raw cell.

Repeated period blocks in one worksheet are supported by selecting the nearest valid preceding period-header row for each data row.

### H-06 Source semantic adapters

Adapters reuse matrix extraction while applying explicit source profiles:

- **RegionMatrixAdapter:** row member becomes `region`; source-level measure concept remains stable; territory scope/type is classified conservatively.
- **ActivityMatrixAdapter:** row member becomes an activity/classification dimension; current `C` sources are tagged `OKVED2`; historical `A` sources remain a distinct regime.
- **IndicatorMatrixAdapter:** each labelled row/block becomes a source-local concept.
- **HierarchyMatrixAdapter:** row code/label/position and inherited recognized context preserve nested concept identity; source-specific rules may promote embedded currency/sector/maturity/valuation dimensions.
- **ExchangeRateAdapter:** reconstructs periods from composite headers and preserves measure-row semantics.
- **MixedBlockAdapter:** handles repeated section/period blocks such as SME borrower information.

Source profiles may share adapter classes without sharing semantic concept IDs.

**FIXED:** no fuzzy cross-source merging; source-local concept identity is the default truth.  
**BOUNDED_OPEN:** individual adapter heuristics may be extended when tests preserve current semantics.

### H-07 Dimension and sheet semantics

A controlled interpreter extracts only evidenced common dimensions from sheet/title/row context: currency denomination, overdue status, acquired-rights treatment, adjustment, valuation/frequency, territory/activity member, balance/transaction and selected maturity/sector cues.

Unrecognized qualifiers remain in exact source labels/hierarchy and `dimensions_extra` rather than being guessed.

### H-08 Concept and bilingual catalog

Each source-local concept receives a stable deterministic ID derived from source ID plus source-local semantic key. User names are fields, not keys.

The catalog carries:

- exact source Russian label/path;
- normalized Russian search label;
- readable Russian name;
- English display name;
- translation status (`cbr_official`, `project_translation`, `transliteration_only` where appropriate for proper names/technical identifiers);
- hierarchy/source context.

Dataset/family/measure terms use curated RU/EN source specifications and official CBR terminology where established. Dimension-member translation uses curated controlled mappings plus deterministic proper-name transliteration where semantic translation is inappropriate. Any user-exposed unresolved translation is reported by validation.

### H-09 Observation store

The canonical build output is long-form. Core observation columns are stable:

`build_id, source_id, source_revision_id, source_concept_id, period, frequency, period_role, value_exact, value_kind, unit, scale, dimensions_json, sheet_exact, cell_coordinate, raw_cell_id`.

Frequently used dimensions are projected into convenience columns when available (`region_id/name`, `currency`, `overdue`, `sme_scope`, `valuation`, `maturity`, `adjustment`, `activity_code/name`). Open dimensions remain in canonical sorted JSON, preventing a brittle universal wide schema.

`value_exact` is authoritative for source preservation; a parsed Decimal-compatible text/numeric projection supports filtering/display without replacing it.

### H-10 Raw-cell dispositions

After semantic extraction, every raw non-empty cell has a role. Numeric/numeric-text/formula-cached cells are classified as observation value, period/header, hierarchy/classification code, metadata/helper or explicit unmapped residue. A complete semantic build requires zero unresolved numeric-value candidates under recognized source contracts.

### H-11 Persistence/export

A build writes:

- `build_manifest.json`;
- `source_revisions.csv`;
- `raw_cells.csv`;
- `cell_dispositions.csv`;
- `concepts.csv`;
- `dimension_members.csv`;
- `observations.csv`;
- `validation.json`;
- `cbr_unified.sqlite` containing equivalent query tables/indexes.

CSV is the portability contract; SQLite is a dependency-free query acceleration/package surface.

### H-12 Query and pivot

`Dataset` loads CSV or SQLite and exposes:

- catalog search in RU/EN;
- `filter()` over core columns and arbitrary dimensions;
- `pivot()` with rows/columns/value/language;
- CSV export of filtered or pivoted data.

Pivot performs no aggregation by default. Duplicate output keys raise `AmbiguousObservationError` with candidate source/provenance rows.

### H-13 Validation

`validate_build()` runs structural, preservation, semantic, bilingual and provenance checks and writes typed claims/evidence. The build command exits non-zero when a protected claim fails.

## HOW-A — application

### Complete internet build

1. install package dependencies;
2. call `build_from_internet(output_dir=...)`;
3. inspect returned validation summary;
4. open `Dataset(output_dir)`;
5. discover concepts/dimensions, filter and pivot;
6. export requested CSVs.

### Local build

1. place source files in a local directory using source IDs/known filenames or provide an explicit source mapping;
2. call `build_from_directory(input_dir, output_dir)`;
3. downstream semantics and validation are identical to the internet path.

### External system reuse

External Python code imports acquisition, build, validation and query operations directly. No notebook state is required.

## HOW-O — operation, failure and recovery

- Acquisition retries transient HTTP errors and records terminal failures.
- Source hash changes are visible in the manifest and treated as a new revision.
- Semantic adapter mismatch stops that source's semantic admission while retaining acquired/raw evidence.
- Build output is written to a staging directory and promoted only after required validation passes; a failed build does not overwrite a prior successful output.
- Re-running from identical source bytes/spec version is deterministic except acquisition timestamps.
- Translation/catalog warnings are explicit and can block bilingual completeness claims.
- SQLite/CSV outputs are rebuildable projections from the same manifest/spec version and are not independent truth owners.

## WHAT-to-HOW trace

- TW-01/02 → H-02 manifests and converged acquisition/local path.
- TW-03/04 → H-03/H-10 raw ledger plus disposition reconciliation.
- TW-05/06 → H-04..H-07 source profiles/adapters and explicit concept IDs.
- TW-07 → source hashes/revisions plus duplicate-safe query behavior.
- TW-08 → conservative normalization, semantic anchor checks and fail-closed adapters.
- TW-09/10 → H-08 bilingual catalog with translation provenance.
- TW-11 → H-12 non-aggregating filter/pivot.
- TW-12 → H-11 CSV/SQLite persistence.
- TW-13/14 → package APIs plus notebook surface on ordinary Python dependencies.
- TW-15 → H-13 typed validation evidence.

## Design freedom ledger

**FIXED:** layered raw/semantic model; exact source-cell provenance; explicit source specs; no fuzzy semantic merging; non-aggregating default pivot; CSV portability; complete validation gate; internet/local path convergence.

**BOUNDED_OPEN:** internal function/class names, pandas versus streaming implementation in local pieces, exact SQLite indexes, translation catalog file layout, caching strategy, optional convenience columns.

**UNRESOLVED_BLOCKING:** none for implementation. Sparse cross-source canonical equivalence is an intentional supported state, not a blocker.

## Verification strategy

A complete real-source run verifies all 41 inputs and reconciles raw OOXML cell identities/values to exported raw data, semantic numeric dispositions, provenance, bilingual catalog completeness, source-spec coverage, internet/local equivalence on a sampled full source set using downloaded bytes, CSV roundtrip, SQLite counts, pivot behavior, ambiguity failure and synthetic unknown-variant failure.

## Reopen triggers

Target WHAT change, registry/source-set change, a new source distinction that the common observation contract cannot represent, evidence that lexical preservation is incomplete, or an implementation constraint that prevents Colab/Jupyter use.
