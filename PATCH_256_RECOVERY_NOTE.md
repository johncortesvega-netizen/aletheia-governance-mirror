# Patch 256 Recovery Note

Patch 256 adds a legacy-test collection quarantine only.

## To roll back

Remove or revert:

- `tests/conftest.py`
- the Patch 256 section in `tests/README.md`
- `docs/legacy_test_quarantine_patch_256.md`
- Patch 256 entries in `PATCH_STATUS.md` and `PATCH_NOTES.md`
- `PATCH_256_MANIFEST.txt`
- `PATCH_256_RECOVERY_NOTE.md`
- `PATCH_256_DELETE_LIST.txt`

## Expected result after rollback

Explicit whole-tree pytest collection may again import broken historical test files and may again collect old patch-contract tests that expect root-level patch artifacts removed by Patch 255.

## Runtime impact

Rollback is not required for runtime behavior. Patch 256 does not change app behavior.
