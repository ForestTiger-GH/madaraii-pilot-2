# RES-IMPLEMENTATION-CBR-001 — CBR Unified Statistics implementation result

**Work kind:** `ENGINEERING_PRODUCT_IMPLEMENTATION`  
**Commission:** `WORK-CBR-001`  
**Plan:** `PLAN-CBR-001` at `_mw/work/PLAN-0001.md`  
**Target at implementation completion:** `TW-CBR-1` / `TH-CBR-1` / `PRODUCT-ARCH-CBR-001`  
**Final product-code candidate:** `4ee8583b3feff7775a956c51812232fa0d0516d2`  
**Status:** implementation producer-complete; exact candidate verified by `RES-VERIFICATION-CBR-001`; Product admission remains a separate owner transition.

## Actual realized change

The repository contains a reusable Python product for the registry-defined Bank of Russia Excel universe.

- `src/cbr_unified/registry.py` owns the reviewed 41-source registry snapshot derived from the single permitted stratbox registry input.
- `acquisition.py` implements live HTTP acquisition, exact local rebinding, source hashes and revision manifests.
- `raw.py` implements a lossless OOXML raw-cell ledger independent of openpyxl value coercion. It retains source revision, sheet, coordinate, OOXML type, style, lexical value, resolved text and formula.
- `normalization.py`, `semantic.py` and `processing.py` implement conservative period, unit, dimension and source-concept interpretation with source-scoped compatibility behavior.
- Mortgage sheets representing acquired claims only and measures including acquired claims remain distinct dimensions; abbreviated overdue labels remain distinct from total debt; footnoted date headers retain raw source text while receiving a bounded semantic period interpretation.
- `validation.py` requires complete source coverage, raw-cell disposition coverage, exact observation lineage, valid semantic identities, zero unexplained numeric cells, zero conflicting semantic duplicate groups and complete typed RU/EN user surfaces.
- `persistence.py` materializes deterministic CSV and SQLite representations from one validated owner set.
- `build.py` coordinates staged live/local builds, deterministic build identity, canonical promotion and retained failure evidence.
- `query.py` provides pandas-based bilingual catalog lookup, filtering, dimension expansion, lineage and fail-closed pivots.
- `cli.py` exposes build, validate, source listing, indicator lookup, observation query, pivot and lineage operations with CSV view export.
- `README.md`, `docs/` and `examples/` provide cold-use guidance.
- `tests/`, `tools/verify_full_build.py` and `tools/independent_verify_preservation.py` provide unit/contract, complete-build/replay and independent raw-preservation evidence surfaces.

## Plan trace

1. **Preservation foundation:** source revision and raw OOXML ledger implemented before semantic normalization.
2. **Semantic unification:** observations retain source-local concept identity plus explicit period/frequency/role/unit/dimensions and exact raw lineage.
3. **Persistence:** deterministic CSV plus SQLite bundle implemented.
4. **Use surface:** Python API, bilingual names, filters, pivots, CLI and examples implemented.
5. **Assurance:** fail-closed source-variant handling, numeric residue gate, semantic-conflict checks, bilingual completeness, deterministic offline replay and independent OOXML comparison implemented.
6. **Build-state integrity:** successful builds are promoted from staging only after complete validation; failed builds retain diagnostics without replacing a prior canonical build.

## Material implementation choices

- SQLite and CSV are parallel derived projections; neither is a second semantic authority.
- Source numeric values remain exact strings in authoritative raw/observation representations and are converted only at query convenience boundaries.
- Source-local semantic identity remains source-scoped. Structural similarity and normalized labels never merge concepts automatically.
- Exchange-rate calendar compatibility is restricted to proven current presentations and a semantic view; raw evidence is untouched.
- Acquired-claims, overdue, valuation, currency and other evidenced axes remain explicit rather than being collapsed by worksheet similarity.
- Unknown numeric residue in a complete source universe is an implementation error.
- Build identity is deterministic over exact source revisions, source specifications and the declared build-contract version.
- English display surfaces are typed as project translation, official terminology when explicitly established, or transparent transliteration where appropriate; display language never forms identity.

## Defects discovered and repaired before final candidate

Full-source verification deliberately exposed and bounded four real presentation/semantic gaps:

1. exchange-rate quarterly labels `N кварт.`;
2. mortgage sheets for acquired claims versus debt including acquired claims;
3. abbreviated overdue marker `проср.`;
4. debt-securities period header `01.01.2019*` with footnote marker.

A later claim audit also showed that bilingual completeness was only indirectly exercised. The final candidate therefore added a fail-closed bilingual validation gate for every dataset, source concept and dimension member before the decisive verification run.

The strict preservation, numeric-residue and semantic-conflict gates were retained throughout; repairs changed interpretation contracts rather than weakening acceptance criteria.

## Producer-completion evidence

Exact independent verification is owned by `RES-VERIFICATION-CBR-001` / `VERIFY-CBR-001`. The decisive run on this exact candidate produced:

- 41/41 source coverage;
- 1,257,254 raw cells;
- 1,209,622 observations;
- zero unmapped numeric cells;
- complete 41 / 2,970 / 208 bilingual dataset/concept/member coverage;
- deterministic live/local replay;
- 100% independent OOXML raw/value equality.

These facts are verification evidence, not producer self-admission.

## Effects and exclusions

Implementation effects are limited to this repository and GitHub Actions verification activity. CBR sources were read only. No external database/service, production deployment, release, customer state or business outcome was created or claimed.

## Handoff

The implementation candidate is immutable at `4ee8583b3feff7775a956c51812232fa0d0516d2`. Target HOW nomenclature discovered as stale during verification was reconciled separately to `TH-CBR-1.1` and bounded-revalidated without changing this Product code. Admission/integration must use that verification chain and keep deployment/release/validation states distinct.