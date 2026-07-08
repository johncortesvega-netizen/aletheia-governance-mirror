# Patch 246 Recovery Note — App-wide Copy Cleanup Pass

Patch 246 is a copy-only cleanup patch. If any copy change feels conceptually weaker, restore the affected string from the previous version while keeping the rest of the patch.

## Recovery steps

1. Restore the affected file from the previous commit or from the pre-Patch-246 backup.
2. Re-run:

```cmd
python -m py_compile app.py ui/pages/*.py ui/components/*.py
python -m pytest
```

3. Confirm the app still opens with:

```cmd
python -m streamlit run app.py
```

## What must not change during recovery

- Scanner behavior
- Scoring behavior
- MEI7 gate behavior
- Z-axis behavior
- Evidence Lab calculations
- World Lens math
- Receipt schema or receipt generation
- Telemetry/storage posture
- Mirror-not-throne boundary
