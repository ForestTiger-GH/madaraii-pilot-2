# JST-CBR-004 — Restoration verification

**Work:** `WORK-JESTER-0004`  
**Experiment branch:** `jester/jst-0004`  
**Recovery target:** `4ee8583b3feff7775a956c51812232fa0d0516d2`  
**State:** `AUTHORITATIVE_DERIVED_SURFACE_RESTORED_EXACTLY`

After `JST-CBR-004` and `JR-CBR-004` were established on `main`, the disposable experiment branch was force-reset to the exact admitted Product baseline.

Independent GitHub branch resolution after reset returned:

`refs/heads/jester/jst-0004 → 4ee8583b3feff7775a956c51812232fa0d0516d2`.

The branch-only workflow and disposable Jester tests are absent from its current state. Canonical Product code on `main` was never part of the experiment mutation surface. `PRODUCT-CBR-001` remains admitted at the same exact revision and `CLOSURE-CBR-001: PASS` remains unchanged.

Historical experiment commits and CI runs remain evidence locators only. Mandatory non-Jester processing may now consume the standalone Report and durable Evidence.
