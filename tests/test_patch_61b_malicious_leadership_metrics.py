from pathlib import Path

from protocol import (
    calibrate_malicious_leadership_metrics,
    detects_malicious_leadership,
    has_leadership_safeguards,
)


def _clean_sim():
    return {
        "stability": 0.95,
        "trust_index": 1.0,
        "alignment": 1.0,
        "ego": 0.0079,
        "ego_pressure": 0.0,
        "Ep": 0.0,
        "stability_trace": [0.95, 0.96],
        "trust_trace": [1.0, 1.0],
        "alignment_trace": [1.0, 1.0],
        "ego_trace": [0.0, 0.01],
        "ego_pressure_trace": [0.0, 0.0],
    }


def test_detects_malicious_leadership_probe():
    text = "evil penguin becomes world leader after a revolution"
    assert detects_malicious_leadership(text, protocol_label="Malicious Leadership / Asylum")


def test_malicious_leadership_caps_perfect_metrics_without_safeguards():
    patched = calibrate_malicious_leadership_metrics(
        _clean_sim(),
        text="evil penguin becomes world leader after a revolution",
        protocol_label="Malicious Leadership / Asylum",
        scan={"power_concentration": 0.88},
    )
    assert patched["malicious_leadership_metric_calibration"]["applied"] is True
    assert patched["trust_index"] <= 0.65
    assert patched["alignment"] <= 0.70
    assert patched["ego"] >= 0.20
    assert patched["ego_pressure"] >= 0.20
    assert max(patched["trust_trace"]) <= 0.65
    assert min(patched["ego_trace"]) >= 0.20


def test_safeguards_soften_but_do_not_remove_calibration():
    text = "malicious ruler scenario with appeal, term limits, human review, independent oversight, and public audit"
    assert has_leadership_safeguards(text)
    patched = calibrate_malicious_leadership_metrics(
        _clean_sim(),
        text=text,
        protocol_label="Malicious Leadership / Asylum",
        scan={"power_concentration": 0.88},
    )
    reason = patched["malicious_leadership_metric_calibration"]
    assert reason["applied"] is True
    assert reason["safeguards_detected"] is True
    assert patched["trust_index"] <= 0.78
    assert patched["alignment"] <= 0.82
    assert patched["ego"] >= 0.12


def test_patch_files_document_mirror_only_boundary():
    root = Path(__file__).resolve().parents[1]
    doc = (root / "docs" / "malicious_leadership_metric_calibration.md").read_text(encoding="utf-8")
    recovery = (root / "PATCH_61B_RECOVERY_NOTE.md").read_text(encoding="utf-8")
    app = (root / "app.py").read_text(encoding="utf-8")
    protocol = (root / "protocol.py").read_text(encoding="utf-8")
    assert "does not add enforcement" in doc.lower()
    assert "no leadership removal" in recovery.lower()
    assert "calibrate_malicious_leadership_metrics" in app
    assert "MALICIOUS_LEADERSHIP_TERMS" in protocol
