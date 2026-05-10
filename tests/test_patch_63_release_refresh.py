from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def read(rel: str) -> str:
    return (ROOT / rel).read_text(encoding="utf-8")


def test_patch_63_release_refresh_docs_exist_and_name_scope():
    doc = read("docs/post_62_release_refresh.md")
    assert "Patch 63" in doc
    assert "Post-62 Release Refresh" in doc
    assert "61A" in doc and "61E" in doc and "Patch 62" in doc
    assert "ALETHEIA remains a mirror, not a throne" in doc


def test_public_release_notes_are_refreshed_and_command_typo_fixed():
    notes = read("docs/public_release_notes.md")
    assert "Patch 63 — Post-62 Release Refresh" in notes
    assert "tools\\run_patch_checks.bat 63" in notes
    assert "tools\nun_checks" not in notes
    assert "tools\nun_patch_checks" not in notes


def test_readme_and_about_show_post_62_release_refresh():
    readme = read("README.md")
    about = read("about_page.py")
    assert "Patch 63 — Post-62 Release Refresh" in readme
    assert "tools\\run_patch_checks.bat 63" in readme
    assert "Post-62 Release Refresh" in about
    assert "release-surface hardening only" in about


def test_patch_status_and_progress_database_updated_without_authority_claims():
    status = read("PATCH_STATUS.md")
    progress = read("docs/progress_database.md")
    combined = status + "\n" + progress
    assert "Patch 63 — Post-62 Release Refresh" in combined
    assert "diagnostic only" in combined.lower()
    assert "adds no governance authority" in combined.lower() or "no governance authority" in combined.lower()
    forbidden = ["AI has decided", "leader must be removed", "guardrails no longer apply"]
    assert not any(term in combined for term in forbidden)
