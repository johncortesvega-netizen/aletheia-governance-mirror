# Patch 110 Recovery Note — App Shell Router Refactor Step 3

Patch 110 continues the behavior-preserving app-shell refactor. It extracts the stable public header and first-use note into `ui/app_shell.py` through `render_app_header(...)` and `render_how_to_use_note(...)`.

## What changed

- `app.py` now calls `render_app_header(mascot_logo_uri, APP_VERSION, st)` for the public hero/header block.
- `app.py` now calls `render_how_to_use_note(st)` for the first-use note below the header.
- `ui/app_shell.py` now contains the header and first-use copy alongside the existing boundary/sidebar shell helpers.
- Patch 110 tests verify the helper remains copy-only, importable without a Streamlit runtime, and boundary-safe.

## What did not change

- No scoring change.
- No verdict-routing change.
- No signal-pattern change.
- No signal-weight change.
- No receipt schema change.
- No module routing change.
- No external calls.
- No live model calls.
- No telemetry.
- No analytics.
- No central storage.
- No Global ID sync.
- No public ledger sync.
- No privacy guarantee.
- No certification.
- No enforcement.
- No final truth claim.

## Recovery

If Patch 110 needs to be reverted, restore the prior inline header block and first-use note in `app.py`, remove the two new helper functions from `ui/app_shell.py`, and remove `tests/test_patch_110_app_shell_router_refactor_step_3.py` plus this patch manifest/recovery note. No scoring or receipt migration is required because Patch 110 is a shell-copy extraction only.
