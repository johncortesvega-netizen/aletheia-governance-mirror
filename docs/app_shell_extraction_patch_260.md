# Patch 260 — App Shell Helper Extraction

Patch 260 performs the first behavior-preserving app-shell extraction after the
Patch 259 inventory.

## What changed

- Moved the Streamlit page configuration and global ALETHEIA CSS theme from
  `app.py` into `ui/app_shell.py`.
- Added `ALETHEIA_GLOBAL_CSS` as the single app-shell CSS constant.
- Added `apply_app_page_config_and_theme(st)` as the shell helper that applies:
  - page title;
  - page icon;
  - wide layout;
  - global CSS.
- Replaced the large inline setup block in `app.py` with:

```python
apply_app_page_config_and_theme(st)
```

## Why this is safe

This patch only moves static shell setup. It does not change routing, session
state, scanner behavior, scoring, MEI7, Z-axis, receipts, Evidence Lab
calculations, World Lens math, telemetry, storage, or the mirror boundary.

## What stays in app.py

- imports and compatibility fallbacks;
- constants and demo metadata;
- remaining protocol/guardrail helpers;
- session-state substrate;
- sidebar interactive controls;
- top-level module routing.

## Next safe step

Patch 261 should extract top-level routing into a `ui/main.py` or similar shell
module while preserving the current controlled single-app navigation behavior.
Native Streamlit multipage remains deferred.
