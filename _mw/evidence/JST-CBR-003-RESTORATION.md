# JST-CBR-003 — Restoration verification

**Work:** `WORK-JESTER-0003`  
**Experiment branch:** `jester/jst-0003`  
**Recovery target:** `4ee8583b3feff7775a956c51812232fa0d0516d2`  
**State:** `AUTHORITATIVE_DERIVED_SURFACE_RESTORED_EXACTLY`

After `JST-CBR-003` and `JR-CBR-003` were established on `main`, the disposable experiment branch was force-reset to the exact admitted Product baseline.

Independent branch resolution after reset returned:

`refs/heads/jester/jst-0003 → 4ee8583b3feff7775a956c51812232fa0d0516d2`.

The experiment workflow and disposable tests are absent from the branch's current state. Canonical Product code on `main` was never part of the experiment mutation surface. `PRODUCT-CBR-001` and `CLOSURE-CBR-001: PASS` remain unchanged.

The standalone Report and durable Evidence on `main` are now the only current Jester-session owners needed for mandatory non-Jester processing; historical experiment commits/runs remain evidence locators only.
