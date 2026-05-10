# Patch 50 — v0.1 Release Package

## Summary

Packaged ALETHEIA v0.1 as a public MVP by adding a release-package document with module list, out-of-scope boundaries, quickstart commands, release readiness criteria, and the public interpretation rule.

## Changed / Added

- `docs/v01_release_package.md`
- `docs/public_release_notes.md`
- `README.md`
- `about_page.py`
- `PATCH_STATUS.md`
- `docs/progress_database.md`
- `tests/test_patch_50_v01_release_package.py`
- `PATCH_50_MANIFEST.txt`

## Safety Boundary

Patch 50 is packaging only. It does not add governance authority, Global ID sync, real 9k selection, World Leader logic, public ledger, neural data, automatic enforcement, legal advice, religious validation, or any authority above human review.

## Check

```bat
tools\run_patch_checks.bat 50
```
