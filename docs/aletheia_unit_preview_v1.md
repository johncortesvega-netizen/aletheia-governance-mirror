# Aletheia Unit Preview v1

Patch 135 adds Aletheia Unit Preview as a small front-door preview before the full app appears.

The preview helps users decide where to begin. It does not decide for them.

## Behavior

The preview appears before the normal ALETHEIA module tabs. Users may paste a short text, question, scenario, or receipt and click `Preview review path`. The preview shows a `Suggested path` and a short explanation based on transparent keyword rules.

Users can still choose any module after entering ALETHEIA. Clicking `Proceed to ALETHEIA` sets the Streamlit session key `aletheia_unit_preview_passed` and reruns the app so the normal module interface appears.

The choice is session-only. It is not persisted beyond the active Streamlit session.

## Boundary

Aletheia Unit Preview suggests where to begin. It does not score, certify, approve, reject, or replace the full modules.

ALETHEIA gives readings, not verdicts. Human judgment remains required.

For sensitive material, run locally. Hosted deployments may have platform-level logs outside ALETHEIA's app-code boundary.

## Local Rules

The preview uses simple local rules:

- receipt-like text suggests Receipt Reader - Standard View;
- AI prompt, model-output, agent, or code-like text suggests AI Integrity Mirror;
- scenario, stress, or pressure language suggests Stress Test;
- review or audit questions suggest Mirror Check / Question Review;
- evidence, CSV, dataset, source, upload, or documentation language suggests Evidence Lab;
- country/year or governance context language suggests World Lens;
- otherwise it suggests Mirror Check.

These are suggestions, not decisions.

## Non-Expansion Boundary

Patch 135 does not change scoring, verdict routing, taxonomy, SANCTUARY / THRESHOLD / ASYLUM logic, QUESTION_PROMPT logic, receipt schema, receipt generation, signal regexes, signal weights, AI Integrity scan behavior, Privacy Audit scan behavior, World Lens math, uploads/download behavior, batch behavior, data storage, or external calls.

It adds no chatbot, LLM calls, embeddings, agentic routing, automatic approval, automatic rejection, compliance finding, legal/medical/political/institutional authority claim, accounts, persistent user profiles, database, Global ID sync, public ledger sync, new scoring engine, new risk states, final-truth claim, or privacy guarantee.
