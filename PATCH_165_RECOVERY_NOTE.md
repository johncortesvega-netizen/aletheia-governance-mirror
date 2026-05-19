# Patch 165 Recovery Note — Protocol Guide Compact Panel Layout

Patch 165 is a UI/copy organization patch for the Protocol Guide tab.

## What it changed

- Replaced the long Protocol Guide stack with a compact panel index.
- Grouped the tab into four side-by-side rows / eight collapsed panels:
  1. Operating boundary
  2. Artificial Mind Formation Theory
  3. Navigation & module map
  4. Shared protocol state
  5. Release & continuity
  6. Evidence & source rules
  7. Review lenses
  8. World / taxonomy / limits
- Included Artificial Mind Formation Theory in the same overall Protocol Guide panel layout.

## What it did not change

- No scoring behavior.
- No taxonomy state.
- No routing behavior.
- No receipt schema or generation.
- No World Lens logic.
- No Evidence Lab math.
- No AI Integrity behavior.
- No external calls, telemetry, storage, Global ID sync, public ledger sync, certification, enforcement, official authority, or final-truth behavior.

## Recovery

To revert Patch 165 only:

1. Restore `app.py` from the last known Patch 164 state.
2. Restore `tests/test_patch_162_artificial_mind_formation_theory.py` from the last known Patch 164 state if needed.
3. Remove `tests/test_patch_165_protocol_guide_compact_panel_layout.py`.
4. Remove this Patch 165 entry from `PATCH_STATUS.md` and `docs/progress_database.md`.
5. Delete `PATCH_165_MANIFEST.txt` and `PATCH_165_RECOVERY_NOTE.md`.

Then rerun:

```bat
python tools\run_patch_checks.py 164
python tools\run_patch_checks.py 163
python tools\run_patch_checks.py 162
```
