# Patch 122 Recovery Note

Patch 122 is a stabilization checkpoint for the current app-shell router refactor sequence.

If recovery is needed, restore the changed files listed in `PATCH_122_MANIFEST.txt` from the previous accepted baseline. This patch should be reversible without affecting scoring, routing, receipts, uploads, downloads, privacy scan logic, AI Integrity scan logic, World Lens math, or session state because it adds documentation and tests only.

Review focus:

- `docs/refactor_stabilization_checkpoint_2.md` describes the checkpoint boundary.
- `tests/test_patch_122_refactor_stabilization_checkpoint_2.py` verifies helper importability, `app.py` wiring, copy-only helper limits, and non-authoritative language.
- Status and architecture docs identify Patch 122 as a no-behavior-change checkpoint.
- `data/protocol_baseline_manifest.json` records the updated baseline for human review.

This patch does not certify ALETHEIA, guarantee privacy, enforce outcomes, or claim final truth. Humans keep the judgment.
