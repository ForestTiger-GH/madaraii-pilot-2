# JST-CBR-001 — Jester provocative exploration evidence

**Owner:** `JST-CBR-001`  
**Work:** `WORK-JESTER-0001`  
**Method:** `MADARAII-40`  
**Product baseline under provocation:** `4ee8583b3feff7775a956c51812232fa0d0516d2`  
**Admitted build identity at baseline:** `bld_204724c672460b3deaa50675`  
**Experimental branch:** `jester/jst-0001`  
**Governing MADARAII baseline:** `ForestTiger-GH/MADARAII@721a199352b5c5282b1478cd6a5eb36a9872fb34`  
**Evidence state:** CAPTURED; restoration verification pending at initial write

## 1. Control-shell evidence

All executable provocations were confined to the derived branch `jester/jst-0001`, created from the exact admitted Product revision. The canonical Product code on `main` was not mutated by the Jester experiments.

The experiment-only workflow was scoped to that branch and performed only:

1. repository checkout;
2. Python 3.12 setup;
3. editable package installation with test dependencies;
4. `pytest -q`.

Workflow token permission was `contents: read`. No release, deployment, source publication, Bank of Russia live acquisition, secret use or customer-data operation formed part of the experiment.

## 2. Exact experiment trajectory

| Wave | Experimental commit | CI run | Outcome | Material change in attack surface |
|---|---|---:|---|---|
| Harness | `afececb60566ea9301042ef9f6872ad7cf4207a7` | branch workflow bootstrap | harness only | isolated branch-only pytest runner |
| 1 | `5223e41cc2c5e7516cd1aa2d2508700fcf124c66` | `34893047550` | PASS | query exactness + validation semantic-coherence attacks |
| 2 | `063b4fc40f6c240c56a1bbb26304aa65fe0b2812` | `34893234309` | PASS | persistence/FK coherence + build-identity mutation attack |
| 3 | `42d0b4070bd61e87a75f711327ecc7d6b4bf5b19` | `34893483411` | PASS | custom SourceSpec split-brain + promotion interruption |
| 4 | `3387d4461b0acff6e58308487d08c0b5a2b6d951` | `34893656477` | PASS | wrong-role semantic false-positive through real parser |
| 5 | `40fd3479ad0619587da881d29a8e6723d2ee34e7` | `34893811182` | PASS | concept-identity stability under harmless row movement |

Final runner evidence for `34893811182`:

- Ubuntu 24.04;
- CPython 3.12.14;
- `pandas 3.0.5`, `numpy 2.5.3`, `openpyxl 3.1.5`, `pytest 9.1.1` resolved from the Product's lower-bounded dependency ranges;
- `pytest -q` output: `................................... [100%]`, i.e. **35 tests passed** including the disposable Jester reproducers and the ordinary repository unit suite.

The disposable executable reproducers existed only on the experimental branch and are evidence, not Product requirements.

## 3. Provocation ledger

The names below are Jester mnemonics. They describe what was attempted and observed; they do not assert defect status, priority, root cause or prescribed repair.

### JST-P01 — «Float tuxedo»

**Provocation.** Put a large exact decimal (`9999999999999999.99`) through the ordinary query/pivot convenience surface while leaving the exact source lexical value intact.

**Observed.** `value_exact` and `decimal_values=True` preserve the exact decimal. The default `observations()` convenience `value`, produced through `pandas.to_numeric`, and the default `pivot()` value differ from that exact Decimal. The README already documents the distinction between `value_exact`, numeric convenience `value` and `decimal_values=True`.

**Evidence locus.** `src/cbr_unified/query.py`; disposable test `test_jester_float_tuxedo_default_view_changes_exact_decimal`.

### JST-P02 — «Passport swap»

**Provocation.** Give an observation from source `x` a valid `source_concept_id` whose concept row declares another `source_id`.

**Observed.** `validate_bundle` returns `status=passed`. SQLite foreign keys also admit and persist the pair because the FK joins on concept ID while source ownership remains an independent column.

**Evidence locus.** `src/cbr_unified/validation.py`, `src/cbr_unified/persistence.py`; two executable reproducers including persisted SQLite join evidence.

### JST-P03 — «JSON shell game»

**Provocation.** Create two observations with the same semantic dimensions and conflicting values, expressing the same JSON object with a different key order.

**Observed.** Conflict grouping uses the raw `dimensions_json` string in its semantic key. The reordered JSON strings therefore form different groups and the validation result reports no conflicting semantic duplicate group. The normal Product parser emits sorted JSON, so the experiment concerns the validation boundary rather than the ordinary parser's current output convention.

**Evidence locus.** `src/cbr_unified/validation.py`; disposable test `test_jester_json_shell_game_hides_semantic_conflict_by_key_order`.

### JST-P04 — «Cardboard calendar»

**Provocation.** Supply period `2026-99-99` as an observation period.

**Observed.** Validation accepts the value because the gate checks ISO-like string shape rather than calendar validity.

**Evidence locus.** `src/cbr_unified/validation.py`; disposable test `test_jester_cardboard_calendar_accepts_impossible_iso_date`.

### JST-P05 — «Ghost provenance museum»

**Provocation.** Bind one raw cell and its disposition to a real source revision while assigning mutually different, unmanifested `source_id` values to the raw and disposition rows.

**Observed.** Validation passes. SQLite persists the mismatch because both rows reference an existing revision and source-id coherence across those owners is not a physical FK condition.

**Evidence locus.** `src/cbr_unified/validation.py`, `src/cbr_unified/persistence.py`; persisted SQLite reproducer.

### JST-P06 — «One cell, two careers»

**Provocation.** Point two semantically different observations to the same raw cell.

**Observed.** `validate_bundle` returns top-level `status=passed` while the returned invariant `every_observation_has_raw_lineage` evaluates to `False` under this construction. The SQLite observation table separately has a unique source-revision/sheet/cell constraint, so normal persistence supplies another boundary after validation.

**Evidence locus.** `src/cbr_unified/validation.py`, `src/cbr_unified/persistence.py`; disposable validation reproducer.

### JST-P07 — «Semantic blank cheque»

**Provocation.** Give an otherwise structurally valid observation empty frequency, empty period role, empty unit and scale `-999`.

**Observed.** Validation returns `status=passed`; those semantic fields do not have a value-domain gate at this boundary.

**Evidence locus.** `src/cbr_unified/validation.py`; disposable test `test_jester_semantic_blank_cheque_accepts_empty_roles_and_absurd_scale`.

### JST-P08 — «Ship of Theseus build»

**Provocation.** Replace executable semantic parser behavior while holding the source specification and source revisions fixed.

**Observed.** `_fingerprints()` returns the same `build_id`. Build identity is derived from a static processing-contract string, SourceSpec fingerprint and source revisions; executable source code and resolved dependency versions are not direct identity inputs. Product governance separately binds accepted Product state to an exact code/configuration commit.

**Adjacent evidence.** The final Jester CI resolved current dependency versions from lower-bounded package requirements; those resolved versions likewise do not participate directly in `_fingerprints()`.

**Evidence locus.** `src/cbr_unified/build.py`, `pyproject.toml`, `docs/SCHEMA.md`, `docs/MAINTENANCE.md`; disposable monkeypatch reproducer.

### JST-P09 — «Split-brain SourceSpec»

**Provocation.** Call the build internals with a deliberately modified `SourceSpec` for an existing source ID.

**Observed.** `_fingerprints()` incorporates the passed custom SourceSpec, while `_build_into_staging()` later resolves `spec = get_source(sid)` and supplies the global registry SourceSpec to semantic parsing. The reproducer records a build ID calculated from the custom specification and parser invocation with the different global specification.

**Evidence locus.** `src/cbr_unified/build.py`; disposable test `test_jester_split_brain_custom_spec_is_fingerprinted_but_global_spec_is_parsed`.

### JST-P10 — «Atomic promotion trapdoor»

**Provocation.** Interrupt `_promote()` with `KeyboardInterrupt` after the prior Product output is renamed to its temporary backup but before staging becomes the requested final path.

**Observed.** The requested final path is absent after the injected interruption; the previous Product remains recoverable in the hidden `.previous-*` sibling. `_promote()` restores on caught `Exception`; `KeyboardInterrupt` is outside that catch. Maintenance documentation already describes the temporary move and recovery where the filesystem operation permits it.

**Evidence locus.** `src/cbr_unified/build.py`, `docs/MAINTENANCE.md`; filesystem-isolated reproducer.

### JST-P11 — «Footnote cosplay»

**Provocation.** Build a real synthetic XLSX with three recognized monthly headers, one ordinary data row, and a later row labelled `Источник: техническое примечание` containing numeric `2024` underneath one recognized period column.

**Observed.** Real `extract_raw_cells()` + `parse_source_checked()` materialize the note number as a semantic observation. Its disposition is `observation_value`, and the numeric disposition gate reports `passed`. The experiment demonstrates that a value can receive a semantically wrong-looking role while satisfying the gate that prevents unexplained numerics.

**Evidence locus.** `src/cbr_unified/raw.py`, `src/cbr_unified/semantic.py`, `src/cbr_unified/processing.py`; end-to-end synthetic-workbook reproducer.

### JST-P12 — «Row-number tattoo»

**Provocation.** Move an otherwise identical non-region/non-activity indicator from row 10 to row 11 while preserving sheet, label, title and source.

**Observed.** `_concept()` changes `source_local_key` from a key containing `row:10` to one containing `row:11`, producing a different `source_concept_id`. `docs/MAINTENANCE.md` separately states that row numbers are not durable business identities and recommends `source_concept_id` for source-local concept identity.

**Evidence locus.** `src/cbr_unified/semantic.py`, `docs/MAINTENANCE.md`; disposable test `test_jester_durable_concept_identity_has_a_row_number_tattoo`.

## 4. Diminishing-significance boundary

The trajectory reached the pre-bound maximum of **12 materially different provocations**. Candidate further attacks were screened and rejected from execution because they were either subsumed by an established class or materially weaker:

- repeated CLI `--dim` keys collapse through ordinary dictionary semantics — primarily an interface-expression issue, not a new semantic-integrity class;
- CSV cells containing source formulas may be interpreted by spreadsheet software — peripheral to the core statistical semantic path and dependent on downstream consumer behavior;
- additional title/footnote/header heuristics reduce to the already demonstrated wrong-role semantic-classification attack in JST-P11;
- dimension-member catalogue linkage variants reduce to the cross-owner coherence boundary already exposed by JST-P02/JST-P05.

The Jester budget is therefore exhausted without widening the authorized control shell.

## 5. Evidence preservation statement

The experiment commits, CI run identifiers, exact test names and observed outcomes above capture the material evidence needed for downstream Actor Input Development. The disposable branch itself is not a Product candidate and carries no admission claim.

After this evidence owner and the Jester Report are written to the canonical workspace, `jester/jst-0001` is to be force-restored to `4ee8583b3feff7775a956c51812232fa0d0516d2` and the resulting branch SHA is to be recorded here.
