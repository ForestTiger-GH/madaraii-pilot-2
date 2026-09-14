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
    ├── cell_dispositions.csv
    ├── raw_cell_dispositions.csv  # generated compatibility alias
    ├── diagnostics.json
    └── validation.json
```

`raw_cells` is the preservation layer. `observations` is the analytical layer. They are linked by `raw_cell_id` and `source_revision_id`.

Every observation carries one deterministic `build_id`. The identity binds the processing contract, exact source-specification fingerprint, exact source revisions, implementation SHA-256 and resolved Python/requests/openpyxl/pandas versions. A code or bound-runtime change therefore creates a distinct build identity even when source bytes remain the same.

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

The command downloads the complete reviewed source universe, records HTTP/source metadata, verifies that the requested and final resolved hosts stay within `cbr.ru`, validates each workbook as an OOXML package, hashes the exact bytes, extracts raw cells, constructs semantic observations, validates the candidate and writes CSV + SQLite outputs.

A bounded `www.cbr.ru → cbr.ru` fallback may be used when the same path/query returns HTTP 403 on the `www` alias. The fallback stays inside the Bank of Russia trust boundary.

Every attempt is built in a sibling staging directory. The requested output path changes only after the candidate passes processing, validation and persistence. A failed attempt preserves an existing successful output and retains acquisition/failure evidence.

A complete build fails closed when a required source is missing, an OOXML package is malformed, a workbook has an unrecognized material structure, ownership/lineage disagree, a raw cell loses disposition, an unexplained numeric source cell remains, or conflicting semantic duplicates appear.

## Offline and reproducible replay

After one successful online build:

```bash
cbr-unified build --input-dir ./build/cbr/sources --output ./build/cbr-replay
```

Local binding accepts `<source_id>.xlsx`, the original registry filename or an explicit mapping. Exactly one binding must resolve for each source and the local workbook must pass the same OOXML structural gate. For identical source revisions, specification, implementation and runtime, online and offline builds must produce the same `build_id` and deterministic Product tables.

## Query from CLI

List source revisions with Russian or English dataset names:

```bash
cbr-unified sources --db ./build/cbr/data/cbr_unified.sqlite --language en
```

Search indicators:

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

Repeated values for the same dimension form an OR-list:

```bash
cbr-unified query \
  --db ./build/cbr/data/cbr_unified.sqlite \
  --source mortgage_debt \
  --dim region=Москва \
  --dim region=Санкт-Петербург
```

Dimension-member filters accept the source/Russian value and the exposed Russian or English display value where a catalog member exists.

Trace one observation back to the exact workbook cell:

```bash
cbr-unified lineage --db ./build/cbr/data/cbr_unified.sqlite <observation_id>
```

The lineage result exposes observation, concept, raw-cell and disposition source owners separately, together with source revision, workbook SHA-256, sheet/cell locator, raw lexical value, formula and disposition.

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

`UnifiedDatabase(...)` requires embedded validation status `passed` by default. `allow_unvalidated=True` exists for explicit diagnostic work only.

`value_exact` preserves the source numeric lexical representation. The convenience `value` column is numeric for pandas work. Use `decimal_values=True` for exact `Decimal` values.

`pivot()` performs no implicit aggregation. It also rejects a displayed series that would silently mix hidden semantic signatures such as unit, scale, frequency or period role. Narrow filters or expose the differing axes instead.

## Statistical identity

The database does not treat a visually similar row label or physical row position as a universal indicator identity.

A semantic observation is bound to source revision, source-local concept, period/frequency, stock/flow/change role, unit/scale, explicit dimensions, exact source locator, raw-cell lineage and complete build identity.

Source-local concept identity uses source-visible semantics. Depending on source geometry this may include measure title, unit/scale signature, period-block heading, merged parent, hierarchy/section ancestry or explicit source parent. Physical row number remains provenance geometry rather than an ordinary business identity component.

The parser uses conservative context rules:

- negated cues take precedence over positive substring matches;
- ambiguous combined maturity buckets are left unclassified;
- explicit currency headings may scope repeated branch children;
- inherited currency scope is removed from later unique aggregates when the source does not establish that scope;
- exact short-/long-term parent labels may separate repeated instruments without inventing a normalized maturity bucket;
- exchange-rate indicators retain explicit source measure definitions such as change versus previous December, previous period or corresponding prior-year period.

For `obs_table_20s`, denomination and measurement currency remain separate dimensions. Foreign-currency denomination can coexist with `measurement_currency=USD`.

## Russian and English names

Russian source text remains the evidence-bearing identity surface. English names are project-facing translations or transparent transliteration unless the source establishes official English terminology.

Source catalog, concept names and reusable dimension members expose RU/EN surfaces. English display/filter behavior is symmetric for cataloged dimension members.

## Preservation model

The raw layer reads XLSX as OOXML rather than relying only on pandas/openpyxl interpretation. For every non-empty stored cell it preserves source/revision, workbook hash, exact sheet/coordinate, OOXML type/style, lexical `<v>`, resolved string text and formulas where present.

Semantic parsing prefers the preserved lexical numeric value and uses openpyxl for workbook structure/date interpretation. Source-specific semantic compatibility views may normalize proven presentation variants only for interpretation; raw evidence remains tied to untouched source bytes.

Every raw cell receives a disposition. `unmapped_numeric` is a blocking residue in a complete build. One raw cell cannot back multiple observations.

## Validation and verification

`validation.json` records blocking invariants and coverage, including:

- one build identity and complete source universe;
- manifest/raw/disposition/concept/observation owner coherence;
- source revision and file-hash coherence;
- complete raw-cell dispositions and one-to-one observation lineage;
- zero unresolved numeric cells;
- canonical dimension JSON;
- real ISO calendar dates;
- allowed frequency/period-role domains;
- non-empty units and valid positive integer scales;
- bilingual user-surface completeness;
- strict semantic duplicate/conflict detection.

The semantic conflict key is:

`source_id + source_concept_id + period + frequency + period_role + unit + scale + canonical dimensions`.

Conflicting values under this key block the build. Validation is repaired through source semantics rather than weakened.

Inspect embedded validation through:

```bash
cbr-unified validate --db ./build/cbr/data/cbr_unified.sqlite
```

Repository verification additionally performs a live 41-source build, offline deterministic replay, independent OOXML preservation comparison, CSV↔SQLite reconciliation, post-Jester contract checks, bilingual/query/lineage checks and publication-metadata applicability audit.

## Persistence and failure evidence

Direct SQLite materialization builds a sibling temporary database, runs `PRAGMA integrity_check` and atomically replaces the requested path. A failed direct replacement keeps the previous database.

Full Product builds use a separate staging/promotion transaction. Failed source acquisition or binding retains `source_manifest.acquisition.json` with detailed per-source status. Semantic failures additionally retain `failure.json` and source-local raw evidence where available.

A successful promoted output removes failure-only acquisition state and exposes one canonical `source_manifest.json`.

## Source changes

The registry is a reviewed Product input. Changed workbook bytes create a new SHA-based `source_revision_id`.

Presentation changes compatible with an explicit parser contract may build normally. Material unknown variants fail closed. The response is to inspect the source contract and update the adapter with evidence and regression coverage.

Publication metadata such as hidden sheets/rows/columns, comments and number formats is audited for applicability. Presence by itself does not define statistical semantics.

## Repository structure

```text
src/cbr_unified/
├── registry.py
├── acquisition.py
├── raw.py
├── normalization.py
├── semantic.py
├── processing_core.py  # established checked semantic mechanics
├── processing.py       # post-Jester semantic/context reconciliation
├── validation.py
├── persistence.py
├── query.py
├── build.py
└── cli.py
```

See `docs/SCHEMA.md` for data semantics, `docs/MAINTENANCE.md` for source-change handling and `examples/quickstart.py` for notebook-oriented use.
