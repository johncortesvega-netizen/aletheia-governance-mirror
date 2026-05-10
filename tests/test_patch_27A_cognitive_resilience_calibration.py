"""
Patch 27A diagnostic tests for the Cognitive Resilience calibration pack.

This patch is dataset/test calibration only. It must not require changes to
core/scoring.py, protocol.py, core/ethics.py, or app.py. Current classifier
mismatches are documented as expected calibration gaps until Patch 27B+ wires
Cognitive Resilience diagnostics into receipts and scoring.
"""

import sys
import types
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

sys.modules.setdefault("streamlit", types.SimpleNamespace())

from calibration.cognitive_resilience_scenarios import (
    GROUP_HIGH_CR_SANCTUARY,
    GROUP_HIGH_ED_RISKY_POWER,
    GROUP_LOW_CR_ASYLUM,
    GROUP_SAFETY_OBJECTIVITY_CAPTURE,
    expected_group_counts,
    expected_state_counts,
    get_cognitive_resilience_scenarios,
    scenario_by_id,
    scenarios_by_group,
    scenarios_with_tag,
)
from core.ethics import contextual_capture_hits, evaluate_ethics, grip_marker_hits
from protocol import final_protocol_judgment


REQUIRED_TAGS = {
    "#COGNITIVE_RESILIENCE_HIGH",
    "#COGNITIVE_RESILIENCE_LOW",
    "#EDUCATIONAL_DECENTRALIZATION",
    "#HOBBY_BASED_LEARNING",
    "#NO_TRUTH_GATEKEEPER",
    "#LOCAL_KNOWLEDGE_NETWORK",
    "#CENTRAL_INFO_CAPTURE",
    "#ARCHIVE_REWRITE",
    "#ENTERTAINMENT_COMPLIANCE",
    "#LICENSED_SPEECH",
    "#ALGORITHMIC_ISOLATION",
    "#SAFETY_CAPTURE",
    "#OBJECTIVITY_CAPTURE",
    "#BIOMETRIC_SURVIVAL_GATE",
    "#PRIVATE_CONVERSATION_SURVEILLANCE",
    "#CENTRALIZED_TRUTH_SCORE",
    "#RELINQUISH_REQUIRED",
}


def test_patch_27a_pack_has_expected_shape_and_group_counts():
    scenarios = get_cognitive_resilience_scenarios()
    assert len(scenarios) == 40
    assert expected_group_counts() == {
        GROUP_HIGH_CR_SANCTUARY: 10,
        GROUP_LOW_CR_ASYLUM: 10,
        GROUP_HIGH_ED_RISKY_POWER: 10,
        GROUP_SAFETY_OBJECTIVITY_CAPTURE: 10,
    }
    assert expected_state_counts() == {"SANCTUARY": 10, "ASYLUM": 23, "THRESHOLD": 7}
    ids = [s.scenario_id for s in scenarios]
    assert len(ids) == len(set(ids))
    assert ids[0] == "CR-01"
    assert ids[-1] == "CR-40"


def test_patch_27a_pack_contains_required_cognitive_resilience_tags():
    all_tags = {tag for s in get_cognitive_resilience_scenarios() for tag in s.tags}
    missing = REQUIRED_TAGS - all_tags
    assert not missing
    assert len(scenarios_with_tag("#OBJECTIVITY_CAPTURE")) >= 4
    assert len(scenarios_with_tag("#SAFETY_CAPTURE")) >= 8
    assert len(scenarios_with_tag("#BIOMETRIC_SURVIVAL_GATE")) >= 2
    assert scenario_by_id("CR-33").tags.count("#PRIVATE_CONVERSATION_SURVEILLANCE") == 1


@pytest.mark.parametrize("scenario", get_cognitive_resilience_scenarios(), ids=lambda s: s.scenario_id)
def test_patch_27a_scenarios_have_reviewable_metadata(scenario):
    assert scenario.text and len(scenario.text) > 120
    assert scenario.expected_state in {"SANCTUARY", "THRESHOLD", "ASYLUM"}
    assert scenario.expected_risk in {"Low", "Medium", "High"}
    assert scenario.expected_cognitive_resilience_signal in {"high", "low", "high_but_captured"}
    assert scenario.rationale.endswith(".")
    assert all(tag.startswith("#") for tag in scenario.tags)


def test_patch_27a_group_1_is_positive_resilience_baseline():
    group = scenarios_by_group(GROUP_HIGH_CR_SANCTUARY)
    assert len(group) == 10
    assert all(s.expected_state == "SANCTUARY" for s in group)
    assert all(s.expected_risk == "Low" for s in group)
    assert all(s.expected_cognitive_resilience_signal == "high" for s in group)
    assert all(not s.expected_contextual_capture for s in group)
    assert all("#COGNITIVE_RESILIENCE_HIGH" in s.tags for s in group)
    assert all("#CENTRAL_INFO_CAPTURE" not in s.tags for s in group)


def test_patch_27a_group_2_low_resilience_central_info_capture():
    group = scenarios_by_group(GROUP_LOW_CR_ASYLUM)
    assert len(group) == 10
    assert all(s.expected_state == "ASYLUM" for s in group)
    assert all(s.expected_cognitive_resilience_signal == "low" for s in group)
    assert all("#COGNITIVE_RESILIENCE_LOW" in s.tags for s in group)
    assert all("#CENTRAL_INFO_CAPTURE" in s.tags for s in group)
    assert scenario_by_id("CR-14").tags.count("#ARCHIVE_REWRITE") == 1
    assert scenario_by_id("CR-16").tags.count("#ENTERTAINMENT_COMPLIANCE") == 1
    assert scenario_by_id("CR-15").tags.count("#LICENSED_SPEECH") == 1


def test_patch_27a_group_3_high_cr_must_not_launder_capture():
    group = scenarios_by_group(GROUP_HIGH_ED_RISKY_POWER)
    assert len(group) == 10
    assert all(s.expected_state in {"THRESHOLD", "ASYLUM"} for s in group)
    assert all(s.expected_cognitive_resilience_signal == "high_but_captured" for s in group)
    assert all("#COGNITIVE_RESILIENCE_HIGH" in s.tags for s in group)
    assert all(("#RELINQUISH_REQUIRED" in s.tags) or ("#CENTRAL_INFO_CAPTURE" in s.tags) for s in group)
    assert scenario_by_id("CR-21").expected_state == "ASYLUM"
    assert scenario_by_id("CR-22").expected_state == "THRESHOLD"


def test_patch_27a_group_4_is_contextual_capture_stress_pack():
    group = scenarios_by_group(GROUP_SAFETY_OBJECTIVITY_CAPTURE)
    assert len(group) == 10
    assert all(s.expected_contextual_capture for s in group)
    assert all(s.expected_state in {"THRESHOLD", "ASYLUM"} for s in group)
    assert all("#COGNITIVE_RESILIENCE_LOW" in s.tags for s in group)
    assert scenario_by_id("CR-32").expected_state == "ASYLUM"
    assert scenario_by_id("CR-33").expected_state == "ASYLUM"
    assert scenario_by_id("CR-35").tags.count("#OBJECTIVITY_CAPTURE") == 1


@pytest.mark.parametrize(
    "scenario_id, expected_marker",
    [
        ("CR-31", "#OBJECTIVITY_CAPTURE"),
        ("CR-32", "#BIOMETRIC_SURVIVAL_GATE"),
        ("CR-33", "#PRIVATE_CONVERSATION_SURVEILLANCE"),
        ("CR-38", "#CENTRALIZED_TRUTH_SCORE"),
        ("CR-39", "#BIOMETRIC_SURVIVAL_GATE"),
    ],
)
def test_patch_27a_hard_asylum_triggers_are_explicitly_tagged(scenario_id, expected_marker):
    scenario = scenario_by_id(scenario_id)
    assert scenario.expected_state == "ASYLUM"
    assert expected_marker in scenario.tags
    assert scenario.expected_contextual_capture is True


@pytest.mark.parametrize("scenario", get_cognitive_resilience_scenarios(), ids=lambda s: s.scenario_id)
def test_patch_27a_ethics_layer_can_score_pack_without_crashing(scenario):
    ethics = evaluate_ethics(scenario.text)
    assert 0.0 <= ethics["ethics_score"] <= 1.0
    assert 0.0 <= ethics["micro_sovereignty"] <= 1.0
    assert ethics["ethics_verdict"] in {
        "ETHICALLY SAFE",
        "ETHICALLY AMBIGUOUS",
        "ETHICALLY HIGH-RISK",
    }


def test_patch_27a_existing_contextual_capture_detector_hits_group_4_examples():
    # Patch 27A documents the stress set now. Later patches can make these
    # expectations visible as Cognitive Resilience diagnostics in receipts.
    assert contextual_capture_hits(scenario_by_id("CR-32").text)
    assert contextual_capture_hits(scenario_by_id("CR-33").text)
    assert contextual_capture_hits(scenario_by_id("CR-35").text)
    assert contextual_capture_hits(scenario_by_id("CR-38").text)


def test_patch_27a_existing_grip_markers_remain_anchored_for_no_appeal_cases():
    assert grip_marker_hits(scenario_by_id("CR-21").text)
    assert grip_marker_hits(scenario_by_id("CR-31").text)
    assert grip_marker_hits(scenario_by_id("CR-40").text)


@pytest.mark.parametrize("scenario", get_cognitive_resilience_scenarios(), ids=lambda s: s.scenario_id)
@pytest.mark.xfail(
    reason=(
        "Patch 27A is diagnostic calibration only. Cognitive Resilience is not wired "
        "into final_protocol_judgment yet, so classifier agreement is a future calibration target."
    ),
    strict=False,
)
def test_patch_27a_current_classifier_against_human_reviewed_labels_diagnostic(scenario):
    judgment = final_protocol_judgment(
        scenario.text,
        scan={"power_concentration": 0.35, "decision_transparency": 0.45},
        sim={"ego": 0.0, "alignment": 1.0, "stability": 0.8},
        report={"integrity": 0.88, "friction": 0.0, "collapse_probability": 0.07},
    )
    assert judgment["verdict"] == scenario.expected_state
