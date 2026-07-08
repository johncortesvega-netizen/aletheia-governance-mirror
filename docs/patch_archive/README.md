# Patch Archive

This directory preserves ALETHEIA patch artifacts without keeping every patch file in the repository root.

## Structure

- `manifests/` — patch manifests (`PATCH_N_MANIFEST.txt`)
- `recovery_notes/` — recovery notes (`PATCH_N_RECOVERY_NOTE.md`)
- `delete_lists/` — delete lists (`PATCH_N_DELETE_LIST.txt`)
- `other_patch_artifacts/` — older or non-standard patch records if retained

## Current archive inventory

- Manifests archived: 287
- Recovery notes archived: 325
- Delete lists archived: 72

## Root policy

The repository root should only keep the current patch status and current patch artifacts.
Older patch records belong here so the patch chain remains inspectable without cluttering the working root.

## Boundary

The archive is documentation/history only. It is not runtime code, not a release gate, and not an authority layer.
