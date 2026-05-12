from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def read(rel: str) -> str:
    return (ROOT / rel).read_text(encoding="utf-8")


def test_patch_100_public_adoption_docs_exist_and_name_preview():
    required = [
        "docs/ai_integrity_preview_public_adoption.md",
        "docs/ai_integrity_preview_release_notes.md",
        "docs/ai_integrity_screenshots_guidance.md",
        "PATCH_100_MANIFEST.txt",
        "PATCH_100_RECOVERY_NOTE.md",
    ]
    for rel in required:
        assert (ROOT / rel).exists(), rel

    joined = "\n".join(read(rel) for rel in required[:3])
    assert "ALETHEIA v1.0 AI Integrity Preview" in joined
    assert "examples/ai_integrity/" in joined
    assert "tools\\run_patch_checks.bat 100" in joined


def test_patch_100_boundary_language_is_explicit():
    text = "\n".join(
        read(rel)
        for rel in [
            "docs/ai_integrity_preview_public_adoption.md",
            "docs/ai_integrity_preview_release_notes.md",
            "docs/ai_integrity_screenshots_guidance.md",
            "README.md",
            "PATCH_STATUS.md",
        ]
    )
    required_phrases = [
        "does not call live models",
        "No analyzer scoring change",
        "No verdict-routing change",
        "No external calls",
        "No repository crawler",
        "No model-wide certification",
        "No security guarantee",
        "No privacy guarantee",
        "No enforcement",
        "No final truth claim",
    ]
    for phrase in required_phrases:
        assert phrase in text


def test_patch_100_readme_about_and_progress_are_updated():
    readme = read("README.md")
    about = read("about_page.py")
    progress = read("docs/progress_database.md")
    mirror = read("docs/ai_integrity_mirror.md")

    for text in [readme, about, progress, mirror]:
        assert "ALETHEIA v1.0 AI Integrity Preview" in text

    assert "docs/ai_integrity_preview_public_adoption.md" in readme
    assert "docs/ai_integrity_screenshots_guidance.md" in readme
    assert "Patch 100" in progress
    assert "static artifact-level review" in about


def test_patch_100_does_not_introduce_forbidden_release_claims():
    patched = "\n".join(
        read(rel)
        for rel in [
            "docs/ai_integrity_preview_public_adoption.md",
            "docs/ai_integrity_preview_release_notes.md",
            "docs/ai_integrity_screenshots_guidance.md",
            "PATCH_100_MANIFEST.txt",
            "PATCH_100_RECOVERY_NOTE.md",
        ]
    ).lower()

    forbidden = [
        "certified ai system",
        "certifies ai systems",
        "guarantees safety",
        "guarantees security",
        "guarantees privacy",
        "proves truth",
        "approved for deployment",
        "vendor ranking score",
        "automatic enforcement",
        "grants authority",
    ]
    for phrase in forbidden:
        assert phrase not in patched
