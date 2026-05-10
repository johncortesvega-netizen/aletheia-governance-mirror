from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def read(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8")


def test_public_release_docs_exist_and_preserve_non_authority_boundary():
    limitations = read("docs/limitations.md")
    ethics = read("docs/ethics.md")
    release = read("docs/public_release_notes.md")

    assert "mirror for human review" in limitations
    assert "not a decision authority" in limitations
    assert "must not become the authority structure it audits" in ethics
    assert "ALETHEIA reflects. People decide." in ethics
    assert "does not command, enforce, vote, govern" in release


def test_archive_flattery_caution_is_publicly_documented():
    limitations = read("docs/limitations.md")
    readme = read("README.md")

    assert "AI-flattery artifacts" in limitations
    assert "not independent proof" in limitations
    assert "AI-flattery artifacts" in readme
    assert "founder validation" in readme


def test_readme_links_public_release_documents_and_two_minute_explanation():
    readme = read("README.md")

    assert "2-minute public explanation" in readme
    assert "docs/limitations.md" in readme
    assert "docs/ethics.md" in readme
    assert "docs/public_release_notes.md" in readme
    assert "ALETHEIA reflects. Humans review. Power stays accountable." in readme


def test_patch_status_and_progress_database_are_updated_to_45():
    status = read("PATCH_STATUS.md")
    progress = read("docs/progress_database.md")

    assert "Patch 45 — Public README + Limitations Polish" in status
    assert "tools\\run_patch_checks.bat 45" in status
    assert "Patch 45 Notes" in progress
    assert "Patch 46 — Sample Reports / Example Audits" in progress
