# Patch 226 Recovery Note — Navigation Containment Refactor

## What changed
The top-level `st.tabs(APP_NAVIGATION_LABELS)` navigation was replaced with a single active-module selector. Each module body is now wrapped behind a conditional check so only the selected module renders.

## Why
The previous tab approach could show inactive tab content after reruns, especially in long stateful modules. This created the appearance that every tab loaded into one page.

## Recovery
If this patch causes problems, restore the previous `app.py` from Patch 221/225 state. No data, scanner, scoring, receipt, or core logic migration is required.

## Test
```cmd
python -m py_compile app.py
python -m pytest
python -m streamlit run app.py
```

Then switch through all top-level modules and confirm only one module body is visible at a time.
