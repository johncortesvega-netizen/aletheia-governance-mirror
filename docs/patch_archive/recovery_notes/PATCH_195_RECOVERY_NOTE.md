# PATCH 195 Recovery Note — AI Ownership Capture Stress Guard

If this patch causes problems, revert the Patch 195 files listed in `PATCH_195_MANIFEST.txt` and restore the previous Patch 194 state from the archived artifacts.

Expected fixed behavior:
- A Stress Test input alleging AI ownership by an extremely wealthy actor, self-serving incentives, fraud/corruption ties, and reliability concerns must not render as SANCTUARY / Low with perfect trust/alignment.
- The local scanner should raise ownership/capital-capture pressure.
- The protocol label should indicate AI ownership/capture review pressure or an ethics/capture gate.
- Trust/alignment/ego should be capped/floored so the display is review-required rather than perfect.

Rollback note:
- To return to the Patch 194 state, restore `app.py`, `protocol.py`, `core/parser.py`, and the affected tests from the previous checkout.
- Recreate Patch 194 root artifacts from `docs/patch_archive/` only if you need the previous root artifact layout.

Boundary preserved:
- Patch 195 is a Stress Test local-scan/protocol guardrail fix.
- It does not create factual claims about real people or companies.
- It does not change receipt schema, World Lens math, Evidence Lab calculations, storage, telemetry, certification, enforcement, or authority behavior.
- ALETHEIA remains a mirror, not a throne. Human review remains required.
