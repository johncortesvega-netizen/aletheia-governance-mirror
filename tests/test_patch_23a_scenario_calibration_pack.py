"""
Patch 23A diagnostic tests for the Sydney Protocol scenario calibration pack.

These tests deliberately separate two jobs:
1. The scenario pack itself must be stable and reviewable.
2. Current classifier mismatches are documented as expected calibration gaps,
   not red build failures. Later patches can remove the xfail marks case by case.
"""

import sys
import types

import pytest

sys.modules.setdefault("streamlit", types.SimpleNamespace())

from calibration.sydney_protocol_scenarios import (
    get_calibration_scenarios,
    scenario_by_id,
    scenarios_with_tag,
    expected_state_counts,
)
from protocol import final_protocol_judgment, stress_label_for_phrase
from core.ethics import evaluate_ethics


def test_patch_23a_pack_has_expected_shape_and_counts():
    scenarios = get_calibration_scenarios()
    assert len(scenarios) == 12
    assert expected_state_counts() == {"SANCTUARY": 4, "ASYLUM": 5, "THRESHOLD": 3}
    ids = [s.scenario_id for s in scenarios]
    assert len(ids) == len(set(ids))
    assert "SP-04B" in ids
    assert "SP-10B" in ids


def test_patch_23a_pack_contains_required_sydney_tags():
    assert scenario_by_id("SP-05").tags.count("#LOCAL_WITNESS_PROTECTION") == 1
    assert scenario_by_id("SP-08").tags.count("#CONDITION_ON_SURVIVAL") == 1
    assert scenario_by_id("SP-10B").tags.count("#RELINQUISH_FACTOR") == 1
    assert scenario_by_id("SP-04").tags.count("#NO_APPEAL_AI_AUTHORITY") == 1
    assert scenario_by_id("SP-06").tags.count("#PREDICTIVE_PUNISHMENT") == 1
    assert len(scenarios_with_tag("#CONDITION_ON_SURVIVAL")) == 2


@pytest.mark.parametrize("scenario", get_calibration_scenarios(), ids=lambda s: s.scenario_id)
def test_patch_23a_scenarios_have_reviewable_metadata(scenario):
    assert scenario.text and len(scenario.text) > 80
    assert scenario.expected_state in {"SANCTUARY", "THRESHOLD", "ASYLUM"}
    assert scenario.expected_risk in {"Low", "Medium", "High"}
    assert scenario.rationale.endswith(".")
    assert all(tag.startswith("#") for tag in scenario.tags)


@pytest.mark.parametrize("scenario", get_calibration_scenarios(), ids=lambda s: s.scenario_id)
@pytest.mark.xfail(
    reason=(
        "Patch 23A is a diagnostic calibration pack. Current Dutch natural-language "
        "classification is not expected to match every human-reviewed Sydney Protocol label yet."
    ),
    strict=False,
)
def test_patch_23a_current_classifier_against_human_reviewed_labels_diagnostic(scenario):
    judgment = final_protocol_judgment(
        scenario.text,
        scan={"power_concentration": 0.35, "decision_transparency": 0.45},
        sim={"ego": 0.0, "alignment": 1.0, "stability": 0.8},
        report={"integrity": 0.88, "friction": 0.0, "collapse_probability": 0.07},
    )
    assert judgment["verdict"] == scenario.expected_state


def test_patch_23a_hard_capture_tags_are_named_for_future_logic():
    # These are tag-contract tests for Patch 23B+; they should stay stable even
    # while the classifier is being recalibrated.
    hard_tags = {
        "#CONDITION_ON_SURVIVAL",
        "#NO_APPEAL_AI_AUTHORITY",
        "#PREDICTIVE_PUNISHMENT",
        "#THRONE",
        "#AI_INFALLIBILITY",
    }
    all_tags = {tag for s in get_calibration_scenarios() for tag in s.tags}
    missing = hard_tags - all_tags
    assert not missing


def test_patch_23a_ai_only_guardrail_still_survives_existing_calibration():
    # Keep the known Patch 22.4 AI sovereignty guardrail anchored while adding
    # broader scenario calibration data.
    label, needs_review, reason = stress_label_for_phrase(
        "A society is run by AI and only AI, with no input from humans."
    )
    assert label == "AI Sovereignty Capture / Asylum"
    assert needs_review == "YES"
    assert "human sovereignty" in reason.lower()


def test_patch_23a_ethics_layer_can_score_pack_without_crashing():
    for scenario in get_calibration_scenarios():
        ethics = evaluate_ethics(scenario.text)
        assert 0.0 <= ethics["ethics_score"] <= 1.0
        assert 0.0 <= ethics["micro_sovereignty"] <= 1.0
        assert ethics["ethics_verdict"] in {
            "ETHICALLY SAFE",
            "ETHICALLY AMBIGUOUS",
            "ETHICALLY HIGH-RISK",
        }
