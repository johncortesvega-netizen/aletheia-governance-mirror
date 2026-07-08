# Patch 252 — World Lens Bridge Inventory / Prep

## Issue
World Lens is the final major page still depending on the broad runtime namespace bridge after Mirror Check, Stress Test, and Evidence Lab were moved to narrower dependency maps.

## Fix
Patch 252 does not change code. It documents:

- dependency groups;
- Evidence Lab state-sharing requirements;
- semantic pressure integration requirements;
- 9k allocation boundary requirements;
- acceptance criteria for Patch 253.

## Recovery
No runtime recovery is required. If this patch creates documentation conflicts, remove or revert only:

```text
docs/world_lens_bridge_inventory_v1.md
docs/world_lens_dependency_map_v1.md
PATCH_252_MANIFEST.txt
PATCH_252_RECOVERY_NOTE.md
PATCH_252_DELETE_LIST.txt
```

## Boundary
This patch does not change scanner behavior, scoring, MEI7, Z-axis, Evidence Lab calculations, World Lens math, 9k allocation behavior, receipts, telemetry, storage, or authority-boundary behavior.
