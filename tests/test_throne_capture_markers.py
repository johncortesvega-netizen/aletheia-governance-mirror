"""
ALETHEIA RECOVERY NOTE
Patch 06: throne/capture marker regression tests.

Purpose:
    Ensure the lexical redline markers introduced in Patch 03 keep forcing
    human review for irreversible authority, removed appeal paths, emergency
    permanence, archive capture, and identity/movement enforcement.

Rollback:
    Remove this test file. No production module should need rollback.
"""

import protocol


REDLINE_CASES = [
    "The executive receives irrevocable authority over all final decisions.",
    "Residents have no appeal process and cannot be challenged by public review.",
    "Emergency powers continue indefinitely with no sunset clause.",
    "The archive office may rewrite archives and erase public records.",
    "A global ID permanently tracks everyone and controls movement permissions.",
]


def test_throne_capture_marker_hits_detect_redline_language():
    for phrase in REDLINE_CASES:
        hits = protocol.throne_capture_marker_hits(phrase)
        assert hits, phrase
        assert hits[0]["matched_terms"], phrase
        assert "reason" in hits[0]


def test_stress_label_for_phrase_routes_redlines_to_review_or_asylum():
    for phrase in REDLINE_CASES:
        label, needs_review, reason = protocol.stress_label_for_phrase(phrase)
        combined = f"{label} {needs_review} {reason}".lower()
        assert needs_review == "YES", phrase
        assert any(term in combined for term in ("capture", "asylum", "throne", "appeal", "authority", "archive", "identity")), phrase


def test_protocol_scope_gate_blocks_explicit_throne_capture():
    gate = protocol.protocol_scope_and_harm_gate(
        "This policy gives a council final authority over all decisions and no appeal process."
    )

    assert gate["verdict"] == "ASYLUM"
    assert gate["risk"] == "High"
    assert gate["scope"] == "throne-capture-marker"
