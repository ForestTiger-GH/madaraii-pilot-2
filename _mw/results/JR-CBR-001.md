# JR-CBR-001 — Post-closure Jester Report

**Method:** `MADARAII-40 — JESTER_PROVOCATIVE_EXPLORATION`  
**Work:** `WORK-JESTER-0001`  
**Actor:** `JESTER-ACTOR-JST-0001`  
**Engineering Object:** `PRODUCT-CBR-001`  
**Exact Product baseline:** `4ee8583b3feff7775a956c51812232fa0d0516d2`  
**Prior closure:** `CLOSURE-CBR-001: PASS` remains untouched  
**Experiment surface:** `jester/jst-0001`  
**Detailed evidence:** `_mw/evidence/JST-CBR-001.md`  
**Report state at initial write:** EXPERIMENT COMPLETE / RESTORATION PENDING

## 1. What the Jester tried to do

The Jester treated the finished CBR Unified Statistics Product as an overconfident analyst who believes every green validation light, every stable identifier and every convenient DataFrame exactly as presented.

The attack trajectory deliberately targeted premises that ordinary conformance work had good reason to trust:

- exact-number preservation through the analyst-facing query path;
- semantic ownership across source, concept, raw and disposition records;
- the distinction between syntactic validation and statistical meaning;
- `build_id` as an exact-build identity;
- configurable source specifications;
- atomic Product promotion/recovery;
- fail-closed handling of unfamiliar workbook structure;
- durability of source-local concept identities across harmless presentation movement.

The Crazy-Idea Generator used wrong-role substitutions, grotesque-but-valid objects, identity swaps, reordered equivalent representations, interruption timing and deliberately respectable-looking source drift rather than ordinary regression cases.

## 2. What was done

A derived branch was created from the exact admitted Product revision. An experiment-only GitHub Actions workflow ran the ordinary unit suite plus disposable Jester reproducers. The Product on `main` was not modified.

Five expanding test waves completed successfully. The final wave at experimental commit `40fd3479ad0619587da881d29a8e6723d2ee34e7` completed in CI run `34893811182` with **35/35 tests passing**.

Twelve materially distinct provocations were completed. Their exact constructions and evidence are retained in `JST-CBR-001`.

## 3. Surprises observed

The Jester observed the following facts. These are provocations and observations only; this report assigns no defect status, priority, root cause or repair prescription.

1. **Exact data can become inexact at the ordinary convenience surface.** `value_exact` remains exact and Decimal mode preserves it, while the default numeric query/pivot convenience path can represent a sufficiently long decimal differently. The behavior is documented by the Product.

2. **Cross-owner source identity can disagree while validation and persistence remain satisfied.** An observation may reference a concept whose own source ID is different; raw and disposition records can likewise carry different source IDs while pointing at the same admitted source revision.

3. **Equivalent dimension objects with different JSON key ordering can evade semantic-conflict grouping.** The ordinary parser currently emits stable sorted JSON, while the validation owner itself treats raw string representation as part of the grouping key.

4. **ISO-shaped periods can be calendar-impossible and still pass the validation boundary.**

5. **A validation result can report `status=passed` while an exposed invariant is false under a constructed bundle.** A later SQLite uniqueness boundary rejects the specific duplicated-cell construction used in the experiment.

6. **Several semantic fields can carry empty or absurd values without changing validation status.**

7. **The deterministic build identity does not directly bind executable parser code or resolved dependency versions.** Accepted Product governance separately binds reliance to an exact code/configuration revision.

8. **A caller-supplied SourceSpec can influence the fingerprint while parsing resolves the global registry SourceSpec for the same source ID.**

9. **Promotion has an interruption window in which the canonical output path is temporarily absent while the prior Product exists only under the recovery sibling.**

10. **The fail-closed numeric-disposition mechanism can accept a wrong-looking semantic role.** In a real synthetic workbook, a numeric value on a row labelled as a technical source note became an admitted observation and the numeric disposition gate still reported `passed`.

11. **Ordinary indicator concept IDs incorporate worksheet row numbers.** Moving an unchanged indicator by one row changes `source_concept_id`, while Product maintenance guidance separately says row numbers are not durable business identities.

These observations cluster around a broader surprise: the Product is strongest when preserving evidence and rejecting *unexplained* content; several experiments instead attacked *plausibly explained but semantically incoherent* content. That class passes farther because the system already has a role, identity or representation to point to.

## 4. Things that resisted the Jester

The exercise also confirmed useful strength in the Product:

- exact lexical values remain retained even when convenience numeric projection changes representation;
- Decimal mode provides an explicit exact Python surface;
- ordinary parser output canonicalizes dimension JSON;
- SQLite foreign keys and uniqueness rules add an independent persistence boundary beyond validation;
- source revisions are SHA-bound to workbook bytes;
- the build process stages candidates before promotion and retains prior output in a recovery sibling during replacement;
- the existing documentation explicitly separates build success from admitted Product reliance on an exact commit/configuration;
- unknown/unexplained numeric material is handled conservatively by the disposition gate.

The Jester therefore did not establish that the original closure was unsound. It established a set of new inputs that deserve ordinary engineering interpretation after restoration.

## 5. Stop condition

The pre-bound budget of 12 materially different provocations is exhausted. Further candidate ideas either duplicated an existing class or were materially more peripheral. Extending the Jester run would require widening its control shell rather than continuing the authorized trajectory.

## 6. Restoration and handoff

Before non-Jester interpretation, the experimental branch is to be restored to the exact admitted Product baseline `4ee8583b3feff7775a956c51812232fa0d0516d2`. Restoration verification will be appended after the ref has been reset and independently read back.

The report then routes, under the already bound Commission, to:

- `ADI-JR-CBR-001` — `MADARAII-03 ACTOR_INPUT_DEVELOPMENT`;
- `WSR-JR-CBR-001` — `MADARAII-04 WORK_STATE_RECONCILIATION_AND_ROUTING`.

Those owners may interpret, consolidate, reject, defer or route the observations. This Jester Report does not make those decisions.
