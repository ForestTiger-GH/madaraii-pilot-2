# Maintenance and source-change procedure

## Principle

A Bank of Russia workbook is an external statistical contract expressed through an Excel presentation. Presentation drift is admitted only when the source-aware parser still proves the statistical interpretation. Unknown structural or semantic variants fail closed.

## Routine rebuild

1. Run a fresh online build into the normal output path.
2. Confirm the complete reviewed registry was acquired.
3. Confirm every live manifest row has `cbr_domain_ooxml_validated` trust status.
4. Review `build_manifest.json`, `validation.json` and `diagnostics.json`.
5. Compare source SHA-256 values with the prior accepted build.
6. For changed revisions, inspect sheet structure, period bindings, concept/dimension changes and raw-cell dispositions.
7. Run offline replay from the newly bound `sources/` directory.
8. Confirm the same `build_id` and deterministic Product tables under the same code/runtime.
9. Run independent OOXML preservation verification.
10. Run the post-Jester contract and publication-metadata applicability checks.

A changed source hash creates a new source revision and enters the normal validation path.

## Source trust boundary

The live registry URL and final resolved URL must stay on `cbr.ru` or a subdomain. The implementation may retry a `www.cbr.ru` HTTP-403 request on `cbr.ru` with the same path/query; it does not follow a source outside the CBR trust domain.

Downloaded and locally bound XLSX files must be valid OOXML workbook packages: valid ZIP, required workbook/content-type relationships, at least one worksheet and clean CRC. A `PK` prefix alone is insufficient.

Acquisition/local binding writes a diagnostic acquisition manifest before the complete-source admission gate. This retains source-local failures instead of collapsing them into one generic error.

## Build identity

`build_id` binds:

- build-contract version;
- exact source-specification fingerprint;
- exact sorted source revisions;
- package implementation SHA-256;
- resolved Python, requests, openpyxl and pandas versions.

A source, semantic implementation or bound-runtime change therefore creates a distinct build identity. Acquisition timestamps and output paths remain outside semantic identity.

## Staging and promotion

Every Product build is materialized under a sibling `.<output>.staging-*` directory. The requested output path changes only after acquisition, parsing, validation and persistence complete successfully.

If a prior successful output exists, it remains available during candidate construction. Promotion moves the prior output to a sibling backup, moves the validated staging candidate into place and removes the backup. Promotion interruption restores the previous output where filesystem semantics permit it.

A failed build retains its staging directory. Evidence may include:

- `source_manifest.acquisition.json`;
- acquired source workbooks;
- `failure.json`;
- `failure-evidence/<source_id>-raw.csv` for source-local semantic failures.

A successful promoted build removes the failure-only acquisition manifest and exposes one canonical `source_manifest.json`.

Direct SQLite writing is separately transactional: build a sibling candidate DB, run `PRAGMA integrity_check`, then `os.replace`. Failure preserves the previous DB.

## Hard stop conditions

Treat a complete build as invalid when any of the following occurs:

- a required registry source cannot be acquired or bound;
- the requested/resolved live URL leaves the CBR trust domain;
- a workbook fails OOXML structural validation;
- more than one local file resolves for a source;
- workbook bytes disagree with the recorded hash;
- a material numeric sheet has no recognized period/observation contract;
- methodology/change-log material is misbound as statistical periods;
- observation, concept, raw-cell or disposition source ownership disagrees;
- source revision or raw locator lineage disagrees;
- one raw cell backs multiple observations;
- a raw source cell lacks a disposition;
- a numeric source cell remains `unmapped_numeric`;
- a period is not a real canonical ISO date;
- frequency/period-role/unit/scale fall outside the admitted domain;
- one complete semantic key contains conflicting values;
- an unknown source layout would require guessing from label similarity;
- complete-build observations do not share one build identity;
- bilingual user surfaces are incomplete.

## Reviewing a changed source

### 1. Determine whether the change is presentation-only

Examples include whitespace, typographic punctuation, styling or a period extension following the same proven geometry. Continue unchanged only when observations, source-visible identities, dimensions and lineage remain valid.

### 2. Determine whether statistical semantics changed

Review population/institutional sector, measure definition, hierarchy/merged parents, row/column classification, unit/scale, stock/flow role, period/frequency, currency denomination versus measurement currency, overdue status, maturity, valuation, adjustment, acquired-rights treatment, territorial aggregation and methodology notes.

A semantic change requires a reviewed source-adapter/contract change. Keep the strict conflict gate; correct the semantic identity instead of weakening validation.

### 3. Preserve source-visible identity

A continuing registry publication keeps its `source_id`; different bytes create a new SHA-based `source_revision_id`.

Repeated source labels may require source-visible context such as period-block heading, merged parent, stable section ancestry, exact maturity parent or explicit measure heading. Physical row numbers remain provenance coordinates and should not become ordinary concept identity.

### 4. Keep dimension inference conservative

Check positive and negated cues separately. Avoid assigning a canonical maturity/currency/other qualifier when the source combines categories or the scope boundary is ambiguous.

Inherited structural scope is appropriate for proven branch children. Review unique aggregates following a branch: a preceding heading does not automatically govern a later total.

### 5. Review publication metadata applicability

Audit hidden sheets/rows/columns, comments and number formats across the changed source. Their presence alone does not make them statistical semantics. Add a Product rule only when evidence shows that the metadata controls meaning, publication status or numeric interpretation.

## Adding a registry source

The runtime registry is reviewed and static. To add a source:

1. establish the authorized registry input;
2. add one `SourceSpec` with stable identity, RU/EN names, family, row axis/parser and known classification/period role;
3. inspect the workbook exhaustively;
4. add/refine source-aware parsing semantics;
5. add focused fixtures for distinctive geometry and statistical dimensions;
6. execute full live build and offline replay;
7. review duplicate/conflict results and raw-cell dispositions;
8. run independent preservation, post-Jester contract and publication-metadata checks;
9. update Target HOW/schema/documentation for material new semantics;
10. route the exact candidate through normal verification/admission.

## Translation maintenance

Russian source labels remain the evidence-bearing source text. English display names are project translations or transparent transliteration unless an official English source establishes otherwise.

Preserve `translation_status` and source text. Source catalog and reusable dimension-member display/filter surfaces must remain RU/EN complete.

## Stable consumer identities

Consumers should prefer:

- `build_id` for an exact processing/source/runtime state;
- `source_id` for publication identity;
- `source_revision_id` for exact workbook revision;
- `source_concept_id` for source-local semantic identity;
- explicit dimensions for statistical slices.

Worksheet coordinates remain provenance locators. Row numbers, display names and normalized text are not durable business identities.

## Consumer reliance

Ordinary `UnifiedDatabase` access requires embedded validation status `passed`. Use `allow_unvalidated=True` only for explicit diagnosis.

A pivot must remain semantically homogeneous. If hidden unit, scale, frequency or period-role differences would be collapsed into one displayed series, narrow the selection or expose those fields.

## Recovery and acceptance

Build success, independent verification, Product admission, closure, release and deployment are distinct states. Verify the exact candidate state before `MADARAII-34` admission. Keep the prior accepted Product current until the successor is admitted. Closure audit follows integration and audits the exact integrated state rather than repairing it.
