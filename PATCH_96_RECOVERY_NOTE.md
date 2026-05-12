# PATCH 96 RECOVERY NOTE — Privacy Boundary Audit Panel

Patch 96 adds a static Privacy Boundary Audit Panel to AI Integrity Mirror.

## Recovery / rollback

To roll back Patch 96, remove the Patch 96 additions from:

- `core/ai_integrity_mirror.py`
- `app.py`
- `docs/ai_integrity_mirror.md`
- `README.md`
- `PATCH_STATUS.md`
- `docs/progress_database.md`

Then delete:

- `docs/privacy_boundary_audit_panel.md`
- `PATCH_96_MANIFEST.txt`
- `PATCH_96_RECOVERY_NOTE.md`
- `tests/test_patch_96_privacy_boundary_audit_panel.py`

## Boundary reminder

Privacy Boundary Audit is static pasted-artifact review only. It does not monitor runtime behavior, inspect hosting logs, crawl dependencies or repositories, call external services, certify privacy, approve compliance, audit vendors, audit hosting providers, or prove that no data is collected.

ALETHEIA remains a mirror, not a throne. Patch 96 is review support, not authority.
