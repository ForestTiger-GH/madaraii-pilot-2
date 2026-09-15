# MADAR Workspace — madaraii-pilot-2

## Cold entry

This repository is the sole project workspace for the commissioned CBR unified-statistics Product.

- **Engineering Subject:** a reproducible Python Product that acquires the permitted registry-defined Bank of Russia Excel universe, preserves source numerical values/provenance, performs source-safe semantic interpretation without false unification, exposes bilingual catalog/query/pivot/export operations, and runs in Colab/Jupyter-class Python environments.
- **Project boundary:** `ForestTiger-GH/madaraii-pilot-2` plus read-only governing MADARAII and the single permitted registry input `ForestTiger-GH/stratbox/src/stratbox/macrobanks/cbr_file_collector/registry.py@b7af2c380a028984ec4b465250ac44a0f05efab6`.
- **Original development governing baseline:** `ForestTiger-GH/MADARAII@7d5ef3d92c4e0982061d422208fdf913c55cc604`.
- **Post-Jester/integration governing baseline:** `ForestTiger-GH/MADARAII@721a199352b5c5282b1478cd6a5eb36a9872fb34`.
- **Explicit exclusions:** all other `stratbox` content; MADAR, Compass and other repositories/workspaces.

The original development contour closed as `CLOSURE-CBR-001: PASS`. Four later Jester contours completed exact restoration plus mandatory non-Jester reconciliation. `WORK-CBR-002` then processed their justified candidates through ordinary engineering Work, admitted `PRODUCT-CBR-002`, propagated it to authoritative `main`, and closed as `CLOSURE-CBR-002: PASS` after a failed first closure audit was repaired and re-audited.

## Current owners and exact routes

| Semantic role | Stable identity | Current locator / state |
| --- | --- | --- |
| Work Architecture | `WA-CBR-001` | `_mw/work/WORK-ARCHITECTURE.md`; current |
| Original Work contour | `WORK-CBR-001` | `_mw/work/WORK-0001.md`; **closed** |
| Post-Jester Work contour | `WORK-CBR-002` | `_mw/work/WORK-0002.md`; **closed** |
| Raw human inbox carrier | `INBOX-CBR-001` | `_mw/inbox/INBOX-0001.md`; immutable provenance carrier |
| Developed actor input | `RES-ACTOR-001` | `_mw/results/RES-0001-actor-input.md` |
| Research corpus/source universe | `RC-CBR-001` | `_mw/research/CORPUS.md`; 41-source baseline |
| Current Scientific Knowledge | `KNOWLEDGE-CBR-001` | `_mw/knowledge/KNOWLEDGE-CBR.md` |
| Target WHAT | `TARGET-WHAT-CBR-001` / `TW-CBR-1` | `_mw/knowledge/TARGET-WHAT.md`; unchanged/current |
| Target HOW | `TARGET-HOW-CBR-001` / `TH-CBR-1.2` | `_mw/knowledge/TARGET-HOW.md`; current |
| Product Architecture | `PRODUCT-ARCH-CBR-001` | `_mw/knowledge/PRODUCT-ARCHITECTURE.md`; current |
| Post-Jester delta | `RES-DELTA-CBR-002` | `_mw/results/RES-0007-post-jester-delta.md` |
| Post-Jester Plan | `PLAN-CBR-002` | `_mw/work/PLAN-0002.md` |
| Implementation Result | `RES-IMPLEMENTATION-CBR-002` | `_mw/results/RES-0008-post-jester-implementation.md` |
| Verification Result | `RES-VERIFICATION-CBR-002` | `_mw/results/RES-0009-post-jester-verification.md` |
| Verification evidence | `VERIFY-CBR-002` | `_mw/evidence/VERIFY-CBR-002.md`; decisive run `34909613235`, artifact `10373729077` |
| Current Product | `PRODUCT-CBR-002` | admitted product-code/configuration revision `e6411bf3680b53e250d5499465d8e91feb10e1c5`; integration `_mw/results/RES-0010-post-jester-integration.md` |
| Current contour closure | `CLOSURE-CBR-002` | `_mw/results/RES-0012-closure-audit-pass.md`; **PASS** |
| Prior failed closure audit | `CLOSURE-AUDIT-CBR-002A` | `_mw/results/RES-0011-closure-audit-fail.md`; historical `FAIL`, repaired/re-audited |
| Historical Product | `PRODUCT-CBR-001` | `4ee8583b3feff7775a956c51812232fa0d0516d2`; superseded history only |
| Historical closure | `CLOSURE-CBR-001` | `_mw/results/RES-0006-closure-audit.md`; **PASS** for prior contour only |
| Jester sessions | `WORK-JESTER-0001..0004` | all **closed**; Reports `JR-CBR-001..004`, evidence `JST-CBR-001..004`, continuations `ADI/WSR-JR-CBR-001..004` |

## Current Product posture

`PRODUCT-CBR-002` is the sole current admitted Product for the repository scope under `TW-CBR-1` / `TH-CBR-1.2` / `PRODUCT-ARCH-CBR-001`.

Verified build identity: `bld_f07e63fc4029cdcb3dd0df38`.  
Verified implementation SHA-256: `f50200dcbda9757bacce0849ab88b84b4a2bab3184e96e5a780a6954a874286c`.

Decisive verification run `34909613235` (#64) passed 54 unit/regression tests, live 41-source build, offline deterministic replay, independent OOXML preservation, post-Jester contract checks and publication-metadata applicability audit.

After repository integration, authoritative `main@24eabda17b14295ef062425593f68585c0b879c0` was independently reconfirmed by run `34911192167` (#70), artifact `10374981872`. It produced the same build identity, implementation fingerprint, source revisions/counts and deterministic table hashes.

Admission and closure are bounded to the repository Product. Public release, external deployment, production operation and business-outcome validation remain separate and unclaimed states.

## Jester disposition

The four Jester sessions remain historical challenge evidence, not Product owners. Their material candidates were developed through `RES-DELTA-CBR-002`, `PLAN-CBR-002`, implementation, exact verification and Product integration.

Current bounded residue:

- exact-vs-convenience numeric projection: terminal no-action for current scope because `value_exact`/Decimal paths retain exact values;
- empty-export schema: low-materiality convenience candidate;
- generic numeric-year header grammar: evidence-only unless current-source applicability emerges;
- publication visibility metadata: present in a bounded source subset, with no current evidence that visibility itself defines statistical/publication semantics; reopen on explicit methodology or changed behavior;
- full system evidence is strongest for Python 3.12.14; broader declared support remains outside exhaustive matrix proof.

No residue above is an active Product defect or an implied successor Commission.

## Closure history

The first successor closure audit, `CLOSURE-AUDIT-CBR-002A`, returned `FAIL` for two state defects: incomplete final implementation-lineage accounting and lack of authoritative `main` propagation. It performed no repair.

The routed repair reconciled `RES-IMPLEMENTATION-CBR-002`, merged the already admitted Product state to `main`, and completed exact post-merge verification. The second MADARAII-36 audit, `CLOSURE-CBR-002`, returned `PASS`. Both audit results remain durable history.

## Resolution policy

1. Resolve material by semantic role/stable identity from this file, then follow the exact owner locator.
2. The Product owner is `PRODUCT-CBR-002@e6411bf3680b53e250d5499465d8e91feb10e1c5`; later `_mw` closure/state commits do not silently change that Product payload.
3. Filenames, search rank, directory proximity, branch labels, dashboards and chat memory are discovery aids only.
4. Generated CSV/SQLite/build outputs and CI reports are evidence/projections unless explicitly admitted by an owner transition.
5. Historical Jester experiment branches and failed implementation candidates remain evidence/history only.
6. `PRODUCT-CBR-001` and `CLOSURE-CBR-001` remain immutable historical baselines and do not describe current Product posture.

## Authority and effect boundaries

- Bank of Russia sources and external methodology are read-only evidence/source inputs.
- MADARAII and the permitted stratbox registry are read-only governing/input repositories.
- Research, Knowledge, WHAT/HOW, Product, verification, admission, closure, release/deployment and outcome validation remain distinct states.
- Unknown or ambiguous source semantics fail closed where governed by the current Product contract.
- Product admission/closure does not imply public release, deployment or external activation.

## Recovery and use route

For Product use/reliance:

1. resolve `PRODUCT-CBR-002` to `e6411bf3680b53e250d5499465d8e91feb10e1c5`;
2. use `README.md` / `docs/` / `examples/` for operating guidance;
3. resolve `VERIFY-CBR-002` and `RES-VERIFICATION-CBR-002` for Product assurance;
4. resolve `CLOSURE-CBR-002` for terminal contour state and post-integration confirmation;
5. resolve `TW-CBR-1` / `TH-CBR-1.2` for target/mechanism semantics.

For scientific challenge, resolve `KNOWLEDGE-CBR-001` → `RC-CBR-001` → topic/evidence routes.

For a historical Jester session, resolve:

`WORK-JESTER-000N → JR-CBR-00N / JST-CBR-00N / restoration evidence → ADI-JR-CBR-00N → WSR-JR-CBR-00N`.

## Current terminal posture and reopen triggers

`WORK-CBR-001`, `WORK-CBR-002` and all four Jester Works are **closed**. There is no active or scheduled successor Work under the current Commission.

Open new scoped Work after a material registry/source revision, source-semantic change, governing-contract change, Target WHAT/HOW change, Product code/schema/build-contract mutation, translation-policy change, runtime constraint change, invalidated verification evidence, or new explicit Commission. A future CBR source revision creates a new delta and does not retroactively invalidate either historical closure.