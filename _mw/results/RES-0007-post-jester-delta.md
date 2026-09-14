# RES-DELTA-CBR-002 — Post-Jester current→target correspondence and delta

**Work kind:** `CURRENT_TARGET_CORRESPONDENCE_AND_DELTA` (`MADARAII-27`)  
**Work:** `WORK-CBR-002`  
**Current Product:** `PRODUCT-CBR-001@4ee8583b3feff7775a956c51812232fa0d0516d2`  
**Target owners:** `TW-CBR-1`, `TH-CBR-1.1`, `PRODUCT-ARCH-CBR-001`  
**Input evidence:** `WSR-JR-CBR-001..004` plus underlying Jester evidence

## Delta verdict

The Jester campaign does not establish a replacement Product concept. It exposes bounded implementation and reliance deltas inside already accepted obligations. `TW-CBR-1` remains applicable. Most changes are realization corrections under existing HOW/Architecture; a selective HOW reconciliation is required only where public reliance/build identity/source trust become more explicit.

## Typed deltas

| Delta | Current behavior | Target relation | Disposition |
|---|---|---|---|
| D01 semantic owner coherence | validation permits selected cross-owner `source_id` mismatches | TW-05/06/15; H-13 | implement blocking coherence gates |
| D02 validation semantic key | dimension JSON string ordering can split equivalent keys | TW-07/11; H-13 | canonicalize parsed dimensions before conflict grouping |
| D03 semantic domains | impossible dates and empty/absurd semantic fields can pass | TW-05/15 | validate calendar and required domains |
| D04 lineage cardinality | one raw cell can back multiple observations while top-level status is passed | TW-03/05/15 | make cardinality a blocking invariant |
| D05 wrong-role parser | technical note/methodology-shaped content can become observations | TW-04/08; H-04..H-10 | add conservative metadata/note/header rejection and regression tests |
| D06 concept durability | ordinary concept ID includes row number | TW core identity; H-08 | derive ID from source-local semantic key without row position |
| D07 measure identity | region/activity source can collapse incompatible measures into one concept | TW-05/10; H-08 | include stable measure signature in source-local concept identity |
| D08 context inference | negation, competing unit cues, combined buckets can create false qualifiers | TW-05/08 | precedence/negation-aware inference; omit ambiguous qualifier rather than guess |
| D09 numeric lexical boundary | accounting-parenthesis number-like text escapes numeric completeness | TW-03/04 | recognize standard accounting parentheses as numeric lexical form; verify against corpus |
| D10 bilingual consumer surface | source catalog lacks names; dimension output/filter remains Russian in English mode | TW-09/11 | expose bilingual source catalog and dimension display/filter mapping |
| D11 pivot homogeneity | one displayed series can mix unit/scale/frequency/period-role | TW-05/11 | fail closed when hidden semantic signature varies |
| D12 CLI dimensions | repeated same-key `--dim` silently overwrites | TW-11/13 | preserve repeated values as OR-list per dimension |
| D13 query reliance | failed embedded validation does not gate ordinary queries | TW-15; H-12/13 | default fail-closed facade with explicit diagnostic override |
| D14 lineage transparency | owner source IDs are collapsed in projection | TW-07/15 | expose observation/concept/raw/disposition owner IDs separately |
| D15 SourceSpec split authority | fingerprint can bind a caller spec while parser uses global registry spec | H-01; TW-15 | build from one source-id→spec map supplied by the build call |
| D16 build identity | build ID does not bind executable implementation/resolved runtime | TW-15; Build entity | add implementation/runtime fingerprints to build identity/evidence |
| D17 source trust | acquisition/local binding can call malformed/redirected bytes `ok` before structural proof | TW-01/02/08 | validate OOXML package structure; constrain remote resolved host to CBR domain |
| D18 publication metadata | hidden state/comments/format-only semantics are absent from raw contract | conditional TW-03/05/08 | applicability-first audit on all 41 sources; implement only evidenced classes |
| D19 direct SQLite replacement | direct reusable operation unlinks prior DB before replacement succeeds | H-11/13 | make direct writer transactional via temporary DB + atomic replace |

## No-change / bounded residue

- Default float convenience projection remains explicitly non-authoritative; `value_exact`/Decimal are exact.
- Promotion interruption under `KeyboardInterrupt` remains a separate resilience concern; ordinary failed-build protection already satisfies the accepted build transaction for caught build failures.
- Empty-table CSV headers may be improved opportunistically but are not an admission blocker.
- Generic numeric-year headers remain deliberately conservative unless current-source evidence establishes a required grammar.

## Dependency geometry

`D05+D06+D07+D08+D09` can be implemented/tested as semantic producer work. `D01..D04` independently harden the verification gate. `D10..D14` depend on persisted catalog semantics but can proceed in parallel. `D15..D17+D19` are build/runtime boundaries. `D18` is evidence-first and may end in a documented no-change disposition.

All implementation streams fan into one exact candidate. Any changed Product requires fresh `MADARAII-33` verification before `MADARAII-34` admission.