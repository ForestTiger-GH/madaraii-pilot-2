# JST-CBR-003 — Consumer-surface and persistence Jester evidence

**Owner:** `JST-CBR-003`  
**Work:** `WORK-JESTER-0003`  
**Method:** `MADARAII-40`  
**Product baseline:** `4ee8583b3feff7775a956c51812232fa0d0516d2`  
**Experimental branch:** `jester/jst-0003`  
**Governing MADARAII:** `ForestTiger-GH/MADARAII@721a199352b5c5282b1478cd6a5eb36a9872fb34`  
**Evidence state:** CAPTURED; restoration pending at initial write

## Control shell and run trace

All executable provocations used synthetic bundles and temporary local SQLite/CSV files on a branch derived from the exact admitted Product revision. Canonical Product code was outside the experiment surface.

| Wave | Commit | CI run | Result |
|---|---|---:|---|
| Harness | `d2d0b12c46b279d9595f8bada6ea4310a7b7a3ef` | `34895819236` | PASS |
| Consumer wave | `47cd99a650906ba42dfe27671571d65e41893f49` | `34895874162` | PASS |
| Interface-reliance wave | `de8e044969e0848e0797526e4a0a51ba9cab6ed8` | `34895954949` | PASS |

The branch-only workflow had `contents: read`; it installed declared test dependencies and ran `pytest -q`. No live CBR acquisition, release, deployment, external write, protected data or secret-bearing operation was used.

## Provocation ledger

### JST3-P01 — «English with a Russian passport»

**Tried:** persist a region member with `name_en=Moskva`, then query the same observation with `language="en"`.

**Observed:** indicator display becomes `Debt`, while `dim_region` remains raw `Москва`. Filtering the English query by `region=Moskva` returns no row; filtering by `region=Москва` succeeds. The dimension-member English surface exists in persistence but is not applied to observation dimensions or filters.

### JST3-P02 — «Dataset catalog that refuses to speak any language»

**Tried:** ask `UnifiedDatabase.sources()` for the user-visible dataset/source catalog.

**Observed:** the returned frame exposes source IDs/revisions/URLs and acquisition metadata but no `name_ru` or `name_en` fields and has no language selector.

### JST3-P03 — «One indicator, two currencies, perfectly respectable pivot»

**Tried:** give one concept two periods, with `RUB` in one period and `USD` in another, then use default pivot.

**Observed:** observations expose both units, but default pivot succeeds as one `Debt` column across the two periods. Duplicate-cell protection does not enforce unit/scale homogeneity across different output cells of one displayed series.

### JST3-P04 — «Lineage witness with selective amnesia»

**Tried:** persist an observation whose observation, concept, raw-cell and disposition `source_id` owners disagree, then ask `lineage()` to explain it.

**Observed:** lineage reports the observation-level `source_id` plus concept names/raw value/disposition role, but provides no separately named concept/raw/disposition source-owner IDs. The consumer cannot see the stored owner mismatch through this lineage projection.

### JST3-P05 — «Empty catalog, empty constitution»

**Tried:** export a valid bundle with zero dimension members.

**Observed:** `dimension_members.csv` is emitted as an empty UTF-8-SIG file with no header row. Therefore an empty exported catalog carries no self-describing column schema.

### JST3-P06 — «Replace the database; optimism first, transaction second»

**Tried:** create a valid SQLite database, then call `write_sqlite()` again at the same path with a replacement that fails on a foreign-key violation.

**Observed:** the previous database is unlinked before replacement construction. After the failed call, the previous one-row Product is gone and the newly created database has zero observations. This behavior belongs to the direct persistence operation; the higher-level build staging path was not the Subject of this provocation.

### JST3-P07 — «Repeatable CLI filter that remembers only the last lover»

**Tried:** pass `--dim region=Москва --dim region=Санкт-Петербург` through the CLI parser helper.

**Observed:** `_dims()` returns only `{"region": "Санкт-Петербург"}`. Repetition for the same dimension silently overwrites the earlier value even though the underlying query API can accept multiple wanted values for a dimension.

### JST3-P08 — «Validation says FAILED; query says come right in»

**Tried:** create a database with embedded validation metadata `status="failed"`, then use `UnifiedDatabase`.

**Observed:** `validation()` faithfully returns `failed`, while `observations()` and default `pivot()` still serve the persisted data without a reliance gate.

## Session boundary

All eight authorized materially different provocations executed and the fixed session budget was reached. The final wave still produced distinct consumer-reliance behavior, so stop was budget-driven rather than caused by three consecutive low-signal attempts.

These are factual session observations only. No item is thereby a Product defect, security finding, requirement, priority or repair mandate. Applicability to the supported build/query contract and current verified 41-source Product belongs to mandatory downstream reconciliation.
