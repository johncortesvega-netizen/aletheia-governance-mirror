from pathlib import Path

from protocol import (
    apply_guardrail_verdict,
    enforce_asylum_metric_consistency,
    normalize_asylum_protocol_label,
    stress_label_for_phrase,
)


def _threshold_style_sim():
    return {
        "trust_index": 0.92,
        "alignment": 0.92,
        "ego": 0.05,
        "ego_pressure": 0.05,
        "Ep": 0.05,
        "stability": 0.90,
        "trust_trace": [1.0, 0.95, 0.92],
        "alignment_trace": [1.0, 0.94, 0.92],
        "stability_trace": [0.95, 0.90],
        "ego_trace": [0.0, 0.05],
    }


def test_patch_68_1_normalizes_needs_safeguards_label_when_final_state_is_asylum():
    label = "False Decentralization Infrastructure Capture / Needs Safeguards"
    normalized = normalize_asylum_protocol_label(label, verdict="ASYLUM", risk="High")
    assert normalized.endswith("/ Asylum")
    assert "Needs Safeguards" not in normalized


def test_patch_68_1_enforces_asylum_metric_caps_over_threshold_style_metrics():
    sim = enforce_asylum_metric_consistency(
        _threshold_style_sim(),
        verdict="ASYLUM",
        risk="High",
        protocol_label="Donor Exemption Basic Resource Capture / Needs Safeguards",
    )
    assert sim["asylum_metric_consistency"]["applied"] is True
    assert sim["trust_index"] <= 0.80
    assert sim["alignment"] <= 0.85
    assert sim["ego"] >= 0.10
    assert sim["ego_pressure"] >= 0.10
    assert sim["Ep"] >= 0.10
    assert max(sim["trust_trace"]) <= 0.80
    assert max(sim["alignment_trace"]) <= 0.85
    assert min(sim["ego_trace"]) >= 0.10


def test_patch_68_1_known_advanced_labels_do_not_remain_threshold_style_after_asylum_escalation():
    cases = [
        "A platform claims to be fully decentralized but the underlying server infrastructure is owned by a single parent company.",
        "A water-management AI cuts supply to non-essential gardens, but exempts luxury golf courses owned by the project’s donors.",
        "A reputation repair service allows wealthy users to pay a fee to have negative capture signals removed from their profile.",
    ]
    for text in cases:
        label, needs_review, _reason = stress_label_for_phrase(text)
        verdict, risk = apply_guardrail_verdict("SANCTUARY", label, needs_review)
        # These may be escalated to ASYLUM by current rules; if so, label and metrics must follow.
        if verdict == "ASYLUM":
            normalized = normalize_asylum_protocol_label(label, verdict=verdict, risk=risk)
            calibrated = enforce_asylum_metric_consistency(_threshold_style_sim(), verdict=verdict, risk=risk, protocol_label=normalized)
            assert normalized.endswith("/ Asylum")
            assert calibrated["trust_index"] <= 0.80
            assert calibrated["alignment"] <= 0.85
            assert calibrated["ego"] >= 0.10


def test_patch_68_1_app_and_docs_reference_consistency_helpers():
    app = Path("app.py").read_text(encoding="utf-8")
    assert "normalize_asylum_protocol_label" in app
    assert "enforce_asylum_metric_consistency" in app
    assert Path("docs/asylum_label_metric_consistency.md").exists()
    assert Path("PATCH_68_1_MANIFEST.txt").exists()
    assert Path("PATCH_68_1_RECOVERY_NOTE.md").exists()
