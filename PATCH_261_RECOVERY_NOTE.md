# Patch 261 Recovery Note

Patch 261 only changes legacy test collection hygiene and documentation.

To revert:

1. Restore the previous `tests/conftest.py` from before Patch 261.
2. Remove:
   - `docs/legacy_manifest_quarantine_completion_patch_261.md`
   - `docs/refactor_pause_roadmap_patch_261.md`
   - `PATCH_261_MANIFEST.txt`
   - `PATCH_261_RECOVERY_NOTE.md`
   - `PATCH_261_DELETE_LIST.txt`
3. Restore `PATCH_STATUS.md` and `PATCH_NOTES.md` to their pre-Patch-261 versions.

No runtime files are changed by this patch.
