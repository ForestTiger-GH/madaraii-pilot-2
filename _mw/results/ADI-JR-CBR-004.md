# ADI-JR-CBR-004 — Developed acts from JR-CBR-004

**Work kind:** `ACTOR_INPUT_DEVELOPMENT` (`MADARAII-03`)  
**Source carrier:** `_mw/results/JR-CBR-004.md`  
**Evidence:** `_mw/evidence/JST-CBR-004.md`, `_mw/evidence/JST-CBR-004-RESTORATION.md`  
**Product baseline:** `PRODUCT-CBR-001@4ee8583b3feff7775a956c51812232fa0d0516d2`  
**Governing instruction baseline:** `ForestTiger-GH/MADARAII@721a199352b5c5282b1478cd6a5eb36a9872fb34`  
**Status:** COMPLETE

## Status ceiling

The carrier establishes exact synthetic behavior at the acquisition/raw/publication boundary. It does not establish that the verified 41-source corpus currently contains semantically material hidden sheets/rows, comments, style-only units, hostile redirects or malformed local bindings. It also does not override downstream parsing/validation gates.

## Developed acts

| Act | Source | Normalized meaning | Status / limit | Disposition |
|---|---|---|---|---|
| `ADI4-A01` | JST4-P01 | Network acquisition records a redirected response as `ok` after HTTP success + `PK` prefix even when the resolved host differs from the requested CBR host and structural OOXML validity is unproven at that stage. | Reproduced with synthetic response; later parsing remains a separate gate. | **route** as acquisition trust/stage-contract candidate. |
| `ADI4-A02` | JST4-P02 | A hidden worksheet can produce ordinary observations; sheet visibility is absent from raw evidence. | End-to-end synthetic XLSX reproduction. Current-corpus occurrence UNKNOWN. | **route** as publication-metadata applicability candidate. |
| `ADI4-A03` | JST4-P03 | A hidden source row can produce ordinary observations; row-hidden state is absent from raw evidence. | End-to-end reproduction; current-corpus occurrence UNKNOWN. | **route** with A02 as publication-metadata candidate. |
| `ADI4-A04` | JST4-P04 | Excel number-format semantics can be present while semantic output falls back to `unit=source_defined`; raw exposes style index but not resolved number-format meaning. | Reproduced after correcting the Jester's initial mistaken assertion. The raw workbook still retains the actual style internally, but the Product raw record does not expose its semantic format. | **route** with publication-metadata candidate; first establish whether any supported source relies on formatting for statistical meaning. |
| `ADI4-A05` | JST4-P05 | Cell comments containing a publication warning are absent from the raw contract and therefore cannot influence ordinary semantic admission. | End-to-end reproduction; current CBR use of comments for such meaning UNKNOWN. | **route** with publication-metadata candidate. |
| `ADI4-A06` | JST4-P06 | Local source binding validates path cardinality/hash, not OOXML structure, and can return `status=ok` for arbitrary bytes under the expected filename. | Reproduced; later raw parsing would fail. | **route** with A01 as stage-contract candidate; no full-build failure claim. |

## Recovery and campaign stop input

`ADI4-R01` — `jester/jst-0004` was independently resolved after restoration to exact SHA `4ee8583b3feff7775a956c51812232fa0d0516d2`. Canonical Product code remained outside the mutation surface. **Admitted evidence**.

`ADI4-S01` — the Jester Report records diminishing marginal novelty after four sessions: remaining safe attacks are mainly variants of source-presentation metadata, package/trust boundaries or previously exposed consumer/parser classes. This is a factual Work/campaign stop input, not a Product-quality conclusion.

## Accounting

All six provocations, the one adaptive correction, restoration and stop input are accounted. No act creates a defect, Task, Product requirement, Decision, priority or repair.

**Mandatory handoff:** `WSR-JR-CBR-004` under MADARAII-04.
