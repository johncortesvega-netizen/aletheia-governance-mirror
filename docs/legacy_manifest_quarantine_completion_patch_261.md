# Patch 261 — Legacy Manifest Quarantine Completion

## Purpose

Patch 261 completes the Patch 256 legacy-manifest quarantine list after a follow-up full-suite triage found 16 historical patch-contract tests that still asserted the old root-level `PATCH_N_*` artifact layout.

This is a test-governance cleanup only. It does not change runtime behavior.

## Context

Patch 255 intentionally moved old patch manifests, recovery notes, and delete lists out of repository root and into the patch archive:

```text
docs/patch_archive/manifests/
docs/patch_archive/recovery_notes/
docs/patch_archive/delete_lists/
```

Patch 256 then quarantined historical tests that still expected those artifacts to live in the repository root. A later full-suite triage showed that 16 files with the same obsolete contract remained outside the quarantine list.

## Files added to the root-artifact quarantine list

The following files were added to `PATCH_ARTIFACT_ROOT_CONTRACT_QUARANTINE` in `tests/conftest.py`:

```text
tests/test_patch_81_android_webview_hello_android_guard.py
tests/test_patch_82_android_app_icon_webview_template_purge.py
tests/test_patch_83_android_gradle_plugin_resolution.py
tests/test_patch_84_android_adaptive_icon_resource_fix.py
tests/test_patch_88_ai_integrity_signal_evidence.py
tests/test_patch_93_ai_integrity_demo_pack.py
tests/test_patch_95_code_integrity_static_scan.py
tests/test_patch_96_privacy_boundary_audit_panel.py
tests/test_patch_97_ai_integrity_comparison_view.py
tests/test_patch_98_red_team_prompt_pack.py
tests/test_patch_99_ai_integrity_report_builder.py
tests/test_patch_101_protocol_baseline_self_audit.py
tests/test_patch_103_signal_detection_transparency.py
tests/test_patch_107_boundary_privacy_ui_wiring.py
tests/test_patch_108_app_shell_router_refactor.py
tests/test_patch_131_test_check_hygiene.py
```

## Interpretation

These tests are not quarantined because their subjects are unimportant. They are quarantined because their artifact-location contract is obsolete after Patch 255.

The tests remain on disk for audit continuity. They can later be restored by rewriting them to inspect `docs/patch_archive/` rather than the repository root.

## Boundary preserved

Patch 261 does not change:

- scanner behavior;
- scoring;
- MEI7;
- Z-axis routing;
- semantic pressure logic;
- receipts;
- Evidence Lab calculations;
- World Lens math;
- navigation;
- telemetry/storage posture;
- authority-boundary language.

## Validation target

```bat
python -m py_compile tests\conftest.py
python -m pytest
python -m pytest tests --collect-only -q
```
