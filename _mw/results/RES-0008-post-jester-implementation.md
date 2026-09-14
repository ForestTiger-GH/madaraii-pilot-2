# RES-IMPLEMENTATION-CBR-002 — Post-Jester Product hardening

**Work kind:** `IMPLEMENTATION` (`MADARAII-32`)  
**Work:** `WORK-CBR-002`  
**Plan:** `PLAN-CBR-002`  
**Delta owner:** `RES-DELTA-CBR-002`  
**Target owners:** `TW-CBR-1`, `TH-CBR-1.2`, `PRODUCT-ARCH-CBR-001`  
**Governing MADARAII:** `ForestTiger-GH/MADARAII@721a199352b5c5282b1478cd6a5eb36a9872fb34`  
**Historical current Product at implementation start:** `PRODUCT-CBR-001@4ee8583b3feff7775a956c51812232fa0d0516d2`  
**Initial implementation-complete checkpoint:** `c80d2cf1461c3f43dc9a61c2b7c6f17264144a1b`  
**HOW/docs reconciliation checkpoint:** `99cdda9750d0d582244dad543b028fbf16c99098`  
**Final executable implementation checkpoint:** `904febee0bab5010f799ff5dbedc63de5bd55deb`  
**Final executable SHA-256:** `f50200dcbda9757bacce0849ab88b84b4a2bab3184e96e5a780a6954a874286c`  
**Verified Product candidate:** `e6411bf3680b53e250d5499465d8e91feb10e1c5`  
**Status:** implementation lineage complete and reconciled; later verification/integration are owned by `RES-VERIFICATION-CBR-002` and `RES-INTEGRATION-CBR-002`.

## Readiness path

`MADARAII-31` is conditional. This contour used no standalone Work Plan Readiness Review. `PLAN-CBR-002` itself carried scope boundaries, recovery controls, blocking checks and stop/replan conditions; all repository changes remained reversible on the Work branch. Independent assurance is owned by `MADARAII-33` rather than reconstructed retrospectively.

## Implemented delta disposition

| Delta | Implementation result |
|---|---|
| D01 source-owner coherence | manifest/raw/disposition/concept/observation source and revision ownership is blocking validation |
| D02 semantic-key canonicalization | dimension JSON is parsed and canonically sorted before duplicate/conflict grouping |
| D03 semantic domains | real ISO dates, admitted frequency/period-role domains, non-empty units and positive integer scales are validated |
| D04 lineage cardinality | one raw cell can back at most one observation |
| D05 wrong-role parser | methodology/change-log period rows and source/note metadata numerics are excluded from observations |
| D06 durable concept identity | ordinary concept identity no longer uses physical row number; source-visible semantic ancestry is used where required |
| D07 measure identity | region/activity concepts bind stable measure title + unit/scale rather than collapsing distinct measures |
| D08 context inference | unit precedence, negation and ambiguous maturity handling are conservative and regression-covered |
| D09 numeric lexical boundary | accounting-parenthesis numeric text enters exact numeric completeness |
| D10 bilingual consumer surface | source catalog and reusable dimension values expose RU/EN display/filter surfaces; indicator discovery also uses bilingual dataset/source context without changing concept identity |
| D11 pivot homogeneity | pivot rejects hidden unit/scale/frequency/period-role mixing |
| D12 CLI dimensions | repeated same-key `--dim` values form OR-lists |
| D13 query reliance | `UnifiedDatabase` requires passed embedded validation by default; explicit diagnostic paths may inspect failed validation; CLI `validate` is such a diagnostic surface |
| D14 lineage transparency | observation/concept/raw/disposition source owners are projected separately |
| D15 SourceSpec authority | one exact build SourceSpec map is used by fingerprinting and semantic parsing |
| D16 build identity | build identity binds implementation SHA-256 and resolved Python/requests/openpyxl/pandas versions |
| D17 source trust | live URLs stay inside CBR domain; XLSX files pass structural OOXML/CRC validation; trusted apex alias fallback is bounded |
| D18 publication metadata | applicability audit tooling added; semantic change remains evidence-driven |
| D19 direct SQLite replacement | sibling candidate + integrity check + atomic replace preserves prior DB on failure |

## Corpus-driven semantic repairs

Strict full-corpus validation exposed additional source-visible distinctions while the planned mechanisms were being exercised. Each conflict was repaired by source semantics rather than by relaxing the duplicate gate.

- `mortgage_ihc`: repeated child labels separated by semantic parent ancestry.
- `sme_borrowers_info`: repeated period blocks and vertically merged legal-entity / individual-entrepreneur parents incorporated into source-local context; region/activity row axes remain dimensions.
- `debt_securities`: repeated total/ruble/foreign-currency hierarchy sections separated through stable source-visible section ancestry.
- `debt_new`: `ОФЗ` under foreign-currency versus `в российских рублях` branches separated; Russian-ruble heading grammar corrected.
- `debt_cur-mat_new`: exact `Национальная валюта` heading admitted as ruble scope; broad national-currency matching deliberately avoided.
- `debt_maturity`: identical instruments under `Краткосрочные обязательства` and `Долгосрочные обязательства` retain those exact parent labels in concept ancestry. No unsupported mapping to normalized one-year maturity buckets was introduced.
- structural currency inheritance: inherited branch scope is removed from later unique aggregates where the source does not establish continued scope.
- `exchange_rate`: repeated indicator labels retain explicit source measure definitions such as growth versus previous December, previous period and corresponding prior-year period.

These repairs remain inside `TW-CBR-1`: they preserve distinctions already present in source publications and improve correctness of the common representation.

## Post-checkpoint implementation lineage

The first version of this Result was written after checkpoint `c80d2cf...`. Subsequent verification attempts exposed and then resolved bounded issues before Product admission:

1. `1b7383895bcfb56b3bce5d62c3170999e09935fe` reorganized source-row semantic reconciliation so structural-currency and exchange-measure context discovery is cached at source-row granularity. This changed implementation mechanics while preserving the intended semantic rules.
2. `904febee0bab5010f799ff5dbedc63de5bd55deb` completed the final executable repair: English indicator discovery uses bilingual dataset/source context in addition to concept labels, CLI `validate` can explicitly inspect failed validation, and schema documentation was aligned with actual trust ownership.
3. `64c293fb85320d2950232ef89b9bcd42121febf9` added a focused exchange-rate regression only; `src/cbr_unified` was unchanged.
4. `e6411bf3680b53e250d5499465d8e91feb10e1c5` strengthened verification-artifact retention only; Product implementation was unchanged.

Therefore the admitted candidate `e6411bf...` carries final executable implementation checkpoint `904febee...` with implementation SHA-256 `f50200dcbda9757bacce0849ab88b84b4a2bab3184e96e5a780a6954a874286c`. Runs #62, #63 and decisive exact-state run #64 all exercised that same executable payload.

This reconciliation was required by closure audit `CLOSURE-AUDIT-CBR-002A`, which correctly identified that the earlier Result did not account for the post-`c80d2cf` Product-code changes. The reconciliation changes this Work Result only; it does not mutate the verified Product implementation.

## Verification controls implemented with the Product

The repository verification workflow runs on PRs to `main`, pushes to `main` and manual invocation. It executes:

1. unit/regression suite;
2. complete live 41-source build plus local deterministic replay;
3. independent OOXML preservation comparison;
4. post-Jester Product-contract verification;
5. publication-metadata applicability audit;
6. verification/failure artifact retention, including late consumer/replay evidence.

The post-Jester verifier checks complete validation invariants, build/runtime fingerprint coherence, live source trust, English source catalog, English dimension display/filter symmetry and lineage-owner agreement.

## Target HOW / documentation reconciliation

`TARGET-HOW.md` is reconciled to `TH-CBR-1.2`. README, schema and maintenance guidance describe the implemented source-trust boundary, semantic identity rules, validation ownership, build fingerprint, validated-by-default consumer behavior, pivot safety, atomic persistence and evidence-first publication-metadata policy.

`TW-CBR-1` remains unchanged. No new Product purpose, source universe or fuzzy cross-source canonicalization was introduced.

## Failed candidate lineage

The Work branch/CI history deliberately retains failed full-corpus candidates. Representative strict-gate failures included repeated concepts in mortgage/SME/debt tables and, at later checkpoints, `debt_maturity`, `exchange_rate` and the consumer English-discovery assertion. Those failures are superseded implementation evidence, not accepted Product states. Each material failure produced a source-semantic or consumer-contract correction plus focused regression coverage before another full-corpus run.

## Effects and recovery

Effects are limited to repository mutations, read-only Bank of Russia acquisition, GitHub Actions compute and workflow artifacts. External source publications are untouched.

Recovery remains branch/commit based. Product build attempts preserve the prior promoted output; direct SQLite replacement preserves the prior database on failure; failed acquisition/semantic attempts retain diagnostic staging evidence.

## Implementation conclusion

All planned implementation slices PJ1–PJ7 and all material pre-admission repair iterations are accounted. The final executable state is `904febee...`; later test/workflow/owner commits do not change its implementation fingerprint.

`RES-VERIFICATION-CBR-002` subsequently verified candidate `e6411bf...`, and `RES-INTEGRATION-CBR-002` admitted it as `PRODUCT-CBR-002`. Those later transitions remain separate semantic owners and do not rewrite the implementation facts recorded here.
