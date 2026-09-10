# RT-CBR-004 — Bilingual semantic surface and readable naming

**Work kind:** `EXTERNAL_DESCRIPTIVE_RESEARCH` (`MADARAII-08`)  
**Research Topic:** `RT-CBR-004`  
**Baseline:** `RT-CBR-001..003`  
**Status:** established Research Result

## Central question

How can exact Bank of Russia Russian labels, interpreted meanings, shorter Russian working names and English names coexist without identity loss or collision; where is Bank of Russia English terminology authoritative and where must project translations be identified as project semantics?

## Main conclusion

Language/presentation must be a **surface over stable semantic identity**, not an identity mechanism. Each concept needs to retain the exact source Russian wording and may additionally expose readable Russian and English names with an explicit translation/naming provenance.

A short label such as `Ипотечная задолженность` / `Mortgage debt` is useful for navigation but cannot replace the full source meaning `задолженность по ипотечным жилищным кредитам ... физическим лицам-резидентам ...` together with currency, acquired-rights treatment, territory and unit dimensions.

## Required naming layers

Research supports four separate fields/relations where materially available:

1. **Exact source label (`label_ru_source`)** — verbatim CBR text or exact hierarchical source path; immutable within a source revision.
2. **Normalized source label (`label_ru_normalized`)** — conservative whitespace/Unicode normalization for search/navigation; not identity.
3. **Readable Russian name (`name_ru`)** — shorter project working name created only after dimensions have been factored out explicitly.
4. **English name (`name_en`)** — authoritative CBR English term where an official English publication/methodology clearly corresponds; otherwise a project translation marked as such.

The system should additionally retain a description/definition and source path for concepts whose short names would otherwise be ambiguous.

## What can safely be shortened

Long source phrases often repeat dimensions already represented structurally. For example, once an observation records:

- subject = resident individuals;
- instrument = housing mortgage loan;
- currency denomination = rubles;
- measure = outstanding debt;
- unit = million rubles;
- territory = selected row member;

its working display name can be shorter than the full A1 title. Shortening is safe only because the removed qualifiers remain structured fields and the exact source label is preserved.

## What must remain explicit

Do not shorten away distinctions that are not already represented structurally, including:

- debt versus overdue debt;
- amount including or excluding acquired claims;
- SME versus all resident legal entities/individual entrepreneurs;
- deposits excluding escrow versus deposits generally;
- balance versus transaction;
- original versus seasonally adjusted;
- nominal versus market valuation;
- original versus remaining maturity;
- historical classification versus OKVED2/classification regime;
- reporting population/institutional sector.

## Bank of Russia English terminology available for reuse

Official English Bank of Russia publication/methodology surfaces provide stable terminology for several recurring concepts, including:

- `Granted Funds and Borrowings`;
- `Outstanding amount of loans`, `Overdue loans`, `Volume of loans granted`;
- `Small and medium-sized businesses (SME)`;
- `Financial assets and liabilities of the households sector`;
- `balances` and `transactions`;
- `Monetary Aggregates`, `Central Bank Survey`, `Other Depository Corporations Survey`, `Depository Corporations Survey`;
- `External debt`, `original maturity`, `remaining maturity`, `institutional sector`, `financial instrument`, `national currency`, `foreign currency`.

Where an exact source row has no verified official English counterpart, the product may provide a project translation, but its status must be `project_translation` rather than presenting it as official CBR wording.

## Translation identity and maintenance

A translation record should bind to a semantic concept identity and carry:

- language;
- display name;
- status (`cbr_official`, `project_translation`, `transliteration_only`, `missing` if ever allowed internally);
- optional source URL/locator for official terminology;
- version/revision of the translation catalog.

Changing a display translation must not change the concept ID or source observation identity.

## Regions and classification members

Territorial English names should map to the exact territorial semantic member, not merely a normalized place string. Parent-region-excluding-subregion rows need descriptive English scopes, for example an English expression equivalent to “Arkhangelsk Region excluding the Nenets Autonomous Area”, rather than being collapsed into `Arkhangelsk Region`.

Economic activity names are classification members. Where current OKVED2/NACE correspondence is established, English classification terminology may be used with the classification identity preserved. Historical activity/use categories require their own translation records; approximate matching to modern NACE labels is unsafe.

## Hierarchical indicators

For nested sources (`obs_table_20s`, household instruments, monetary surveys, external debt), a readable English name may be local while the full hierarchy remains available. Example conceptual representation:

- short name: `Overdue debt` / `Просроченная задолженность`;
- hierarchy: `Assets > Loan portfolio > Loans to legal entities > Non-financial corporations > Overdue debt`;
- source line code/path: retained separately.

This prevents generic names from colliding across contexts.

## Query/display behavior

User-facing filtering should support both Russian and English names while resolving internally to stable IDs. Search may use conservative normalized aliases. Ambiguous short names should return multiple candidate concepts with context rather than choosing one implicitly.

Prepared two-dimensional tables should let the caller choose display language (`ru`/`en`) while retaining stable machine identifiers and provenance columns/metadata outside the visual label where needed.

## Coverage strategy for the finite source universe

The bound source universe is finite but contains a large number of source labels. A practical bilingual system can combine:

- curated bilingual names for dataset families, measure types and recurring dimensions;
- explicit bilingual maps for territorial members and common institutional sectors;
- source-specific concept catalog entries generated from parsed hierarchy;
- project translations for remaining concept labels with clear status;
- exact source Russian text retained for audit.

Automatic fuzzy translation is unsuitable as an identity-forming step. Translation completeness should be verified as a separate data-quality claim: every user-exposed semantic concept must have a non-empty Russian and English display name and a translation-status field.

## Collision policy

Two concepts may share the same readable name. The UI/API resolves by stable ID and returns contextual dimensions/hierarchy. The product must never merge concepts because their Russian or English names are equal.

## Residual limitations

Official English CBR publication surfaces do not necessarily provide an exact English translation for every cell-level Russian classification member. Project translations are therefore unavoidable for part of the semantic catalog. Their provenance/status must make this distinction visible.

This result establishes naming semantics but does not choose the storage schema or implementation library.
