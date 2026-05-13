# Patch 127 Recovery Note — Encoding Cleanup and Tab Icon Restore

Patch 127 is a public UI text cleanup patch.

If it needs to be rolled back, restore the files listed in `PATCH_127_MANIFEST.txt` from the Patch 126 baseline or reapply the Patch 126 local-review stabilization hotfix.

## What changed

- Restored app navigation tab icons and page icon after UTF-8 mojibake appeared in the UI.
- Replaced visible mojibake punctuation such as broken em dashes, bullets, arrows, ellipses, and smart apostrophes in public app text.
- Cleaned the extracted About page and public progress notes where the same encoding corruption appeared.
- Added a regression test that fails if common mojibake tokens return to the public UI surface.
- Kept the Patch 126 stabilization test compatible with later baseline manifests.

## What did not change

Patch 127 does not change scoring, verdict routing, signal patterns, signal weights, receipt schemas, module routing, session state, upload handling, download handling, privacy scan behavior, AI Integrity scan behavior, World Lens math, external calls, telemetry, analytics, storage or identity sync, privacy guarantees, certification, enforcement, or final-truth behavior.

Human review remains required. ALETHEIA surfaces signals; humans keep the judgment.
