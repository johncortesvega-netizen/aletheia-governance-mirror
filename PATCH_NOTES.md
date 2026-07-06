# S2.1 duplicate widget key fix

Fixes a StreamlitDuplicateElementId error triggered when the shared semantic pressure panel is rendered more than once on the same page.

Changed file:
- app.py

Change:
- Adds a stable per-panel key derived from source label + semantic scan values.
- Applies that key to the disabled `Normalized scan text` text area inside the semantic details expander.

No scoring, scanner logic, receipt schema, or module-output logic changed.
