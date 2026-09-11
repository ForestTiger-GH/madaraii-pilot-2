# RES-VERIFICATION-CBR-001B — Target HOW bounded revalidation

**Work kind:** `IMPLEMENTATION_VERIFICATION` (`MADARAII-32`)  
**Subject:** unchanged product-code candidate `4ee8583b3feff7775a956c51812232fa0d0516d2`  
**Changed owner:** Target HOW `TH-CBR-1` → `TH-CBR-1.1` at commit `8fe3e9c6269cfa240ca76994410b6da36f1d08c4`  
**Target WHAT:** unchanged `TW-CBR-1`  
**Primary evidence:** `VERIFY-CBR-001`; verification run `34544307123`  
**Status:** bounded revalidation complete.

## Why revalidation was required

`RES-VERIFICATION-CBR-001` classified several provisional mechanism names/surfaces in `TH-CBR-1` as stale relative to the verified implementation. The Target HOW owner was reconciled rather than changing Product code to mimic stale provisional names.

The owner delta changes only `_mw/knowledge/TARGET-HOW.md`. Product source, tests, registry, build contract and verification data are unchanged.

## Reconciled items and evidence

| TH-CBR-1.1 item | Actual verified surface | Evidence disposition |
| --- | --- | --- |
| H-07 open qualifiers | exact source sheet/row/context plus canonical `dimensions_json`; no fictitious `dimensions_extra` field | `CONFORMS` — verified observations retain dimensions/provenance and raw/source labels. |
| H-11 concept catalog | `data/source_concepts.csv` | `CONFORMS` — deterministic live/replay hash `2cefb50e5c010d0b3cb03469c1bfb0c4387721af6af3b65284465c84244321af`; 2,970 rows match SQLite. |
| H-11 disposition alias | canonical `cell_dispositions.csv`, compatibility `raw_cell_dispositions.csv` | `CONFORMS` — identical hash `e8ba877d190677a1354e17305bc3dab690262470512e841960c010dfd2b7b3cd`. |
| H-12 query facade | `UnifiedDatabase(sqlite_path)` with `sources`, `indicators`, `observations`, `pivot`, `raw_cell`, `lineage`, `validation` | `CONFORMS` — query/lineage/CLI smoke tests and unit tests passed. |
| H-12 ambiguity behavior | `QueryError` on multi-observation pivot cell | `CONFORMS` — contract test verifies fail-closed pivot. |
| HOW-A internet build | `build_database(output_dir)` | `CONFORMS` — decisive 41-source live build passed. |
| HOW-A local build | `build_database(output_dir, input_dir=...)` | `CONFORMS` — full replay produced same build ID, revisions and deterministic tables. |
| H-13 validation | build-time `validate_bundle()`, persisted/embedded validation, `UnifiedDatabase.validation()` and CLI `validate` | `CONFORMS` — complete gate and CLI validation passed. |
| H-09 dimension convenience | dynamic query-time `dim_*` projections rather than persisted global columns | `CONFORMS` — open-dimension filtering/query implementation and tests preserve canonical `dimensions_json`. |
| Verification strategy wording | full 41-source live/local replay rather than provisional sampling wording | `CONFORMS` — run `34544307123` exercised the full registry universe. |

## Criterion integrity

This reconciliation does not reduce any `TW-CBR-1` obligation. It removes provisional implementation names that were explicitly bounded-open and replaces them with the already verified mechanism. The earlier stale-design finding remains part of history; it is not rewritten into a false original conformance claim.

## Conclusion

**`TH-CBR-1.1` against product-code candidate `4ee8583b3feff7775a956c51812232fa0d0516d2`: `CONFORMS`.**

No Product-code re-verification run is required because the candidate and executable configuration did not change; the same exact evidence directly exercises every reconciled mechanism surface. A later Product-code, registry/source-revision or semantic target change reopens the affected verification scope.