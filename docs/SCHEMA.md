# Data model

The product separates preservation from interpretation. The same source value therefore appears in two linked forms with different responsibilities.

## `source_revisions`

One row per bound workbook revision.

Primary key: `source_revision_id = <source_id>@sha256:<sha256>`.

Material fields:

- `source_id` — stable project source identity from the reviewed registry;
- `requested_url`, `resolved_url` — acquisition lineage;
- `registry_filename` — filename declared by the reviewed source registry;
- `local_path` — bound build input;
- `sha256` — exact workbook content identity;
- HTTP metadata and acquisition timestamp where available.

A later workbook with the same URL but different bytes is a different source revision.

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

## `raw_cell_dispositions`

One and only one disposition for every `raw_cells` row.

Typical roles:

- `observation_value` — cell is used as an analytical numeric observation;
- `period_key` — cell establishes an observation period;
- `source_metadata_numeric` — numeric content belongs to a metadata surface;
- `hierarchy_or_header_code` — numeric content contributes to source hierarchy/header semantics;
- `non_observation_numeric` — numeric cell lacks an admitted period binding and remains preserved;
- `source_cell` — preserved source content with no more specific role.

Complete disposition coverage is a validation invariant.

## `source_concepts`

Source-local statistical concept identities.

Primary key: `source_concept_id`.

The product intentionally avoids one global universal indicator key. Equivalent-looking labels from different source populations, classifications or methodological contexts retain separate source concepts unless an explicit cross-source equivalence is established later.

Material fields:

- `source_local_key` — source-scoped concept identity basis;
- `label_ru_source` — original Russian source label/context;
- `label_ru_normalized` — conservative search representation;
- `name_ru` — readable Russian project name;
- `name_en` — English project surface;
- `translation_status` — translation provenance;
- `row_axis` — indicator, region, activity, hierarchy or mixed source geometry;
- `source_context` — workbook/sheet context needed to interpret the concept.

## `dimension_members`

Reusable labels for dimensions that benefit from explicit identities, currently especially region and activity members.

A dimension member carries source text plus Russian/English project display fields and classification when material.

## `observations`

Analytical fact table.

Every row points back to exactly one raw source cell and one source concept.

Material identity fields:

- `source_revision_id`;
- `source_concept_id`;
- `period`;
- `frequency`;
- `period_role`;
- `unit` and `scale`;
- `dimensions_json`;
- exact source locator.

Value fields:

- `value_exact` — source numeric lexical representation, stored as text to avoid binary-float loss;
- `value_kind` — numeric, numeric text or cached formula value.

`period` is an ISO anchor (`YYYY-MM-DD`). `frequency` states how that anchor is interpreted. `period_role` separates stock, flow, published change and source-defined cases.

### Dimensions

`dimensions_json` is a sorted JSON object. This preserves extensibility while keeping one observation table.

Dimensions may include:

- `currency_category`;
- `region`, `region_type`;
- `activity`, `activity_code`, `classification`;
- `overdue`;
- `maturity_bucket`, `maturity_basis`;
- `adjustment`;
- `valuation`;
- `frequency_sheet`;
- `statement_side`;
- `measurement_currency`;
- `acquired_claims`;
- `sme_scope`, `entrepreneur_scope`, `escrow_coverage`.

The exact dimension universe can grow when a reviewed source contract requires another statistically material distinction.

## Statistical identity rule

Two rows are candidates for the same semantic observation only when all material identity axes agree. Text similarity and workbook geometry are insufficient.

The validation layer therefore checks duplicate candidates over:

`source_id + source_concept_id + period + frequency + period_role + unit + scale + dimensions_json`.

Different values under the same complete key are a hard conflict and fail the build. Same-valued repetitions are retained and reported rather than silently dropped.

## SQLite and CSV parity

The CSV tables are direct human-readable projections of the stored rows. SQLite is the indexed query representation. Neither is a separate semantic truth owner.

The source workbooks and their hashes remain the ultimate evidence for raw values; `raw_cells` is the reproducible preservation representation; `observations` is the admitted analytical interpretation.
