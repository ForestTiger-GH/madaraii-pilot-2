# Data model

The product separates preservation from interpretation. The same source value therefore appears in linked raw and semantic forms with different responsibilities.

## Build identity

A successful build has one deterministic `build_id` derived from the processing-contract version, reviewed source-specification fingerprint and exact sorted source revisions. Acquisition timestamps and output paths do not change this identity.

`build_manifest.json` is the canonical build evidence manifest. `build.json` is a generated compatibility alias. Every semantic observation carries the same `build_id`.

## `source_revisions`

One row per bound workbook revision.

Primary key: `source_revision_id = <source_id>@sha256:<sha256>`.

Material fields include stable `source_id`, requested/resolved URL, registry filename, final local source path, SHA-256, size, HTTP metadata and acquisition timestamp. A later workbook with the same URL but different bytes is a different source revision.

## `raw_cells`

Lossless OOXML preservation table. One row per non-empty stored XLSX cell.

Primary key: `raw_cell_id`, deterministically derived from source revision + exact sheet title + cell coordinate.

Material fields:

- `sheet_exact`, `cell_coordinate` — source locator;
- `ooxml_type`, `style_index` — source representation metadata;
- `value_lexical` — exact text stored in `<v>` when present;
- `text_resolved` — shared-string or inline-string resolution;
- `formula` — formula expression where present.

This table does not claim that a cell is a statistical observation.

## `cell_dispositions`

One and only one disposition for every `raw_cells` row. The SQLite physical table remains `raw_cell_dispositions`; `cell_dispositions.csv` is the canonical Target-HOW export and `raw_cell_dispositions.csv` is a generated compatibility alias with identical rows.

Typical roles include `observation_value`, `period_key`, `source_metadata_numeric`, `hierarchy_or_header_code` and `source_cell`. `unmapped_numeric` denotes unresolved numeric source content and blocks a complete build.

## `source_concepts`

Source-local statistical concept identities. Primary key: `source_concept_id`.

The product intentionally avoids one universal indicator key. Equivalent-looking labels from different source populations, classifications or methodological contexts retain separate source concepts unless an explicit cross-source equivalence is established later.

Material fields include `source_local_key`, exact Russian source label/context, conservative normalized label, RU/EN display names, `translation_status`, row axis and source context.

## `dimension_members`

Reusable labels for dimensions that benefit from explicit identities, especially region and activity members. A member retains source text, classification and RU/EN project display surfaces.

## `observations`

Analytical fact table. Every row points to exactly one raw source cell and one source concept and carries the build identity.

Material fields:

- `build_id`;
- `source_revision_id`, `source_concept_id`;
- `period`, `frequency`, `period_role`;
- `unit`, `scale`;
- `dimensions_json`;
- exact source sheet/cell and `raw_cell_id`;
- `value_exact`, stored as text to preserve source numeric lexical representation;
- `value_kind`.

`period` is an ISO anchor (`YYYY-MM-DD`). `frequency` states how that anchor is interpreted. `period_role` separates stock, flow, published change and source-defined cases.

### Dimensions

`dimensions_json` is a sorted JSON object. This keeps one observation table while allowing source-specific statistical qualifiers.

Current dimensions may include:

- `currency_category`;
- `region`, `region_type`;
- `activity`, `activity_code`, `classification`;
- `overdue`, `acquired_claims`;
- `maturity_bucket`, `maturity_basis`;
- `adjustment`, `valuation`, `frequency_sheet`;
- `statement_side`, `measurement_currency`;
- `sme_scope`, `entrepreneur_scope`, `escrow_coverage`.

Denomination and measurement currency are separate. For example, `obs_table_20s` may carry `currency_category=foreign_currency` and independently `measurement_currency=USD`.

## Statistical identity rule

Two rows are candidates for the same semantic observation only when all material identity axes agree. Text similarity and workbook geometry are insufficient.

Validation checks duplicate candidates over:

`source_id + source_concept_id + period + frequency + period_role + unit + scale + dimensions_json`.

Different values under the same complete key are a hard conflict. Same-valued repetitions remain stored and are reported.

## SQLite and CSV parity

CSV tables are human-readable projections of the stored rows. SQLite is the indexed query representation. Verification reconciles row counts and deterministic content; neither surface is a separate semantic truth owner.

The source workbooks and hashes remain the ultimate raw evidence. `raw_cells` is the reproducible preservation representation; `observations` is the analytical interpretation.
