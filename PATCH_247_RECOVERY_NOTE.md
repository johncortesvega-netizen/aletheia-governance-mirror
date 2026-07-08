# Patch 247 Recovery Note — Mirror Check Bridge Removal

If Mirror Check fails after this patch, restore:
- `app.py`
- `ui/pages/mirror_check.py`

from the previous working state.

Most likely failure mode:
- `RuntimeError: Mirror Check page dependency map is incomplete: ...`

That means Mirror Check is using a dependency that is not listed in `MIRROR_CHECK_DEPENDENCIES`.
Add the missing dependency to the list and to the local variable assignments in `render_mirror_check_page(...)`.

Validation commands:

```cmd
python -m py_compile app.py ui\pages\mirror_check.py
python -m pytest
python -m streamlit run app.py
```

Manual checks:
- Mirror Check opens.
- Review idea works.
- Mirror Reading Tree renders.
- Semantic pressure panel renders.
- Batch testing expander opens.
- Other modules still render one-at-a-time.
