# Patch 260 Recovery Note

If Patch 260 causes a startup issue, restore:

- `app.py`
- `ui/app_shell.py`

from the previous working patch.

Patch 260 only moves the global Streamlit page setup and CSS theme into
`ui/app_shell.py`. It does not intentionally change runtime behavior.
