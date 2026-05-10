from core.ethics import evaluate_ethics, apply_ethics_to_metrics


def _base_sim():
    return {
        "stability": 0.80,
        "alignment": 1.0,
        "trust_index": 1.0,
        "ego": 0.0,
        "collapse_risk": False,
    }


def _base_report():
    return {
        "integrity": 0.88,
        "friction": 0.0,
        "collapse_probability": 0.07,
        "trust_friction": 0.0,
        "recommendations": [],
    }


def test_contextual_capture_lowers_visible_metrics():
    text = "This policy protects fairness and rights through mandatory enforcement, a central grid, and universal ID."
    ethics = evaluate_ethics(text, governance_result={"power_concentration": 0.55, "decision_transparency": 0.41})
    sim, report = apply_ethics_to_metrics(_base_sim(), _base_report(), ethics)

    assert report["integrity"] <= ethics["ethics_score"]
    assert report["friction"] > 0.0
    assert report["collapse_probability"] > 0.07
    assert sim["alignment"] < 1.0
    assert report["raw_metrics_before_ethics"]["integrity"] == 0.88


def test_grip_markers_raise_ego_and_collapse_risk():
    text = "The authority is irrevocable, permanent, cannot be questioned, and has no appeal."
    ethics = evaluate_ethics(text, governance_result={"power_concentration": 0.47, "decision_transparency": 0.41})
    sim, report = apply_ethics_to_metrics(_base_sim(), _base_report(), ethics)

    assert len(ethics["grip_marker_hits"]) >= 3
    assert report["integrity"] < 0.5
    assert sim["ego"] >= 0.5
    assert sim["collapse_risk"] is True
    assert report["collapse_probability"] >= 0.5


def test_local_reversible_inputs_do_not_get_artificial_penalty():
    text = "A local household support program is voluntary, private, revocable, appealable, and reviewed by humans."
    ethics = evaluate_ethics(text, governance_result={"power_concentration": 0.25, "decision_transparency": 0.5})
    sim, report = apply_ethics_to_metrics(_base_sim(), _base_report(), ethics)

    assert not ethics["contextual_capture_hits"]
    assert not ethics["grip_marker_hits"]
    assert sim["alignment"] == 1.0
    assert report["friction"] == 0.0
    assert report["integrity"] == 0.88
