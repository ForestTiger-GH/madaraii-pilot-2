# CBR Unified Statistics

`cbr-unified-statistics` builds one provenance-aware analytical database from the Bank of Russia Excel files declared in the reviewed project registry.

The product combines two obligations:

1. every material source cell remains reconstructable from the output;
2. analytical observations are normalized enough for filtering, DataFrame work and pivoting while statistically different concepts remain distinct.

## What a successful build produces

```text
<output>/
├── source_manifest.json
├── build_manifest.json         # canonical build identity/evidence manifest
├── build.json                  # generated compatibility alias
├── sources/                    # exact source workbooks bound by SHA-256
└── data/
    ├── cbr_unified.sqlite
    ├── source_revisions.csv
    ├── raw_cells.csv
    ├── source_concepts.csv
    ├── dimension_members.csv
    ├── observations.csv
    ├── cell_dispositions.csv   # canonical raw-cell disposition export
    ├── raw_cell_dispositions.csv  # generated compatibility alias
    ├── diagnostics.json
    └── validation.json
```

`raw_cells` is the preservation layer. `observations` is the analytical layer. They are linked by `raw_cell_id` and `source_revision_id`. Every observation also carries the deterministic `build_id` of the complete source-revision/specification set that produced it.

## Installation

```bash
python -m pip install -e .
```

For development and verification:

```bash
python -m pip install -e ".[test]"
```

Python 3.10+ is supported.

## Build from Bank of Russia URLs

```bash
cbr-unified build --output ./build/cbr
```

The command downloads the complete reviewed source universe, records redirects and HTTP metadata where available, hashes every workbook, extracts raw OOXML cells, constructs semantic observations, validates the candidate and writes CSV + SQLite outputs.

Every attempt is built in a sibling staging directory. The requested output path changes only after the candidate passes processing, validation and persistence. If an attempt fails, an existing successful output remains intact and the failed staging directory keeps acquisition/failure evidence for diagnosis.

A complete build fails closed when a required source is missing, a workbook has an unrecognized material structure, an observation loses source lineage, a raw cell loses disposition, an unexplained numeric source cell remains, or conflicting semantic duplicates appear.

`build_manifest.json` records the build contract version, source-specification fingerprint, source revisions, validation result and diagnostics. `build_id` is deterministic for the same processing contract, source specifications and source revisions; acquisition timestamps do not change it.

## Offline and reproducible replay

After one successful online build:

```bash
cbr-unified build --input-dir ./build/cbr/sources --output ./build/cbr-replay
```

Local binding accepts either `<source_id>.xlsx` or the original registry filename. Exactly one binding must resolve for each source. For identical source revisions and product specification, online and offline builds must produce the same `build_id` and deterministic analytical/preservation tables.

## Query from CLI

List source revisions:

```bash
cbr-unified sources --db ./build/cbr/data/cbr_unified.sqlite
```

Search indicators in Russian:

```bash
cbr-unified indicators \
  --db ./build/cbr/data/cbr_unified.sqlite \
  --text "ипотеч" \
  --language ru
```

Search the English project surface:

```bash
cbr-unified indicators \
  --db ./build/cbr/data/cbr_unified.sqlite \
  --text "mortgage" \
  --language en
```

Filter observations:

```bash
cbr-unified query \
  --db ./build/cbr/data/cbr_unified.sqlite \
  --source mortgage_debt \
  --start 2025-01-01 \
  --end 2026-08-01 \
  --dim currency_category=rubles \
  --language ru \
  --csv ./mortgage.csv
```

Dimensions are passed as `--dim key=value`. Common dimensions include `currency_category`, `region`, `region_type`, `activity`, `classification`, `overdue`, `maturity_bucket`, `maturity_basis`, `adjustment`, `valuation`, `statement_side`, `measurement_currency`, `acquired_claims` and source-specific qualifiers.

Trace one observation back to the exact workbook cell:

```bash
cbr-unified lineage --db ./build/cbr/data/cbr_unified.sqlite <observation_id>
```

The lineage result includes `build_id`, source revision, workbook SHA-256, sheet, cell coordinate, raw OOXML lexical value, formula where present and the raw-cell disposition.

## Python / pandas

```python
from cbr_unified import UnifiedDatabase


db = UnifiedDatabase("./build/cbr/data/cbr_unified.sqlite")

df = db.observations(
    source_ids="mortgage_debt",
    start="2025-01-01",
    dimensions={"currency_category": "rubles"},
    language="ru",
)

wide = db.pivot(
    source_ids="mortgage_debt",
    dimensions={"currency_category": "rubles", "region": "РОССИЙСКАЯ ФЕДЕРАЦИЯ"},
    index="period",
    columns="indicator",
    language="ru",
)
```

`value_exact` retains the source numeric lexical representation. The convenience `value` column is numeric for pandas work. Use `decimal_values=True` when exact `Decimal` values are required in Python.

`pivot()` performs no implicit aggregation. If several observations would occupy one requested pivot cell, it raises `QueryError` and requires additional filters or dimensions.

## Statistical identity

The database does not treat a visually similar row name as a universal indicator identity.

A semantic observation is bound to:

- source revision;
- source-local concept;
- period and frequency;
- stock/flow/change role where known;
- unit and scale;
- explicit dimensions;
- exact source sheet and cell;
- exact raw-cell lineage;
- complete build identity.

This prevents collisions such as:

- `1.1` versus `11` after punctuation stripping;
- ruble denomination versus a USD measurement unit;
- original versus remaining maturity;
- nominal versus market valuation;
- original versus seasonally adjusted series;
- historical activity classification versus OKVED2;
- ordinary regions versus inclusive/exclusive territorial aggregates;
- ordinary mortgage debt versus acquired claims only versus debt including acquired claims;
- structurally identical workbooks describing different statistical populations.

For `obs_table_20s`, currency denomination and measurement currency are separate dimensions. `Активы/Пассивы - валюта` denotes foreign-currency denomination, while `Активы/Пассивы - в ин. валюте $` additionally sets `measurement_currency=USD`.

## Russian and English names

Russian source text is preserved separately from normalized search text and display labels.

English names are a project-facing semantic surface. `translation_status` distinguishes project translation and transparent transliteration fallback. English text never replaces the Russian source identity and is not represented as an official Bank of Russia translation unless the source itself establishes that status.

## Preservation model

The raw layer reads XLSX as OOXML rather than relying only on pandas/openpyxl interpretation. For every non-empty stored cell it keeps:

- source and source revision;
- workbook SHA-256;
- exact sheet title and coordinate;
- OOXML type and style index;
- raw `<v>` lexical value;
- resolved shared/inline text;
- formula text when present.

Semantic parsing uses the raw lexical numeric value as the preferred analytical value and openpyxl for workbook structure/date interpretation. Source-specific semantic compatibility views may normalize proven presentation variants only for interpretation; raw evidence always remains tied to the untouched workbook.

Every raw cell receives a disposition. Typical roles are `observation_value`, `period_key`, `source_cell`, `hierarchy_or_header_code`, `source_metadata_numeric` and other explicit non-observation roles. `unmapped_numeric` is a blocking residue in a complete build.

## Validation and verification

`validation.json` records build-level invariants and coverage, including:

- one complete build identity;
- complete registry source universe;
- unique source revisions and raw-cell identities;
- complete raw-cell disposition coverage;
- zero unresolved numeric source cells;
- observation-to-raw lineage coverage;
- concept references;
- source observation coverage;
- ISO period anchors;
- valid decimal observation values;
- semantic duplicate/conflict detection;
- counts by source, period, frequency and disposition role.

Inspect it through:

```bash
cbr-unified validate --db ./build/cbr/data/cbr_unified.sqlite
```

Repository verification additionally performs a live 41-source build, offline replay, byte comparison of deterministic CSV outputs, CSV↔SQLite count reconciliation, CLI/query smoke checks and an independent stdlib OOXML re-extraction that compares every preserved raw-cell locator/type/style/value/formula and every observation value against the source workbook.

## Failure evidence

If semantic processing fails after a source has been acquired, the retained staging directory contains:

- `source_manifest.acquisition.json`;
- `failure.json`;
- `failure-evidence/<source_id>-raw.csv` for the failing source where available;
- the already acquired source workbooks.

A successful promoted output removes the failure-only acquisition manifest and exposes one canonical `source_manifest.json`.

## Source changes

The registry is a reviewed product input, not a dynamic dependency on the original repository. A changed workbook receives a new SHA-based `source_revision_id`.

Presentation changes that remain compatible with an explicit parser contract can build normally. Material unrecognized variants fail closed through `SourceVariantError` or validation. The required response is to review the changed source contract and update the adapter; the product does not guess through an unknown layout.

## Repository structure

```text
src/cbr_unified/
├── registry.py       # reviewed source universe and source contracts
├── acquisition.py    # online acquisition and exact local binding
├── raw.py            # lossless OOXML-cell extraction
├── normalization.py  # conservative text/period/unit/dimension helpers
├── semantic.py       # source-aware semantic observation extraction
├── processing.py     # checked semantic gate and explicit presentation adapters
├── validation.py     # integrity and statistical-conflict checks
├── persistence.py    # CSV and SQLite materialization
├── query.py          # pandas/query/pivot/lineage facade
├── build.py          # staging, build identity, validation and promotion
└── cli.py            # command-line surface
```

See `docs/SCHEMA.md` for table semantics, `docs/MAINTENANCE.md` for source-change handling and `examples/quickstart.py` for notebook-oriented use.
