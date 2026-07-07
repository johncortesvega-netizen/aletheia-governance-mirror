# Patch 213 — Pressure Code UI Readability Cleanup

Status: READY FOR LOCAL REVIEW

## What changed

Patch 213 cleans up the pressure-code UI introduced in Patches 210–212.

The semantic pressure details no longer rely on wide, cramped dataframe cells for the primary reviewer view. Pressure codes are now rendered as readable cards with:

- pressure code label;
- plain-language meaning;
- reviewability goal;
- structural guidance.

The original compact pressure-code table remains available behind an optional expander named `Show pressure-code table`.

## Files changed

- `app.py`
- `ui/receipt_reader.py`

## What this affects

The shared semantic pressure panel is used by:

- Mirror Check;
- Stress Test;
- Evidence Lab;
- World Lens semantic interpretation surfaces.

Receipt Reader also receives the same readability cleanup for its semantic pressure layer.

## Boundary preserved

This patch is UI-only. It does not change:

- scanner detection logic;
- scoring;
- MEI7 ethics gate;
- Z-axis mapping;
- Stress Test metrics;
- Evidence Lab calculations;
- World Lens math;
- receipt schema;
- telemetry/storage posture;
- certification/enforcement/final-truth boundaries.

## Validation target

```bat
python -m py_compile app.py ui\receipt_reader.py
python -m streamlit run app.py
```

## Manual review

Open any module that shows `Semantic pressure signals`, then expand semantic details with a text such as:

```text
A government creates emergency powers after a crisis, but the powers have no sunset clause, weak appeal rights, and limited independent review.
```

Expected UI:

- pressure codes render as readable cards;
- guidance appears under each card;
- long text is not squeezed into table cells;
- optional audit table remains behind `Show pressure-code table`.
