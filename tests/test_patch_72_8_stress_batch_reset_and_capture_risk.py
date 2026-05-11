from pathlib import Path

from core.witness import build_local_witness_receipt, render_local_witness_receipt_text


def test_patch_72_8_stress_batch_uses_signature_and_hides_stale_results():
    app_text = Path("app.py").read_text(encoding="utf-8")

    assert "stress_batch_signature = hashlib.sha256(" in app_text
    assert "stress_batch_active_signature" in app_text
    assert "stress_batch_is_stale = stress_batch_has_active_results and not stress_batch_matches_active" in app_text
    assert "The Stress batch input has changed. The previous batch result is closed for this draft." in app_text
    assert "Click Run Stress Batch to create a new batch and receipts." in app_text
    assert 'st.session_state.stress_batch_active_signature = stress_batch_signature' in app_text
    assert 'st.session_state.get("stress_batch_summary") and not stress_batch_is_stale' in app_text
    assert 'st.session_state.get("stress_batch_archive_bytes") and not stress_batch_is_stale' in app_text
    assert "Last closed Stress batch" in app_text


def test_patch_72_8_stress_batch_stale_branch_does_not_offer_download():
    app_text = Path("app.py").read_text(encoding="utf-8")
    start = app_text.index("if stress_batch_is_stale and st.session_state.get")
    end = app_text.index('if "last_report" not in st.session_state:', start)
    stale_branch = app_text[start:end]

    assert "Last closed Stress batch" in stale_branch
    assert "download_button" not in stale_branch
    assert "stress_batch_archive_bytes" not in stale_branch


def test_patch_72_8_asylum_receipt_separates_simulation_collapse_from_protocol_capture():
    receipt = build_local_witness_receipt(
        module="Simulation",
        input_text="High-risk scenario",
        processed_text="High-risk scenario",
        input_status="USER_INPUT",
        input_type="USER_INPUT",
        scan={
            "power_concentration": 0.70,
            "decision_transparency": 0.20,
            "regulatory_presence": 0.20,
            "anonymity_level": 0.30,
            "capital_scale": 0.30,
            "technical_complexity": 0.30,
            "scan_mode": "test",
        },
        sim={
            "stability": 0.80,
            "trust_index": 0.80,
            "alignment": 0.80,
            "ego": 0.10,
            "collapse_risk": False,
        },
        report={
            "integrity": 0.45,
            "friction": 0.20,
            "collapse_probability": 0.20,
            "trust_friction": 0.10,
            "repair_questions": ["Who can appeal?", "Who can pause?"],
        },
        verdict="ASYLUM",
        risk="High",
        protocol_label="MEI7 Ethics Gate / Asylum",
        app_version="test",
    )

    assert receipt["metrics"]["collapse_risk"] is False
    assert receipt["verdict"]["protocol_capture_risk"] is True
    assert "distinct from the raw simulation collapse-risk boolean" in receipt["verdict"]["protocol_capture_risk_note"]

    text = render_local_witness_receipt_text(receipt)
    assert "Collapse risk: False" in text
    assert "Protocol capture risk: True" in text
    assert "Protocol capture risk note:" in text


def test_patch_72_8_non_high_receipt_does_not_force_protocol_capture_risk():
    receipt = build_local_witness_receipt(
        module="Simulation",
        input_text="Medium scenario",
        processed_text="Medium scenario",
        input_status="USER_INPUT",
        input_type="USER_INPUT",
        scan={
            "power_concentration": 0.30,
            "decision_transparency": 0.70,
            "regulatory_presence": 0.70,
            "scan_mode": "test",
        },
        sim={
            "stability": 0.80,
            "trust_index": 0.80,
            "alignment": 0.80,
            "ego": 0.10,
            "collapse_risk": False,
        },
        report={
            "integrity": 0.60,
            "friction": 0.20,
            "collapse_probability": 0.20,
            "trust_friction": 0.10,
            "repair_questions": [],
        },
        verdict="THRESHOLD",
        risk="Medium",
        protocol_label="Needs Safeguards",
        app_version="test",
    )

    assert receipt["verdict"]["protocol_capture_risk"] is False
    assert receipt["verdict"]["protocol_capture_risk_note"] is None


def test_patch_72_8_manifest_recovery_and_status_present():
    for path in [
        "PATCH_72_8_MANIFEST.txt",
        "PATCH_72_8_RECOVERY_NOTE.md",
        "PATCH_STATUS.md",
        "docs/progress_database.md",
    ]:
        assert Path(path).exists(), path

    manifest = Path("PATCH_72_8_MANIFEST.txt").read_text(encoding="utf-8")
    recovery = Path("PATCH_72_8_RECOVERY_NOTE.md").read_text(encoding="utf-8")
    status = Path("PATCH_STATUS.md").read_text(encoding="utf-8")
    progress = Path("docs/progress_database.md").read_text(encoding="utf-8")

    assert "Stress Batch Input Reset and Protocol Capture Risk Presentation" in manifest
    assert "tools\\run_patch_checks.bat 72_8" in recovery
    assert "Patch 72.8" in status
    assert "Patch 72.8" in progress
    assert "Stress Batch Input Reset" in status + progress
