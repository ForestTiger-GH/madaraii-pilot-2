# TS-CBR-PRESERVE — Lossless preservation, provenance and correctness evidence

**Work kind:** `THEMATIC_RESEARCH_SYNTHESIS` (`MADARAII-12`)  
**Theme:** `T-CBR-PRESERVE`  
**Corpus Baseline:** `RC-CBR-001`  
**Status:** established thematic synthesis

## Current bounded answer

The trustworthy architecture needs a preservation layer below semantic parsing. The downloaded XLSX bytes and raw OOXML cells are the evidence carrier; semantic observations are typed interpretations referencing those cells.

A build can therefore make two separate claims:

- **raw completeness:** every source numeric/formula-cached value in every acquired workbook is represented exactly once with source hash, sheet and cell provenance;
- **semantic coverage:** every numeric source cell is either mapped to a semantic observation or explicitly classified as a non-observation numeric/header/helper item.

This is stronger than comparing dataframe row counts because it verifies exact source-cell keys and lexical values.

## Preservation invariants

1. Source revision identity includes source ID, URL, acquisition timestamp and SHA-256.
2. Raw cell key is `(source_revision, sheet_exact, coordinate)`.
3. Numeric lexical value is captured from OOXML before binary-float coercion.
4. Formula text and cached value are both retained where present.
5. Text markers such as `-` remain distinct from numeric zero.
6. Semantic observation retains a reverse route to its source cell.
7. CSV export preserves exact value strings and stable IDs.
8. Re-ingestion of identical local bytes yields the same raw-cell identities/value content as internet acquisition.

## Safe normalization boundary

Unicode/whitespace cleanup and source-scoped aliases can make dispatch robust. Semantic unification remains explicit. Unknown structural or semantic variants fail closed after raw acquisition so evidence survives even when normalized production output cannot safely be built.

## Revision/conflict behavior

A new hash at the same URL creates a new source revision. Historical cells can then be compared, but the new file does not erase the old evidence. If two source observations map to the same canonical concept and disagree, both remain and the canonical query becomes ambiguous until a visible disposition is supplied.

## Evidence requirements

Product verification must operate on all 41 live files for the accepted baseline and show:

- manifest source count and per-source hash;
- raw OOXML numeric count versus raw ledger count, with zero missing/extra/mismatched values;
- semantic disposition coverage of raw numeric cells;
- explicit tests for formula/cached-value handling and textual missing markers;
- internet/local pipeline equivalence on identical bytes;
- CSV roundtrip equality for stable keys/exact values;
- provenance resolution from prepared observation/view back to source cell;
- fail-closed response to an unseen structural variant.

## Limit

The raw ledger preserves source values, not the intent of every numeric cell. Semantic correctness is separately governed by T-CBR-ID. Forward compatibility means safe detection and transparent failure, not guaranteed automatic interpretation of arbitrary future workbook changes.

## Reopen

Reopen if the product changes numeric representation, source acquisition/revision semantics, formula treatment, provenance keys, export formats or canonical conflict policy.
