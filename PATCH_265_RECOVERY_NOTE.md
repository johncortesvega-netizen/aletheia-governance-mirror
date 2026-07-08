# Patch 265 recovery note

To revert Patch 265 manually:

1. Remove `ui/state.py`.
2. Restore the inline sidebar state mutations in `app.py`:
   - `Default` → `Starting preset` normalization;
   - reset button assignments for sidebar profile, steps, voices, capture sensitivity, and alignment floor.
3. Remove the Patch 265 docs, manifest, delete list, and active test.
4. Restore `PATCH_STATUS.md`, `PATCH_NOTES.md`, and the Patch 264 active test to the previous version.

Patch 265 intentionally only moves sidebar review-lens state helpers. No page-local state or protocol behavior should need recovery.
