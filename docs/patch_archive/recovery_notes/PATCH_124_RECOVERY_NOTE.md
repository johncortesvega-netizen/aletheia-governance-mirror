# Patch 124 Recovery Note

Patch 124 exposes the public trust package review route inside the Protocol Guide through `pages_ui/trust_package_page.py`.

If recovery is needed, restore the files listed in `PATCH_124_MANIFEST.txt` from the previous accepted baseline. The expected rollback is small: remove the `pages_ui.trust_package_page` import/call from `app.py`, remove the Patch 124 helper, and remove Patch 124 docs/tests.

Review focus:

- `pages_ui/trust_package_page.py` should render document pointers and review prompts only.
- `app.py` should remain the orchestrator and call the helper from the Protocol Guide tab.
- Documentation remains the source of truth, especially `docs/public_trust_package.md` and `docs/public_review_checklist.md`.
- The helper should not own scoring, routing, session state, receipts, downloads, uploads, signal logic, privacy scan logic, AI Integrity scan logic, or World Lens math.

This patch does not certify ALETHEIA, guarantee privacy, enforce outcomes, or claim final truth. Humans keep the judgment.
