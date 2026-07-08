# Patch 255 Recovery Note — Patch Notes Final Cleanup

Patch 255 is documentation/archive hygiene only.

## If something looks missing

Patch files from earlier recent patches were moved out of the repository root into:

- `docs/patch_archive/manifests/`
- `docs/patch_archive/recovery_notes/`
- `docs/patch_archive/delete_lists/`

They were not deleted as part of the intended cleanup.

## Rollback

To roll back the root layout only, copy the desired `PATCH_N_*` files back from `docs/patch_archive/` into the repository root.
No runtime rollback is required because Patch 255 does not modify application behavior.

## Runtime impact

None. This patch only touches patch notes, archive organization, and status documentation.
