# RES-VERIFICATION-CBR-001 — Implementation Verification

**Work kind:** `IMPLEMENTATION_VERIFICATION` (`MADARAII-32`)  
**Subject:** product-code candidate `4ee8583b3feff7775a956c51812232fa0d0516d2`  
**Plan:** `PLAN-CBR-001`  
**Target baseline:** `TW-CBR-1` / `TH-CBR-1` / `PRODUCT-ARCH-CBR-001`  
**Governing MADARAII:** `7d5ef3d92c4e0982061d422208fdf913c55cc604`  
**Evidence:** `VERIFY-CBR-001` at `_mw/evidence/VERIFY-CBR-001.md`  
**Verification run:** GitHub Actions `34544307123`  
**Status:** verification complete; Product admission remains separate.

## Bound configuration and method

The candidate was frozen before the decisive run. `main` resolved to the same exact SHA at verification completion. Tests ran on GitHub-hosted Ubuntu 24.04 with CPython 3.12.14.

Evidence strategy combined:

- unit/contract tests;
- complete live acquisition and build of all 41 registry sources;
- complete local replay from the downloaded source bundle;
- deterministic build/table identity checks;
- semantic validation with zero numeric residue and conflict gates;
- explicit bilingual completeness gate;
- CSV/SQLite reconciliation;
- query/CLI smoke checks;
- separate OOXML preservation verifier that does not use the Product raw extractor.

The preservation challenge has bounded implementation independence: its extractor and comparison path are separate from `cbr_unified.raw`, but it runs in the same repository, workflow and execution environment. No claim of third-party assurance is made.

## Core observations

The decisive run produced `build_id=bld_204724c672460b3deaa50675` for 41/41 sources, 1,257,254 raw cells and 1,209,622 semantic observations. All raw cells had dispositions; unmapped numeric count was zero. Live and local replay had the same build ID, source revisions, row counts and deterministic CSV hashes.

The independent OOXML verifier extracted exactly 1,257,254 raw cells and checked all 1,209,622 observation values. Locator coverage, raw-field equality and observation/source-value equality were each 1.0.

Bilingual validation covered 41/41 datasets, 2,970/2,970 source concepts and 208/208 dimension members. All concepts are currently marked `project_translation`; dimension members comprise 107 `project_translation` and 101 transparent `transliteration_only` records. This satisfies availability/provenance of RU/EN display surfaces; it does not convert project translations into official CBR terminology.

## Claim dispositions

| Claim | Conclusion | Evidence / bound meaning |
| --- | --- | --- |
| TW-01 complete acquisition | `CONFORMS` | 41/41 live sources; acquisition failure gates complete build. |
| TW-02 local-source path | `CONFORMS` | local replay from live source bytes; same build ID, revisions, counts and deterministic tables. |
| TW-03 lossless numeric preservation | `CONFORMS` | independent OOXML equality for 1,257,254 raw cells and 1,209,622 observations. |
| TW-04 semantic dispositions | `CONFORMS` | every raw cell dispositioned; zero unmapped numeric cells. |
| TW-05 statistical meaning preservation | `CONFORMS` for the bound 41-source revisions | source-local concepts plus period/unit/open dimensions; repairs preserved acquired-claims, overdue and valuation/calendar distinctions. Universal future layouts remain outside the claim. |
| TW-06 no false unification | `CONFORMS` | source-local identity; punctuation retained; no fuzzy canonical merge; collision regression evidence. |
| TW-07 revision/conflict visibility | `CONFORMS` | source revision hashes/build identity retained; conflicting semantic duplicate gate; query ambiguity fails closed. |
| TW-08 presentation robustness | `CONFORMS` for recognized/current variants | bounded presentation adapters plus actual fail-closed historical runs; unknown material variants retain evidence and block promotion. |
| TW-09 bilingual semantics | `CONFORMS` | explicit completeness gate: 41 datasets, 2,970 concepts, 208 members; translation status required. |
| TW-10 readable naming | `CONFORMS` with documented translation-quality limitation | source labels retained; working names are presentation only; remaining project translations/transliterations are explicitly typed. |
| TW-11 query and 2D views | `CONFORMS` | catalog/filter/pivot API; ambiguous pivot raises error; no default aggregation. |
| TW-12 export | `CONFORMS` | complete CSV bundle plus prepared-query/pivot CSV export and provenance fields. |
| TW-13 reusable operations | `CONFORMS` | package modules/API expose build, acquisition, raw/semantic/validation/query/pivot operations; notebook is a caller. |
| TW-14 runtime | `CONFORMS` to tested Python/runtime envelope | installable package, Python >=3.10 declared, Python 3.12 CI proven; no private service/API key required. |
| TW-15 reproducible evidence | `CONFORMS` | source manifest/build manifest/validation outputs plus deterministic build ID and verification reports. |

## HOW / architecture disposition

Implementation mechanics conform to the accepted architecture boundaries and Plan. One naming inconsistency exists in `TH-CBR-1` H-11: the target text calls the concept catalog `concepts.csv`, while the implemented semantic entity is `SourceConcept` and the deterministic output is `source_concepts.csv`.

**Conclusion for that exact H-11 filename:** `STALE_DESIGN_OR_PLAN`.

This is a naming-only owner defect. The semantic catalog itself exists, is fully verified, is reconciled with SQLite, and is the file used by README/schema/query surfaces. The Product must not be changed merely to imitate the stale filename. Route: reconcile Target HOW nomenclature to `source_concepts.csv`, then perform bounded revalidation of that criterion against this unchanged candidate and existing deterministic-hash evidence.

## Expected-to-actual delta and protected non-goals

Material implementation repairs discovered during verification were limited to demonstrated source-presentation/semantic distinctions: exchange quarterly headings, acquired-claims treatment, abbreviated overdue labeling and a footnoted debt-securities date header. Strict gates were retained.

Protected non-goals remain preserved: no new economic indicator calculation, no fuzzy cross-source equivalence, no universal future-layout claim, no server deployment, and no mutation of external CBR sources.

## Effects, recovery and limitations

Effects were repository writes, read-only CBR downloads, GitHub Actions compute and verification-artifact storage. Release, deployment, operating-state and business-outcome validation are outside this verification and remain unclaimed.

The exact candidate and evidence are reproducible from the SHA, deterministic build contract and run/evidence locators. A Product-code change, source-revision change, registry change, parser/spec change, materially changed translation policy or target-semantic change reopens affected verification.

## Verification conclusion

**Product behavior and all `TW-CBR-1` obligations: `CONFORMS` within the stated 41-source/runtime envelope.**  
**Exact TH-CBR-1 filename `concepts.csv`: `STALE_DESIGN_OR_PLAN`; bounded owner reconciliation required before admission.**

No implementation defect remains established by this verification. Product admission is not performed here.