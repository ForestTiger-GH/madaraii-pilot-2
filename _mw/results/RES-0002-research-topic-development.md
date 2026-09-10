# RES-RESEARCH-QUAL-001 — Initial research-topic development

**Work kind:** `RESEARCH_TOPIC_DEVELOPMENT` (`MADARAII-07`)  
**Signal universe:** `RES-ACTOR-001`, registry Baseline `b7af2c380a028984ec4b465250ac44a0f05efab6`, explicit absence of project Scientific Knowledge  
**Consumer:** formation of trustworthy CBR Scientific Knowledge and later Target WHAT/HOW  
**Status:** established qualification Result; topics below are commissioned by the active user contour only where explicitly marked

## Signal disposition

The dominant gap is genuine empirical/external knowledge: the actual workbook structures and statistical semantics are unknown. Product schema/API/normalization choices are therefore design questions gated by Research rather than Research Topics themselves. Mechanical retrieval of the URL list is already resolved by the permitted registry.

## Commissioned rolling research set

### RT-CBR-001 — Complete source-universe census and structural classification

**Question.** What files, sheets, table geometries, label patterns, numeric regions, units, periods, regions/classifications, revisions and structural variants actually exist across every registry URL, and which apparent differences are presentation-only versus potentially semantic?

**Scope.** Every URL declared by the bound registry revision. Inspect each workbook and each material sheet/table. Capture acquisition provenance and a reproducible structural/textual census. External CBR publication pages may be used only to interpret the same sources where needed.

**Non-goals.** No final normalization schema, indicator merging, shortened naming system or product architecture.

**Evidence strategy.** Acquire all files from CBR with reproducible HTTP metadata/hash; inspect workbook/sheet metadata, merged cells, formulas, text labels, number formats, data-density geometry and representative raw grids; record failures explicitly. Prefer source files themselves as primary evidence.

**Stopping.** Every registry source has an explicit acquisition/inspection disposition and the observed structural space is classified sufficiently to qualify semantic follow-up topics.

**Status:** commissioned now by `WORK-CBR-001`.

### RT-CBR-002 — Statistical identity, dimensions and semantic collision model

**Question.** Across the observed source families, what makes two observations/indicators semantically identical, equivalent representations, distinct slices, or distinct statistics; which dimensions, units, temporal conventions and population definitions form identity; where can apparent duplicates or revisions conflict?

**Activation.** After RT-CBR-001 provides the empirical family/collision map.

**Sources.** Exact workbooks, CBR metadata/methodological pages tied to those publications, and only materially necessary external statistical terminology.

**Non-goals.** Choosing code classes or a database engine.

**Status:** qualified, conditionally commissioned after RT-CBR-001.

### RT-CBR-003 — Robust source normalization and preservation boundary

**Question.** Which source variations can be normalized safely as presentation noise, which require source-family adapters or explicit ambiguity, and what provenance/value-preservation model is sufficient to prove that accepted source numbers survive parsing and normalization without false semantic collapse?

**Activation.** RT-CBR-001/002 findings.

**Status:** qualified, conditionally commissioned after prerequisite evidence.

### RT-CBR-004 — Bilingual semantic surface and readable naming

**Question.** How can exact CBR Russian source labels, interpreted meanings, shorter Russian working names and English names coexist without identity loss or collision; where does CBR already provide authoritative English terminology and where must project translations remain explicit project labels?

**Activation.** Stable indicator/dimension identity from RT-CBR-002.

**Status:** qualified, conditionally commissioned.

### RT-CBR-005 — Queryable two-dimensional view semantics

**Question.** Given the real dimensional/frequency heterogeneity, what observation model and pivot/view semantics can expose meaningful two-dimensional tables without inventing aggregates or silently comparing incompatible statistics?

**Activation.** RT-CBR-002/003.

**Disposition:** primarily target/data-model design informed by empirical research; use external Research only for unresolved statistical semantics. Do not treat the illustrative human parameter list as a closed taxonomy.

## Non-Research routes

- Exact package/module/API layout, local-file interface shape, CSV partitioning, storage engine and notebook ergonomics are Target HOW/Product Architecture concerns after Research.
- Correctness of an implemented parser is assurance/verification Work, not Research.
- Runtime execution in Colab/Jupyter is a Target requirement and later verification claim.

## Reopen triggers

Registry source-set change, newly discovered source family, unresolved source conflict affecting identity, or CBR methodological revision that changes interpretation.
