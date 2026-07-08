# Patch 240 Recovery Note

If Receipt Reader appears missing after Stage 9, apply this patch and open:

`Why ALETHEIA → Support utilities — includes Receipt Reader → Receipt Reader — Standard View`

This patch does not restore Receipt Reader as a top-level module. It clarifies the intended support-utility location.

Validation:

```cmd
python -m py_compile app.py
python -m pytest
python -m streamlit run app.py
```

Check: Why ALETHEIA page shows Support utilities and the Receipt Reader expander.
