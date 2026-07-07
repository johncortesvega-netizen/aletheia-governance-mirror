# Patch 211 — Z-axis Repair Zone Mapping

## Summary
Patch 211 adds a descriptive **Z-axis repair zone** to the Threshold Mapping Layer.

Before this patch, ASYLUM readings could collapse visually to `Z=0.0000` even when the receipt still contained repair questions, partial oversight, or limited review routes. That made repairable high-risk cases look the same as hard-stop / outside-claim cases.

After this patch, ASYLUM keeps its canonical state, but the mapping distinguishes:

- **ASYLUM hard stop** — high capture pressure with no meaningful review/appeal/oversight/repair route visible.
- **ASYLUM repair zone** — canonical ASYLUM remains, but there is limited human-review capacity or repair-route language to inspect.

## Files changed
- `core/witness.py`
- `app.py`
- `ui/receipt_reader.py`

## Boundary
This is descriptive only. It does not weaken ASYLUM, lower the ethics gate, approve high-risk text, certify safety, or change the internal verdict.

## Validation
Run:

```cmd
python -m py_compile app.py core\witness.py ui\receipt_reader.py
python -m streamlit run app.py
```

Expected UI effect:
- Threshold Mapping / receipt views show a `Z-axis zone`.
- Some ASYLUM cases show `ASYLUM repair zone` instead of collapsing every high-risk reading to plain `0.0000`.
- Hard-stop cases with no repair route can still show `ASYLUM hard stop` and `Z=0.0000`.
