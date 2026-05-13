# Patch 125 Recovery Note

Patch 125 extracts static Evidence Lab intro and public-data build guidance into `pages_ui/evidence_lab_page.py`.

If recovery is needed, restore the files listed in `PATCH_125_MANIFEST.txt` from the previous accepted baseline. The expected rollback is small: move the intro/build guidance back into the Evidence Lab section of `app.py`, remove the `pages_ui.evidence_lab_page` import/calls, and remove Patch 125 docs/tests.

Review focus:

- `pages_ui/evidence_lab_page.py` should render copy only.
- `app.py` should still own upload widgets, build buttons, dataframe processing, scoring, diagnostics, downloads, receipts, session state, and Evidence Lab / World Lens synchronization.
- No evidence behavior should move into the helper.

This patch does not certify ALETHEIA, guarantee privacy, enforce outcomes, or claim final truth. Humans keep the judgment.
