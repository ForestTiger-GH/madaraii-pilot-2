# VERIFY-CBR-001 — Exact verification evidence

**Verification subject:** Product-code candidate `4ee8583b3feff7775a956c51812232fa0d0516d2`  
**Workflow:** `.github/workflows/product-verification.yml`  
**GitHub Actions run:** `34544307123`  
**Unit job:** `103093498623` — `success`  
**Full-build job:** `103093586951` — `success`  
**Runtime:** GitHub-hosted Ubuntu 24.04; CPython 3.12.14  
**Evidence cutoff:** 2026-09-11 00:05 UTC

## Exact build identity

- `build_id`: `bld_204724c672460b3deaa50675`
- registry sources: **41 / 41**
- raw cells: **1,257,254**
- semantic observations: **1,209,622**
- source concepts: **2,970**
- dimension members: **208**
- formula raw cells: **11**
- unmapped numeric source cells: **0**
- identical semantic duplicate groups: **0**
- conflicting semantic duplicate groups: **0** by admitted validation invariant

## Bilingual surface

- bilingual datasets: **41 / 41**
- bilingual source concepts: **2,970 / 2,970**
- bilingual dimension members: **208 / 208**
- concept translation status: `project_translation` = **2,970**
- dimension-member translation status: `project_translation` = **107**; `transliteration_only` = **101**
- `bilingual_user_surface_complete`: **true**

No claim is made that every English label is official CBR wording. Translation status remains part of the user-visible semantic catalog.

## Live / local deterministic replay

Live acquisition and local replay resolved to the same build ID and identical source revisions. Deterministic CSV hashes were identical in both runs:

- `raw_cells.csv`: `d1d5edbb5f41a31fa6517555e3a6483827fde4fd49cefb05354e4c269dc1b441`
- `source_concepts.csv`: `2cefb50e5c010d0b3cb03469c1bfb0c4387721af6af3b65284465c84244321af`
- `dimension_members.csv`: `9cb9349177b2f1344c64a11d493e73ef6f0336d3eb29e539499e180bc73f54cc`
- `observations.csv`: `7fadb5089177e26cc224283698b0418e714eee295266850cdadc244820001f85`
- `cell_dispositions.csv`: `e8ba877d190677a1354e17305bc3dab690262470512e841960c010dfd2b7b3cd`
- compatibility alias `raw_cell_dispositions.csv`: same hash as `cell_dispositions.csv`

CSV and SQLite counts matched exactly for source revisions, raw cells, source concepts, dimension members, observations and raw-cell dispositions.

## Independent preservation challenge

`tools/independent_verify_preservation.py` re-read the downloaded XLSX files with an independent OOXML extraction implementation rather than `cbr_unified.raw`.

- independently extracted raw cells: **1,257,254**
- product raw cells: **1,257,254**
- observations checked against independently extracted source values: **1,209,622**
- raw locator coverage: **1.0**
- raw field equality: **1.0**
- observation/source-value equality: **1.0**

This is bounded implementation independence inside the same repository/workflow/runtime, not an external laboratory or third-party audit.

## Query and interface evidence

- mortgage query smoke rows: **89,280**
- English indicator lookup: passed
- lineage lookup: passed
- CLI `validate`: passed
- CLI `query`: passed
- fail-closed pivot behavior is covered by unit/contract tests.

## Workflow artifact

- artifact name: `cbr-unified-verification`
- artifact ID: `10178658180`
- artifact ZIP SHA-256: `0bd7c76ca92acb6dfa256915510f5ec74cf2269b0121401eb68feecc3eddeca9`
- artifact belongs to run `34544307123`

## Historical negative evidence

Earlier candidate runs correctly failed closed on real source-contract defects rather than promoting incomplete data:

1. exchange-rate quarterly presentation `N кварт.`;
2. mortgage acquired-claims populations missing a distinguishing semantic dimension;
3. abbreviated overdue label `проср.`;
4. debt-securities footnoted period header `01.01.2019*`.

Each was resolved by bounded source-presentation/semantic repair plus regression coverage. Validation gates were retained rather than weakened.

## Effect boundary

Verification performed read-only HTTP acquisition of public CBR files and GitHub Actions computation/artifact storage. It did not deploy or release a service, mutate Bank of Russia sources, create an external database, or validate business outcomes.