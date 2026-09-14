# WORK-JESTER-0001 — Post-closure Product provocation

**Work kind:** `JESTER_PROVOCATIVE_EXPLORATION` (`MADARAII-40`)  
**Commission:** user instruction of 2026-09-14 to continue MADARAII work in `madaraii-pilot-2`, enter as Jester, and continue while material significance remains.  
**Governing instruction baseline:** `ForestTiger-GH/MADARAII@721a199352b5c5282b1478cd6a5eb36a9872fb34` (`dev` at Commission binding).  
**Status:** ACTIVE  
**Sole executing actor:** `JESTER-ACTOR-JST-0001`

## Subject and baseline

- **Engineering Object:** `PRODUCT-CBR-001`, CBR Unified Statistics.
- **Exact Product baseline:** admitted product-code/configuration revision `4ee8583b3feff7775a956c51812232fa0d0516d2`.
- **Prior contour:** `WORK-CBR-001` remains closed under `CLOSURE-CBR-001: PASS`; this Jester Work is a new post-closure bounded contour and does not rewrite that closure.
- **Primary attack sector:** Product semantics and executable behavior in `src/cbr_unified/`, with tests and package surface used only as experiment instruments.

## Purpose and materiality

Provoke the finished Product with deliberately disrespectful simplifications, premise inversions, wrong-role substitutions, pathological ordering and absurd-but-plausible analyst behavior. A result is material when it exposes a hidden assumption, surprising coupling, semantic blind spot, misleadingly safe-looking behavior, or a genuinely useful alternate capability that ordinary conformance review is unlikely to surface.

Stop after three consecutive materially different provocations add no new engineering signal, or when the control shell, budget, or recovery contract would need widening.

## Mode and experiment surface

**Mode:** `INTERVENTION` on a derived Git branch only.

- **Derived surface:** `refs/heads/jester/jst-0001`, created from exact Product baseline `4ee8583b...`.
- The branch is explicitly experimental, non-current-for-reliance and outside Product admission.
- Authoritative `main`, Product owner state, Knowledge owners and prior closure artifacts are outside the mutation surface.
- Allowed mutation: source code, tests and experiment-only CI configuration on the derived branch.
- Allowed external effect: bounded GitHub-hosted CI for package installation and `pytest` only; no release, deployment, publication workflow, Bank of Russia live acquisition, credentials, secrets, customer data or other external system mutation.
- Prohibited: changes to `main` Product code, releases/tags, deployment, source-system writes, destructive Git history on admitted owners, or any effect that cannot be reconciled by discarding/restoring the derived branch.

## Recovery and evidence

- **Recovery target:** force-reset `refs/heads/jester/jst-0001` to `4ee8583b...` after evidence capture.
- Baseline recoverability is inherent in the separately admitted immutable commit and will be verified by branch SHA equality after reset.
- Material diffs, CI outcomes and reproducers must be copied into the standalone Jester Report before reset; the branch is disposable evidence, not a retained Product path.
- Abort on any write outside the branch, unexpected workflow scope, secret access, deployment/release path, inability to identify exact branch head, or uncertainty about restoration.

## Crazy-Idea Generator contract

Every selection must collide at least three of: ridiculous analyst role, sacred Product premise, operation from the wrong layer, grotesque simplification, pathological dataset/ordering/scale/timing, or humiliating metaphor. Ordinary regression tests are rejected unless deformed into a materially different attack frame.

## Budget

Initial budget: up to 12 materially different provocations in one adaptive trajectory, with early stop under the diminishing-significance rule above.

## Report and continuation

- **Jester Report owner:** `JR-CBR-001`, route `_mw/results/JR-CBR-001.md`.
- **Retained evidence owner:** `_mw/evidence/JST-CBR-001.md` plus exact CI/commit references captured in the Report.
- **Mandatory continuation owner:** `ADI-JR-CBR-001`, separately authorized by the same user Commission to perform `ACTOR_INPUT_DEVELOPMENT` (`MADARAII-03`) after restoration.
- **Subsequent reconciliation owner:** `WSR-JR-CBR-001`, separately authorized by the same Commission to perform `WORK_STATE_RECONCILIATION_AND_ROUTING` (`MADARAII-04`) on the developed acts.
- Jester creates no defect, Task, Topic, repair, Product change or priority. `ADI-JR-CBR-001` and `WSR-JR-CBR-001` own downstream semantic interpretation and routing.
