# Patch 267 Recovery Note — Safe Config Extraction

To revert Patch 267 only:

1. Restore the four extracted assignments in `app.py`:
   - `APP_VERSION`
   - `SUPPORTED_INPUT_LANGUAGE_NOTE`
   - `APP_UX_POLISH_SUMMARY`
   - `DEMO_INPUT_FILES`
2. Remove these imports from `app.py`:
   - `from ui.config import APP_VERSION, SUPPORTED_INPUT_LANGUAGE_NOTE`
   - `from ui.examples import APP_UX_POLISH_SUMMARY, DEMO_INPUT_FILES`
3. Delete:
   - `ui/config.py`
   - `ui/examples.py`
   - `docs/config_extraction_patch_267.md`
   - `docs/config_extraction_patch_267_summary.md`
   - `tests/active/test_patch_267_safe_config_extraction.py`
4. Restore Patch 266 status/notes if rolling back to Patch 266.

Behavior-sensitive constants were not moved in Patch 267.
