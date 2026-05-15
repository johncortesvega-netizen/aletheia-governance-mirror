# Patch 106 Recovery Note — Signal Dictionary and Glossary

## Scope

Patch 106 is documentation-only. It adds a reviewer-facing signal dictionary / glossary and links it from the existing signal-detection, public-trust, contributor, patch-index, and README surfaces.

## Rollback

To roll back Patch 106, remove or revert these files:

- `docs/SIGNAL_DICTIONARY.md`
- `tests/test_patch_106_signal_dictionary_glossary.py`
- `PATCH_106_MANIFEST.txt`
- `PATCH_106_RECOVERY_NOTE.md`

Then revert the Patch 106 edits in:

- `docs/signal_detection.md`
- `docs/public_trust_package.md`
- `docs/patch_index.md`
- `examples/Trust_Package_README.md`
- `CONTRIBUTING.md`
- `README.md`
- `PATCH_STATUS.md`
- `docs/progress_database.md`
- `data/protocol_baseline_manifest.json`

## Boundary check

Patch 106 does not change scoring, verdict routing, signal patterns, signal weights, receipt schema, Streamlit page wiring, `app.py`, external-call behavior, telemetry, analytics, storage, Global ID sync, public ledger sync, or enforcement behavior.

The signal dictionary is a reviewer-facing glossary, not a scoring specification. It does not certify truth, safety, legality, ethics, privacy, security, legitimacy, vendors, models, institutions, or artifacts.

Human review remains required.

## Verification

Run:

```bat
tools\run_patch_checks.bat 106
tools\run_patch_checks.bat 105
tools\run_patch_checks.bat 104
tools\run_patch_checks.bat 103
tools\run_patch_checks.bat 102
tools\run_patch_checks.bat 101
python tools\run_protocol_baseline_self_audit.py
```
