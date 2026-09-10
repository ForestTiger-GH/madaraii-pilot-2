# RES-ACTOR-001 — Developed actor input

**Work kind:** `ACTOR_INPUT_DEVELOPMENT` (`MADARAII-03`)  
**Source carrier:** `INBOX-CBR-001` at `_mw/inbox/INBOX-0001.md`  
**Interpretation Baseline:** `WORK-CBR-001` during bootstrap; Product and Knowledge owners absent  
**Status:** established input-development Result; downstream acts retain their own status ceilings

## Developed semantic acts

| Act | Type | Normalized meaning | Status / Authority ceiling | Route |
| --- | --- | --- | --- | --- |
| A01 | product need / Work request | Create code that turns the registry-defined CBR Excel universe into one coherent, usable statistical system. | authorized project intent; implementation meaning still unresolved | source Research → Scientific Knowledge → Target WHAT |
| A02 | source-boundary constraint | Use the specified `registry.py` as the list of CBR files; do not use other `stratbox` content. | binding constraint | Work State / research source universe |
| A03 | research requirement | Inspect the real files broadly before defining how indicators, sheets, dimensions, regions, periods, duplicates and source families are unified. | binding process/correctness requirement | Research Program |
| A04 | semantic-correctness requirement | Distinguish presentation noise, equivalent labels, dimensions, cuts, distinct indicators, duplicates, and semantic collisions; avoid false unification. | target correctness candidate supported by required Research | Research → Knowledge → Target WHAT |
| A05 | preservation requirement | Preserve every material numeric value accepted from the sources; do not calculate new economic indicators as part of this product. | binding target intent; exact preservation semantics require Research | Target WHAT after Research |
| A06 | provenance requirement | Keep enough origin information to trace normalized data back to source file/sheet/table/cell or equivalent source position. | binding target intent; exact mechanism unresolved | Target WHAT / Target HOW |
| A07 | retrieval need | Provide prepared two-dimensional tables selected by meaningful parameters such as indicator, region, currency, overdue status, SME/IE status and temporal granularity where such dimensions actually exist. | authorized outcome; dimension list illustrative rather than exhaustive taxonomy | Research → Target WHAT |
| A08 | export requirement | Make the unified data available for export/saving at least as CSV. | binding minimum capability | Target WHAT |
| A09 | robustness concern | Tolerate presentation-level naming variation including spaces, punctuation and drifting sheet/label forms, while preserving semantic distinctions. | target quality/correctness candidate | Research → Target WHAT/HOW |
| A10 | runtime requirement | Support practical execution in Google Colab or Jupyter Notebook with internet access. | binding environment requirement | Target WHAT/HOW |
| A11 | acquisition requirement | Internet download from registry URLs is a required supported path. | binding target behavior | Target WHAT/HOW |
| A12 | local-input preference | Separate acquisition from processing if justified so processing can also operate on pre-downloaded local files. | strong design preference, not yet admitted target obligation | Research/Target HOW decision |
| A13 | bilingual semantics requirement | Provide Russian and English semantic surfaces for indicators, regions and other meaningful labels. | binding target intent | Research → Scientific Knowledge → Target WHAT/HOW |
| A14 | readable-name preference | Where safe, expose shorter readable Russian/English names while retaining exact CBR labels and meaning. | preference constrained by semantic fidelity | Research → Target WHAT/HOW |
| A15 | modularity preference | Keep materially independent operations separable and callable so the product can later be embedded into external software systems. | strong architecture/design preference; avoid unnecessary complexity | Target HOW / Product Architecture |
| A16 | empirical unknown | Actual workbook families, sheet/table structures, dimensions, units, temporal conventions, revisions, overlaps, conflicts and ambiguity set are unknown until source inspection. | UNKNOWN, explicitly blocking final data model | Research owner |
| A17 | interface unknown | Concrete user/programmatic API and final two-dimensional view contract are not preselected. | open design Question | Target WHAT/HOW after Research |
| A18 | naming unknown | Safe rules for concise bilingual naming, translation, identity and collision handling are unresolved. | open semantic Question | Research / Scientific Knowledge |

## Impact and disposition

The carrier establishes strong product intent and several binding constraints, but it does not establish a data schema, indicator taxonomy, parser architecture, module list, normalization algorithm, final API, Target WHAT/HOW, or implementation plan. Acts A03/A04/A16 make source Research a prerequisite for those owner transitions.

No claim about the actual content or structure of the CBR files is admitted solely from the carrier. Examples such as region/currency/SME/IE/overdue/time frequency are research hypotheses and desired query concepts, not a closed dimension list.

## Traceability

The raw wording remains preserved in `INBOX-CBR-001`. This Result is a routed interpretation and never replaces the source carrier as provenance.

## Completion

All material acts in the human inbox are separately status-limited and routed. The next commissioned substantive operation is source-universe qualification and empirical Research, followed by maintained knowledge before target formation.
