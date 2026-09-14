# TARGET-HOW-CBR-001 — Target Mechanism Model

**Work kind:** `TARGET_HOW_FORMATION` (`MADARAII-23`)  
**Target WHAT:** `TW-CBR-1` at `_mw/knowledge/TARGET-WHAT.md`  
**Target HOW Baseline:** `TH-CBR-1.2`  
**Supersedes:** `TH-CBR-1.1` for current mechanism behavior  
**Status:** current target HOW for `WORK-CBR-002`; Product admission still requires exact-candidate verification and `MADARAII-34`  
**Environment:** Python 3.10+; Google Colab/Jupyter-class runtime; ordinary internet access for acquisition

## Reconciliation note

`TH-CBR-1.2` preserves `TW-CBR-1` and incorporates the justified post-Jester mechanism corrections from `RES-DELTA-CBR-002`. The change is mechanism hardening rather than a Product-purpose expansion. It makes source trust, executable build identity, source-visible concept ancestry, validation ownership, consumer reliance and persistence boundaries explicit.

The implementation remains a deterministic source-registry pipeline:

`registry → trusted acquisition/local binding → source revisions → lossless OOXML ledger → source-aware semantic interpretation → catalogs/observations → blocking validation → atomic persistence/promotion → validated query/pivot views`.

Raw evidence and semantic interpretation remain separate owners. Parser convenience never replaces the exact source ledger.

## HOW-R — realization

### H-01 Registry and source specification

A package-owned registry declares the exact 41 source IDs/URLs and source-level metadata for the accepted Baseline. Each `SourceSpec` carries the row-axis role (`region`, `activity`, `indicator`, `hierarchy`, `mixed`) and source-specific parser/period semantics.

The exact build call supplies one source-id→`SourceSpec` authority used by acquisition, build identity and semantic parsing. A caller-supplied specification therefore cannot be fingerprinted while a different global specification is used for interpretation.

**FIXED:** baseline source IDs/URLs and source-local parser authority.  
**BOUNDED_OPEN:** internal representation may evolve while stable IDs and verified behavior remain compatible.

### H-02 Acquisition and local binding

`download_sources()` acquires each source independently with retry/timeouts, records HTTP/source metadata and SHA-256, and admits remote bytes only when the registry URL and final resolved URL remain on `cbr.ru` or a subdomain. A bounded `www.cbr.ru → cbr.ru` fallback may be used for the same path/query when the `www` endpoint returns 403.

Every downloaded or locally bound workbook must pass an OOXML structural gate: valid ZIP package, required workbook/content-type relationships, at least one worksheet and clean archive CRC. Successful manifest records carry a trust status (`cbr_domain_ooxml_validated` for live acquisition; `local_ooxml_validated` for local replay).

Acquisition/local binding first materializes a complete diagnostic manifest. Admission of the manifest is a separate gate, so a failed attempt retains per-source failure details. A complete-build claim requires the complete registry universe.

### H-03 Lossless OOXML extraction

The preservation layer reads XLSX OOXML directly and emits one raw record for every non-empty stored cell. It retains source/revision ID, workbook SHA-256, exact sheet/coordinate, OOXML type/style index, lexical `<v>` value, resolved shared/inline text, formula text and cached value where present.

Native numerics, formula-cached numerics and numeric-looking text, including standard accounting-parenthesis numeric forms, remain inside the numeric-completeness boundary. Source date serials remain exact in raw evidence even when a semantic period is interpreted.

**FIXED:** exact raw provenance and lexical preservation.

### H-04 Period discovery

The interpreter scans worksheets for repeated statistical period-header rows rather than assuming one fixed header. Supported current-universe grammars include Excel date/datetime cells, `dd.mm.yyyy` strings with evidenced footnote markers, Russian month+year, quarterly/annual headers and exchange-rate composite calendars.

Obvious methodology/change-log date rows are excluded from statistical period binding. Each admitted binding carries period, frequency and source representation. Required unknown period geometry fails closed.

### H-05 Shared matrix extraction

For each identified period block, extraction maps numeric data cells to the nearest valid preceding period-header row and preserves the exact row-side labels/codes plus raw-cell lineage.

Repeated blocks in one sheet are supported. Technical note/source rows remain metadata rather than observations when their source-visible role establishes that interpretation.

### H-06 Source semantic profiles/adapters

Source profiles reuse shared extraction while adding explicit, conservative semantics:

- region/activity matrices expose row labels as dimensions while concept identity remains the measure;
- indicator/hierarchy/mixed tables preserve source-local semantic ancestry;
- repeated measure blocks may use period-block headings, merged parent cells, stable section anchors and source-visible parent paths;
- explicit short-/long-term source parent labels may enter concept ancestry without inventing a normalized maturity bucket;
- exchange-rate series retain explicit source measure definitions such as growth versus previous December, previous period or corresponding prior-year period;
- source-specific calendar compatibility views alter interpretation only; raw OOXML stays untouched.

Source profiles may share mechanics without sharing concept identity.

**FIXED:** source-local identity; no fuzzy cross-source merge; no physical row number as an ordinary concept-identity component.  
**BOUNDED_OPEN:** evidenced source-profile extensions with regression and full-corpus verification.

### H-07 Dimension and source-context semantics

Only evidenced qualifiers become dimensions. Current logic covers currency denomination, overdue status, acquired-rights treatment, adjustment, territory/activity members, selected maturity cues, statement/measurement currency and source-specific scope markers.

Inference is precedence- and negation-aware. Ambiguous combined buckets are omitted rather than guessed. Explicit currency headings may scope repeated branch children; inheritance is removed from later unique aggregates where the source does not establish that scope. Region/activity row labels remain dimension members and are excluded from concept-splitting logic.

Unknown qualifiers remain available through exact source labels/context. Stored dimension JSON is canonical and sorted.

### H-08 Concept and bilingual catalog

Each source-local concept receives a deterministic ID from source ID plus a source-visible semantic key. Stable semantic ancestry may include exact measure title, unit/scale signature, source hierarchy, repeated-block heading, merged parent, section anchor or explicit source parent label. Physical row numbers are provenance geometry rather than business identity.

The catalog preserves exact Russian source label/path, normalized Russian search label, readable Russian name, English project display name, translation status and source context. A complete build requires bilingual user surfaces and allowed translation statuses.

### H-09 Observation store

The canonical observation form includes:

`build_id, source_id, source_revision_id, source_concept_id, period, frequency, period_role, value_exact, value_kind, unit, scale, dimensions_json, sheet_exact, cell_coordinate, raw_cell_id`.

`value_exact` is authoritative. Query-time numeric projection is a convenience only. Open dimensions remain canonical JSON in storage and become `dim_*` columns in the consumer facade.

### H-10 Raw-cell dispositions

Every raw non-empty cell receives one disposition. Numeric/numeric-text/formula-cached content is classified as observation value, period/header structure, hierarchy/classification code, metadata/helper or explicit unmapped residue.

A complete build requires zero `unmapped_numeric` residue and one-to-one observation→raw-cell cardinality.

### H-11 Persistence/export

A successful build writes `build_manifest.json`, compatibility `build.json`, `source_manifest.json`, canonical CSV exports, validation/diagnostics and `data/cbr_unified.sqlite`.

CSV and SQLite derive from the same validated owner set. Direct SQLite writing uses a sibling temporary database, integrity check and atomic `os.replace`; a failed direct persistence attempt therefore preserves the prior reusable database. Full Product promotion remains a separate sibling-staging transaction.

### H-12 Query and pivot

`UnifiedDatabase(sqlite_path, allow_unvalidated=False)` is fail-closed by default. Ordinary queries require embedded validation status `passed`; diagnostic callers may explicitly opt into an unvalidated database.

The facade exposes:

- bilingual `sources(language=...)`;
- `indicators()` with RU/EN search;
- `observations()` with source/concept/time/frequency/period-role/open-dimension filters;
- dimension-member display and filtering through Russian source value, Russian display name or English display name;
- `pivot()` with no implicit aggregation and an additional hidden semantic-homogeneity gate over unit, scale, frequency and period role;
- `raw_cell()` and `lineage()` with separate observation/concept/raw/disposition source owners;
- `validation()` for embedded build evidence.

CLI repeated same-key `--dim` values represent an OR-list rather than silent overwrite.

### H-13 Validation

`validate_bundle()` is the blocking build-time gate. It checks source/revision ownership across manifest, raw cells, dispositions, concepts and observations; raw file hashes; exact locator coherence; one raw cell per observation; canonical dimension JSON; valid ISO calendar dates; allowed frequency/period-role domains; non-empty units; positive integer scales where present; complete source coverage; zero unmapped numeric cells; bilingual completeness; and semantic duplicate/conflict rules.

The semantic duplicate key is:

`source_id + source_concept_id + period + frequency + period_role + unit + scale + canonical dimensions`.

Conflicting values under that complete key block admission. The gate remains strict; source semantics are repaired rather than conflict checks weakened.

## HOW-A — application

### Complete internet build

1. install package/dependencies;
2. call `build_database(output_dir)`;
3. require successful validation/build evidence;
4. open `UnifiedDatabase(<output>/data/cbr_unified.sqlite)`;
5. discover concepts/dimensions and query a sufficiently disambiguated slice;
6. export CSV/query/pivot views as required.

### Local replay

1. bind exact source files by stable source ID/registry filename or explicit mapping;
2. call `build_database(output_dir, input_dir=...)`;
3. require OOXML trust validation and the same semantic/validation path used by live acquisition.

### External reuse

External Python code may import `build_database`, `UnifiedDatabase`, registry/spec objects and lower-level acquisition/raw/semantic/validation modules. Notebook state is optional.

## HOW-O — operation, failure and recovery

- Source bytes are accepted only after CBR-domain/OOXML trust checks for live builds or OOXML validation for local replay.
- Source hash change creates a new source revision.
- `build_id` binds build-contract version, exact source-spec fingerprint, exact sorted source revisions, implementation SHA-256 and resolved Python/requests/openpyxl/pandas versions.
- Code/runtime changes therefore create a distinct build identity even when source bytes are unchanged.
- Semantic/profile mismatch or validation failure retains staging evidence and preserves the prior promoted Product output.
- Acquisition failures retain the diagnostic acquisition manifest before admission.
- Full output promotion restores the prior output on promotion interruption where filesystem semantics permit.
- Direct SQLite replacement is itself atomic and preserves the prior database on failure.
- Internet build and local replay over the same exact bytes/spec/code/runtime must agree on deterministic Product tables and build identity.
- SQLite/CSV remain rebuildable projections, not independent truth owners.

## WHAT-to-HOW trace

- TW-01/02 → H-02 trusted acquisition/local binding and revision manifests.
- TW-03/04 → H-03/H-10 raw ledger plus complete dispositions.
- TW-05/06 → H-04..H-08 source-aware periods, contexts, dimensions and concept identity.
- TW-07 → source revisions, canonical semantic key and explicit lineage-owner coherence.
- TW-08 → conservative inference, source adapters, fail-closed unknown variants and source trust.
- TW-09/10 → H-08 bilingual catalog and dimension-member surfaces.
- TW-11 → H-12 validated non-aggregating query/pivot behavior.
- TW-12 → H-11 CSV/SQLite persistence.
- TW-13/14 → package/CLI/notebook/external reuse.
- TW-15 → H-13 validation plus implementation/runtime-bound build evidence.

## Design freedom ledger

**FIXED:** layered raw/semantic model; exact source-cell provenance; explicit source specs; source-local identity; no fuzzy merge; non-aggregating pivot; fail-closed ordinary query; CSV portability; complete validation gate; trusted acquisition; implementation/runtime-bound build identity.

**BOUNDED_OPEN:** internal helpers, SQLite indexes, caching, optional convenience projections, compatibility aliases and source-profile refinements backed by evidence.

**UNRESOLVED_BLOCKING:** none at target-model level. Sparse cross-source equivalence remains intentional.

## Verification strategy

A complete verification run covers the 41-source live build, offline deterministic replay, independent raw OOXML preservation, CSV↔SQLite reconciliation, source-trust statuses, implementation/runtime fingerprint agreement, bilingual/query/filter behavior, lineage ownership, strict semantic conflicts, direct persistence behavior and publication-metadata applicability audit.

Publication metadata such as hidden sheets/rows/columns, comments and percent formatting is evidence-first. Presence alone does not create a semantic rule; only demonstrated Product relevance authorizes a mechanism change.

## Reopen triggers

Reopen Target HOW when Target WHAT changes, registry/source universe changes, a new source distinction exceeds the observation model, preservation evidence fails, material source presentation/semantics changes, publication metadata proves semantically controlling, or implementation/runtime constraints invalidate the accepted operating environment.
