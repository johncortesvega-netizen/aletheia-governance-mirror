# Patch 206 — Stress Test Semantic Stale-State Alignment Fix

## Problem
Stress Test could show a stale semantic result from Streamlit session state. In practice this meant a scenario like:

> a group of bankers have world power in secret

could still display semantic SANCTUARY/NO SIGNAL even after the scanner itself correctly detected `opaque_capture_claim` as THRESHOLD.

## Change
Stress Test now recomputes semantic diagnostics from the current raw/processed scenario text at render time and chooses the strongest semantic-pressure result among:

- stored session semantic scan;
- current raw + processed Stress Test text;
- visible editor text + processed text.

The strongest scan is saved back into session state.

## Preserved boundary
This patch does not change scoring, scanner weights, receipt schemas, audit math, World Lens, Evidence Lab, Mirror Check, or module routing. It only prevents a stale semantic panel from overriding a stronger current signal.

## Validation
Run:

```bat
python -m py_compile app.py core\semantic_pressure_scanner.py
python -m streamlit run app.py
```

Then test Stress Test with:

```text
a group of bankers have world power in secret
```

Expected semantic panel:

- Semantic finding: THRESHOLD
- Risk: Needs safeguards
- Integrity pressure: about -0.400
- Hit/note: opaque capture-power claim / hidden broad-scale power claim
