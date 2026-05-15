# Patch 74 Recovery Note - Public Evaluation Case Pack

Patch 74 is documentation/examples/test only.

## What changed

- Added public copy/paste evaluation cases under `examples/evaluation_cases/`.
- Added `docs/evaluation_method.md` to explain how to test ALETHEIA's mirror behavior.
- Added `docs/public_test_cases.md` as a case catalog.
- Added README pointers to the case pack.
- Added `tests/test_patch_74_public_evaluation_case_pack.py`.
- Updated `PATCH_STATUS.md` and `docs/progress_database.md`.

## What did not change

- No scoring formula changed.
- No verdict routing changed.
- No witness receipt schema changed.
- No app UI changed.
- No Evidence Lab or World Lens data model changed.
- No storage, public ledger, Global ID sync, central storage, authority boundary, or enforcement behavior changed.

## Local validation

Run:

```bat
tools\run_patch_checks.bat 74
```

Expected result:

```text
Patch checks passed.
```

## Rollback

Remove the files listed in `PATCH_74_MANIFEST.txt` and restore the previous versions of `README.md`, `PATCH_STATUS.md`, and `docs/progress_database.md`.
