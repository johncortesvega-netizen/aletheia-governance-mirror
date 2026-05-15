# Patch 136 Recovery Note - Aletheia Unit Preview Stabilization

Patch 136 is a test/check/docs checkpoint for the Patch 135 Aletheia Unit Preview.

Recovery inspection:

1. Review `docs/aletheia_unit_preview_stabilization.md`.
2. Review `tests/test_patch_136_aletheia_unit_preview_stabilization.py`.
3. Confirm `app.py` still gates before module tabs and still renders the normal app after the gate passes.
4. Confirm `ui/unit_preview.py` remains local suggestion logic only.
5. Run:

```bat
python tools\run_patch_checks.py 136
python tools\run_patch_checks.py 135
python tools\run_patch_checks.py 134
python tools\run_protocol_baseline_self_audit.py
```

Boundary preserved: no scoring, verdict routing, receipt schema, receipt generation, signal regex, signal weight, AI Integrity scan behavior, Privacy Audit scan behavior, World Lens math, upload/download behavior, batch behavior, external-call behavior, telemetry, analytics, tracking, storage, identity sync, certification, enforcement, approval/rejection, final-truth claim, or privacy-guarantee claim changed. Human review remains required.
