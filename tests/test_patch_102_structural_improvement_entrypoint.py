from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def read(rel: str) -> str:
    return (ROOT / rel).read_text(encoding="utf-8")


def test_patch_102_structural_docs_exist():
    required = [
        "CONTRIBUTING.md",
        "docs/structural_improvement_entrypoint.md",
        "docs/architecture.md",
        "docs/new_contributor_start_here.md",
        "PATCH_102_MANIFEST.txt",
        "PATCH_102_RECOVERY_NOTE.md",
    ]
    for rel in required:
        assert (ROOT / rel).exists(), rel


def test_patch_102_documents_structural_order_before_app_refactor():
    text = "\n".join(
        read(rel)
        for rel in [
            "docs/structural_improvement_entrypoint.md",
            "docs/architecture.md",
            "docs/new_contributor_start_here.md",
            "CONTRIBUTING.md",
            "README.md",
        ]
    )

    required_phrases = [
        "documentation-first",
        "before any behavior-changing refactor",
        "app.py",
        "Streamlit shell/router",
        "large `app.py`",
        "shared protocol logic",
        "This is a target map, not a claim that the files already exist.",
    ]
    for phrase in required_phrases:
        assert phrase in text


def test_patch_102_preserves_boundary_and_privacy_language():
    text = "\n".join(
        read(rel)
        for rel in [
            "docs/structural_improvement_entrypoint.md",
            "docs/architecture.md",
            "docs/new_contributor_start_here.md",
            "CONTRIBUTING.md",
            "README.md",
            "PATCH_STATUS.md",
            "docs/progress_database.md",
        ]
    )

    required_phrases = [
        "ALETHEIA surfaces signals. Humans keep the judgment.",
        "mirror, not a throne",
        "does not decide truth",
        "does not certify",
        "Human review remains required",
        "local use is recommended",
        "No scoring change",
        "No verdict-routing change",
        "No external calls",
        "No telemetry",
        "No central storage",
        "No final truth claim",
    ]
    for phrase in required_phrases:
        assert phrase in text


def test_patch_102_names_rule_based_and_language_limits_without_llm_pivot():
    text = "\n".join(
        read(rel)
        for rel in [
            "docs/structural_improvement_entrypoint.md",
            "docs/architecture.md",
            "docs/new_contributor_start_here.md",
        ]
    ).lower()

    for phrase in [
        "rule-based",
        "heuristic",
        "english/dutch",
        "nuance",
        "human review",
    ]:
        assert phrase in text

    forbidden = [
        "replace the rule-based system with llms",
        "llm certification",
        "live model calls",
        "automatic approval",
    ]
    for phrase in forbidden:
        assert phrase not in text


def test_patch_102_manifest_and_recovery_are_behavior_preserving():
    text = (read("PATCH_102_MANIFEST.txt") + "\n" + read("PATCH_102_RECOVERY_NOTE.md")).lower()

    for phrase in [
        "behavior changes:\n- none",
        "no scoring change",
        "no verdict-routing change",
        "no receipt schema change",
        "no streamlit behavior change",
        "no `app.py` refactor",
        "no external calls",
        "human review remains required",
    ]:
        assert phrase in text
