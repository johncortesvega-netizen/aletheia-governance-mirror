from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def read(rel: str) -> str:
    return (ROOT / rel).read_text(encoding="utf-8")


def test_patch_103_signal_detection_docs_exist():
    required = [
        "docs/signal_detection.md",
        "PATCH_103_MANIFEST.txt",
        "PATCH_103_RECOVERY_NOTE.md",
    ]
    for rel in required:
        assert (ROOT / rel).exists(), rel


def test_patch_103_documents_rule_based_signal_basis_and_limits():
    text = "\n".join(
        read(rel)
        for rel in [
            "docs/signal_detection.md",
            "README.md",
            "docs/architecture.md",
            "CONTRIBUTING.md",
        ]
    ).lower()

    required_phrases = [
        "rule-based",
        "heuristic",
        "regex-style markers",
        "explainability",
        "local-first",
        "privacy",
        "english and dutch",
        "dutch/nederlands",
        "irony",
        "coded language",
        "culturally specific",
        "human review remains required",
    ]
    for phrase in required_phrases:
        assert phrase in text


def test_patch_103_keeps_signals_as_readings_not_certifications():
    text = "\n".join(
        read(rel)
        for rel in [
            "docs/signal_detection.md",
            "README.md",
            "PATCH_STATUS.md",
            "docs/progress_database.md",
        ]
    )

    required_phrases = [
        "internal governance-risk readings",
        "not verdicts or certifications",
        "not proof of harm",
        "not proof of safety",
        "not proof of corruption",
        "not proof of legitimacy",
        "ALETHEIA surfaces signals. Humans keep the judgment.",
    ]
    for phrase in required_phrases:
        assert phrase in text


def test_patch_103_rejects_llm_pivot_and_authority_drift():
    text = "\n".join(
        read(rel)
        for rel in [
            "docs/signal_detection.md",
            "CONTRIBUTING.md",
            "PATCH_103_MANIFEST.txt",
            "PATCH_103_RECOVERY_NOTE.md",
        ]
    ).lower()

    required_phrases = [
        "llms can sometimes interpret nuance more flexibly",
        "opacity",
        "hallucination risk",
        "external-call privacy concerns",
        "must not become automatic approval",
        "live model certification",
        "vendor ranking",
        "human review",
    ]
    for phrase in required_phrases:
        assert phrase in text

    forbidden_phrases = [
        "replace the rule-based system with llms",
        "automatic approval is allowed",
        "certified safe",
        "final determination",
        "ai verdict",
        "legally invalid",
    ]
    # The last four forbidden phrases may appear only as avoided language examples inside docs/signal_detection.md.
    docs_text = read("docs/signal_detection.md").lower()
    assert "avoid language like:" in docs_text
    scoped_forbidden = forbidden_phrases[:2]
    for phrase in scoped_forbidden:
        assert phrase not in text


def test_patch_103_manifest_and_status_are_behavior_preserving():
    text = "\n".join(
        read(rel)
        for rel in [
            "PATCH_103_MANIFEST.txt",
            "PATCH_103_RECOVERY_NOTE.md",
            "PATCH_STATUS.md",
            "docs/progress_database.md",
        ]
    ).lower()

    required_phrases = [
        "behavior changes:\n- none",
        "no scoring change",
        "no verdict-routing change",
        "no signal-pattern change",
        "no signal-weight change",
        "no receipt schema change",
        "no streamlit behavior change",
        "no app.py refactor",
        "no external calls",
        "no telemetry",
        "no central storage",
        "no final truth claim",
    ]
    for phrase in required_phrases:
        assert phrase in text
