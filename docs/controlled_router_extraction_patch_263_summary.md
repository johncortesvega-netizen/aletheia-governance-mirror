# Patch 263 Summary — Controlled Router Extraction

Patch 263 moves the controlled top-level module selector and dispatch from `app.py` into `ui/main.py`.

`app.py` remains the Streamlit entrypoint and now delegates to `render_controlled_router(...)`.

This patch preserves:

- top-level navigation labels and order;
- `key="aletheia_active_module"`;
- Receipt Reader placement under Why ALETHEIA support utilities;
- page dispatch targets;
- current controlled-router behavior.

This patch does not introduce native multipage, state extraction, config extraction, scoring changes, taxonomy changes, or receipt behavior changes.
