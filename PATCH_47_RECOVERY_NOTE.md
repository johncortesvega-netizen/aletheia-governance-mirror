# Patch 47 — App Navigation + Smoke Test Cleanup

## Summary

Patch 47 makes the main v0.1 navigation path explicit and adds smoke-test coverage for the visible module order.

## Changed / Added

- Added `docs/app_navigation_smoke.md`.
- Added `tests/test_patch_47_app_navigation_smoke.py`.
- Added `PATCH_47_MANIFEST.txt`.
- Updated `PATCH_STATUS.md`.
- Updated `docs/progress_database.md`.
- Updated `README.md`.
- Updated `about_page.py`.
- Updated `app.py`.

## Safety Boundary

This patch adds no governance authority, no Global ID sync, no real 9k selection, no World Leader logic, no automatic reset, no enforcement mechanism, no spiritual validation, and no public ledger.

The app path remains:

> ALETHEIA reflects. Humans review. Power stays accountable.

## Local Check

```bat
tools\run_patch_checks.bat 47
```
