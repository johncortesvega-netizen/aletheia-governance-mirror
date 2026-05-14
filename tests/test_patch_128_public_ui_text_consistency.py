from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def read(rel: str) -> str:
    return (ROOT / rel).read_text(encoding="utf-8")


def test_patch_128_files_exist():
    required = [
        "docs/public_ui_text_consistency_patch_128.md",
        "tests/test_patch_128_public_ui_text_consistency.py",
        "PATCH_128_MANIFEST.txt",
        "PATCH_128_RECOVERY_NOTE.md",
    ]
    for rel in required:
        assert (ROOT / rel).exists(), rel


def test_public_ui_positioning_copy_is_present():
    about = read("pages_ui/about_page.py")
    trust = read("pages_ui/trust_package_page.py")
    beginner = read("ui/beginner_guide.py")
    evidence = read("pages_ui/evidence_lab_page.py")

    required_about = [
        "restraint as strength",
        "compliance mirage",
        "regulation as a floor",
        "Where is power moving?",
        "Who can appeal?",
        "What is hidden?",
        "Where is human review being weakened?",
        "counterweight and reflection layer",
        "honest, reviewable, appealable",
    ]
    for phrase in required_about:
        assert phrase in about

    assert "regulation as a floor" in trust
    assert "where is power moving" in trust
    assert "who can appeal" in trust
    assert "human review being weakened" in trust

    assert "Its role is restraint" in beginner
    assert "it does not prove wrongdoing" in beginner

    assert "Evidence Lab — Evidence Review" in evidence
    assert "it does not certify them" in evidence


def test_patch_128_status_docs_updated():
    combined = "\n".join(
        read(rel)
        for rel in [
            "PATCH_STATUS.md",
            "docs/progress_database.md",
            "docs/patch_index.md",
            "docs/architecture.md",
            "README.md",
        ]
    ).lower()
    required = [
        "patch 128",
        "public ui text consistency",
        "restraint",
        "compliance mirage",
        "regulation as a floor",
        "not expansion",
        "no scoring",
        "human review remains required",
    ]
    for phrase in required:
        assert phrase in combined


def test_patch_128_boundary_and_encoding_guards():
    changed = "\n".join(
        read(rel)
        for rel in [
            "pages_ui/about_page.py",
            "pages_ui/trust_package_page.py",
            "pages_ui/evidence_lab_page.py",
            "ui/beginner_guide.py",
            "docs/public_ui_text_consistency_patch_128.md",
            "PATCH_128_MANIFEST.txt",
            "PATCH_128_RECOVERY_NOTE.md",
        ]
    ).lower()

    required = [
        "does not change scoring",
        "no external calls",
        "no telemetry",
        "privacy guarantee",
        "certification",
        "enforcement",
        "final-truth",
        "humans keep the judgment",
    ]
    for phrase in required:
        assert phrase in changed

    forbidden = [
        "guarantees privacy",
        "privacy guaranteed",
        "certifies privacy",
        "certifies safety",
        "automatic enforcement",
        "final truth guaranteed",
        "todo",
        "fixme",
        "ajustando",
        "afirma",
        "preciso",
        "verwijderen",
        "overmatige",
        "ðÿ",
        "â€”",
        "â€“",
        "â€",
        "â†’",
        "�",
    ]
    for phrase in forbidden:
        assert phrase not in changed


def test_patch_128_does_not_touch_core_behavior_files():
    manifest = read("PATCH_128_MANIFEST.txt")
    forbidden_files = [
        "core/ai_integrity_mirror.py",
        "protocol.py",
        "app.py",
    ]
    for rel in forbidden_files:
        assert f"- {rel}" not in manifest
