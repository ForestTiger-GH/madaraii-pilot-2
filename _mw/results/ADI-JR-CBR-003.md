# ADI-JR-CBR-003 — Developed acts from JR-CBR-003

**Work kind:** `ACTOR_INPUT_DEVELOPMENT` (`MADARAII-03`)  
**Source carrier:** `_mw/results/JR-CBR-003.md`  
**Evidence:** `_mw/evidence/JST-CBR-003.md`, `_mw/evidence/JST-CBR-003-RESTORATION.md`  
**Product baseline:** `PRODUCT-CBR-001@4ee8583b3feff7775a956c51812232fa0d0516d2`  
**Governing instruction baseline:** `ForestTiger-GH/MADARAII@721a199352b5c5282b1478cd6a5eb36a9872fb34`  
**Status:** COMPLETE

## Status ceiling

The Jester carrier establishes what exact synthetic consumer/persistence experiments did. It does not establish that every lower-level function is a supported public contract, that any current 41-source result is wrong, or that a Product repair is required.

## Developed acts

| Act | Source | Normalized meaning | Status / limit | Disposition |
|---|---|---|---|---|
| `ADI3-A01` | JST3-P01 | English observation/query mode translates indicator names but leaves dimension display/filter values on raw Russian strings despite persisted English member names. | Reproduced consumer behavior; direct relation to bilingual/query commitments. | **route** as bilingual-dimension projection candidate. |
| `ADI3-A02` | JST3-P02 | `sources()` exposes source/revision identity without RU/EN dataset display names or a language selector. | Reproduced API behavior; whether `sources()` is the intended dataset catalog surface requires owner interpretation. | **route** with A01 as bilingual catalog qualification. |
| `ADI3-A03` | JST3-P03 | Default pivot can present one indicator column whose observations use different units across periods. | Reproduced on a coherent persisted bundle. Current parser may normally keep units stable for many concepts; cross-period homogeneity is not enforced by pivot itself. | **route** as consumer semantic-homogeneity candidate. |
| `ADI3-A04` | JST3-P04 | `lineage()` can hide concept/raw/disposition source-owner disagreement present in persistence because it exposes one observation source ID rather than separate owner IDs. | Reproduced against a deliberately inconsistent bundle; depends on lower-level persistence accepting such state, already evidenced in `JR-CBR-001`. | **route** as consumer amplification of semantic-gate candidate. |
| `ADI3-A05` | JST3-P05 | Empty CSV catalog files contain no header/schema. | Reproduced export behavior; no data loss because table is empty. Consumer portability impact is bounded. | **retain as evidence**; low-materiality export-schema candidate only if self-describing empty catalogs are required. |
| `ADI3-A06` | JST3-P06 | Direct `write_sqlite()` deletes an existing database before replacement succeeds; a failed replacement loses the previous database at that path. | Reproduced direct-operation behavior. Normal higher-level build staging provides a materially stronger recovery boundary. | **route** for supported-operation boundary/resilience qualification; no claim against normal build promotion. |
| `ADI3-A07` | JST3-P07 | Repeating the same CLI `--dim key=value` silently overwrites earlier values even though the Python query API accepts a sequence for one dimension. | Reproduced interface behavior. | **route** as CLI/API semantic-correspondence candidate. |
| `ADI3-A08` | JST3-P08 | `UnifiedDatabase` serves query/pivot data even when embedded validation metadata says `failed`. | Reproduced lower-level consumer behavior. Normal accepted build path validates before ordinary persistence/use; supported reliance semantics of manually supplied DBs remain unresolved. | **route** as query-reliance gate candidate. |

## Recovery

`ADI3-R01` — independent branch resolution after force-reset established `jester/jst-0003` at exact SHA `4ee8583b3feff7775a956c51812232fa0d0516d2`. Canonical Product code remained outside the experiment mutation surface. **Admitted evidence** for continuation readiness.

## Accounting and UNKNOWNs

- All eight provocations plus recovery are accounted.
- A01/A02 directly concern the accepted bilingual user surface and therefore have a higher status ceiling than purely malformed persistence experiments.
- A03 concerns consumer interpretation of a valid DataFrame/pivot even when each individual output cell is unambiguous.
- A04/A08 depend partly on whether lower-level construction of inconsistent/failed databases is inside the supported Product contract.
- A05 is bounded portability residue.
- No act creates a defect, Task, priority, Decision or repair.

**Mandatory handoff:** `WSR-JR-CBR-003` under MADARAII-04.
