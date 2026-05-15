# PATCH 147 RECOVERY NOTE — Root Patch Hygiene / Latest Patch Only

Patch 147 archives older root-level patch artifacts while keeping the current patch visible at the repository root.

## Recovery

If the archive move needs to be reviewed or reversed, use Git history or move files from:

```text
docs/patch_archive/manifests/
docs/patch_archive/recovery_notes/
docs/patch_archive/other_patch_artifacts/
```

back to the repository root.

## Standard future update rule

For each future GitHub update:

```bash
python tools/archive_root_patch_artifacts.py --dry-run --current-patch <patch_id>
python tools/archive_root_patch_artifacts.py --current-patch <patch_id>
```

Keep only the latest patch manifest and recovery note visible at root. Archive older patch artifacts; do not delete the audit trail.

## Boundary

This patch is repository hygiene only. It does not alter app behavior, scoring, verdict routing, taxonomy, receipts, signal behavior, World Lens math, AI Integrity behavior, Privacy Audit behavior, upload/download behavior, telemetry/storage/network behavior, certification, enforcement, or authority claims.

Human review remains required. Patch history is evidence for review, not proof of truth, safety, legality, privacy, or integrity.
