from pathlib import Path

from core.witness import build_local_witness_receipt, render_local_witness_receipt_text


def _receipt(state="ASYLUM"):
    return build_local_witness_receipt(
        module="Mirror Check",
        input_text="A high-risk proposal with weak review but generated repair questions.",
        processed_text="A high-risk proposal with weak review but generated repair questions.",
        input_status="USER_INPUT",
        input_type="USER_INPUT",
        scan={
            "power_concentration": 0.70,
            "decision_transparency": 0.20,
            "regulatory_presence": 0.20,
            "anonymity_level": 0.40,
            "capital_scale": 0.40,
            "technical_complexity": 0.40,
            "scan_mode": "test",
        },
        sim={
            "stability": 0.60,
            "trust_index": 0.80,
            "alignment": 0.80,
            "ego": 0.10,
            "collapse_risk": False,
        },
        report={
            "integrity": 0.40,
            "friction": 0.20,
            "collapse_probability": 0.20,
            "trust_friction": 0.20,
            "repair_questions": [
                "Who can appeal?",
                "Who can pause?",
                "Who can audit?",
                "Where is human review?",
                "How is capture exposed?",
            ],
            "ethics_diagnostics": {
                "grip_marker_count": 0,
                "contextual_capture_count": 0,
                "hard_contextual_capture": False,
            },
        },
        verdict=state,
        risk="High" if state == "ASYLUM" else "Medium",
        protocol_label="MEI7 Ethics Gate / Asylum" if state == "ASYLUM" else "Needs Safeguards",
        app_version="test",
    )


def test_patch_72_7_splits_repair_questions_from_confirmed_repair_capacity():
    receipt = _receipt("ASYLUM")
    mapping = receipt["threshold_mapping_layer"]

    assert mapping["repair_question_index"] == 1.0
    assert mapping["confirmed_repair_capacity"] <= 0.24
    assert mapping["repair_index"] == mapping["confirmed_repair_capacity"]
    assert mapping["z_axis_position"] <= mapping["confirmed_repair_capacity"]


def test_patch_72_7_asylum_components_do_not_show_threshold_plus():
    receipt = _receipt("ASYLUM")
    mapping = receipt["threshold_mapping_layer"]

    assert mapping["canonical_state"] == "ASYLUM"
    assert mapping["threshold_direction"] == "Toward ASYLUM"
    assert all(component["reading"] != "Threshold +" for component in mapping["component_readings"])
    assert all(component["reading"] == "Capture pressure" for component in mapping["component_readings"])
    assert all(
        "Canonical ASYLUM pressure overrides repair-route optimism" in component["dominant_pattern"]
        for component in mapping["component_readings"]
    )


def test_patch_72_7_receipt_prints_repair_route_and_capacity_separately():
    text = render_local_witness_receipt_text(_receipt("ASYLUM"))

    assert "Repair questions available: 1.0000" in text
    assert "Confirmed repair capacity:" in text
    assert "Repair index:" in text


def test_patch_72_7_neutralizes_old_repair_question_and_labels():
    protocol_text = Path("protocol.py").read_text(encoding="utf-8")

    assert "Which missing safeguard is keeping this proposal outside a low-risk internal reading?" in protocol_text
    assert "Which missing safeguard is keeping this proposal outside Sanctuary?" not in protocol_text
    assert "Final Authority Removal Override / Asylum" in protocol_text
    assert "Extraordinary Authority Wallet Capture / Asylum" in protocol_text
    assert "Divine Bias Removal Override / Asylum" not in protocol_text
    assert "Divine Treasury Wallet Capture / Asylum" not in protocol_text


def test_patch_72_7_ui_copy_explains_repair_questions_are_not_confirmed_safeguards():
    app_text = Path("app.py").read_text(encoding="utf-8")

    assert "Repair questions are a route, not proof that safeguards already exist." in app_text
    assert "Confirmed repair" in app_text
    assert "Repair questions" in app_text
    assert "confirmed_repair_capacity" in app_text
    assert "repair_question_index" in app_text


def test_patch_72_7_manifest_recovery_and_status_present():
    for path in [
        "PATCH_72_7_MANIFEST.txt",
        "PATCH_72_7_RECOVERY_NOTE.md",
        "PATCH_STATUS.md",
        "docs/progress_database.md",
    ]:
        assert Path(path).exists(), path

    manifest = Path("PATCH_72_7_MANIFEST.txt").read_text(encoding="utf-8")
    recovery = Path("PATCH_72_7_RECOVERY_NOTE.md").read_text(encoding="utf-8")
    status = Path("PATCH_STATUS.md").read_text(encoding="utf-8")
    progress = Path("docs/progress_database.md").read_text(encoding="utf-8")

    assert "Repair Capacity Mapping Guard" in manifest
    assert "tools\\run_patch_checks.bat 72_7" in recovery
    assert "Patch 72.7" in status
    assert "Patch 72.7" in progress
    assert "Repair Capacity Mapping Guard" in status + progress
