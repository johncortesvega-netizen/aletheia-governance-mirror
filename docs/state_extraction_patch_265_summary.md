# Patch 265 summary — State Extraction

Patch 265 creates `ui/state.py` and moves only sidebar review-lens defaults/reset helpers out of `app.py`.

Changed:

- `ui/state.py` added as the first canonical state-helper module.
- `app.py` imports `normalize_sidebar_lens_state` and `reset_sidebar_lens_state`.
- the sidebar reset button delegates to `reset_sidebar_lens_state(st.session_state)`.
- the old `Default` profile migration delegates to `normalize_sidebar_lens_state(st.session_state)`.

Preserved:

- all sidebar widget keys;
- all sidebar default values;
- the legacy `Default` → `Starting preset` normalization;
- app.py as the Streamlit entrypoint;
- `ui/main.py` as the controlled-router owner;
- active suite behavior.

Not changed:

- no router/session key rename;
- no Evidence Lab, World Lens, Mirror Check, or Stress Test state movement;
- no protocol/scoring/taxonomy/Z-axis/receipt behavior movement.
