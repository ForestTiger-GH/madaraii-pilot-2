# JR-CBR-004 — Acquisition/raw publication-boundary Jester Report

**Method:** `MADARAII-40 — JESTER_PROVOCATIVE_EXPLORATION`  
**Work:** `WORK-JESTER-0004`  
**Actor:** `JESTER-ACTOR-JST-0004`  
**Engineering Object:** `PRODUCT-CBR-001`  
**Exact Product baseline:** `4ee8583b3feff7775a956c51812232fa0d0516d2`  
**Experiment surface:** `jester/jst-0004`  
**Evidence:** `_mw/evidence/JST-CBR-004.md`  
**Restoration evidence:** `_mw/evidence/JST-CBR-004-RESTORATION.md`  
**Report state:** COMPLETE / RESTORED / HANDED OFF

## Attack frame

This pass challenged a narrower premise than the previous sessions: exact workbook/cell preservation is not necessarily the same thing as preserving which data the workbook author intended to expose, qualify, hide or trust. The Jester attacked acquisition trust and source-presentation metadata rather than statistical-language heuristics.

Six materially different provocations reached the fixed budget. One intermediate assertion was sharpened after the Product correctly returned `unit="source_defined"` instead of an empty unit; the final run `34896619311` passed the ordinary suite plus all disposable reproducers.

## Material observations

1. **Acquisition trusts a redirected payload at the stage boundary.** A response resolving to an unrelated host can be recorded as an `ok` source revision when HTTP succeeds and content begins with `PK`; exact OOXML validity is deferred downstream.
2. **Hidden worksheets remain semantically live.** A hidden Excel sheet containing an ordinary matrix produces observations, while sheet visibility is absent from the raw contract.
3. **Hidden rows remain semantically live.** Hiding the source row does not alter observation production and the hidden-state distinction is not preserved in raw rows.
4. **Excel number-format meaning is only indirectly preserved by style index.** A visually formatted percentage with no textual `%` reaches semantic output as generic `source_defined`, because resolved number-format semantics are absent from the raw/semantic inference contract.
5. **Cell comments can contain publication-relevant warnings that disappear before semantic processing.** A synthetic “preliminary / do not publish” comment attached to an otherwise valid numeric cell is absent from raw evidence and does not affect observation admission.
6. **Local binding is a path/hash binding, not an XLSX-validity gate.** Arbitrary bytes under the expected `.xlsx` name can receive an `ok` local binding record; structural validity is deferred to later parsing.

The common pattern is **stage-correct but meaning-incomplete preservation**. The Product is strong at immutable cell-level provenance, yet some workbook-level or presentation-level distinctions are outside the current raw evidence contract. Whether those distinctions matter depends on actual source conventions and the accepted Product boundary.

## Limits and stop rationale

The accepted Product was already verified against the full bound 41-source corpus. This session did not establish that current CBR files use hidden rows/sheets, comments or number formats in a way that invalidates that verified build. Redirect/package observations are also stage-bound because later parsing/validation supplies additional gates.

After four Jester sessions, remaining safe candidate attacks are largely variants of classes already exposed: more Excel presentation metadata, more source-package edge cases, or more consumer projections. They can still produce examples, but expected engineering novelty has fallen materially. The overall Jester campaign therefore stops after this session rather than manufacturing volume from increasingly speculative variants.

## Restoration and continuation

The experiment branch was force-restored after evidence capture and independently resolved to exact Product baseline:

`jester/jst-0004 → 4ee8583b3feff7775a956c51812232fa0d0516d2`.

Canonical Product code on `main` was never part of the experiment mutation surface. `PRODUCT-CBR-001` and `CLOSURE-CBR-001: PASS` remain unchanged.

Mandatory continuation completed:

- `ADI-JR-CBR-004` — `_mw/results/ADI-JR-CBR-004.md` — MADARAII-03 — COMPLETE;
- `WSR-JR-CBR-004` — `_mw/results/WSR-JR-CBR-004.md` — MADARAII-04 — COMPLETE.

The reconciliation established two bounded Work-candidate families: `WC-JR4-PUBLICATION-METADATA` and `WC-JR4-SOURCE-TRUST`. Both require separate Authority before substantive execution. This Report creates no defect, Task, priority, Product change or repair.
