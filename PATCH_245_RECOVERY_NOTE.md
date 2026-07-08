# PATCH 245 RECOVERY NOTE — Repository Hygiene / Patch Archive Consolidation

## What this patch does
This patch cleans the distributable repository package after the modularization round. It preserves the patch trail, but moves old root-level patch artifacts into the patch archive so the root folder is readable again.

## What changed
- Root-level `PATCH_195` through `PATCH_244` artifacts were moved into `docs/patch_archive/` folders.
- `.git/`, `__pycache__/`, `.pytest_cache/`, and bytecode files were removed from the zip package.
- Current repository status and patch notes were refreshed.

## What did not change
No application behavior was changed. No scoring, scanner, MEI7, Z-axis, Evidence Lab, World Lens, Stress Test, receipt, telemetry, storage, certification, enforcement, or final-authority behavior was changed.

## Recovery
If a patch artifact appears missing at root, check:

```text
docs/patch_archive/manifests/
docs/patch_archive/recovery_notes/
docs/patch_archive/delete_lists/
```

If runtime behavior changes after applying this package, the cause should not be Patch 245 because it is hygiene/documentation-only.
