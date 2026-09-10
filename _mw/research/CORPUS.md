# RC-CBR-001 — Research Corpus Assembly

**Work kind:** `RESEARCH_CORPUS_ASSEMBLY` (`MADARAII-09`)  
**Purpose:** exact source/result accounting for Scientific Knowledge assembly supporting the current CBR statistics product  
**Cutoff:** 2026-09-11 project run; registry Baseline `b7af2c380a028984ec4b465250ac44a0f05efab6`  
**Status:** established corpus census; this file contains navigation/accounting, not a scientific conclusion

## Declared source universe

The primary empirical universe consists of all 41 Bank of Russia workbooks declared by the permitted registry revision. Acquisition/inspection evidence is frozen at commit `140338646aef5a0cc5ab8db4abf04af3945b25c5` and human-readable evidence at `4782c08fc86b0d6e481103970499b3559d73062a`.

Every registry source has status `inspected`; no source is missing or failed. Every one of the 162 worksheets is represented in `SHEET_INDEX.csv`; exact source workbook hashes are in `MANIFEST.json`.

Supplementary external evidence is restricted to official Bank of Russia current publication/methodological surfaces materially required to interpret the same statistics: granted funds/borrowings, mortgage methodology, household financial assets/liabilities, monetary/financial statistics and external-debt methodology. These sources clarify published statistical concepts; they do not expand the registry file universe.

## Research Result census

| Result identity | Topic | Status | Exact route | Primary role |
| --- | --- | --- | --- | --- |
| `RT-CBR-001-RR` | complete source-universe census | established/current at cutoff | `RT-CBR-001-source-universe.md` | empirical structural universe and family distinctions |
| `RT-CBR-002-RR` | statistical identity/collisions | established/current at cutoff | `RT-CBR-002-statistical-identity.md` | semantic identity, dimensions, equivalence boundary |
| `RT-CBR-003-RR` | preservation/normalization | established/current at cutoff | `RT-CBR-003-preservation-normalization.md` | raw preservation, provenance, fail-closed normalization |
| `RT-CBR-004-RR` | bilingual semantics | established/current at cutoff | `RT-CBR-004-bilingual-semantics.md` | RU/EN naming layers and translation provenance |
| `RT-CBR-005` | 2D view semantics | design-facing disposition | qualified in `RES-0002`; its remaining question is primarily Target/data-model design after current research | routed downstream; no separate external Research Result required |

## Mechanical evidence census

- `MANIFEST.json` — 41/41 acquisition and hash records.
- `SHEET_INDEX.csv` — 162/162 sheet records.
- `LABEL_INDEX.csv` — 36,161 exact text labels/coordinates.
- 41 per-source JSON evidence files — detailed worksheet structures.
- nine family-readable evidence packs — all registry families.
- structural-cluster and presentation-collision reports — discovery relations; explicitly non-authoritative for semantic identity.

Document count is not treated as evidence independence. Family packs are projections of the same workbook evidence, not additional studies.

## Lineage and dependence

`RT-CBR-002..004` depend on the complete source census and reuse its empirical evidence. Official CBR methodology adds independent definitional Authority for concepts such as activity classification, household balance/transaction semantics, monetary survey breakdowns and external-debt maturity. It does not independently confirm each workbook cell.

Mechanical evidence and readable packs share the same downloaded source bytes and must be counted as one empirical lineage.

## Coverage and residue

All material current research questions needed before Target formation are covered or routed:

- actual source universe/variants — covered by RT-CBR-001;
- semantic identity/dimensions/duplicates/revisions — covered by RT-CBR-002;
- source-value preservation and normalization safety — covered by RT-CBR-003;
- bilingual/readable names — covered by RT-CBR-004;
- concrete 2D query/API/data schema — intentionally routed to Target WHAT/HOW because the remaining uncertainty is engineering choice rather than missing external description.

No material admitted Research Result is missing. No inaccessible source remains. Future changes to a live CBR workbook after the frozen hashes are late inputs and enter through a source-revision delta, never silently into this corpus.

## Navigation

Start with `RT-CBR-001` for empirical structure, then `RT-CBR-002` for semantic identity, `RT-CBR-003` for preservation and `RT-CBR-004` for language. Use raw evidence only for source-level challenge or adapter implementation.

## Rebuild/reopen rule

Rebuild this census if the permitted registry revision/source list changes, any source hash used by the active product baseline changes, a new material Research Result is admitted, or a current CBR methodology change alters interpretation. Generated indexes remain projections, not editable source Authority.
