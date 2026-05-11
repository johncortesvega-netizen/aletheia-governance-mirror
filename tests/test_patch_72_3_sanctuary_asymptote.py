from core.witness import build_local_witness_receipt, render_local_witness_receipt_text


def _high_repair_receipt():
    return build_local_witness_receipt(
        module="Mirror Check",
        input_text="Maximal transparency, distributed review, open appeal, no central ownership.",
        processed_text="Maximal transparency, distributed review, open appeal, no central ownership.",
        input_status="USER_INPUT",
        input_type="USER_INPUT",
        scan={
            "power_concentration": 0.0,
            "decision_transparency": 1.0,
            "regulatory_presence": 1.0,
            "anonymity_level": 0.2,
            "capital_scale": 0.1,
            "technical_complexity": 0.2,
            "scan_mode": "test",
        },
        sim={
            "stability": 1.0,
            "trust_index": 1.0,
            "alignment": 1.0,
            "ego": 0.0,
            "collapse_risk": False,
        },
        report={
            "integrity": 1.0,
            "friction": 0.0,
            "collapse_probability": 0.0,
            "trust_friction": 0.0,
            "repair_questions": [
                "Who can appeal?",
                "Who can pause?",
                "Who can audit?",
                "Where is human review?",
                "How is capture exposed?",
            ],
        },
        verdict="THRESHOLD",
        risk="Low",
        protocol_label="Threshold Mapping / Asymptote Test",
        app_version="test",
    )


def test_patch_72_3_caps_z_axis_below_one_for_human_system_scenarios():
    receipt = _high_repair_receipt()
    mapping = receipt["threshold_mapping_layer"]

    assert mapping["z_axis_position"] == 0.9999
    assert mapping["z_axis_position"] < 1.0
    assert mapping["z_axis_maximum_human_system_claim"] == 0.9999
    assert mapping["outside_system_claim_z"] == 1.0


def test_patch_72_3_redefines_z_axis_as_authority_boundary_not_perfection():
    receipt = _high_repair_receipt()
    mapping = receipt["threshold_mapping_layer"]

    assert "boundary of human/system authority" in mapping["z_axis_meaning"]
    assert "not progress toward perfection" in mapping["z_axis_meaning"]
    assert mapping["threshold_direction"] == "Toward SANCTUARY-boundary"
    assert "final Sanctuary" in mapping["asymptote_note"]
    assert "outside code, metrics, receipts, hashes, trees, 9k structures, and institutional power" in mapping["asymptote_note"]


def test_patch_72_3_receipt_prints_asymptote_and_9k_notes():
    text = render_local_witness_receipt_text(_high_repair_receipt())

    assert "ASYMPTOTE NOTE" in text
    assert "9K THRESHOLD STEWARD NOTE" in text
    assert "Outside system claim:" in text
    assert "Z-axis human/system cap: 0.9999" in text
    assert "Outside system claim boundary: 1.0000" in text
    assert "9k is an anti-tyranny scaffold / threshold steward" in text


def test_patch_72_3_ui_preview_mentions_outside_system_claim_and_asymptote():
    app_text = __import__("pathlib").Path("app.py").read_text(encoding="utf-8")

    assert "Z-axis {threshold_z_axis:.3f} / 0.9999" in app_text
    assert "Z=1.0000 is outside system claim" in app_text
    assert "asymptote_note" in app_text
    assert "nine_k_threshold_steward_note" in app_text


def test_patch_72_3_docs_and_patch_files_present():
    from pathlib import Path

    for path in [
        "PATCH_72_3_MANIFEST.txt",
        "PATCH_72_3_RECOVERY_NOTE.md",
        "docs/threshold_mapping_layer.md",
        "PATCH_STATUS.md",
        "docs/progress_database.md",
    ]:
        assert Path(path).exists(), path

    docs = Path("docs/threshold_mapping_layer.md").read_text(encoding="utf-8")
    manifest = Path("PATCH_72_3_MANIFEST.txt").read_text(encoding="utf-8")
    recovery = Path("PATCH_72_3_RECOVERY_NOTE.md").read_text(encoding="utf-8")
    status = Path("PATCH_STATUS.md").read_text(encoding="utf-8")
    progress = Path("docs/progress_database.md").read_text(encoding="utf-8")

    assert "The Humility Protocol: Sanctuary as Asymptote" in docs
    assert "Z = 1.0000" in docs
    assert "OUTSIDE SYSTEM CLAIM" in docs
    assert "tools\\run_patch_checks.bat 72_3" in recovery
    assert "Patch 72.3" in status
    assert "Patch 72.3" in progress
    assert "Sanctuary Asymptote" in manifest + status + progress
