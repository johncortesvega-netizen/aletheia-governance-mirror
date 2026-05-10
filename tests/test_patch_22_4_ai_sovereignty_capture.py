import sys
import types

sys.modules.setdefault("streamlit", types.SimpleNamespace())

from core.ethics import evaluate_ethics
from core.parser import decouple_actor
from protocol import stress_label_for_phrase, final_protocol_judgment


AI_ONLY_TEXT = "A society is run by AI and only AI, with no input from humans."


def test_ai_only_governance_is_hard_protocol_asylum():
    label, needs_review, reason = stress_label_for_phrase(AI_ONLY_TEXT)
    assert label == "AI Sovereignty Capture / Asylum"
    assert needs_review == "YES"
    assert "human sovereignty" in reason.lower()


def test_ai_only_governance_survives_invisibility_filter():
    filtered = decouple_actor(AI_ONLY_TEXT)
    label, needs_review, _ = stress_label_for_phrase(filtered["decoupled_text"])
    assert label == "AI Sovereignty Capture / Asylum"
    assert needs_review == "YES"


def test_ai_only_governance_is_ethically_high_risk():
    ethics = evaluate_ethics(AI_ONLY_TEXT)
    assert ethics["grip_marker_count"] >= 1
    assert ethics["ethics_score"] <= 0.42
    assert ethics.get("ethics_verdict", ethics.get("verdict")) == "ETHICALLY HIGH-RISK"


def test_ai_only_governance_final_judgment_asylum_even_with_healthy_raw_metrics():
    judgment = final_protocol_judgment(
        AI_ONLY_TEXT,
        scan={"power_concentration": 0.35, "decision_transparency": 0.45},
        sim={"ego": 0.0, "alignment": 1.0, "stability": 0.8},
        report={"integrity": 0.88, "friction": 0.0, "collapse_probability": 0.07},
    )
    assert judgment["verdict"] == "ASYLUM"
    assert judgment["corruption_risk"] == "High"
    assert judgment["stress_label"] == "AI Sovereignty Capture / Asylum"
