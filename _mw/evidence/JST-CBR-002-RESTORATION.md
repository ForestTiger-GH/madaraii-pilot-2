# JST-CBR-002 — Restoration verification

**Work:** `WORK-JESTER-0002`  
**Experiment branch:** `jester/jst-0002`  
**Declared recovery target:** `4ee8583b3feff7775a956c51812232fa0d0516d2`  
**Restoration state:** `AUTHORITATIVE_DERIVED_SURFACE_RESTORED_EXACTLY`

After durable capture of `JST-CBR-002` and `JR-CBR-002`, the disposable experiment branch was force-reset to the exact admitted Product baseline.

An independent GitHub branch read after the reset resolved:

`refs/heads/jester/jst-0002 → 4ee8583b3feff7775a956c51812232fa0d0516d2`.

Therefore the branch-only workflow, disposable Jester tests and all experiment commits are absent from the current branch state. The canonical Product code on `main` was never part of the Jester mutation surface. The admitted Product owner remains `PRODUCT-CBR-001` at the same exact revision and the prior `CLOSURE-CBR-001: PASS` claim is unchanged.

The preserved experiment evidence is the durable evidence/report on `main` plus exact historical commit and CI-run references recorded there. Mandatory non-Jester continuation may now rely on this restoration proof and the standalone Jester Report as its Subject.
