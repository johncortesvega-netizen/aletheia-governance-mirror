# Patch 258 Recovery Note

Patch 258 is documentation and active-test hygiene only.

To revert Patch 258:

1. Remove `tests/active/test_behavior_regression_review.py`.
2. Restore the previous `tests/README.md`, `PATCH_STATUS.md`, and `PATCH_NOTES.md`.
3. Remove `docs/behavior_regression_review_patch_258.md`.
4. Remove the Patch 258 root metadata files.

No runtime files are modified by this patch.
