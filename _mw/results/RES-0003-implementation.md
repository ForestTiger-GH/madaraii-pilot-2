# RES-IMPLEMENTATION-CBR-001 — CBR Unified Statistics implementation result

**Work kind:** `ENGINEERING_PRODUCT_IMPLEMENTATION`  
**Commission:** `WORK-CBR-001`  
**Plan:** `PLAN-CBR-001` at `_mw/work/PLAN-0001.md`  
**Target:** `TW-CBR-1` / `TH-CBR-1` / `PRODUCT-ARCH-CBR-001`  
**Product-code candidate:** `dd5d4e591de0e0d23f0b0bffb138bd0d892f58ae`  
**Status:** implementation candidate established; independent verification and Product admission remain separate.

## Actual realized change

The repository now contains a reusable Python product for the registry-defined Bank of Russia Excel universe.

- `src/cbr_unified/registry.py` owns the reviewed 41-source registry snapshot derived from the single permitted stratbox registry input.
- `acquisition.py` implements live HTTP acquisition, exact local rebinding, source hashes and revision manifests.
- `raw.py` implements a lossless OOXML raw-cell ledger independent of openpyxl value coercion. It retains source revision, sheet, coordinate, OOXML type, style, lexical value, resolved text and formula.
- `normalization.py`, `semantic.py` and `processing.py` implement conservative period, unit, dimension and source-concept interpretation. Presentation compatibility for the current exchange-rate workbook is source-scoped and operates on a temporary semantic view; raw evidence remains the untouched workbook.
- `validation.py` requires complete source coverage, raw-cell disposition coverage, exact observation lineage, valid semantic identities, zero unexplained numeric cells in a complete build, and zero conflicting semantic duplicate groups.
- `persistence.py` materializes CSV and SQLite representations from the same in-memory owner set.
- `build.py` coordinates live and local/replay builds.
- `query.py` provides pandas-based bilingual lookup, filtering, dimension expansion, exact lineage and fail-closed pivots.
- `cli.py` exposes build, validate, source listing, indicator lookup, observation query, pivot and lineage operations.
- `README.md`, `docs/` and `examples/` provide cold-use guidance.
- `tests/` and `tools/verify_full_build.py` / `tools/independent_verify_preservation.py` provide producer and independent-verification surfaces.

## Plan trace

1. **Preservation foundation:** source revision and raw OOXML ledger implemented before semantic normalization.
2. **Semantic unification:** observations retain source-local concept identity plus explicit period/frequency/role/unit/dimensions and exact raw lineage.
3. **Persistence:** deterministic CSV plus SQLite bundle implemented.
4. **Use surface:** pandas API, bilingual names, filters, pivots, CLI and examples implemented.
5. **Assurance:** fail-closed source-variant handling, numeric residue gate, conflict checks, deterministic offline replay and independent OOXML comparison implemented.

## Material implementation choices exercised

- SQLite and CSV are parallel derived projections from one build state; neither is a second semantic authority.
- Source numeric values are stored as exact strings in the authoritative observation representation and converted to numeric types only at the query convenience boundary.
- Source-local semantic identity remains source-scoped. Structural similarity and normalized labels never merge concepts automatically.
- Exchange-rate calendar repair is restricted to proven current presentations (`N кварт.` and the annual year formula chain) in the semantic view. Any other layout remains fail-closed.
- Unknown numeric residue in a complete source universe is an implementation error, not silently classified metadata.

## Producer evidence available before independent verification

- Unit and contract tests passed in GitHub Actions on the implementation lineage immediately preceding final verification.
- An earlier full-build attempt correctly stopped on an unrecognized exchange-rate quarterly presentation instead of silently dropping 2,354 numeric candidates. The exact source presentation was investigated and bounded compatibility logic plus regression tests were added.
- The current verification workflow separately executes live acquisition, complete build, offline replay, CSV/SQLite reconciliation, query/CLI smoke checks, and independent raw OOXML preservation checks.

Producer evidence is evidence of implementation discipline; it is not an independent conformance verdict.

## Effects and exclusions

Actual effects are limited to repository files and GitHub Actions verification activity. No external database, production service, deployment, release, customer state or Bank of Russia source is mutated. Network effects are read-only HTTP acquisition of the declared public source files.

## Verification handoff

Verification must bind the exact current product-code candidate and the 41-source data revisions acquired by the verification run. It must establish, at minimum:

- all 41 registry sources acquire and produce semantic observations;
- every raw source cell is dispositioned and every observation resolves to one raw cell;
- zero unexplained numeric source cells remain in a complete build;
- no conflicting semantic duplicates are admitted;
- live and offline replay produce identical deterministic semantic/raw tables from the same source revisions;
- independent OOXML extraction matches the product raw ledger field-for-field and every observation `value_exact` matches source lexical/resolved content;
- bilingual query, filters, lineage and CLI surfaces execute on the produced database;
- no evidence supports a deployment or business-outcome claim.

## Residue at handoff

Independent verification, Product state reconciliation/admission, Work State refresh, removal of one-shot repair infrastructure, and Development Contour Closure Audit remain pending. Any verification defect returns to the owning implementation or design surface under a new exact Baseline.
