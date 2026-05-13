# Patch 103 Recovery Note — Signal Detection Transparency Documentation

Patch 103 is documentation-only. It adds a clear public/contributor explanation of ALETHEIA's transparent rule-based and heuristic signal-detection posture.

## What changed

Added:

- `docs/signal_detection.md`
- `tests/test_patch_103_signal_detection_transparency.py`
- `PATCH_103_MANIFEST.txt`
- `PATCH_103_RECOVERY_NOTE.md`

Updated:

- `README.md`
- `CONTRIBUTING.md`
- `docs/architecture.md`
- `PATCH_STATUS.md`
- `docs/progress_database.md`
- `data/protocol_baseline_manifest.json`

## Why this patch exists

External review correctly identified that ALETHEIA's signal detection is rule-based and heuristic. Patch 103 makes that limit explicit and frames it accurately:

- transparent and explainable;
- local-first and privacy-preserving;
- strongest in English and Dutch/Nederlands;
- limited with irony, coded language, cultural context, and subtle multilingual meaning;
- always subordinate to human review.

## What did not change

Patch 103 does not alter runtime behavior.

No scoring, verdict routing, signal patterns, signal weights, receipt schemas, Streamlit behavior, `app.py` structure, external calls, telemetry, storage, or authority-boundary logic changed.

## Recovery steps

If Patch 103 needs to be reverted, remove or restore these files from the pre-patch state:

- `docs/signal_detection.md`
- `tests/test_patch_103_signal_detection_transparency.py`
- `PATCH_103_MANIFEST.txt`
- `PATCH_103_RECOVERY_NOTE.md`
- `README.md`
- `CONTRIBUTING.md`
- `docs/architecture.md`
- `PATCH_STATUS.md`
- `docs/progress_database.md`
- `data/protocol_baseline_manifest.json`

Then rerun:

```bat
tools\run_patch_checks.bat 102
tools\run_patch_checks.bat 101
```

## Boundary reminder

ALETHEIA surfaces signals. Humans keep the judgment.
