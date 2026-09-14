# VERIFY-CBR-002 — Post-Jester Product verification evidence

**Subject:** post-Jester Product candidate `e6411bf3680b53e250d5499465d8e91feb10e1c5`  
**PR verification tree:** generated merge state `0a8051401324a18ff2e11f569d8b5bd00ec27b0a`; comparison to the candidate reports zero changed files  
**Verification run:** GitHub Actions `34909613235` (`Product verification` #64)  
**Artifact:** `10373729077` / `cbr-unified-verification`  
**Artifact digest:** `sha256:fedf459c06b331abfa16e361b69265ad63fa798678ac672a81cec2a3fccfb1db`  
**Governing targets:** `TW-CBR-1`, `TH-CBR-1.2`, `PRODUCT-ARCH-CBR-001`  
**Status:** exact verification evidence captured; Product admission is separate.

## Exact environment and build identity

- Ubuntu 24.04 GitHub-hosted runner;
- Python `3.12.14`;
- requests `2.34.2`;
- openpyxl `3.1.5`;
- pandas `3.0.5`;
- implementation SHA-256 `f50200dcbda9757bacce0849ab88b84b4a2bab3184e96e5a780a6954a874286c`;
- build ID `bld_f07e63fc4029cdcb3dd0df38`.

The current repository head adds regression/evidence-retention material after the last executable repair; the exact `src/cbr_unified` implementation fingerprint above is the Product implementation tested by runs #62, #63 and #64.

## Unit and regression evidence

Run #64 unit job `104193952080` completed successfully with **54 passed**. Coverage includes Jester-derived negative cases and later corpus regressions for semantic identity, exchange-rate measure context, source trust, build identity, consumer reliance, pivot safety, CLI dimensions, persistence atomicity and promotion recovery.

## Complete live build and deterministic replay

Run #64 full-build job `104194061457` completed successfully.

| Measure | Live | Replay |
|---|---:|---:|
| registry sources | 41 | 41 |
| raw cells | 1,257,254 | 1,257,254 |
| observations | 1,209,622 | 1,209,622 |
| source concepts | 3,027 | 3,027 |
| dimension members | 208 | 208 |
| unmapped numeric cells | 0 | 0 |
| semantic duplicate/conflict groups | 0 | 0 |

Live and replay have the same source revisions and the same build ID. Deterministic hashes match exactly for `raw_cells.csv`, `source_concepts.csv`, `dimension_members.csv`, `observations.csv`, `cell_dispositions.csv` and its compatibility alias. CSV and SQLite row counts are identical for every persisted table.

Query smoke evidence: 89,280 `mortgage_debt` rows, 12 English `mortgage` indicator hits, CLI validation passed and CLI query returned data.

## Independent OOXML preservation challenge

`independent-preservation-report.json` passed using a separate stdlib/XML extraction path rather than the Product raw extractor:

- independently extracted raw cells: **1,257,254**;
- Product raw cells: **1,257,254**;
- observations checked against source OOXML: **1,209,622**;
- raw locator coverage: **1.0**;
- raw-field equality: **1.0**;
- observation/source-value equality: **1.0**.

Independence is bounded: the challenge implementation is separate from `cbr_unified.raw`, while it remains in the same repository/workflow/runtime. No third-party assurance claim is made.

## Post-Jester contract challenge

`post-jester-contract-report.json` passed. All 41 live source revisions carry the required CBR-domain + OOXML trust admission. Required invariants are true:

- one build identity;
- complete 41-source registry universe;
- every raw cell dispositioned;
- every observation has raw lineage;
- every source has observations;
- zero unmapped numeric cells;
- zero conflicting semantic duplicates;
- cross-owner source coherence;
- complete bilingual user surface.

The English source catalog covers 41/41 datasets. English region display/filter symmetry is demonstrated on `mortgage_debt`; the sampled observation/concept/raw/disposition lineage resolves to one source owner.

## Publication-metadata applicability

The complete 41-workbook audit found:

- hidden sheets: `0`;
- hidden rows: `531`, all in `obs_table_20s.xlsx`;
- hidden columns: `10`, across `dep_corp`, `funds_clients`, `funds_org`, `monetary_agg` and `obs_table_20s`;
- cell comments: `0`;
- numeric percent-format-only cells: `0`.

The audit establishes applicability, not semantic Authority. Current evidence does not establish worksheet visibility flags as statistical meaning or publication-control semantics. Raw OOXML preservation already retains stored cells irrespective of visibility. Therefore no additional semantic rule is admitted from visibility alone. Reopen this disposition if Bank of Russia methodology or a source revision establishes visibility as a material semantic/publication contract.

## Expected-to-actual comparison with PRODUCT-CBR-001

Historical verified Product evidence recorded 1,257,254 raw cells, 1,209,622 observations, 2,970 source concepts and 208 dimension members. The post-Jester candidate retains the same raw-cell, observation and dimension-member counts while source concepts increase by **57** to 3,027.

This is consistent with the intended repair: demonstrated source-local distinctions are separated in concept identity while source values, raw coverage and observation cardinality remain intact. The candidate introduces no new source universe, fuzzy cross-source merge or implicit aggregation.

## Repeat evidence

Two preceding full-corpus runs over the same executable implementation also passed the complete envelope:

- run `34909360238` (#62), candidate checkpoint `904febee0bab5010f799ff5dbedc63de5bd55deb`;
- run `34909506329` (#63), candidate checkpoint `64c293fb85320d2950232ef89b9bcd42121febf9`.

These are replication evidence. Admission relies on exact-state run #64.

## Evidence boundary

This evidence supports repository Product conformance for the bound 41-source revisions and tested runtime. It does not establish public release, deployment, external operating state, business outcome validation, official status of project English translations, or universal compatibility with arbitrary future workbook layouts.
