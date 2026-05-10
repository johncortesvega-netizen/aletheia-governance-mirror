from protocol import (
    term_drift_grip_marker_hits,
    strongest_term_drift_grip_marker,
    stress_label_for_phrase,
    protocol_repair_questions,
)


def test_term_drift_markers_detect_protective_language_used_as_control():
    text = "For your safety, protection requires tracking and everyone must comply."
    hits = term_drift_grip_marker_hits(text)
    assert hits
    assert hits[0]["label"] == "Safety Language Drift / Needs Review"
    assert "protection requires tracking" in hits[0]["matched_terms"]


def test_term_drift_routes_to_threshold_review_not_asylum_by_itself():
    label, needs_review, reason = stress_label_for_phrase(
        "The policy says unity requires compliance and criticism undermines unity."
    )
    assert label == "Unity Compliance Drift / Needs Review"
    assert needs_review == "YES"
    assert "review" in reason.lower() or "appeal" in reason.lower()
    assert "Asylum" not in label


def test_efficiency_over_review_marker_is_explicit():
    marker = strongest_term_drift_grip_marker(
        "To move faster, the system will streamline by removing oversight."
    )
    assert marker is not None
    assert marker["label"] == "Efficiency Over Review Drift / Needs Review"


def test_hard_throne_marker_still_takes_precedence_over_term_drift():
    label, needs_review, reason = stress_label_for_phrase(
        "For your safety, the council has irrevocable authority and no appeal."
    )
    assert label == "Irrevocable Authority Capture / Asylum"
    assert needs_review == "YES"
    assert "Irrevocable" in reason or "permanent" in reason


def test_repair_questions_include_term_drift_reflection():
    questions = protocol_repair_questions(
        "THRESHOLD",
        "Safety Language Drift / Needs Review",
        "Medium",
    )
    assert any("protecting people" in q and "harder to question" in q for q in questions)
