# Maintenance and source-change procedure

## Principle

A Bank of Russia workbook is an external statistical contract expressed through an Excel presentation. Presentation drift is accepted only when the source-aware parser still proves the same statistical interpretation. Unknown structural or semantic variants fail closed.

## Routine rebuild

1. Run a fresh online build into the normal output path. The implementation creates a sibling staging candidate automatically.
2. Confirm all reviewed registry sources were acquired.
3. Review `build_manifest.json`, `validation.json` and `diagnostics.json`.
4. Compare source SHA-256 values with the prior accepted build.
5. For changed revisions, inspect sheet structure, period bindings, concept/dimension changes and raw-cell dispositions.
6. Run the offline replay from the newly bound `sources/` directory.
7. Confirm the same `build_id` and byte-identical deterministic CSV tables.
8. Run independent OOXML preservation verification.

A changed hash means a new source revision and enters the normal validation path.

## Staging and promotion

Every build attempt is materialized under a sibling `.<output>.staging-*` directory. The requested output path changes only after acquisition, parsing, validation and persistence complete successfully.

If a prior successful output exists, it remains untouched throughout candidate construction. Promotion temporarily moves the prior output to a sibling backup, moves the validated staging candidate into the requested path, then removes the backup. If promotion itself fails, the implementation restores the previous output where the filesystem operation permits it.

A failed build retains its staging directory for diagnosis. When failure occurs during source semantic processing, the retained evidence includes:

- `source_manifest.acquisition.json`;
- acquired source workbooks;
- `failure.json` with source revision and failure type;
- `failure-evidence/<source_id>-raw.csv` for the failing source.

A successful promoted build removes the failure-only acquisition manifest and exposes one canonical `source_manifest.json`.

## Hard stop conditions

Treat a complete build as invalid when any of the following occurs:

- a required registry source cannot be acquired or bound;
- more than one local file resolves for a source;
- workbook bytes do not match the recorded hash;
- a material numeric sheet has no recognized period/observation contract;
- an observation loses exact raw-cell lineage;
- a raw source cell lacks a disposition;
- a numeric source cell remains `unmapped_numeric`;
- a concept identity collides with different content;
- one complete semantic key contains conflicting values;
- an unknown source layout would require guessing from label similarity;
- observations in one complete build do not share one `build_id`.

## Reviewing a changed source

### 1. Determine whether change is presentation-only

Examples include whitespace or typographic-dash changes, cell styling, harmless comments and a period extension following the same proven geometry. The parser may continue unchanged when observations, dimensions and lineage remain valid.

### 2. Determine whether statistical semantics changed

Review changes to population or institutional sector, row/column classification, unit/scale, stock/flow interpretation, period/frequency, currency denomination versus measurement currency, overdue status, maturity, valuation, seasonal adjustment, acquired-rights treatment, territorial aggregation and methodology notes affecting comparability.

A semantic change requires a reviewed adapter/source-contract change. It is never resolved by weakening conflict checks or adding aggressive generic text normalization.

### 3. Preserve source identity boundaries

A continuing registry publication keeps its `source_id`; different workbook bytes create a new SHA-based `source_revision_id`. If a registry entry becomes a materially different statistical product, review whether it requires a new product source identity rather than reusing the old concept space.

## Adding a registry source

The runtime registry is reviewed and static. To add a source:

1. establish the authorized registry input;
2. add one `SourceSpec` with stable identity, RU/EN names, family, row axis/parser and known classification/period role;
3. inspect the workbook exhaustively;
4. add or refine source-aware parsing semantics;
5. add focused fixtures for distinctive geometry and statistical dimensions;
6. execute full live build and offline replay;
7. review duplicate/conflict results and raw-cell dispositions;
8. run independent preservation verification;
9. update schema/documentation for newly material semantics.

## Translation maintenance

Russian source labels remain the evidence-bearing source text. English display names are project translations or transparent transliteration fallbacks unless an official English source establishes otherwise. Preserve `translation_status` and the exact Russian label; presentation changes never redefine semantic identity.

## Stable consumer identities

Consumers should prefer:

- `build_id` for an exact complete build;
- `source_id` for publication identity;
- `source_revision_id` for exact workbook revision;
- `source_concept_id` for source-local concept identity;
- explicit dimensions for statistical slices.

Worksheet coordinates remain provenance locators. Row numbers, display names and normalized text are not durable business identities.

## Recovery and acceptance

Build success, independent verification, integration, release and deployment are separate states. A green build candidate should be verified against its exact commit/configuration before it is treated as the accepted Product state. Keep the prior accepted output until the new candidate has passed the required acceptance path.
