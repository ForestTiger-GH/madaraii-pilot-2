# WA-CBR-001 — Engineering Work Architecture

**Status:** current; reconciled after `CLOSURE-CBR-002: PASS`  
**Original bootstrap Baseline:** explicit empty repository before commit `260ab2fe3fdcbe89adc5e1a114f67882aa6ac3ed`  
**Original governing basis:** `ForestTiger-GH/MADARAII@7d5ef3d92c4e0982061d422208fdf913c55cc604`  
**Post-Jester governing basis:** `ForestTiger-GH/MADARAII@721a199352b5c5282b1478cd6a5eb36a9872fb34`

## Purpose and boundary

Organize durable development of the CBR unified-statistics software Product inside this repository. The architecture preserves semantic ownership across source evidence, Scientific Knowledge, target semantics, implementation, verification, Product admission and closure.

The project boundary remains exactly the one declared in `WORKSPACE.md`. Other repositories and accumulated project knowledge are excluded except read-only governing MADARAII and the single permitted stratbox registry input.

## Current semantic owners

- **Original Work State:** `WORK-CBR-001` — closed historical contour.
- **Post-Jester Work State:** `WORK-CBR-002` — **closed**, `CLOSURE-CBR-002: PASS`.
- **Raw input:** `INBOX-CBR-001` — immutable provenance carrier.
- **Developed input:** `RES-ACTOR-001` — normalized original semantic acts/routes.
- **Jester challenge history:** `WORK/JR/JST/ADI/WSR-CBR-001..004` — closed challenge/continuation lineage, historical evidence rather than Product truth.
- **Current Scientific Knowledge:** `KNOWLEDGE-CBR-001`.
- **Target WHAT:** `TARGET-WHAT-CBR-001` / `TW-CBR-1`.
- **Target HOW:** `TARGET-HOW-CBR-001` / `TH-CBR-1.2`.
- **Product Architecture:** `PRODUCT-ARCH-CBR-001`.
- **Current Product:** `PRODUCT-CBR-002@e6411bf3680b53e250d5499465d8e91feb10e1c5`.
- **Current Verification:** `RES-VERIFICATION-CBR-002` / `VERIFY-CBR-002`.
- **Current integration:** `RES-INTEGRATION-CBR-002`.
- **Current closure:** `CLOSURE-CBR-002` at `_mw/results/RES-0012-closure-audit-pass.md`; historical first audit `CLOSURE-AUDIT-CBR-002A: FAIL` is retained.
- **Historical predecessor closure:** `CLOSURE-CBR-001: PASS`.

## Work geometry

1. **Intake and Work binding.** Preserve human/Jester carriers and develop their semantic acts before consequential Work.
2. **Evidence and Research.** Resolve the exact registry source universe, source revisions and materially distinct statistical/source concerns. Research evidence remains distinct from Product commitment.
3. **Knowledge and target semantics.** Maintain Scientific Knowledge, Target WHAT and Target HOW as separate owners; implementation discoveries reconcile only affected owners.
4. **Realization.** Implement source acquisition, raw preservation, semantic interpretation, catalogs, validation, persistence and consumer surfaces only within accepted targets.
5. **Assurance.** Verify exact candidates against exact targets and source/runtime Baselines. Jester results may supply challenge directions but never assurance by themselves.
6. **Integration.** Admit only adequately verified Product configuration through explicit owner transition; preserve historical Products and candidate dispositions.
7. **Closure.** Audit Product, Knowledge, Work State, evidence, effects, Jester continuation and residue from durable owners. Closure audit judges and routes; it does not repair. A failed audit is preserved and followed by separate repair/re-audit.

Dependencies follow semantic prerequisites. Independent source-family work may fan out; Product admission serializes at the Product owner.

## Product responsibility boundaries

| Unit | Primary responsibility |
|---|---|
| Registry/specification | stable source IDs/URLs, source profiles, bilingual dataset metadata |
| Acquisition | trusted internet/local binding, source hashes/revisions and diagnostic manifest |
| OOXML raw extraction | lossless cell ledger and exact provenance |
| Period/structural interpretation | recognized calendar/table geometry |
| Semantic adapters | source-local concepts, dimensions and observation admission |
| Catalog/translation | stable IDs and RU/EN presentation surfaces |
| Validation/evidence | preservation, ownership, completeness and semantic-conflict gates |
| Persistence | deterministic CSV + SQLite projections with recoverable writes |
| Query/view | discovery, filtering, lineage and non-aggregating pivot |
| Orchestrator | build transaction, staging/promotion and reusable API coordination |

Raw evidence and semantic interpretation remain separate owners. Query/display layers cannot redefine semantic identity. Generated storage is reconstructable projection, not independent truth.

## Authority boundaries

The user Commission authorizes repository mutation inside this project boundary. Research, Jester output and agent design remain candidates until the appropriate owner transition. Verification establishes reliance evidence and cannot admit a Product. Product admission occurs only through governed integration. Repository merge, closure, release, deployment, operation and business validation remain distinct effects/states.

## Continuity and recovery

A cold actor starts from `WORKSPACE.md`, resolves the current Work/Product/Knowledge/verification/closure owners, and rebinds exact revisions before consequential reliance. Chat/model memory is discovery-only.

Current Product recovery anchors:

- prior: `PRODUCT-CBR-001@4ee8583b3feff7775a956c51812232fa0d0516d2`;
- current: `PRODUCT-CBR-002@e6411bf3680b53e250d5499465d8e91feb10e1c5`;
- authoritative integrated state: `main@24eabda17b14295ef062425593f68585c0b879c0`;
- build: `bld_f07e63fc4029cdcb3dd0df38`;
- decisive Product evidence: `VERIFY-CBR-002`, run `34909613235`, artifact `10373729077`;
- post-integration confirmation: run `34911192167`, artifact `10374981872`;
- closure: `CLOSURE-CBR-002: PASS`.

## Physical realization contract

- `WORKSPACE.md` — pointer-first front door;
- `_mw/inbox/` — preserved human carriers;
- `_mw/work/` — durable Work State, Plans and this architecture;
- `_mw/results/` — developed inputs, implementation/verification/integration/closure Results;
- `_mw/research/` — research history/evidence;
- `_mw/knowledge/` — maintained Knowledge and target owners;
- `_mw/evidence/` — durable verification evidence summaries;
- `src/`, `tests/`, `notebooks/`, `README.md`, `docs/` — Product implementation and user/engineering surfaces;
- `.github/workflows/` — internet-enabled verification where justified.

Stable identities live in artifact payloads/front-door mappings rather than filenames. Large generated builds and CBR workbooks remain rebuildable external evidence unless specific retention is justified.

## Current terminal posture and re-evaluation

`WORK-CBR-002` completed implementation, exact verification, Product integration, authoritative-main propagation, post-integration verification and closure. The first closure audit failed on state/currentness defects; those defects were repaired outside the audit and the new exact Baseline passed re-audit.

There is no active successor Work under the current Commission.

Reassess this architecture only after a material source-universe, repository-boundary, Authority, multi-actor geometry, retention or Product-lifecycle change. Ordinary source-profile evolution proceeds within the existing boundaries when Target WHAT remains unchanged.