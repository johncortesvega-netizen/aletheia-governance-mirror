# Patch 123 Recovery Note

Patch 123 extracts the in-app `Why ALETHEIA` page copy from `app.py` into `pages_ui/about_page.py`.

If recovery is needed, restore the files listed in `PATCH_123_MANIFEST.txt` from the previous accepted baseline. The expected rollback is simple: put the About tab copy back into `app.py`, remove the `pages_ui.about_page` import/call, and remove the Patch 123 docs/tests.

Review focus:

- `app.py` should only open `tab_about`, resolve the optional header image, and call `render_about_public_info_page`.
- `pages_ui/about_page.py` should render copy only.
- The root-level `about_page.py` remains available for the standalone page and historical tests.
- The Patch 122 checkpoint test now references `render_privacy_boundary_audit_panel`, which is the existing helper name.

This patch does not certify ALETHEIA, guarantee privacy, enforce outcomes, or claim final truth. Humans keep the judgment.
