# Patch 131 Recovery Note - Start Page / How to Start Gate

Patch 131 adds a first-entry Start Page / How to Start gate. The normal module interface remains unchanged after the user clicks `Proceed to ALETHEIA`.

Recovery inspection:

1. Review `ui/start_page.py`. It is a copy-only helper with one proceed button.
2. Review the small `app.py` gate after `st.set_page_config`. It checks `st.session_state["aletheia_start_gate_passed"]`, renders the Start Page when missing or false, sets the key when the button is clicked, reruns the app, and stops before the main modules render.
3. Run the validation commands below.

```bat
python tools\run_patch_checks.py 131
python tools\run_patch_checks.py 130
python tools\run_patch_checks.py 129
python tools\run_protocol_baseline_self_audit.py
```

Boundary preserved: no scoring, routing, receipts, receipt schema, signal regex, signal weights, Privacy Audit scan behavior, AI Integrity scan behavior, World Lens math, uploads, downloads, telemetry, analytics, tracking, cookies, accounts, persistent storage, external calls, local LLM calls, embeddings, database, auth, login, certifying claim, enforcement claim, approval/rejection claim, privacy-guarantee claim, or final-truth claim changed. Humans keep the judgment.
