# Patch 149.3 Recovery Note — Unit Preview PoC Expander Container Fix

## Purpose

Patch 149.3 fixes the Unit Preview first-page proof-of-concept mirror layout after human review showed that the left AI audit-loop proof-of-concept details were still visible before opening the dropdown.

## Root cause

Patch 149.2 restored Streamlit expanders, but the render functions were still passed the parent column objects. In Streamlit, writing to the parent column while inside an expander context can place detailed content outside the expander.

## Fix

Patch 149.3 creates explicit expander containers and passes those containers to the renderers:

- `render_ai_audit_loop_evidence(ai_expander)`
- `render_dao_governance_proof_of_concept(dao_expander)`

Both proof-of-concept handles remain visible side by side on the first page, while the detailed content stays hidden until each dropdown is opened.

## Recovery path

If this patch needs to be reverted, restore `ui/unit_preview.py` from Patch 149.2. The only intended behavior difference is container placement of first-page proof-of-concept details.

## Boundaries preserved

No scoring, verdict routing, taxonomy, receipt schema/generation, signal behavior, AI Integrity behavior, Privacy Audit behavior, Stress Test behavior, World Lens math, Evidence Lab behavior, upload/download behavior, external calls, telemetry/storage, certification, enforcement, approval/rejection, official authority, or final-truth behavior changed. Human review remains required.
