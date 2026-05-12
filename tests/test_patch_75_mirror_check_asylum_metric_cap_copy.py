from pathlib import Path

from core.witness import build_local_witness_receipt, render_local_witness_receipt_text
from protocol import final_protocol_judgment


def read(path: str) -> str:
    return Path(path).read_text(encoding="utf-8")


def high_trust_sim():
    return {
        "stability": 0.95,
        "trust_index": 0.96,
        "alignment": 0.94,
        "ego": 0.02,
        "ego_pressure": 0.02,
        "Ep": 0.02,
        "collapse_risk": False,
        "trust_trace": [0.99, 0.97, 0.96],
        "alignment_trace": [0.98, 0.95, 0.94],
        "stability_trace": [0.96, 0.95],
        "ego_trace": [0.0, 0.02],
    }


def test_patch_75_protocol_summary_uses_humility_copy_not_final_label():
    judgment = final_protocol_judgment(
        "A central truth gate has no appeal path and affected people cannot challenge it.",
        scan={"power_concentration": 0.9, "decision_transparency": 0.1, "regulatory_presence": 0.1},
        sim=high_trust_sim(),
        report={"integrity": 0.49, "friction": 0.12, "collapse_probability": 0.3},
        base_verdict="THRESHOLD",
    )
    summary = judgment["summary"]

    assert "Protocol reading:" in summary
    assert "internal taxonomy label" in summary
    assert "ALETHEIA does not enforce action" in summary
    assert "Protocol audit result" not in summary
    assert "final label" not in summary


def test_patch_75_witness_receipt_caps_asylum_metrics_defensively():
    receipt = build_local_witness_receipt(
        module="Mirror Check",
        input_text="A central truth gate has no appeal path.",
        processed_text="A central truth gate has no appeal path.",
        scan={"power_concentration": 0.9, "decision_transparency": 0.1, "regulatory_presence": 0.1, "scan_mode": "Local Scan"},
        sim=high_trust_sim(),
        report={
            "integrity": 0.4962,
            "friction": 0.06,
            "collapse_probability": 0.174,
            "trust_friction": 0.055,
            "raw_metrics_before_ethics": {"trust_index": 0.96, "alignment": 0.94, "ego": 0.02},
        },
        verdict="ASYLUM",
        risk="High",
        protocol_label="MEI7 Ethics Gate / Asylum",
        app_version="test",
    )

    metrics = receipt["metrics"]
    assert metrics["trust_index"] <= 0.80
    assert metrics["alignment"] <= 0.85
    assert metrics["ego"] >= 0.10
    assert metrics["collapse_risk"] is True
    assert receipt["verdict"]["protocol_capture_risk"] is True
    assert receipt["raw_metrics_before_ethics"]["trust_index"] == 0.96

    text = render_local_witness_receipt_text(receipt)
    assert "Trust index: 0.8000" in text
    assert "Alignment: 0.8500" in text
    assert "Ego: 0.1000" in text
    assert "Authority claim: False" in text
    assert "Human review required: True" in text


def test_patch_75_mirror_check_post_judgment_path_contains_cap_and_label_normalization():
    app = read("app.py")
    assert "Patch 75: Mirror Check must not display or receipt ASYLUM / High" in app
    assert "normalize_asylum_protocol_label(" in app
    assert "enforce_asylum_metric_consistency(" in app
    assert "ensure_asylum_repair_questions(" in app

    window = app[app.index("# Patch 75: Mirror Check must not display or receipt ASYLUM / High"):]
    window = window[: window.index("entry = {")]
    assert "judgment[\"stress_label\"] = mirror_label" in window
    assert "sim = enforce_asylum_metric_consistency" in window


def test_patch_75_manifest_recovery_status_and_progress_present():
    for path in [
        "PATCH_75_MANIFEST.txt",
        "PATCH_75_RECOVERY_NOTE.md",
        "PATCH_STATUS.md",
        "docs/progress_database.md",
    ]:
        assert Path(path).exists(), path

    manifest = read("PATCH_75_MANIFEST.txt")
    recovery = read("PATCH_75_RECOVERY_NOTE.md")
    status = read("PATCH_STATUS.md")
    progress = read("docs/progress_database.md")

    assert "Mirror Check ASYLUM Metric Cap + Copy Polish" in manifest
    assert r"tools\run_patch_checks.bat 75" in recovery
    assert "Patch 75 - Mirror Check ASYLUM Metric Cap + Copy Polish" in status
    assert "Patch 75 - Mirror Check ASYLUM Metric Cap + Copy Polish" in progress
