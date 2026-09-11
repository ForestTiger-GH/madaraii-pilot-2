# TARGET-HOW-CBR-001 — Target Mechanism Model

**Work kind:** `TARGET_HOW_FORMATION` (`MADARAII-23`)  
**Target WHAT:** `TW-CBR-1` at `_mw/knowledge/TARGET-WHAT.md`  
**Target HOW Baseline:** `TH-CBR-1.1`  
**Supersedes:** `TH-CBR-1` for current mechanism nomenclature  
**Status:** accepted under the active Commission; reconciled after implementation verification  
**Environment:** Python 3.10+; Google Colab/Jupyter-class runtime; ordinary internet access for acquisition

## Reconciliation note

`TH-CBR-1.1` does not weaken or expand `TW-CBR-1`. It reconciles bounded implementation-surface choices discovered during realization and verified on the exact Product candidate. The prior mechanism text used provisional names such as `concepts.csv`, `Dataset`, `build_from_internet()`, `build_from_directory()`, `validate_build()` and `dimensions_extra`; the admitted implementation uses `source_concepts.csv`, `UnifiedDatabase`, one `build_database()` entry point with optional `input_dir`, build-time `validate_bundle()` plus embedded validation access, and exact source labels/context plus open `dimensions_json`. These are mechanism/naming reconciliations under previously declared bounded implementation freedom.

## Mechanism overview

The Product is realized as an installable Python package plus thin notebook/example orchestration. Processing is a deterministic pipeline over an explicit source registry:

`registry → acquisition/local binding → source revisions → lossless OOXML ledger → semantic source profiles/adapters → catalogs/observations → validation → CSV/SQLite exports → query/pivot views`.

The raw ledger and semantic observation layer are separate owners of different claims. Raw preservation never depends on semantic adapter success.

## HOW-R — realization

### H-01 Registry and source specification

A package-owned registry declares the exact 41 source IDs/URLs and source-level metadata required for the accepted Baseline. Each source has a semantic profile specifying its row-axis role (`region`, `activity`, `indicator`, `hierarchy`, `mixed`) and any specialized parser behavior.

**FIXED:** source IDs and URLs for this Baseline; source-local parser binding.  
**BOUNDED_OPEN:** internal representation of specifications may evolve if stable IDs/behavior remain compatible.

### H-02 Acquisition and local binding

`download_sources()` downloads each source independently with retry/timeouts, records HTTP/source metadata and SHA-256, and writes a manifest binding `source_id → local file → hash`.

`bind_local_sources()` resolves files by stable source ID/expected filename or explicit mapping, hashes them, and emits the same manifest shape. Downstream processing consumes that resolved source-revision state, so internet and local paths converge before raw/semantic interpretation.

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
- `dd.mm.yyyy` strings, including bounded trailing footnote markers evidenced in the current source set;
- Russian month + year strings;
- quarterly/annual date headers;
- exchange-rate composite year + month/quarter headers through a dedicated source-scoped semantic view.

Each parsed period carries `period`, `frequency` and source representation. Stock/flow/published-change semantics remain source-concept/source-profile attributes rather than being inferred solely from the calendar token.

Unknown required period grammar fails the semantic source contract.

### H-05 Shared matrix extraction

For each identified period block, extraction maps data cells beneath/along the period columns. It collects exact row-side labels/codes before the period axis and links each observation to its raw cell.

Repeated period blocks in one worksheet are supported by selecting the nearest valid preceding period-header row for each data row.

### H-06 Source semantic profiles/adapters

Source profiles reuse shared matrix extraction while applying explicit row-axis and source-specific behavior:

- regional matrices promote the row member into `region` and a conservative territory type;
- activity matrices promote the row member into activity/classification dimensions, preserving current OKVED2 and historical regimes separately;
- indicator/hierarchy matrices retain source-local concept identity and source row context;
- exchange-rate processing reconstructs periods from composite headers through a bounded semantic compatibility view while raw evidence remains untouched;
- mixed/repeated blocks are handled through the same period-binding and nearest-header mechanics where the current source contract supports them.

Source profiles may share structural logic without sharing semantic concept IDs.

**FIXED:** no fuzzy cross-source merging; source-local concept identity is the default truth.  
**BOUNDED_OPEN:** individual source/profile heuristics may be extended when tests preserve current semantics.

### H-07 Dimension and sheet semantics

A controlled interpreter extracts only evidenced dimensions from sheet/title/row context, including currency denomination, overdue status, acquired-rights treatment, adjustment, valuation/frequency, territory/activity member, selected maturity/sector cues and source-specific scope markers.

Unrecognized qualifiers remain available through exact source sheet/row labels and source context rather than being guessed into a canonical dimension. Open recognized dimensions are stored in canonical sorted `dimensions_json`.

### H-08 Concept and bilingual catalog

Each source-local concept receives a stable deterministic ID derived from source ID plus source-local semantic key. User names are fields, not keys.

The catalog carries:

- exact source Russian label/path;
- normalized Russian search label;
- readable Russian name;
- English display name;
- translation status (`cbr_official`, `project_translation`, `transliteration_only` where appropriate);
- source/hierarchy context.

Dataset/family/measure terms use reviewed RU/EN source specifications and project translation where official one-to-one terminology was not established. Dimension members use typed project translation or transparent transliteration according to their semantic role. A complete build requires every user-exposed dataset, concept and dimension member to have both RU/EN display surfaces and an allowed translation status.

### H-09 Observation store

The canonical build output is long-form. Core observation columns include:

`build_id, source_id, source_revision_id, source_concept_id, period, frequency, period_role, value_exact, value_kind, unit, scale, dimensions_json, sheet_exact, cell_coordinate, raw_cell_id`.

Open dimensions remain in canonical sorted JSON in persistence. The query facade expands them into `dim_*` convenience columns dynamically, preventing a brittle universal wide schema.

`value_exact` is authoritative for source preservation; query-time numeric projection supports display/pivoting without replacing exact source text.

### H-10 Raw-cell dispositions

After semantic extraction, every raw non-empty cell has a role. Numeric/numeric-text/formula-cached cells are classified as observation value, period/header, hierarchy/classification code, metadata/helper or explicit unmapped residue. A complete semantic build requires zero unresolved numeric-value candidates under recognized source contracts.

### H-11 Persistence/export

A successful promoted build writes current owner/projection files including:

- `build_manifest.json` and compatibility `build.json`;
- `source_manifest.json`;
- `data/source_revisions.csv`;
- `data/raw_cells.csv`;
- `data/cell_dispositions.csv` plus compatibility alias `raw_cell_dispositions.csv`;
- `data/source_concepts.csv`;
- `data/dimension_members.csv`;
- `data/observations.csv`;
- `data/validation.json`;
- `data/cbr_unified.sqlite` containing equivalent query tables/indexes and embedded build/validation metadata.

CSV is the portability output contract; SQLite is the packaged local query projection. Both derive from the same validated in-memory owner set and are reconciled during verification.

### H-12 Query and pivot

`UnifiedDatabase(sqlite_path)` is the reusable read-only query facade. It exposes:

- `sources()`;
- `indicators()` with RU/EN display search;
- `observations()` with source/concept/time/frequency/period-role/open-dimension filters;
- `pivot()` with caller-selected rows/columns and language;
- `raw_cell()` and `lineage()` for trace-back;
- `validation()` for embedded build evidence.

CLI commands expose the same source/catalog/query/pivot/lineage behaviors and CSV export. CSV bundle outputs remain directly usable by ordinary Python/pandas consumers without becoming a second query-semantics owner.

Pivot performs no aggregation by default. If several observations map to one requested pivot cell, `QueryError` is raised with provenance-bearing samples and the caller must narrow or reshape the request.

### H-13 Validation

`validate_bundle()` is the build-time gate over source coverage, identities, raw-cell dispositions, observation/raw lineage, semantic conflicts, numeric residue and bilingual completeness. A successful build embeds/writes its validation report; `UnifiedDatabase.validation()` and CLI `validate` expose it afterward.

The build fails and retains staging/failure evidence when a protected criterion fails. Failed staging never replaces a previously successful promoted build.

## HOW-A — application

### Complete internet build

1. install the package/dependencies;
2. call `build_database(output_dir)` with no `input_dir`;
3. inspect the returned `BuildResult`, `data/validation.json` or `UnifiedDatabase.validation()`;
4. open `UnifiedDatabase(<output>/data/cbr_unified.sqlite)`;
5. discover concepts, filter observations and construct a sufficiently disambiguated pivot;
6. export complete bundle CSVs or requested CLI/query/pivot views to CSV.

### Local build

1. place source files in a local directory under stable source IDs/known filenames, or supply explicit source mappings through the Python API;
2. call `build_database(output_dir, input_dir=...)`;
3. downstream raw/semantic/validation processing is the same as for downloaded bytes.

### External system reuse

External Python code imports `build_database`, `UnifiedDatabase`, source registry/spec objects and lower-level acquisition/raw/semantic/validation modules directly where needed. No notebook state is required.

## HOW-O — operation, failure and recovery

- Acquisition retries transient HTTP errors and records terminal failures.
- Source hash changes are visible in the manifest and become a new source revision/build identity input.
- Semantic/profile mismatch stops affected semantic admission while retaining acquired/raw evidence in staging.
- Build output is written to a sibling staging directory and promoted only after required validation and persistence pass; a failed build does not overwrite a prior successful output.
- Re-running from identical source bytes/spec/build-contract version is deterministic for semantic/raw tables and build identity; acquisition timestamps are non-semantic metadata.
- Bilingual incompleteness or invalid translation status blocks the complete-build claim.
- SQLite/CSV outputs are rebuildable projections from the same manifest/spec version and are not independent truth owners.

## WHAT-to-HOW trace

- TW-01/02 → H-02 manifests and converged acquisition/local path.
- TW-03/04 → H-03/H-10 raw ledger plus disposition reconciliation.
- TW-05/06 → H-04..H-07 source profiles and explicit concept IDs.
- TW-07 → source hashes/revisions plus conflict/ambiguity-safe behavior.
- TW-08 → conservative normalization, bounded source compatibility and fail-closed source/profile gates.
- TW-09/10 → H-08 bilingual catalog with translation provenance.
- TW-11 → H-12 non-aggregating filter/pivot.
- TW-12 → H-11 CSV/SQLite persistence and view export.
- TW-13/14 → package APIs plus notebook/external-system use on ordinary Python dependencies.
- TW-15 → H-13 machine-readable validation/build evidence.

## Design freedom ledger

**FIXED:** layered raw/semantic model; exact source-cell provenance; explicit source specs; no fuzzy semantic merging; non-aggregating default pivot; CSV portability; complete validation gate; internet/local path convergence.

**BOUNDED_OPEN:** internal helper/class names, pandas versus streaming implementation in local pieces, exact SQLite indexes, translation catalog layout, caching strategy, optional convenience projections and compatibility aliases.

**UNRESOLVED_BLOCKING:** none. Sparse cross-source canonical equivalence is an intentional supported state, not a blocker.

## Verification strategy

A complete real-source run verifies all 41 inputs and reconciles raw OOXML cell identities/values to exported raw data, semantic numeric dispositions, provenance, bilingual catalog completeness, source-spec coverage, full internet/local replay equivalence on the same downloaded bytes, deterministic CSV hashes, SQLite counts, query/CLI operation, pivot ambiguity behavior and fail-closed source-variant handling.

## Reopen triggers

Target WHAT change, registry/source-set change, a new source distinction that the common observation contract cannot represent, evidence that lexical preservation is incomplete, materially changed source presentation/semantics, or an implementation/runtime constraint that prevents Colab/Jupyter-class use.
