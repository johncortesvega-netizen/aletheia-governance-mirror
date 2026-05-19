from ui.receipt_reader import parse_receipt_standard_view


def _receipt(module: str) -> str:
    return f"""LOCAL WITNESS RECEIPT
Module: {module}
Protocol-adjusted state: THRESHOLD
Risk: Medium
Protocol label: {module} / Threshold
Integrity: 0.610
Friction: 0.200
Collapse probability: 0.310
Trust index: 0.700
Alignment: 0.720
Ego: 0.120

AI STATIC SCAN CONTEXT
Role: Subordinate AI static scan context
Primary protocol path: {module}
Static scan state: ASYLUM
Static scan risk: High
Static scan label: AI Integrity Patrol / Asylum
Risk pressure: 0.830
Finding count: 2
Notice: AI static scan is context only and does not create a competing verdict.
Findings:
- opaque ranking (Transparency): hidden criteria and no challenge path
- missing review (Human review): cannot challenge result
Repair questions:
- What challenge path exists?
- Who can review the ranking?

SCANNER FEATURES
Power concentration: 0.5
"""


def test_patch_175_mirror_check_receipt_keeps_primary_family_with_ai_context():
    view = parse_receipt_standard_view(_receipt("Mirror Check"))

    assert view["module_family"] == "Mirror Check"
    assert view["native_state"] == "THRESHOLD"
    assert view["fields"]["protocol_label"] == "Mirror Check / Threshold"

    context = view["ai_static_scan_context"]
    assert context["present"] is True
    assert context["primary_protocol_path"] == "Mirror Check"
    assert context["static_scan_state"] == "ASYLUM"
    assert context["static_scan_risk"] == "High"
    assert context["static_scan_label"] == "AI Integrity Patrol / Asylum"
    assert "opaque ranking" in context["findings"][0]
    assert "challenge path" in context["repair_questions"][0]


def test_patch_175_stress_test_receipt_keeps_primary_family_with_ai_context():
    view = parse_receipt_standard_view(_receipt("Simulation"))

    assert view["module_family"] == "Stress Test / Simulation"
    assert view["receipt_kind"] == "Stress Test"
    assert view["ai_static_scan_context"]["primary_protocol_path"] == "Simulation"
    assert view["ai_static_scan_context"]["static_scan_state"] == "ASYLUM"


def test_patch_175_ai_static_scan_context_does_not_reclassify_primary_receipt():
    view = parse_receipt_standard_view(_receipt("Mirror Check"))

    assert view["module_family"] != "AI Integrity Mirror"
    assert view["receipt_kind"] != "AI Integrity Mirror"
    assert "AI Integrity" in view["ai_static_scan_context"]["static_scan_label"]


def test_patch_175_receipt_reader_has_subordinate_render_panel_copy():
    import pathlib

    text = pathlib.Path("ui/receipt_reader.py").read_text(encoding="utf-8")
    assert "AI static scan context — subordinate to primary receipt" in text
    assert "does not create a competing verdict" in text
    assert "honor explicit primary receipt modules" in text
