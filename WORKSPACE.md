# MADAR Workspace — madaraii-pilot-2

## Cold entry

This repository is the sole project workspace for the commissioned CBR unified-statistics product.

- **Engineering Subject:** a reproducible Python product that acquires the permitted registry-defined Bank of Russia Excel universe, preserves source numerical values/provenance, performs source-safe semantic interpretation without false unification, exposes bilingual catalog/query/pivot/export operations, and runs in Colab/Jupyter-class Python environments.
- **Project boundary:** `ForestTiger-GH/madaraii-pilot-2` plus read-only governing MADARAII and the single permitted input `ForestTiger-GH/stratbox/src/stratbox/macrobanks/cbr_file_collector/registry.py@b7af2c380a028984ec4b465250ac44a0f05efab6`.
- **Original development governing baseline:** `ForestTiger-GH/MADARAII@7d5ef3d92c4e0982061d422208fdf913c55cc604`.
- **Post-closure Jester contour governing baseline:** `ForestTiger-GH/MADARAII@721a199352b5c5282b1478cd6a5eb36a9872fb34` for `WORK-JESTER-0001` and its mandatory continuation only.
- **Explicit exclusions:** all other `stratbox` content; MADAR, Compass, other repositories/workspaces and their accumulated solutions/knowledge.
- **Commission outcome:** the bounded repository Product contour remains complete and closed through `CLOSURE-CBR-001: PASS`; a later post-closure Jester contour is also closed after restoration and mandatory reconciliation.

## Current owners and exact routes

| Semantic role | Stable identity | Current locator / state |
| --- | --- | --- |
| Work Architecture | `WA-CBR-001` | `_mw/work/WORK-ARCHITECTURE.md` |
| Original Work contour / Work State | `WORK-CBR-001` | `_mw/work/WORK-0001.md`; **closed** |
| Raw human inbox carrier | `INBOX-CBR-001` | `_mw/inbox/INBOX-0001.md`; immutable provenance carrier |
| Developed actor input | `RES-ACTOR-001` | `_mw/results/RES-0001-actor-input.md` |
| Research corpus/source universe | `RC-CBR-001` | `_mw/research/CORPUS.md`; 41/41 sources and 162 sheets accounted |
| Current Scientific Knowledge | `KNOWLEDGE-CBR-001` | `_mw/knowledge/KNOWLEDGE-CBR.md` |
| Target WHAT | `TARGET-WHAT-CBR-001` / `TW-CBR-1` | `_mw/knowledge/TARGET-WHAT.md` |
| Target HOW | `TARGET-HOW-CBR-001` / `TH-CBR-1.1` | `_mw/knowledge/TARGET-HOW.md` |
| Product Architecture | `PRODUCT-ARCH-CBR-001` | `_mw/knowledge/PRODUCT-ARCHITECTURE.md` |
| Implementation Result | `RES-IMPLEMENTATION-CBR-001` | `_mw/results/RES-0003-implementation.md` |
| Verification Result | `RES-VERIFICATION-CBR-001` + bounded `001B` | `_mw/results/RES-0004-verification.md`; `_mw/results/RES-0004b-how-revalidation.md` |
| Verification evidence | `VERIFY-CBR-001` | `_mw/evidence/VERIFY-CBR-001.md`; run `34544307123`, artifact `10178658180` |
| Current Product | `PRODUCT-CBR-001` | admitted product-code/configuration revision `4ee8583b3feff7775a956c51812232fa0d0516d2`; integration record `_mw/results/RES-0005-integration.md` |
| Development closure | `CLOSURE-CBR-001` | `_mw/results/RES-0006-closure-audit.md`; **PASS** |
| Post-closure Jester Work | `WORK-JESTER-0001` | `_mw/work/WORK-JESTER-0001.md`; **closed** |
| Jester session Result | `JR-CBR-001` | `_mw/results/JR-CBR-001.md`; complete/restored/handed off |
| Jester evidence | `JST-CBR-001` | `_mw/evidence/JST-CBR-001.md`; restoration proof `_mw/evidence/JST-CBR-001-RESTORATION.md` |
| Jester developed input | `ADI-JR-CBR-001` | `_mw/results/ADI-JR-CBR-001.md`; complete |
| Jester Work reconciliation | `WSR-JR-CBR-001` | `_mw/results/WSR-JR-CBR-001.md`; complete; post-closure Work candidates recorded, none active |

## Current Product posture

`PRODUCT-CBR-001` remains admitted/current for the commissioned repository scope under `TW-CBR-1` / `TH-CBR-1.1` / `PRODUCT-ARCH-CBR-001`.

Verified build identity: `bld_204724c672460b3deaa50675`.

The post-closure Jester intervention did not mutate canonical Product code. Its derived branch was restored and independently read back at the exact Product SHA `4ee8583b3feff7775a956c51812232fa0d0516d2` before downstream reconciliation.

The admission/closure claim is bounded to the repository Product. No packaged/public release, external deployment, production operation or business-outcome validation is claimed.

## Post-closure residue

`WSR-JR-CBR-001` records justified Work **candidates**, not commissioned Work. Highest-materiality candidates are:

- parser robustness under plausible source drift where a note/helper numeric can receive an observation role while numeric-disposition checks remain green;
- durability semantics of `source_concept_id` across harmless row/presentation movement.

Additional bounded candidates cover semantic validation/persistence coherence, build-identity scope and custom SourceSpec binding. Promotion interruption resilience is deferred. The documented exact-vs-convenience numeric projection is terminal no-action for the current scope.

No candidate is ACTIVE, ASSIGNED or Product-changing. A future successor requires proper Commission/Authority and must start from `WSR-JR-CBR-001`, not from the historical experimental branch.

## Resolution policy

1. Resolve material by semantic role/stable identity from this file, then follow the exact current locator.
2. The Product owner is the exact admitted product-code revision above; later `_mw` closure/Jester/evidence commits do not silently change that Product payload.
3. Filenames, search rank, directory proximity, branch labels, dashboards or chat memory are discovery aids only.
4. An absent, duplicated, stale, inaccessible or conflicting locator is a binding defect; reconcile the affected owner before consequential reliance.
5. Generated CSV/SQLite/build outputs and CI reports remain projections/evidence unless an owner explicitly admits them.
6. Historical Jester experiment commits are evidence locators only; `jester/jst-0001` currently resolves to the restored Product baseline and is not a candidate Product tree.

## Authority and effect boundaries

- Bank of Russia sources and external methodology are read-only evidence/source inputs.
- MADARAII and the permitted stratbox registry are read-only governing/input repositories.
- Research, Knowledge, WHAT/HOW, Product, verification, admission, release/deployment and outcome validation remain distinct states.
- Unknown or ambiguous source semantics fail closed rather than being silently merged.
- Jester-derived surprise alone creates no defect, Task, repair or Product transition.

## Recovery and use route

For Product use/reliance:

1. resolve `PRODUCT-CBR-001` to product revision `4ee8583b3feff7775a956c51812232fa0d0516d2`;
2. use `README.md` / `docs/` / `examples/` for operating guidance;
3. resolve `VERIFY-CBR-001` when assurance or exact baseline evidence is required;
4. resolve `TW-CBR-1` / `TH-CBR-1.1` for target/mechanism semantics.

For scientific/semantic challenge, resolve `KNOWLEDGE-CBR-001` → `RC-CBR-001` → topic/evidence routes.

For post-closure Jester findings, resolve in order:

`WORK-JESTER-0001 → JR-CBR-001 / JST-CBR-001 → ADI-JR-CBR-001 → WSR-JR-CBR-001`.

Both `WORK-CBR-001` and `WORK-JESTER-0001` are closed. There is no scheduled or active successor Work.

## Reopen triggers

Open new scoped Work only after a material change to the Commission, permitted registry/source set or source revision/semantics, governing MADARAII revision, accepted Target WHAT/HOW, Product code/schema/build contract, translation policy, runtime requirements or verification claims, or an explicit Commission selecting one of the reconciled post-closure Work candidates. A future CBR source revision is a new delta and does not retroactively invalidate this closed baseline.
