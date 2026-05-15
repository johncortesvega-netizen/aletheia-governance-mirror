# PATCH 143 RECOVERY NOTE — Public Repository Hygiene / Reviewer Onboarding

Patch 143 is a documentation/structure patch. If it causes confusion, revert these files:

- README.md
- CONTRIBUTING.md
- PATCH_STATUS.md
- docs/reviewer_start_here.md
- docs/glossary.md
- docs/validation_and_precision.md
- docs/how_to_review_aletheia_without_trusting_it.md
- docs/patch_archive/README.md
- docs/patch_archive/root_patch_artifact_index.md
- docs/patch_index.md
- docs/progress_database.md
- docs/architecture.md
- tools/archive_root_patch_artifacts.py
- tests/test_patch_143_public_repo_reviewer_onboarding.py
- data/protocol_baseline_manifest.json

If `tools/archive_root_patch_artifacts.py` is run in a full checkout, historical root-level patch artifacts are moved into `docs/patch_archive/`. The helper does not delete the audit trail. Reversal is a normal file move from the archive folders back to the repository root.

No app behavior, scoring, verdict routing, taxonomy, receipt schema/generation, World Lens math, AI Integrity behavior, Privacy Audit behavior, external calls, telemetry/storage, certification, enforcement, or final-truth behavior is changed by this patch.
