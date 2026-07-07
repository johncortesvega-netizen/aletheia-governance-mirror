# Patch 205 — Stress Test Semantic Raw/Filtered Alignment

## Issue
In Stress Test, semantic pressure signals could show `NO SIGNAL` / `SANCTUARY` for text such as:

`a group of bankers have world power in secret`

while the main Stress Test reading correctly showed high-risk/capture pressure.

The mismatch happened because Stress Test may run the main audit on Invisibility-Filter processed text. The processed text is useful for reducing actor/name bias, but the semantic layer needs access to the raw phrase when the raw phrase carries the structural pattern.

## Fix
- Added `choose_stress_semantic_scan(raw_text, processed_text)`.
- Stress Test now scans both raw and processed user text when available.
- It keeps the stronger semantic-pressure signal using state rank, integrity pressure, and evidence count.
- Included current opaque-capture semantic calibration in `core/semantic_pressure_scanner.py`.

## Expected result
For:

`a group of bankers have world power in secret`

Stress Test semantic panel should show a THRESHOLD diagnostic with an opaque/capture-power signal, not `NO SIGNAL`.

## Preserved boundaries
No scoring, receipt schema, module routing, external calls, telemetry, storage, certification, enforcement, or final truth claim changed.
