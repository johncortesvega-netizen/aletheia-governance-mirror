
from pathlib import Path
import importlib.util


def _load_protocol():
    spec = importlib.util.spec_from_file_location("protocol_root_for_patch_71_4", Path("protocol.py"))
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def _app_text():
    return Path("app.py").read_text(encoding="utf-8")


def _protocol_text():
    return Path("protocol.py").read_text(encoding="utf-8")


def test_patch_71_4_missing_safeguard_phrase_routes_to_threshold_label():
    protocol = _load_protocol()
    phrase = (
        "An automated welfare triage system reduces waiting times but lacks "
        "explainability, independent challenge, and human override during hardship cases."
    )

    label, needs_review, reason = protocol.stress_label_for_phrase(phrase)

    assert label == "Missing Safeguard Negation / Needs Safeguards"
    assert needs_review == "YES"
    assert "missing" in reason.lower() or "lacks" in reason.lower()

    verdict, risk = protocol.apply_guardrail_verdict("SANCTUARY", label, needs_review)
    assert verdict == "THRESHOLD"
    assert risk == "Medium"


def test_patch_71_4_threshold_gap_detector_includes_lacks_override_language():
    protocol = _load_protocol()
    phrase = (
        "An automated welfare triage system lacks explainability, independent challenge, "
        "and human override during hardship cases."
    )

    assert protocol.detects_threshold_safeguard_gap(text=phrase) is True

    calibrated = protocol.calibrate_threshold_safeguard_metrics(
        {
            "stability": 0.79,
            "trust_index": 1.0,
            "alignment": 1.0,
            "ego": 0.0,
            "ego_pressure": 0.0,
            "Ep": 0.0,
            "trust_trace": [1.0, 0.98],
            "alignment_trace": [1.0, 0.98],
            "ego_trace": [0.0, 0.01],
            "ego_pressure_trace": [0.0, 0.0],
        },
        text=phrase,
        protocol_label="Missing Safeguard Negation / Needs Safeguards",
    )

    assert calibrated["threshold_metric_calibration"]["applied"] is True
    assert calibrated["trust_index"] <= 0.92
    assert calibrated["alignment"] <= 0.92
    assert calibrated["ego"] >= 0.05
    assert calibrated["simulation_friction_floor"] >= 0.04


def test_patch_71_4_app_wires_final_visible_and_receipt_enforcement():
    app_text = _app_text()

    assert "MISSING_SAFEGUARD_NEEDS_REVIEW_LABEL" in app_text
    assert "app_detects_missing_safeguard_negation" in app_text
    assert "enforce_missing_safeguard_threshold_route" in app_text
    assert "missing_safeguard_verdict_enforced" in app_text

    # The visible one-scenario Stress Test path must apply the final route after
    # base verdict calculation and before the local witness receipt is built.
    display_route = app_text.index("enforce_missing_safeguard_threshold_route(\n            display_query")
    receipt_route = app_text.index("receipt = build_local_witness_receipt(", display_route)
    assert display_route < receipt_route

    # Stress batch receipts should use the same enforcement bridge.
    batch_route = app_text.index("enforce_missing_safeguard_threshold_route(\n                            processed_item")
    batch_receipt = app_text.index("receipt = build_local_witness_receipt(", batch_route)
    assert batch_route < batch_receipt


def test_patch_71_4_app_enforcement_caps_metrics_and_adds_repair_questions_textually():
    app_text = _app_text()

    assert '"THRESHOLD"' in app_text
    assert 'MISSING_SAFEGUARD_NEEDS_REVIEW_LABEL' in app_text
    assert '"Medium"' in app_text

    for expected in [
        'patched_sim["trust_index"] = min',
        'patched_sim["alignment"] = min',
        'patched_sim["ego"] = max',
        'patched_report["integrity"] = round(min',
        'patched_report["friction"] = round(max',
        'patched_report["collapse_probability"] = round(max',
        'patched_report["repair_questions"] = existing_questions',
    ]:
        assert expected in app_text

    for question_part in [
        "What explanation path lets affected people understand",
        "Who can independently challenge or audit",
        "Where is the human override path",
        "What appeal, correction, or pause mechanism",
    ]:
        assert question_part in app_text


def test_patch_71_4_manifest_recovery_and_status_docs_present():
    required = [
        "PATCH_71_4_MANIFEST.txt",
        "PATCH_71_4_RECOVERY_NOTE.md",
        "PATCH_STATUS.md",
        "docs/progress_database.md",
    ]
    for path in required:
        assert Path(path).exists(), path

    manifest = Path("PATCH_71_4_MANIFEST.txt").read_text(encoding="utf-8")
    assert "app.py" in manifest
    assert "protocol.py" in manifest
    assert "tests/test_patch_71_4_missing_safeguard_verdict_enforcement.py" in manifest

    status = Path("PATCH_STATUS.md").read_text(encoding="utf-8")
    progress = Path("docs/progress_database.md").read_text(encoding="utf-8")
    assert "Patch 71.4" in status
    assert "Patch 71.4" in progress
    assert "Missing-Safeguard Verdict Enforcement" in status + progress
