# Patch 135 Recovery Note - Aletheia Unit Preview v1

Patch 135 adds Aletheia Unit Preview as a front-door preview before the full ALETHEIA app appears.

Recovery inspection:

1. Review `ui/unit_preview.py`. It uses transparent local keyword rules and does not call scoring, receipt, AI Integrity, Privacy Audit, or World Lens engines.
2. Review the small `app.py` gate after `st.set_page_config`. It checks `st.session_state["aletheia_unit_preview_passed"]`, renders the preview when missing or false, sets the key when `Proceed to ALETHEIA` is clicked, reruns the app, and stops before the normal module tabs render.
3. Confirm the preview only suggests where to begin. It does not decide, score, certify, approve, reject, or replace modules.
4. Run:

```bat
python tools\run_patch_checks.py 135
python tools\run_patch_checks.py 134
python tools\run_patch_checks.py 133
python tools\run_protocol_baseline_self_audit.py
```

Boundary preserved: no chatbot, LLM calls, embeddings, agentic routing, automatic approval/rejection, certification, compliance finding, authority claim, final-truth claim, privacy guarantee, telemetry, analytics, accounts, persistent profiles, database, Global ID sync, public ledger sync, scoring, verdict routing, taxonomy, receipt schema, receipt generation, signal regex, signal weight, AI Integrity scan behavior, Privacy Audit scan behavior, World Lens math, upload/download behavior, batch behavior, storage, or external-call change. Human review remains required.
