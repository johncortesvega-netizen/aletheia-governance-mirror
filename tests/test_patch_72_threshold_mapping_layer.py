from core.witness import build_local_witness_receipt, render_local_witness_receipt_text


def _receipt_for(scan, sim, report, verdict="THRESHOLD", label="MEI7 Ethics Gate / Needs Safeguards"):
    return build_local_witness_receipt(
        module="Mirror Check",
        input_text="Threshold mapping scenario",
        processed_text="Threshold mapping scenario",
        input_status="USER_INPUT",
        input_type="USER_INPUT",
        scan=scan,
        sim=sim,
        report=report,
        verdict=verdict,
        risk="Medium",
        protocol_label=label,
        app_version="test",
    )


def test_patch_72_threshold_mapping_routes_capture_pressure_toward_asylum():
    receipt = _receipt_for(
        scan={
            "power_concentration": 0.90,
            "decision_transparency": 0.10,
            "regulatory_presence": 0.15,
            "anonymity_level": 0.40,
            "capital_scale": 0.50,
            "technical_complexity": 0.70,
            "scan_mode": "test",
        },
        sim={
            "stability": 0.40,
            "trust_index": 0.35,
            "alignment": 0.30,
            "ego": 0.80,
            "collapse_risk": True,
        },
        report={
            "integrity": 0.40,
            "friction": 0.50,
            "collapse_probability": 0.68,
            "trust_friction": 0.30,
            "ethics_diagnostics": {
                "grip_marker_count": 5,
                "contextual_capture_count": 4,
                "hard_contextual_capture": True,
            },
            "repair_questions": ["Who can appeal this?", "What pauses automated action?"],
        },
    )

    mapping = receipt["threshold_mapping_layer"]
    assert receipt["verdict"]["protocol_adjusted_state"] == "THRESHOLD"
    assert mapping["canonical_state"] == "THRESHOLD"
    assert mapping["threshold_direction"] == "Toward ASYLUM"
    assert mapping["z_axis_position"] < 0
    assert mapping["integrity_gap"] == 0.6
    assert any("Conditional access" in signal or "Central truth-gate" in signal for signal in mapping["asylum_pressure_signals"])


def test_patch_72_threshold_mapping_routes_distributed_repair_toward_sanctuary():
    receipt = _receipt_for(
        scan={
            "power_concentration": 0.20,
            "decision_transparency": 0.82,
            "regulatory_presence": 0.78,
            "anonymity_level": 0.40,
            "capital_scale": 0.20,
            "technical_complexity": 0.45,
            "scan_mode": "test",
        },
        sim={
            "stability": 0.80,
            "trust_index": 0.82,
            "alignment": 0.88,
            "ego": 0.12,
            "collapse_risk": False,
        },
        report={
            "integrity": 0.81,
            "friction": 0.20,
            "collapse_probability": 0.12,
            "trust_friction": 0.12,
            "ethics_diagnostics": {
                "grip_marker_count": 0,
                "contextual_capture_count": 0,
                "hard_contextual_capture": False,
            },
            "repair_questions": [
                "Who can appeal?",
                "How is the audit public?",
                "Where is human review?",
                "How can the model be paused?",
            ],
        },
    )

    mapping = receipt["threshold_mapping_layer"]
    assert mapping["threshold_direction"] == "Toward SANCTUARY"
    assert mapping["z_axis_position"] > 0
    assert mapping["repair_index"] == 0.8
    assert any("Repair questions" in signal for signal in mapping["sanctuary_growth_signals"])
    assert {row["component"] for row in mapping["component_readings"]} == {"Power balance", "Correction", "Access"}


def test_patch_72_threshold_mapping_is_receipt_layer_not_new_taxonomy():
    receipt = _receipt_for(
        scan={
            "power_concentration": 0.50,
            "decision_transparency": 0.50,
            "regulatory_presence": 0.50,
            "anonymity_level": 0.40,
            "capital_scale": 0.30,
            "technical_complexity": 0.50,
            "scan_mode": "test",
        },
        sim={
            "stability": 0.55,
            "trust_index": 0.55,
            "alignment": 0.55,
            "ego": 0.45,
            "collapse_risk": False,
        },
        report={
            "integrity": 0.55,
            "friction": 0.35,
            "collapse_probability": 0.35,
            "trust_friction": 0.20,
            "repair_questions": ["What appeal path exists?"],
        },
    )

    mapping = receipt["threshold_mapping_layer"]
    assert receipt["verdict"]["protocol_adjusted_state"] == "THRESHOLD"
    assert mapping["threshold_direction"] in {"Balanced THRESHOLD", "Toward ASYLUM", "Toward SANCTUARY"}
    assert "does not create a new verdict" in mapping["note"]


def test_patch_72_threshold_mapping_appears_between_raw_metrics_and_scanner_features():
    receipt = _receipt_for(
        scan={
            "power_concentration": 0.20,
            "decision_transparency": 0.82,
            "regulatory_presence": 0.78,
            "anonymity_level": 0.40,
            "capital_scale": 0.20,
            "technical_complexity": 0.45,
            "scan_mode": "test",
        },
        sim={
            "stability": 0.80,
            "trust_index": 0.82,
            "alignment": 0.88,
            "ego": 0.12,
            "collapse_risk": False,
        },
        report={
            "integrity": 0.81,
            "friction": 0.20,
            "collapse_probability": 0.12,
            "trust_friction": 0.12,
            "repair_questions": ["Who can appeal?", "Where is human review?"],
        },
    )
    text = render_local_witness_receipt_text(receipt)

    raw_idx = text.index("RAW METRICS BEFORE ETHICS")
    mapping_idx = text.index("THRESHOLD MAPPING LAYER")
    scanner_idx = text.index("SCANNER FEATURES")
    assert raw_idx < mapping_idx < scanner_idx
    assert "Threshold direction:" in text
    assert "Z-axis position:" in text
    assert "Repair index:" in text
    assert "Component readings:" in text


def test_patch_72_manifest_recovery_docs_present():
    for path in [
        "PATCH_72_MANIFEST.txt",
        "PATCH_72_RECOVERY_NOTE.md",
        "docs/threshold_mapping_layer.md",
        "PATCH_STATUS.md",
        "docs/progress_database.md",
    ]:
        assert __import__("pathlib").Path(path).exists(), path

    manifest = __import__("pathlib").Path("PATCH_72_MANIFEST.txt").read_text(encoding="utf-8")
    status = __import__("pathlib").Path("PATCH_STATUS.md").read_text(encoding="utf-8")
    progress = __import__("pathlib").Path("docs/progress_database.md").read_text(encoding="utf-8")
    docs = __import__("pathlib").Path("docs/threshold_mapping_layer.md").read_text(encoding="utf-8")

    assert "Threshold Mapping Layer" in manifest
    assert "Patch 72" in status
    assert "Patch 72" in progress
    assert "Threshold Mapping Layer" in docs
    assert "SANCTUARY / THRESHOLD / ASYLUM" in docs
