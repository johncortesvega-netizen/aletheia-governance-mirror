# Patch 239 Recovery Note — Mirror Check Page Extraction

If Mirror Check fails after applying this patch:

1. Restore the previous `app.py` from Patch 238 or your last Git commit.
2. Remove `ui/pages/mirror_check.py`.
3. Re-run:

```cmd
python -m py_compile app.py
python -m pytest
python -m streamlit run app.py
```

This patch is a page extraction only. It should not alter governance readings, semantic scans, receipts, World Lens data, or Evidence Lab calculations.
