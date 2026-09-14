# JST-CBR-004 — Acquisition/raw publication-boundary Jester evidence

**Owner:** `JST-CBR-004`  
**Work:** `WORK-JESTER-0004`  
**Method:** `MADARAII-40`  
**Product baseline:** `4ee8583b3feff7775a956c51812232fa0d0516d2`  
**Experiment branch:** `jester/jst-0004`  
**Governing MADARAII:** `ForestTiger-GH/MADARAII@721a199352b5c5282b1478cd6a5eb36a9872fb34`  
**Evidence state:** CAPTURED; restoration pending at initial write

## Control shell and run trace

All executable experiments used synthetic XLSX/bytes/HTTP-response objects on a branch derived from the exact admitted Product revision. Live external acquisition was prohibited and was not used. Canonical Product code remained outside the experiment mutation surface.

| Wave | Commit | CI run | Result |
|---|---|---:|---|
| Harness | `979c176862c99f16e74318defdcc22abd756cf08` | `34896444055` | harness established |
| Publication/source-trust wave | `d46269dc9ba54d839fceecb70c9caa1c3d91d60e` | `34896473329` | EXPECTED PROBE FAILURE: Jester guessed missing unit rather than Product's explicit `source_defined`; other probes passed |
| Sharpened number-format wave | `da438f5ee961a04781b4a7fe99bcd72255c33d10` | `34896619311` | PASS |

The failed probe is retained as trajectory evidence. It did not show Product failure: semantic parsing deliberately substitutes `unit="source_defined"` when text-based unit inference returns no exact structured unit. The sharpened probe therefore tests loss of the Excel percent format itself, not absence of the field.

## Provocation ledger

### JST4-P01 — «Redirect in a CBR trench coat»

**Tried:** request the commissioned-looking CBR URL while a synthetic HTTP session resolves it to an unrelated host and returns bytes beginning with `PK` plus an XLSX content type.

**Observed:** `download_sources()` records the source as `status=ok`, keeps the unrelated `resolved_url`, writes the bytes, hashes them and creates a source revision. The acquisition gate checks HTTP success and the first two bytes `PK`; it does not pin the resolved host or prove OOXML structure at this stage.

**Limit:** later raw/build parsing would reject malformed OOXML. This is a trust/acquisition-stage observation, not proof that an invalid full Product build can be admitted.

### JST4-P02 — «Hidden sheet, public statistic»

**Tried:** put a syntactically ordinary statistical matrix on an Excel sheet with `sheet_state="hidden"`; keep a harmless visible cover sheet.

**Observed:** raw extraction and semantic parsing produce three ordinary observations from the hidden sheet. Raw rows preserve `sheet_exact` but carry no sheet-visibility field.

### JST4-P03 — «Hidden row joins the annual report»

**Tried:** hide the entire data row containing the statistical measure while keeping the period axis visible.

**Observed:** the hidden row still produces three semantic observations. Raw records do not preserve row-hidden state.

### JST4-P04 — «Percent costume reduced to source_defined»

**Tried:** create values `0.1/0.2/0.3` with Excel number format `0.0%`, while the row label/title contains no textual percent marker.

**Observed:** style indices show that formatting exists in the workbook/raw cell representation, but raw rows expose only `style_index`, not the resolved number-format string. Semantic observations are admitted with `unit="source_defined"`, not structured `percent`. The first Jester assertion incorrectly expected a missing unit; the adaptive run corrected the claim to the actual behavior.

### JST4-P05 — «The warning lives in a comment, therefore it does not exist»

**Tried:** attach an Excel comment to an observed numeric cell: `Предварительные данные. Не использовать для публикации.`

**Observed:** the cell still becomes an ordinary observation. The raw cell record contains no comment text or comment relation, so the warning is unavailable to downstream semantic processing through the raw contract.

### JST4-P06 — «Local XLSX by filename alone»

**Tried:** bind arbitrary non-OOXML bytes stored under the expected `.xlsx` filename through `bind_local_sources()`.

**Observed:** local binding returns `status=ok` and a hash/source revision because the binding phase checks identity/path cardinality and bytes, not workbook structure.

**Limit:** later raw parsing would fail. This is the local-binding equivalent of an acquisition-stage trust boundary, not a full-build acceptance claim.

## Session boundary and diminishing returns

Six materially different provocations reached the fixed budget. Four observations concern publication/presentation metadata or source trust at a stage boundary. They are distinct from earlier parser, identity, validation and consumer-projection sessions, but their transfer to the already-verified 41-source Product is increasingly conditional on actual source use of hidden states, comments, number formats or unusual redirects.

The marginal Jester opportunity is therefore materially lower after this pass: further safe candidates mostly subdivide the same newly exposed class (hidden columns, print areas, defined names, styles, notes, workbook protection, other redirect/package variations) rather than opening a new engineering mechanism. This is the stop rationale for the overall Jester campaign.

These facts assign no defect, severity, Product requirement or repair. Downstream non-Jester Work owns applicability and disposition.
