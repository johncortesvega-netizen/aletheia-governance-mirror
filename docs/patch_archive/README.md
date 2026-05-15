# Patch Archive Navigation

ALETHEIA has a long patch trail because changes are kept small and reviewable. The patch trail is part of the project's human-auditable record, but root-level patch files can make the repository harder for new reviewers to enter.

Patch 143 introduces this archive navigation layer and a one-time helper script for maintainers who want to move historical patch artifacts into an archive structure without deleting them.

Suggested archive layout:

```text
docs/patch_archive/
  manifests/
  recovery_notes/
  other_patch_artifacts/
```

The audit trail should be preserved. Archiving is for navigability only; it does not certify ALETHEIA, prove integrity, or replace Git history.

## One-time helper

Use this only when intentionally cleaning a full repository checkout:

```bash
python tools/archive_root_patch_artifacts.py --dry-run
python tools/archive_root_patch_artifacts.py
```

The helper moves root-level historical `PATCH_*_MANIFEST.txt` and `PATCH_*_RECOVERY_NOTE.md` files into the archive folders. It does not delete them.

Patched-items-only zip users may need to run the helper after extracting the patch because zip extraction cannot remove old root files by itself.
