# Patch 144 Recovery Note — README 60-Second Clarity / Reviewer Path Polish

Patch 144 is documentation/readability only.

To recover:

1. Revert the changed documentation and test files listed in `PATCH_144_MANIFEST.txt`.
2. Restore `data/protocol_baseline_manifest.json` from the previous baseline if reverting the patch.
3. Rerun:

```bat
python tools\run_patch_checks.py 143
python tools\run_patch_checks.py 142_16
python tools\run_protocol_baseline_self_audit.py
```

No runtime migration is required. Patch 144 does not change scoring, routing, taxonomy, receipts, World Lens math, AI Integrity behavior, Privacy Audit behavior, upload/download behavior, telemetry/storage posture, or app module behavior.

Human review remains required. ALETHEIA remains a mirror, not a throne.
