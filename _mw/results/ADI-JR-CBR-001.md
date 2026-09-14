# ADI-JR-CBR-001 — Developed acts from JR-CBR-001

**Work kind:** `ACTOR_INPUT_DEVELOPMENT` (`MADARAII-03`)  
**Source carrier:** `_mw/results/JR-CBR-001.md`  
**Evidence dependency:** `_mw/evidence/JST-CBR-001.md`, `_mw/evidence/JST-CBR-001-RESTORATION.md`  
**Carrier producer:** `JESTER-ACTOR-JST-0001` under `WORK-JESTER-0001`  
**Processing baseline:** admitted `PRODUCT-CBR-001` code/config revision `4ee8583b3feff7775a956c51812232fa0d0516d2`; existing `CLOSURE-CBR-001: PASS`; current owner model from `WA-CBR-001`  
**Governing instruction baseline:** `ForestTiger-GH/MADARAII@721a199352b5c5282b1478cd6a5eb36a9872fb34`  
**Status:** COMPLETE

## Source and status ceiling

`JR-CBR-001` is preserved as the standalone Jester session owner. Its executable observations are supported by disposable reproducers and successful branch-isolated CI, followed by verified restoration to the exact Product baseline.

The carrier can establish **what happened in the bounded experiments**. It cannot by itself establish that a Product defect exists in the admitted real-source state, that the prior closure is invalid, that a repair is required, or what priority any successor Work should receive. Those status ceilings are retained below.

## Developed acts

| Act | Source | Type / normalized meaning | Epistemic and Authority status | Affected owner candidates | Disposition |
|---|---|---|---|---|---|
| `ADI-A01` | JST-P01 | Evidence: default analyst-facing numeric convenience projection can differ from an exact long Decimal while `value_exact` and Decimal mode remain exact. | Reproduced fact for the constructed value; behavior is already explicitly documented. No new exactness requirement is established. | `PRODUCT-CBR-001` query surface; `TARGET-WHAT-CBR-001` only if consumer-exactness semantics are reconsidered. | **retain as evidence**; route to `WSR-JR-CBR-001` for terminal/no-action versus future usability posture. |
| `ADI-A02` | JST-P02, JST-P05 | Concern supported by evidence: validation/persistence owners can admit records whose declared source IDs disagree across observation↔concept and raw↔disposition while revision/ID references remain formally valid. | Reproduced on synthetic bundles and SQLite. This establishes a reachable API/storage state, not occurrence in the accepted 41-source build. | `TARGET-HOW-CBR-001`, `PRODUCT-CBR-001`, `VERIFY-CBR-001`. | **route** to reconciliation as a semantic-integrity qualification candidate. |
| `ADI-A03` | JST-P03, JST-P04, JST-P07 | Concern supported by evidence: the validation boundary accepts some representation/domain variants that are semantically dubious—reordered equivalent dimensions evade conflict grouping, an impossible calendar date passes ISO-shape checking, and several semantic fields accept empty/absurd values. | Reproduced for direct validation inputs. Ordinary parser canonicalization removes the observed JSON-order variant in the current build path; real-source occurrence remains unestablished. | `TARGET-HOW-CBR-001`, `PRODUCT-CBR-001`, `VERIFY-CBR-001`. | **route** as validation-contract qualification candidate; preserve parser-path mitigation explicitly. |
| `ADI-A04` | JST-P06 | Concern supported by evidence: one constructed bundle returns top-level `status=passed` while an exposed invariant is false; SQLite later rejects the specific duplicate-cell condition through a uniqueness boundary. | Reproduced at validation owner; downstream persistence mitigation is established for the tested construction. No accepted-build contradiction is established. | `PRODUCT-CBR-001` validation result semantics; `VERIFY-CBR-001`. | **route** for status/invariant contract review; candidate may terminate if the invariant is diagnostic rather than acceptance-bearing. |
| `ADI-A05` | JST-P11 | Evidence/concern: a real synthetic XLSX row explicitly labelled as a technical source note, with a numeric cell under an already recognized period column, was materialized as an observation and received `observation_value`; the numeric disposition gate still passed. | End-to-end reproduced through real raw extraction and semantic processing. Establishes a parser behavior class under plausible presentation drift; does not establish that a current bound CBR workbook contains such a false observation. | `KNOWLEDGE-CBR-001` for source-drift semantics, `TARGET-HOW-CBR-001`, `PRODUCT-CBR-001`, `VERIFY-CBR-001`. | **route** as current-state/assurance qualification candidate with higher semantic relevance than pure malformed-bundle probes. |
| `ADI-A06` | JST-P12 | Evidence/concern: for ordinary indicator-axis concepts, changing only worksheet row number changes `source_local_key` and `source_concept_id`; maintenance guidance separately says row numbers are not durable business identities and directs consumers to `source_concept_id`. | Directly established from implementation plus current documentation. Whether row-sensitive identity is intentionally revision-local or conflicts with the accepted identity commitment requires owner interpretation. | `TARGET-WHAT-CBR-001`, `TARGET-HOW-CBR-001`, `PRODUCT-CBR-001`, `KNOWLEDGE-CBR-001`. | **route** as an identity-contract reconciliation candidate. |
| `ADI-A07` | JST-P08 | Evidence/concern: `build_id` stays unchanged when executable parser behavior is changed while source specs/revisions and static contract version are held fixed; resolved dependency versions are also outside the direct fingerprint. | Reproduced for `_fingerprints()`. Existing governance separately binds admitted Product reliance to exact code/config revision, which materially limits the claim. | `TARGET-HOW-CBR-001`, `PRODUCT-CBR-001`, `VERIFY-CBR-001`; Product admission/identity contract. | **route** for identity-scope reconciliation; no claim that current admission is untraceable. |
| `ADI-A08` | JST-P09 | Evidence/concern: caller-supplied `SourceSpec` can determine fingerprint identity while `_build_into_staging()` resolves the global registry SourceSpec for semantic parsing of that source ID. | Reproduced by bounded monkeypatch instrumentation of the build path. Relevance depends on whether custom `sources=` is an intended supported build contract rather than internal test/config surface. | `TARGET-HOW-CBR-001`, `PRODUCT-CBR-001`. | **route** for API/contract ownership determination before any repair posture. |
| `ADI-A09` | JST-P10 | Evidence/concern: an injected `KeyboardInterrupt` between the two promotion renames leaves the requested output path absent while the previous Product remains in the sibling backup. | Filesystem-isolated reproducer. Prior output remains recoverable; current maintenance text already describes temporary backup movement and qualified restoration. | `TARGET-HOW-CBR-001` operational contract; `PRODUCT-CBR-001`; maintenance documentation. | **route** for resilience posture; candidate may be accepted residual behavior if interruption recovery expectations are already sufficiently bounded. |

## Recorded recovery act

`ADI-R01` — **Recovery fact.** The Jester experiment branch was force-restored and independently read back at exact SHA `4ee8583b3feff7775a956c51812232fa0d0516d2`. `main` Product code was never part of the mutation surface. This act is **admitted as evidence** for the mandatory continuation prerequisite and routes directly to `WSR-JR-CBR-001`.

## Explicit limits and UNKNOWNs

- No act establishes a regression in the verified 41-source build without separate comparison or verification evidence.
- No act invalidates `CLOSURE-CBR-001` by itself.
- No act establishes Product priority, release urgency or repair design.
- The intended public/support status of direct `validate_bundle`, custom `sources=`, build-id scope, and interruption recovery are owner questions where documentation/implementation intent must be reconciled before status escalation.
- JST-P01 is already materially disclosed by user documentation and therefore carries a low ceiling absent a new requirement.
- JST-P11 and JST-P12 have the strongest direct relation to the declared statistical-semantic and durable-identity commitments because they arise from ordinary parser/identity mechanisms rather than intentionally malformed standalone records.

## Accounting

All twelve material Jester provocations are accounted through `ADI-A01`–`ADI-A09`; restoration is accounted through `ADI-R01`. No Jester observation was converted directly into a defect, Topic, Task, Decision or repair requirement.

**Mandatory handoff:** the complete developed set routes to `WSR-JR-CBR-001` under `MADARAII-04`.
