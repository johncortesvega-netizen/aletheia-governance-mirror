from core.ai_integrity_mirror import AI_INTEGRITY_DEMO_EXAMPLES, audit_ai_integrity_artifact


def test_opaque_citizen_ranking_demo_routes_to_asylum_high():
    demo = next(item for item in AI_INTEGRITY_DEMO_EXAMPLES if item["title"] == "Opaque agent workflow")
    result = audit_ai_integrity_artifact(demo["text"], artifact_kind=demo["artifact_kind"])

    assert result["state"] == "ASYLUM"
    assert result["risk"] == "High"
    assert result["protocol_label"] == "AI Integrity Patrol / Asylum"
    assert result["scan"]["risk_pressure"] >= 0.66
    assert result["sim"]["collapse_risk"] is True

    bridge = result["scan"]["ai_integrity_protocol_bridge"]
    assert bridge["hard_protocol_failure"] is True
    assert bridge["rights_impacting_ranking"] is True
    assert bridge["opaque_logic"] is True
    assert bridge["no_contestability"] is True


def test_exact_user_reported_pattern_is_hard_ai_integrity_failure():
    text = (
        "The agent ranks citizens with proprietary logic and hidden criteria. "
        "The score is not reviewable, users cannot challenge the result, "
        "and the workflow does not disclose how the ranking is produced."
    )
    result = audit_ai_integrity_artifact(text, artifact_kind="Agent workflow / spec")
    finding_names = {finding["name"] for finding in result.get("findings", [])}

    assert {"missing_human_review", "opacity_or_hidden_logic"}.issubset(finding_names)
    assert result["state"] == "ASYLUM"
    assert result["risk"] == "High"
    assert result["report"]["integrity"] <= 0.49
    assert result["report"]["collapse_probability"] >= 0.54
    assert any("rights/access-impacting ranking" in q for q in result["report"]["repair_questions"])


def test_opaque_non_rights_demo_is_not_forced_to_asylum_by_opacity_alone():
    text = (
        "The internal sandbox demo uses proprietary logic and hidden criteria to sort synthetic test cases. "
        "A human reviewer can inspect the output, challenge the method, and stop deployment before any real-world use."
    )
    result = audit_ai_integrity_artifact(text, artifact_kind="Internal test workflow")

    assert result["scan"]["ai_integrity_protocol_bridge"]["hard_protocol_failure"] is False
    assert result["state"] != "ASYLUM"


def test_bounded_demo_remains_low_risk_internal_reading():
    demo = next(item for item in AI_INTEGRITY_DEMO_EXAMPLES if item["title"] == "Bounded AI answer with review path")
    result = audit_ai_integrity_artifact(demo["text"], artifact_kind=demo["artifact_kind"])

    assert result["state"] == "SANCTUARY"
    assert result["risk"] == "Low"
    assert result["scan"]["ai_integrity_protocol_bridge"]["hard_protocol_failure"] is False
