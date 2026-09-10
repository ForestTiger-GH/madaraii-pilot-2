# TM-CBR-001 — Research Corpus Theme Map

**Work kind:** `RESEARCH_CORPUS_THEME_MAPPING` (`MADARAII-11`)  
**Consumer:** Current Scientific Knowledge needed to form trustworthy Target WHAT/HOW for `WORK-CBR-001`  
**Corpus:** `RC-CBR-001` at `CORPUS.md`  
**Status:** established purpose-bound Theme Map

## Theme map

### T-CBR-STRUCT — Source structure and interpretation boundary

**Central question:** What structural families and presentation variants exist, and what can a parser infer mechanically without inventing statistical meaning?

**Assigned material:** RT-CBR-001 structural census; per-source/sheet probe; structural clusters; relevant parts of RT-CBR-003.

**Scope:** workbook/sheet geometry, period representations, row/hierarchy forms, formula/metadata sheets, reusable structural mechanisms, unseen-variant boundary.

**Non-scope:** cross-source semantic equality, final module architecture, user API.

**Consumer:** parser/data-model design and assurance.

**Required dispositions:** evidence, structural variants, false-generalization counterexamples, presentation drift, failure mode, coverage and reopen triggers.

**Relations:** constrains T-CBR-ID; supplies physical provenance requirements to T-CBR-PRESERVE.

**Stop:** all 41 sources/162 sheets are dispositioned into known structural families/outliers and unsupported inference is explicit.

### T-CBR-ID — Statistical identity, dimensions and overlap

**Central question:** What makes an observation the same statistic versus a different measure/slice/classification/population/revision?

**Assigned material:** RT-CBR-002; semantic parts of RT-CBR-001; official CBR methodology; collision evidence; source hierarchy examples.

**Scope:** measure type, population, classification, territory, currency denomination vs unit, valuation, maturity, adjustment, frequency, period convention, source/canonical identity and duplicate/conflict taxonomy.

**Non-scope:** database technology, UI layout, chosen conflict-resolution UX.

**Consumer:** common observation semantics, canonical mapping policy, query safety.

**Relations:** depends on T-CBR-STRUCT evidence; constrains T-CBR-PRESERVE and T-CBR-SURFACE.

**Stop:** every observed class of semantic collision has an explicit identity disposition or UNKNOWN rule.

### T-CBR-PRESERVE — Lossless preservation, provenance and correctness evidence

**Central question:** How can the system prove source values survive while semantic normalization remains auditable and fail-closed?

**Assigned material:** RT-CBR-003; formula/missing-marker/revision evidence from RT-CBR-001/002.

**Scope:** source revision identity, exact source-cell identity, numeric lexical values, formulas/cached values, dispositions, semantic observation linkage, CSV roundtrip, local/internet byte equivalence, conflict visibility.

**Non-scope:** final Python APIs except where needed to state correctness mechanisms.

**Consumer:** Target correctness claims, architecture and verification plan.

**Relations:** depends on T-CBR-STRUCT; uses identity from T-CBR-ID; constrains all Product admission claims.

**Stop:** preservation can be expressed as machine-reconcilable invariants rather than informal confidence.

### T-CBR-SURFACE — Bilingual semantics and safe analytical views

**Central question:** How can users retrieve/read coherent 2D data in Russian or English without names or pivot operations changing statistical identity?

**Assigned material:** RT-CBR-004, query-facing implications of RT-CBR-002/003, qualified RT-CBR-005 design-facing question.

**Scope:** source/readable/English naming layers, translation provenance, ambiguous-name behavior, stable IDs, non-aggregating filters/pivots, display language.

**Non-scope:** exact UI technology or presentation styling.

**Consumer:** Target WHAT/HOW and user documentation.

**Relations:** depends on T-CBR-ID; provenance requirements from T-CBR-PRESERVE constrain exported views.

**Stop:** user-facing semantics can be stated without relying on label equality or implicit aggregation.

## Cross-theme relations

- Structure is evidence about physical representation, never sufficient semantic identity.
- Identity determines which structural variants may map into shared dimensions and when overlap remains separate.
- Preservation is orthogonal to semantic usability: raw completeness can be proven even when some semantic cells remain unclassified.
- Surface/readability is downstream of identity: translations and short names can vary without changing stable IDs.
- Revision is cross-cutting: source hash identifies evidence revision; semantic identity may persist or change depending on methodology/classification changes.

## Coverage accounting

- RT-CBR-001 → T-CBR-STRUCT, T-CBR-ID, T-CBR-PRESERVE.
- RT-CBR-002 → T-CBR-ID, T-CBR-PRESERVE, T-CBR-SURFACE.
- RT-CBR-003 → T-CBR-STRUCT, T-CBR-PRESERVE, T-CBR-SURFACE.
- RT-CBR-004 → T-CBR-SURFACE and naming-related T-CBR-ID.
- RT-CBR-005 residual → T-CBR-SURFACE for scientific constraints; concrete API/design routed to Target HOW.

No material Research Result has no theme. Product packaging, storage-engine choice and notebook ergonomics are terminally routed outside Research.

## Parallelization and fan-in

The four themes are independently synthesizable after the frozen corpus. T-CBR-ID consumes structural evidence but can be written without waiting for implementation. Final corpus synthesis must reconcile all four before Scientific Knowledge admission.

## Reopen

Reopen mapping if the source universe changes, a new structural family appears, an identity collision requires a new concern, or downstream Product evidence exposes a material scientific gap rather than a design defect.
