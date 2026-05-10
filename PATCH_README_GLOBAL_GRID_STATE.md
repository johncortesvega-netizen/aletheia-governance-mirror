# ALETHEIA v9.6.8 — Shared Protocol State / Global Grid Guard Patch

This patch makes intentional cross-mode propagation visible and doctrine-safe.

## Included changes

1. Added a visible **Shared Protocol State** notice in Audit, Simulation, Empirical Study, and Global Grid.
2. Added a **Protocol State Diagnostics** panel showing empirical/scored evidence status, trust/WGI/V-Dem activity, synthetic demo state, Sydney Protocol state, selected evidence year, selected context, Grid basis, and last update source.
3. Introduced a shared `st.session_state["protocol_state"]` object for visible protocol-state propagation.
4. Namespaced newly touched local UI controls for Audit, Simulation, and Grid to reduce accidental widget bleed while preserving intentional protocol-state propagation.
5. Added a Global Grid partial-coverage guard with `MIN_FULL_GRID_COUNTRIES = 100`.
6. Added dynamic Grid source-state labels:
   - Full empirical scored master
   - Partial empirical subset
   - Prototype regional brackets
   - Inactive/no valid dataset
7. Added sparse-year warning language so low-row selected years, such as a 3-country 2024 subset, are reported as partial-subset diagnostics rather than full global allocations.
8. Clarified that Trust/WGI/V-Dem coverage cards reflect the active selected-year subset after filters, not whole-dataset coverage.
9. Preserved empirical ingestion/scoring behavior and did not create a stable snapshot/tag.

## Validation

`python -m py_compile app.py` passes.
