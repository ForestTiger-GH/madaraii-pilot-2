# JR-CBR-003 — Consumer-surface and persistence Jester Report

**Method:** `MADARAII-40 — JESTER_PROVOCATIVE_EXPLORATION`  
**Work:** `WORK-JESTER-0003`  
**Actor:** `JESTER-ACTOR-JST-0003`  
**Engineering Object:** `PRODUCT-CBR-001`  
**Exact Product baseline:** `4ee8583b3feff7775a956c51812232fa0d0516d2`  
**Experiment surface:** `jester/jst-0003`  
**Evidence:** `_mw/evidence/JST-CBR-003.md`  
**Report state:** COMPLETE / RESTORATION PENDING / HANDOFF PENDING

## Attack frame

This pass assumed that the internal bundle might be correct and asked whether consumer-facing projections still preserve the same meaning. The Jester attacked language selection, dimension display/filtering, pivot homogeneity, lineage transparency, CSV schema projection, direct SQLite replacement and CLI reliance semantics.

Eight provocations reached the fixed budget. All retained reproducers passed with the ordinary test suite in final run `34895954949`.

## Material observations

1. **`language="en"` does not make observation dimensions English.** Indicator names change language, while dimension values/filters still use raw Russian `dimensions_json` values despite a persisted English/transliterated dimension-member surface.
2. **The source catalog lacks a bilingual dataset display surface.** `sources()` returns source/revision/acquisition identity but no RU/EN dataset names.
3. **A pivot can present one displayed series across changing units.** Different periods carrying RUB and USD under one concept become one `Debt` column because ambiguity is checked per output cell, not across the semantic homogeneity of the whole displayed series.
4. **Lineage can omit the exact owner discrepancy stored underneath it.** In a deliberately inconsistent persisted bundle, the consumer-facing lineage projection exposes one source ID and does not separately expose concept/raw/disposition source owners.
5. **An empty CSV catalog loses its schema projection.** Empty tables are exported without headers.
6. **Direct SQLite replacement is destructive before success.** `write_sqlite()` unlinks the existing database before constructing the replacement, so a failed direct rewrite removes the prior database state. Higher-level build staging is a separate, stronger boundary.
7. **Repeated same-key CLI dimension filters silently keep only the final value.** The CLI loses multi-value intent available in the underlying query API.
8. **Embedded failed validation is informational rather than a query gate.** A database whose validation metadata says `failed` remains queryable and pivotable through `UnifiedDatabase`.

The common pattern is now consumer-side: **a projection may be internally consistent as a DataFrame/CSV/SQLite view while dropping a distinction that matters to how the user is allowed to interpret or filter it**. The Product is much stronger at preserving source evidence than at guaranteeing every convenience surface carries every semantic guardrail forward.

## Limits

Several observations exercise lower-level reusable operations directly rather than the normal full-build path. In particular, normal build staging materially mitigates direct SQLite replacement loss, and the accepted full build is validated before its normal persisted/query use. These boundaries reduce claim scope but do not erase the observed interface contracts.

No observation establishes a wrong result in the verified 41-source baseline, nor does the Report decide which low-level functions are public support commitments. Those are downstream owner questions.

## Continuation

The experiment branch must be restored to exact Product baseline before interpretation. After restoration, `ADI-JR-CBR-003` under MADARAII-03 must separate the session into bounded semantic acts; `WSR-JR-CBR-003` under MADARAII-04 must determine justified terminal, deferred or Work-candidate postures. This Report creates no Product change or successor Authority.
