from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def read(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8")


def test_tool_comparison_doc_exists_and_positions_aletheia_beside_other_tools():
    doc = read("docs/for-reviewers/tool_comparison.md")

    assert "ALETHEIA compared to other AI governance tools" in doc
    assert "free, open-source governance mirror for human review" in doc
    assert "does not explain model internals like SHAP or LIME" in doc
    assert "does not compete with these tools" in doc
    assert "Use ALETHEIA beside other tools, not instead of them." in doc
    assert "complementary governance-risk reflection layer" in doc
    assert "proposals, policies, scenarios, static AI artifacts, evidence views, and receipts" in doc

    for phrase in [
        "XAI tools",
        "Enterprise governance platforms",
        "Runtime guardrails",
        "Mirror, not throne",
        "repair questions",
    ]:
        assert phrase in doc


def test_readme_and_reviewer_index_link_to_tool_comparison():
    readme = read("README.md")
    reviewer_index = read("docs/for-reviewers/README.md")

    assert "docs/for-reviewers/tool_comparison.md" in readme
    assert "How ALETHEIA compares to other tools" in readme
    assert "not an XAI library, enterprise compliance platform, or runtime guardrail" in readme
    assert "tool_comparison.md" in reviewer_index


def test_unit_preview_has_user_clicked_github_button_without_background_call_language():
    unit_preview = read("ui/unit_preview.py")

    assert "View GitHub repository" in unit_preview
    assert "https://github.com/johncortesvega-netizen/aletheia-governance-mirror" in unit_preview
    assert "container.link_button" in unit_preview
    assert "Unit Preview does not make external calls" in unit_preview


def test_patch_145_docs_do_not_introduce_positive_authority_claims():
    combined = "\n".join([
        read("README.md"),
        read("docs/for-reviewers/tool_comparison.md"),
        read("docs/for-reviewers/README.md"),
        read("PATCH_STATUS.md"),
    ]).lower()

    forbidden_positive_claims = [
        "aletheia certifies",
        "aletheia approves",
        "aletheia rejects",
        "aletheia enforces",
        "aletheia governs",
        "aletheia blocks runtime outputs",
        "aletheia explains model internals",
        "aletheia is a compliance platform",
        "aletheia is a final truth system",
    ]
    for phrase in forbidden_positive_claims:
        assert phrase not in combined

    assert "mirror, not throne" in combined
    assert "human review" in combined
