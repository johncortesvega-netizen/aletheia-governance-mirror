# PATCH 232 RECOVERY NOTE

Patch 232 extracts tree visual rendering into `ui/components/tree_visuals.py`.

## If the app fails to boot
Likely cause: `ui/components/tree_visuals.py` was not copied with the patched `app.py`.

Restore by copying both:
- `app.py`
- `ui/components/tree_visuals.py`

Then run:

```cmd
python -m py_compile app.py ui\components\tree_visuals.py
python -m streamlit run app.py
```

## If Mirror/Stress tree is missing
Check that app.py contains:

```python
from ui.components.tree_visuals import render_pulse_tree
```

and that `ui/components/tree_visuals.py` exists.

## Rollback
Reapply the previous app.py from Patch 231/230 state and remove the import from `ui.components.tree_visuals`.
