# ALETHEIA Patch 21.1 — Connect Ethics Context to Mirror Check Receipts

Purpose:
- Surface Patch 21 contextual ethics diagnostics in Mirror Check local witness receipts.
- Make contextual capture, grip markers, micro-sovereignty, and ethics-adjusted integrity visible to the user.
- Keep this diagnostic only: no verdict logic, scoring formulas, protocol precedence, or UI layout changes.

Touched:
- `app.py`
- `core/witness.py`
- `tests/test_patch_21_1_ethics_receipt_integration.py`
- `PATCH_21_1_RECOVERY_NOTE.md`

Not touched:
- `protocol.py`
- `core/scoring.py`
- `core/simulation.py`
- `core/parser.py`
- `core/empirical.py`
- verdict formulas
- batch UI classification
- Global Grid / public ledger / Global ID behavior

Expected behavior:
- Mirror Check still runs as before.
- Local receipts now include a `CONTEXTUAL ETHICS DIAGNOSTICS` section when ethics diagnostics are available.
- Machine-readable receipt JSON includes `ethics_diagnostics`.
- `ethics_adjusted_integrity` is shown as a diagnostic value, not as a replacement for the existing integrity metric.

Rollback:
- Revert the `evaluate_ethics` wiring in `app.py`.
- Revert the `ethics_diagnostics` receipt rendering in `core/witness.py`.
- Remove this recovery note and the Patch 21.1 test file.
