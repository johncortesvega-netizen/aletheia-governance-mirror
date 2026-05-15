# Patch 133 Recovery Note - Receipt Reader Standard View Design Doc

Patch 133 is documentation/design only. It defines Receipt Reader - Standard View before any runtime implementation.

Recovery inspection:

1. Review `docs/receipt_reader_standard_view.md`.
2. Confirm there is no runtime Receipt Reader UI and no parser in this patch.
3. Confirm the design states that native receipt values are source of truth and Standard View is an interoperability mapping only.
4. Run:

```bat
python tools\run_patch_checks.py 133
python tools\run_patch_checks.py 132
python tools\run_patch_checks.py 131
python tools\run_protocol_baseline_self_audit.py
```

Boundary preserved: no runtime UI, no parser, no scoring, no receipt schema change, no new risk states, no external standards as authority, no external calls, no telemetry, no storage, no compliance certification language, and no final-truth claim. Human review remains required.
