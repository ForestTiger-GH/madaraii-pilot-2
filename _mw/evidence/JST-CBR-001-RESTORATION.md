# JST-CBR-001 — Restoration verification

**Parent evidence owner:** `JST-CBR-001`  
**Work:** `WORK-JESTER-0001`  
**Restoration target:** `jester/jst-0001` → `4ee8583b3feff7775a956c51812232fa0d0516d2`  
**Status:** VERIFIED

After all material Jester evidence had been copied to `_mw/evidence/JST-CBR-001.md` and `_mw/results/JR-CBR-001.md`, the experimental branch reference was force-restored to the exact admitted Product baseline.

A separate GitHub branch read after the ref update returned:

- branch: `jester/jst-0001`;
- head SHA: `4ee8583b3feff7775a956c51812232fa0d0516d2`;
- baseline commit message: `Align validation fixtures with bilingual contract`.

Therefore the disposable experiment commits, branch-only workflow and branch-only Jester reproducers are absent from the current experiment branch state. The canonical `main` Product code was never modified by the intervention. Only Jester Work/Result/Evidence control objects were written to `main`.

The MADARAII-40 intervention is restored and ready for mandatory non-Jester handoff.
