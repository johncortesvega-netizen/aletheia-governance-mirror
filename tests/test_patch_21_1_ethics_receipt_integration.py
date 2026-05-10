from pathlib import Path

from core.ethics import evaluate_ethics
from core.witness import build_local_witness_receipt, render_local_witness_receipt_text

APP_TEXT = Path("app.py").read_text(encoding="utf-8")
WITNESS_TEXT = Path("core/witness.py").read_text(encoding="utf-8")


def test_mirror_check_runs_contextual_ethics_before_receipts():
    assert "from core.ethics import evaluate_ethics" in APP_TEXT
    assert "ethics_diagnostics = evaluate_ethics" in APP_TEXT
    assert 'report["ethics_diagnostics"] = ethics_diagnostics' in APP_TEXT
    assert 'report["ethics_adjusted_integrity"]' in APP_TEXT


def test_witness_receipt_renders_contextual_ethics_diagnostics():
    ethics = evaluate_ethics(
        "This policy protects fairness and rights through mandatory enforcement and a central grid.",
        governance_result={"power_concentration": 0.72, "decision_transparency": 0.35, "regulatory_presence": 0.4},
    )
    receipt = build_local_witness_receipt(
        module="Mirror Check",
        input_text="This policy protects fairness and rights through mandatory enforcement and a central grid.",
        processed_text="This policy protects fairness and rights through mandatory enforcement and a central grid.",
        report={
            "integrity": 0.88,
            "friction": 0.0,
            "collapse_probability": 0.07,
            "trust_friction": 0.0,
            "ethics_diagnostics": ethics,
            "ethics_adjusted_integrity": min(0.88, ethics["ethics_score"]),
        },
        sim={"stability": 0.8, "trust_index": 1.0, "alignment": 1.0, "ego": 0.0, "collapse_risk": False},
        scan={"power_concentration": 0.72, "decision_transparency": 0.35, "scan_mode": "Local Scan"},
        verdict="THRESHOLD",
        risk="Medium",
        protocol_label="MEI7 Ethics Gate / Needs Safeguards",
        generated_at_utc="2026-01-01T00:00:00Z",
    )
    text = render_local_witness_receipt_text(receipt)
    assert "CONTEXTUAL ETHICS DIAGNOSTICS" in text
    assert "Ethics-adjusted integrity:" in text
    assert "Micro sovereignty:" in text
    assert receipt["ethics_diagnostics"]["contextual_capture_count"] >= 1
    assert receipt["ethics_diagnostics"]["ethics_adjusted_integrity"] <= receipt["metrics"]["integrity"]


def test_witness_hash_includes_ethics_diagnostics_contract():
    assert '"ethics_score": ethics_summary.get("ethics_score")' in WITNESS_TEXT
    assert '"contextual_capture_count": ethics_summary.get("contextual_capture_count")' in WITNESS_TEXT
    assert '"ethics_diagnostics": ethics_summary' in WITNESS_TEXT
