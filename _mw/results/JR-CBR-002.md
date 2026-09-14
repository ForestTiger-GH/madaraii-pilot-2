# JR-CBR-002 — Semantic-inference Jester Report

**Method:** `MADARAII-40 — JESTER_PROVOCATIVE_EXPLORATION`  
**Work:** `WORK-JESTER-0002`  
**Actor:** `JESTER-ACTOR-JST-0002`  
**Engineering Object:** `PRODUCT-CBR-001`  
**Exact Product baseline:** `4ee8583b3feff7775a956c51812232fa0d0516d2`  
**Experiment surface:** `jester/jst-0002`  
**Detailed evidence:** `_mw/evidence/JST-CBR-002.md`  
**Restoration evidence:** `_mw/evidence/JST-CBR-002-RESTORATION.md`  
**Report state:** COMPLETE / RESTORED / HANDED OFF

## What the Jester attacked

The second pass stopped attacking owner coherence and generic validation boundaries already covered by `JR-CBR-001`. It attacked the semantic interpreter where a plausible spreadsheet can look ordinary while wording, geometry or lexical form carries meaning that a heuristic has not actually proved.

The Crazy-Idea Generator combined negation, misleading methodological context, table-level unit perfume, false calendar geometry, tiny table-size changes, mixed measures in one regional dataset, combined qualifiers and accounting-style numeric syntax.

## What was done

A fresh disposable branch was created from the exact admitted Product revision. Four CI runs were generated. One intermediate run failed because the Jester's own phrase did not activate the intended parser rule; the trajectory preserved that evidence, sharpened the phrase, and continued. The last experimental state at `ebcbd7767519321a7de6330c4ea1c5e34dd27dd9` passed the ordinary test suite plus all retained Jester-2 reproducers in run `34894854255`.

Ten materially different provocations exhausted the pre-bound session budget.

## Material observations

1. **Negation can be eaten by qualifier keywords.** Wording equivalent to “non-overdue”, “without overdue”, “without acquired right”, and “non-seasonally adjusted” can produce the affirmative semantic flag when the recognized token is present.
2. **Broad table context can override a more specific row unit.** A table title in million rubles can make a percentage-growth row or borrower-count row resolve as RUB millions.
3. **The word `изменение` can hijack period-role semantics outside an actual change measure.** Methodological and explicitly negated contexts can still resolve to `published_change`.
4. **Territory typing can call a label `country_total` while the label itself declares a territorial exclusion.**
5. **Methodology dates can cosplay as the period axis.** Three date-like cells plus technical values below them can become valid observations with the numeric gate passed.
6. **The unexplained-numeric fail-closed boundary contains a count cliff.** Nine unknown numerics can pass with zero observations while ten in the same pattern trigger a source-variant error.
7. **A combined maturity scope is collapsed to the first recognized bucket.** A label containing both `до 1 года` and `свыше 1 года` resolves to the former.
8. **Period discovery depends on the Excel value type.** Numeric year headers are ignored by the generic path while the same years as text become annual periods.
9. **Region-axis concept construction can collapse different measures into one concept.** Two sheets carrying debt and loan count for the same region can share one `source_concept_id` despite incompatible units.
10. **Accounting-style parenthesized numerics can disappear from the numeric-completeness gate.** `(10)`-style cells can produce zero observations while `unmapped_numeric_count` remains zero and the gate passes.

The strongest common pattern is different from the first session. `JR-CBR-001` showed that plausibly explained but incoherent owner/representation states can pass farther than unexplained states. This session shows that **lexically plausible meaning can be confidently inferred even when nearby negation, scope, unit hierarchy, sheet role or number syntax changes what the phrase actually means**.

## Resistant behavior and limits

Numeric year values are deliberately kept out of generic period discovery, reducing accidental header detection in ordinary data. The ten-number source-variant threshold does eventually fail closed. The final CI trajectory remained deterministic after the Jester corrected its own malformed probe. None of these observations establishes Product failure against the commissioned 41-source baseline; all were synthetic source-variant provocations unless otherwise stated.

## Restoration and handoff

Before downstream interpretation, `jester/jst-0002` was force-restored and independently resolved to exact Product baseline:

`4ee8583b3feff7775a956c51812232fa0d0516d2`.

The branch-only workflow and disposable reproducers are absent from its current state. Canonical `main` Product code was never in the experiment mutation surface.

Mandatory continuation completed:

- `ADI-JR-CBR-002` — `_mw/results/ADI-JR-CBR-002.md` — MADARAII-03;
- `WSR-JR-CBR-002` — `_mw/results/WSR-JR-CBR-002.md` — MADARAII-04.

The reconciliation keeps the original Product admission and closure intact and records bounded post-closure Work candidates. The highest-materiality additions concern contextual semantic inference, false-header parser robustness, measure identity in region/activity sources, and the numeric-completeness boundary.

`WORK-JESTER-0002` is closed. This Report remains the standalone owner of the session record; downstream engineering meaning belongs to the developed-input and reconciliation Results.
