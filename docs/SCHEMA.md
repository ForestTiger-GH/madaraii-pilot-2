# Data model

The Product separates preservation from interpretation. The same source value may appear in linked raw and semantic forms with different responsibilities.

## Build identity

A successful build has one deterministic `build_id` derived from:

- build-contract version;
- reviewed exact source-specification fingerprint;
- exact sorted source revisions;
- implementation SHA-256 over the package Python modules;
- resolved Python, requests, openpyxl and pandas versions.

Acquisition timestamps and output paths do not affect identity. Code/runtime changes do.

`build_manifest.json` is the canonical build evidence manifest. `build.json` is a generated compatibility alias. Validation carries the same implementation/runtime fingerprint and every observation carries the same `build_id`.

## `source_revisions`

One row per bound workbook revision.

Primary key: `source_revision_id = <source_id>@sha256:<sha256>`.

Persisted material fields include stable source ID, requested/resolved URL, registry filename, final local source path, SHA-256, size, selected HTTP metadata and acquisition timestamp. The root `source_manifest.json` additionally owns acquisition trust evidence, including `trust_status`. Live manifest revisions require `cbr_domain_ooxml_validated`; local replay uses `local_ooxml_validated` before Product validation.

## `raw_cells`

Lossless OOXML preservation table. One row per non-empty stored XLSX cell.

Primary key: `raw_cell_id`, deterministically derived from exact source revision + exact sheet title + cell coordinate.

Material fields:

- source/revision owner and workbook SHA-256;
- `sheet_exact`, `cell_coordinate`;
- `ooxml_type`, `style_index`;
- `value_lexical`;
- `text_resolved`;
- `formula`.

This table makes no statistical-observation claim.

## `cell_dispositions`

Exactly one disposition exists for every raw cell. The SQLite physical table remains `raw_cell_dispositions`; `cell_dispositions.csv` is the canonical export and `raw_cell_dispositions.csv` is a compatibility alias.

Typical roles include `observation_value`, `period_key`, `source_metadata_numeric`, `hierarchy_or_header_code` and `source_cell`. `unmapped_numeric` is blocking in a complete build.

Disposition source/revision ownership must equal the corresponding raw-cell owner.

## `source_concepts`

Source-local statistical concept identities. Primary key: `source_concept_id`.

The Product intentionally avoids one universal indicator key. Concept identity is derived from source ID plus a stable source-local semantic key. Physical row number is excluded from ordinary identity.

Depending on source geometry, the semantic key may include:

- exact measure title and unit/scale signature;
- source-visible hierarchy ancestry;
- repeated period-block heading;
- merged parent context;
- stable section anchor;
- exact short-/long-term source parent label;
- explicit exchange-rate measure definition.

These contexts distinguish repeated source concepts without fuzzy cross-source merging or coordinate identity.

Material fields include `source_local_key`, source owner, exact Russian source label, normalized Russian label, RU/EN display names, translation status, row axis and source context.

## `dimension_members`

Reusable dimension labels, especially regions and activities. A member retains dimension/classification, exact Russian source value, RU/EN display values and translation status.

The query layer may accept the source/Russian value, Russian display value or English display value as an equivalent filter for a cataloged member.

## `observations`

Analytical fact table. Every row points to exactly one raw source cell and one source concept and carries the build identity.

Material fields:

- `build_id`;
- `source_id`, `source_revision_id`, `source_concept_id`;
- `period`, `frequency`, `period_role`;
- `unit`, `scale`;
- canonical `dimensions_json`;
- exact source sheet/cell and `raw_cell_id`;
- `value_exact`, `value_kind`;
- source-row provenance fields used for diagnostics.

`period` is a real canonical ISO date (`YYYY-MM-DD`). `frequency` is constrained to the admitted domain; `period_role` separates stock, flow, published change and source-defined cases.

One raw cell may back at most one observation.

### Dimensions

`dimensions_json` is a canonical sorted JSON object. Current dimensions may include:

- `currency_category`;
- `region`, `region_type`;
- `activity`, `activity_code`, `classification`;
- `overdue`, `acquired_claims`;
- `maturity_bucket`, `maturity_basis`;
- `adjustment`, `valuation`, `frequency_sheet`;
- `statement_side`, `measurement_currency`;
- `sme_scope`, `entrepreneur_scope`, `escrow_coverage`.

Dimensions are added conservatively. Negated cues take precedence over positive substrings; ambiguous combined buckets may be omitted. Structural currency inheritance is retained for evidenced repeated branches and removed from later unique aggregates when the source does not establish continued scope.

Denomination and measurement currency remain separate axes.

## Statistical identity rule

Two rows are candidates for the same semantic observation only when every material semantic axis agrees. Text similarity and workbook coordinates are insufficient.

Validation groups candidates by:

`source_id + source_concept_id + period + frequency + period_role + unit + scale + canonical dimensions_json`.

Different values under the same complete key are a hard conflict. Same-valued repetitions remain stored and are reported as identical semantic duplicate groups.

## Ownership and lineage rule

A valid observation chain has one coherent source owner and revision across:

`source_manifest → raw_cell → disposition → observation`,

while the referenced concept must have the same source owner. The observation sheet/cell locator must equal its raw-cell locator and the raw-cell file hash must equal the manifest hash.

The query lineage projection exposes observation, concept, raw and disposition source owners separately so this invariant remains inspectable after persistence.

## Consumer reliance

`UnifiedDatabase` opens validated databases by default. Diagnostic access to a failed/unvalidated database requires explicit `allow_unvalidated=True`. The CLI `validate` command is the explicit diagnostic surface and can display embedded failed validation; other consumer commands retain the fail-closed boundary.

Indicator discovery searches concept labels and the bilingual dataset/source context. Dataset context improves discoverability without becoming concept identity.

Pivoting is non-aggregating and also rejects a displayed series that mixes hidden unit/scale/frequency/period-role signatures.

## SQLite and CSV parity

CSV and SQLite are projections of the same validated owner set. Verification reconciles them. Neither becomes an independent semantic truth owner.

Direct SQLite materialization uses a temporary sibling database, integrity check and atomic replacement. A failed write preserves the prior database.

The exact source workbook remains ultimate raw evidence; `raw_cells` is the reproducible preservation representation and `observations` is the admitted analytical interpretation.
