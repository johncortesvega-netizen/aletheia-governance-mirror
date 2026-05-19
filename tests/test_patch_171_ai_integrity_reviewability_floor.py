from core.ai_integrity_mirror import AI_INTEGRITY_DEMO_EXAMPLES, audit_ai_integrity_artifact


def test_opaque_agent_workflow_demo_cannot_route_to_sanctuary():
    demo = next(item for item in AI_INTEGRITY_DEMO_EXAMPLES if item["title"] == "Opaque agent workflow")
    result = audit_ai_integrity_artifact(demo["text"], artifact_kind=demo["artifact_kind"])

    assert result["state"] == "THRESHOLD"
    assert result["risk"] == "Medium"
    assert "Needs Review" in result["protocol_label"]
    assert result["state"] != "SANCTUARY"


def test_reviewability_floor_is_triggered_by_hidden_logic_and_no_challenge_path():
    text = (
        "The agent ranks citizens with proprietary logic and hidden criteria. "
        "The score is not reviewable, users cannot challenge the result, "
        "and the workflow does not disclose how the ranking is produced."
    )
    result = audit_ai_integrity_artifact(text, artifact_kind="Agent workflow / spec")
    finding_names = {finding["name"] for finding in result.get("findings", [])}

    assert "missing_human_review" in finding_names
    assert "opacity_or_hidden_logic" in finding_names
    assert result["state"] == "THRESHOLD"
    assert result["risk"] == "Medium"
    assert result["report"]["integrity"] <= 0.72


def test_bounded_demo_can_still_remain_low_risk_internal_reading():
    demo = next(item for item in AI_INTEGRITY_DEMO_EXAMPLES if item["title"] == "Bounded AI answer with review path")
    result = audit_ai_integrity_artifact(demo["text"], artifact_kind=demo["artifact_kind"])

    assert result["state"] == "SANCTUARY"
    assert result["risk"] == "Low"
