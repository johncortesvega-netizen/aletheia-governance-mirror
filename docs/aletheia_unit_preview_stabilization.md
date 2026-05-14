# Aletheia Unit Preview Stabilization

Patch 136 stabilizes the Aletheia Unit Preview added in Patch 135.

This checkpoint confirms that the preview remains a front-door suggestion layer only. It suggests where to begin, then lets the user proceed to the existing ALETHEIA app. It is not a router, classifier, scoring engine, chatbot, agent, receipt generator, or authority layer.

## Stabilized Behavior

- `app.py` remains the orchestrator.
- `ui/unit_preview.py` renders before the normal module tabs.
- The gate uses the Streamlit session key `aletheia_unit_preview_passed`.
- If the key is missing or false, the Unit Preview renders and `st.stop()` prevents the normal module interface from rendering.
- If `Proceed to ALETHEIA` is clicked, the key is set to true and `st.rerun()` reveals the existing app.
- The preference is not stored beyond the active Streamlit session.

## No-Drift Boundary

Patch 136 changes tests, documentation, patch records, and the baseline manifest only. It does not change:

- scoring;
- verdict routing;
- taxonomy;
- SANCTUARY / THRESHOLD / ASYLUM logic;
- QUESTION_PROMPT logic;
- receipt schema;
- receipt generation;
- signal regexes;
- signal weights;
- AI Integrity scan behavior;
- Privacy Audit scan behavior;
- World Lens math;
- upload/download behavior;
- batch behavior;
- data storage;
- external calls.

The preview does not use cookies, accounts, local storage, telemetry, analytics, tracking, persistent profiles, database, Global ID sync, public ledger sync, LLM calls, embeddings, or agentic routing.

## Boundary Copy

Aletheia Unit Preview suggests where to begin. It does not score, certify, approve, reject, or replace the full modules.

ALETHEIA gives readings, not verdicts. Human judgment remains required.

For sensitive material, run locally. Hosted deployments may have platform-level logs outside ALETHEIA's app-code boundary.
