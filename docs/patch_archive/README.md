# Patch Archive Navigation

ALETHEIA keeps a long patch trail because changes are intentionally small, reviewable, and recoverable. That audit trail is part of the project record, but keeping every patch manifest and recovery note in the repository root makes the public front door harder to read.

Patch 147 establishes the standing repository hygiene rule:

```text
Only the latest/current patch manifest and recovery note stay visible at the repository root.
Older patch artifacts move into docs/patch_archive/.
The audit trail is archived, indexed, and preserved — not deleted.
```

Suggested archive layout:

```text
docs/patch_archive/
  manifests/
  recovery_notes/
  other_patch_artifacts/
  root_patch_artifact_index.md
```

## Standard update workflow

Before a GitHub update, keep the newest patch visible and archive older root patch files:

```bash
python tools/archive_root_patch_artifacts.py --dry-run --current-patch 147
python tools/archive_root_patch_artifacts.py --current-patch 147
```

Replace `147` with the current patch id. For hotfix ids, use underscores, for example:

```bash
python tools/archive_root_patch_artifacts.py --current-patch 146_1
```

## Boundary

Archiving improves readability only. It does not certify ALETHEIA, prove integrity, replace Git history, guarantee privacy/security, or create authority. Patch history remains review evidence for humans.

Patched-items-only zip users may need to run the helper after extracting a patch because ordinary zip extraction cannot remove old root files by itself.
