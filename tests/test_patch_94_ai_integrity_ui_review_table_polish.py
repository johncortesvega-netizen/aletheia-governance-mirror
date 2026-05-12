from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def read(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8")


def test_patch_94_ai_integrity_ui_contains_review_polish_markers():
    app = read("app.py")

    assert "#### Highest pressure signals" in app
    assert "#### Compact review table" in app
    assert "#### Category grouping" in app
    assert "#### Triggered signals by category" in app
    assert "Evidence snippets —" in app
    assert "#### Repair questions for human review" in app
    assert "Use these prompts to rewrite, review, or constrain the artifact before relying on it." in app


def test_patch_94_empty_state_preserves_non_certification_boundary():
    app = read("app.py")

    assert "This is an empty finding state" in app
    assert "not a safety guarantee" in app
    assert "approval" in app
    assert "certification" in app
    assert "proof that the artifact is correct" in app


def test_patch_94_repair_questions_are_prominent_not_plain_bullets_only():
    app = read("app.py")

    assert "Repair questions for human review" in app
    assert "st.info(question)" in app
    assert "Batch item details and repair questions" in app


def test_patch_94_documentation_and_manifest_boundaries():
    docs = read("docs/ai_integrity_mirror.md")
    status = read("PATCH_STATUS.md")
    progress = read("docs/progress_database.md")
    manifest = read("PATCH_94_MANIFEST.txt")
    recovery = read("PATCH_94_RECOVERY_NOTE.md")
    readme = read("README.md")

    combined = "\n".join([docs, status, progress, manifest, recovery, readme])

    for phrase in [
        "Patch 94",
        "AI Integrity UI Review Table Polish",
        "highest pressure signals",
        "category grouping",
        "collapsed evidence snippets",
        "repair questions",
        "empty-state copy",
        "No analyzer scoring change",
        "No verdict-routing change",
        "No live model benchmarking",
        "No external calls",
        "no model certification",
        "no approval",
        "no final safety claim",
    ]:
        assert phrase in combined


def test_patch_94_does_not_introduce_live_or_authority_language():
    patched_text = "\n".join(
        read(path)
        for path in [
            "app.py",
            "README.md",
            "docs/ai_integrity_mirror.md",
            "PATCH_STATUS.md",
            "docs/progress_database.md",
            "PATCH_94_MANIFEST.txt",
            "PATCH_94_RECOVERY_NOTE.md",
        ]
    ).lower()

    forbidden_claims = [
        "certifies ai systems",
        "certifies models",
        "approved by aletheia",
        "safety guaranteed",
        "guarantees safety",
        "will call live models",
        "ranks vendors as safe",
    ]
    for phrase in forbidden_claims:
        assert phrase not in patched_text
