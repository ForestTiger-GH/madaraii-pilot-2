# TS-CBR-SURFACE — Bilingual semantics and safe analytical views

**Work kind:** `THEMATIC_RESEARCH_SYNTHESIS` (`MADARAII-12`)  
**Theme:** `T-CBR-SURFACE`  
**Corpus Baseline:** `RC-CBR-001`  
**Status:** established thematic synthesis

## Current bounded answer

Readable language and two-dimensional views can be layered over stable statistical IDs without becoming part of identity. The system should retain exact CBR Russian text, provide shorter Russian and English display names, and record whether the English term is official CBR terminology or a project translation.

A prepared table is a **projection**, not a recalculation engine. It filters observations and pivots one dimension to rows and another to columns. By default it performs no aggregation. If multiple observations land on one output cell, the view is ambiguous and must require further filtering or an explicit caller-supplied resolution policy.

## Naming model

- exact CBR Russian source label/path — immutable provenance;
- normalized Russian source text — search only;
- readable Russian display name — project surface;
- English display name — official CBR term when available, otherwise project translation;
- translation status/source — explicit;
- stable concept ID — machine identity independent of names.

Dimensions already represented structurally may be removed from a short name, but never from the observation meaning. Generic aliases such as `Просроченная задолженность` / `Overdue debt` can recur; context and stable ID disambiguate them.

## Query/view semantics

A useful common long-form observation surface should expose core columns plus structured dimensions. Callers can filter by stable IDs or human aliases and request language `ru`/`en`.

A 2D view operation should accept, conceptually:

- filters over source/concept/period/unit/dimensions;
- row key(s);
- column key(s);
- value field;
- display language;
- optional provenance columns/sidecar.

It should reject implicit summation, mean, latest-value selection or source preference. The commissioned product does not need to calculate economic indicators.

## Bilingual completeness

Every user-exposed dataset/concept/dimension member should have a Russian and English display surface. Official CBR English publication terminology is preferred where clearly corresponding. Project translations remain marked `project_translation`; exact Russian source wording always remains available.

The source universe contains more cell labels than meaningful user concepts. Translation completeness therefore applies to the semantic catalog, not every note, date string or raw presentation cell.

## User-facing ambiguity behavior

- searching by a non-unique alias returns multiple contextual matches;
- filtering by stable ID is exact;
- a pivot collision raises an explicit ambiguity error;
- canonical overlaps preserve all source provenance;
- language changes labels only, never observation identity/value.

## Strongest challenge

A system could precompute a single wide bilingual CSV for convenience. The heterogeneous dimensions and changing source regimes make that format either sparse and lossy or semantically overloaded. A normalized long-form store plus deterministic 2D projections gives better preservation and allows CSV outputs without forcing one universal wide schema.

## Downstream implications

The product should offer callable operations for catalog/search, filtering, pivoting and CSV export, usable independently from notebook orchestration. A notebook may demonstrate these operations but should not contain the only implementation.

## Reopen

Reopen on new required language, changed translation policy, a new dimension that cannot be projected safely, or evidence that the selected view semantics hide valid source multiplicity.
