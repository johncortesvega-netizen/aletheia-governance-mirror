# Start Page Stabilization Checkpoint

Patch 132 records the Start Page / How to Start gate as stable in release-candidate refinement mode.

The gate is intentionally small:

- `app.py` remains the orchestrator.
- `ui/start_page.py` renders static first-entry copy and a single `Proceed to ALETHEIA` button.
- The only gate state is the Streamlit session key `aletheia_start_gate_passed`.
- When the key is missing or false, the Start Page renders and `st.stop()` prevents the normal module interface from rendering.
- When the button is clicked, the session key is set to true and `st.rerun()` reveals the existing app.

This is session-state-only behavior. It does not use cookies, accounts, persistent storage, telemetry, analytics, auth, tracking, external calls, local LLM calls, embeddings, or a database.

The normal ALETHEIA module interface remains the same after the gate passes. Patch 132 adds checkpoint documentation and regression tests only; it does not change scoring, routing, receipt schemas, signal behavior, Privacy Audit scan behavior, AI Integrity scan behavior, World Lens math, uploads, downloads, or receipt generation.

Boundary preserved: the Start Page gives orientation, not approval. It does not certify, enforce, approve, reject, guarantee privacy, or claim final truth. Humans keep the judgment.
