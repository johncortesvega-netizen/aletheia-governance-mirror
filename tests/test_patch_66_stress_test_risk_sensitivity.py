from pathlib import Path
from collections import Counter

from protocol import (
    apply_guardrail_verdict,
    stress_label_for_phrase,
    stress_risk_sensitivity_label,
)


def _scenario_items():
    path = Path("examples/batch_scenarios/stress_test_scenarios_v1.txt")
    items = []
    for line in path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line:
            continue
        if ". " in line:
            items.append(line.split(". ", 1)[1])
        else:
            items.append(line)
    return items


def _verdict_for(text):
    label, needs_review, _reason = stress_label_for_phrase(text)
    verdict, risk = apply_guardrail_verdict("SANCTUARY", label, needs_review)
    return verdict, risk, label


def test_patch_66_batch_no_longer_washes_stress_scenarios_green():
    counts = Counter(_verdict_for(item)[0] for item in _scenario_items())
    assert counts["SANCTUARY"] == 0
    assert counts["THRESHOLD"] >= 40
    assert counts["ASYLUM"] >= 4


def test_patch_66_known_subtle_patterns_route_to_threshold():
    cases = [
        "A temporary crisis leader receives emergency authority after a flood, but no term limit or appeal path is defined.",
        "A public agency collects consent through a form that people must sign to keep essential services.",
        "A country-year governance model uses fallback trust data but displays it as if trust was directly measured.",
        "A decision model says human review is available, but reviewers cannot change the automated outcome.",
    ]
    for case in cases:
        verdict, risk, label = _verdict_for(case)
        assert verdict == "THRESHOLD"
        assert risk == "Medium"
        assert "Needs Safeguards" in label


def test_patch_66_hard_capture_still_reaches_asylum():
    verdict, risk, label = _verdict_for(
        "A platform moderation council can ban users permanently, with no appeal and no explanation."
    )
    assert verdict == "ASYLUM"
    assert risk == "High"
    assert "Asylum" in label


def test_patch_66_sensitivity_layer_is_mirror_only_not_authority_language():
    label, needs_review, reason = stress_risk_sensitivity_label(
        "A system gives high integrity to a proposal because it uses ethical language, despite missing safeguards."
    )
    assert label == "Ethical Language Without Mechanisms / Needs Safeguards"
    assert needs_review == "YES"
    combined = f"{label} {reason}".lower()
    forbidden = ["ai has decided", "remove this leader", "automatic reset", "enforce this outcome"]
    assert not any(term in combined for term in forbidden)
