# Patch 76 Recovery Note - Differentiation / Comparison Framing

Patch 76 is documentation and About/README positioning only.

If anything feels too promotional or too broad, revert the patched files listed in `PATCH_76_MANIFEST.txt`. No scoring formulas, verdict-routing logic, receipt schema, storage behavior, public ledger behavior, Global ID sync, central storage, Evidence Lab data model, World Lens data model, or authority boundary logic was intentionally changed.

Expected verification:

```bat
tools\run_patch_checks.bat 76
```

Expected result:

```text
Patch checks passed.
```

Boundary reminder:
ALETHEIA remains a mirror for human review. The free/open-source commitment does not create authority, certification, legal status, or enforcement power.
