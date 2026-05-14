# Test and Check Hygiene

Patch 131 keeps ALETHEIA in release-candidate refinement mode and improves local validation clarity. It is a maintenance patch only: no runtime behavior change, no scoring change, no verdict-routing change, no receipt schema change, no signal-pattern or signal-weight change, no Privacy Audit scan behavior change, no AI Integrity scan behavior change, and no World Lens math change.

The patch strengthens regression coverage for test/check hygiene risks: UTF-8 JSON manifest loading without a BOM, accidental internal repair-note language, authority or certification claims, final-truth claims, and accidental telemetry, analytics, storage, external-call, identity-sync, Global ID sync, or public-ledger sync language in Patch 131 materials.

## Local validation commands

Use this Windows command pattern from the project checkout:

```bat
set PATH=C:\Users\John\AppData\Local\Python\bin;C:\Users\John\AppData\Local\Python\pythoncore-3.14-64\Scripts;%PATH%
cd C:\Users\John\Desktop\aletheia-governance-mirror
python tools\run_patch_checks.py 131
python tools\run_patch_checks.py 130
python tools\run_patch_checks.py 129
python tools\run_protocol_baseline_self_audit.py
python tools\run_checks.py
python -m streamlit run app.py
```

`tools/run_checks.py` mirrors the existing safe-check batch workflow in `tools/run_checks.bat`: it runs the current patch suite and reports the legacy test inventory as non-blocking context. Patch-specific checks remain deterministic and local.

Boundary preserved: Patch 131 changes tests, validation tooling, documentation, patch status, progress/index records, and the protocol baseline manifest only. It adds no features, modules, UI behavior, external calls, telemetry, analytics, storage, identity sync, Global ID sync, public ledger sync, certification, enforcement, privacy guarantee, or final-truth behavior. Humans keep the judgment.
