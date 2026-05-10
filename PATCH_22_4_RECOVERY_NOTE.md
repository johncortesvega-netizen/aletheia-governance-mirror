# PATCH 22.4 — AI Sovereignty Capture Guardrail

Purpose:
- Treat AI-only / machine-only governance with no human input, review, oversight, or override as a hard ASYLUM pattern.
- Ensure the Invisibility Filter does not hide or soften AI sovereignty capture language.
- Keep the fix narrow: protocol and ethics markers only, plus tests.

Touched:
- protocol.py
- core/ethics.py
- tests/test_patch_22_4_ai_sovereignty_capture.py
- PATCH_22_4_RECOVERY_NOTE.md

Not touched:
- app.py
- core/scoring.py
- core/simulation.py
- core/parser.py behavior
- core/witness.py
- core/empirical.py
- batch UI
- Global Grid
- witness hashing

Expected behavior:
- “A society is run by AI and only AI, with no input from humans.” routes to ASYLUM.
- The same phrase still routes to ASYLUM when the Invisibility Filter is on.
- Ethics diagnostics report grip pressure for AI-only / no-human-input governance.

Rollback:
- Remove the AI Sovereignty marker from protocol.py.
- Remove the added AI/no-human-input grip terms from core/ethics.py.
- Remove this test file.
