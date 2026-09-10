# Maintenance and source-change procedure

## Principle

A Bank of Russia workbook is an external statistical contract expressed through an Excel presentation. The product may tolerate presentation drift only when the existing source-aware parser still proves the same statistical interpretation.

Unknown structural or semantic variants fail closed.

## Routine rebuild

1. Run a fresh online build.
2. Confirm all reviewed registry sources were acquired.
3. Review `validation.json` and `diagnostics.json`.
4. Compare source SHA-256 values with the prior accepted build.
5. For changed revisions, inspect sheet structure, period bindings, concept/dimension changes and raw-cell dispositions.
6. Run the offline replay from the newly bound `sources/` directory.
7. Compare deterministic CSV tables between online build and replay.

A changed hash alone is not an error. It means the source revision changed and requires the normal validation path.

## Hard stop conditions

Treat the build as invalid when any of the following occurs:

- a required registry source cannot be acquired or bound;
- more than one local file resolves for a source;
- workbook bytes do not match the recorded hash;
- a material sheet with numeric data has no recognized period/observation contract;
- an observation loses its exact raw-cell lineage;
- a raw source cell lacks a disposition;
- a concept identity collides with different content;
- a semantic key contains conflicting values;
- an unknown source layout is accepted only because labels look similar.

## Reviewing a changed source

For each changed workbook:

### 1. Determine whether change is presentation-only

Examples:

- whitespace or typographic dash change;
- column width/style change;
- harmless source comment addition;
- period extension following the same geometry.

The parser may continue to work unchanged when the resulting observations, dimensions and lineage remain valid.

### 2. Determine whether statistical semantics changed

Review changes to:

- population or institutional sector;
- row/column classification;
- unit or scale;
- stock/flow interpretation;
- period meaning or frequency;
- currency denomination versus measurement currency;
- overdue status;
- maturity basis/bucket;
- valuation basis;
- seasonal adjustment;
- acquired-rights treatment;
- territorial aggregation;
- source methodology notes that alter comparability.

A semantic change requires a reviewed adapter/source-contract change. Do not solve it through a more aggressive generic text normalizer.

### 3. Preserve prior source identity boundaries

A new workbook revision keeps its `source_id` when it is the continuing publication represented by the registry entry. Its `source_revision_id` changes with SHA-256.

If the Bank of Russia replaces one publication with a materially different statistical product, review whether a new product `source_id` is required rather than silently reusing the old concept space.

## Adding a new registry source

The product registry is intentionally reviewed and static at runtime.

To add a source:

1. establish the authorized registry input;
2. add one `SourceSpec` with stable `source_id`, names, family, row axis/parser and known classification/period role;
3. inspect the workbook exhaustively;
4. add or refine source-aware parsing semantics;
5. add fixtures/contracts for distinctive geometry;
6. execute full live build and offline replay;
7. review duplicate/conflict report and raw-cell dispositions;
8. update schema/documentation only for newly material semantic dimensions.

## Translation maintenance

Russian source labels remain the identity-bearing evidence. English display names are project translations/transliterations unless an official English source establishes otherwise.

Do not replace source Russian text to improve English usability. Add or refine the English projection while retaining `translation_status` and the original source label.

## Backward compatibility

Stable analytical consumers should prefer:

- `source_id` for publication identity;
- `source_concept_id` for source-local concept identity;
- explicit dimensions for statistical slices;
- `source_revision_id` when exact historical reproducibility is required.

Consumers should not use row numbers, worksheet coordinates or display strings as long-lived semantic IDs. Coordinates remain provenance locators, not business identities.

## Recovery

A failed build writes only into its selected output directory. The accepted prior build remains untouched when builds use a new output directory.

For production use, build into a candidate directory, verify it, then switch the consumer-facing pointer/path atomically. Keep the prior accepted directory until the new build is accepted.
