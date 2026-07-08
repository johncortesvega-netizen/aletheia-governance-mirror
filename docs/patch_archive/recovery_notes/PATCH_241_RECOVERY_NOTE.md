# Patch 241 Recovery Note

If Mirror Check explanatory panels regress visually, restore `app.py` from the previous stable patch and reapply only the global Receipt Reader caption manually.

Validation:

```cmd
python -m py_compile app.py
python -m pytest
python -m streamlit run app.py
```

Check:
- Mirror Check opens.
- Latest reading appears.
- How-to-read panels are full-width sequential expanders.
- Receipt Reader location hint is visible below the top module selector.
