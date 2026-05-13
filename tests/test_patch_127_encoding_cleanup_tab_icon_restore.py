from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def read(rel: str) -> str:
    return (ROOT / rel).read_text(encoding="utf-8")


def test_patch_127_files_exist():
    required = [
        "docs/encoding_cleanup_tab_icon_restore.md",
        "tests/test_patch_127_encoding_cleanup_tab_icon_restore.py",
        "PATCH_127_MANIFEST.txt",
        "PATCH_127_RECOVERY_NOTE.md",
    ]
    for rel in required:
        assert (ROOT / rel).exists(), rel


def test_app_navigation_icons_are_restored():
    app = read("app.py")
    required_labels = [
        "🪞 Mirror Check",
        "🚀 Stress Test",
        "🧭 Boundary Cases",
        "🤖 AI Integrity Mirror",
        "📊 Evidence Lab",
        "🌐 World Lens",
        "📜 Protocol Guide",
        "ℹ️ Why ALETHEIA",
    ]
    for label in required_labels:
        assert label in app
    assert 'page_icon="🌿"' in app


def test_public_surface_has_no_common_mojibake_tokens():
    public_files = [
        "app.py",
        "pages_ui/about_page.py",
        "docs/progress_database.md",
        "docs/encoding_cleanup_tab_icon_restore.md",
        "README.md",
        "PATCH_STATUS.md",
        "docs/patch_index.md",
        "docs/architecture.md",
    ]
    forbidden = [
        "ðŸ",
        "â€”",
        "â€“",
        "â€",
        "Â·",
        "Â ",
        "â†’",
        "âˆ’",
        "â‰¥",
        "Ã¢",
        "Ã´",
        "Ã¼",
        "ï¸",
        "�",
    ]
    for rel in public_files:
        text = read(rel)
        for token in forbidden:
            assert token not in text, f"{token!r} found in {rel}"


def test_patch_127_public_status_docs_updated():
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
        "patch 127",
        "encoding cleanup",
        "tab icon restore",
        "mojibake",
        "public ui text cleanup",
        "no scoring",
        "no module-routing change",
        "human review remains required",
    ]
    for phrase in required:
        assert phrase in combined


def test_patch_127_boundary_is_non_authoritative():
    changed = "\n".join(
        read(rel)
        for rel in [
            "docs/encoding_cleanup_tab_icon_restore.md",
            "PATCH_127_MANIFEST.txt",
            "PATCH_127_RECOVERY_NOTE.md",
            "README.md",
            "docs/architecture.md",
            "docs/patch_index.md",
            "docs/progress_database.md",
            "PATCH_STATUS.md",
        ]
    ).lower()
    required = [
        "does not change scoring",
        "no scoring",
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
    ]
    for phrase in forbidden:
        assert phrase not in changed
