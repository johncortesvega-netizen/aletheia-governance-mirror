# Patch 224 — Modularization Stage 1 Clean Import Repair

## Symptom
After Patch 221/222, Streamlit may still crash in every module with:

```text
NameError: name 're' is not defined
```

inside:

```text
ui/components/semantic_pressure_panel.py
```

## Cause
The local `semantic_pressure_panel.py` did not receive the corrected import header, or stale copied files/compiled cache remained after applying the earlier hotfix.

## Fix
Replace only:

```text
ui/components/semantic_pressure_panel.py
```

with the file from this patch. Then remove cache folders:

```cmd
rmdir /s /q __pycache__
rmdir /s /q ui\__pycache__
rmdir /s /q ui\components\__pycache__
```

If a folder does not exist, Windows may show an error; that is harmless.

## Test

```cmd
python -m py_compile app.py ui\components\semantic_pressure_panel.py
python -m pytest
python -m streamlit run app.py
```

## Boundary
This patch only repairs imports. It does not change scoring, semantic scanner behavior, MEI7, Z-axis, receipts, Evidence Lab, World Lens, or authority boundaries.
