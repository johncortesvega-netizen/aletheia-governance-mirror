# PATCH STATUS

Current patch: 251 — Evidence Lab Bridge Removal Import Hotfix

Status: ready

Summary:
- Fixes missing hashlib import in the extracted Evidence Lab page after Patch 250.
- Evidence Lab active-input signature hashing now has an explicit local dependency.
- Import-only hotfix; no runtime governance/scoring behavior changed.

Validation:
- python -m py_compile app.py ui/pages/evidence_lab.py
