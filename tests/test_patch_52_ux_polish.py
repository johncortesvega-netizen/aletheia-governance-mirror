from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def read(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8")


def test_patch_52_docs_exist_and_define_boundary():
    text = read("docs/ux_polish.md")
    assert "Patch 52" in text
    assert "First-use path" in text
    assert "no command authority" in text
    assert "no spiritual validation" in text
    assert "Clearer UX" in text


def test_app_exposes_patch_52_ux_polish_without_new_authority():
    text = read("app.py")
    assert 'APP_VERSION = "v0.1-patch52-ux-polish"' in text
    assert "APP_UX_POLISH_SUMMARY" in text
    assert "Patch 52 UX polish" in text
    assert "Have a document?" in text
    assert "It adds no doctrine and no authority" in text
    # Patch 52 is copy/navigation polish only; it must keep authority boundaries visible.
    assert "no doctrine and no authority" in text.lower()
    assert "does not decide for people" in text.lower()
    assert "does not activate Global ID" in text


def test_about_page_has_short_first_use_guidance():
    text = read("about_page.py")
    assert "Patch 52 UX polish" in text
    assert "First-use path" in text
    assert "Mirror Check" in text
    assert "does not decide, enforce, or replace human judgment" in text
    assert "does not change scoring, doctrine, evidence handling" in text


def test_patch_ledgers_reference_patch_52():
    status = read("PATCH_STATUS.md")
    progress = read("docs/progress_database.md")
    readme = read("README.md")
    assert "52 | Optional UX Polish | Current" in status
    assert "Patch 52 — Optional UX Polish" in status
    assert "tools\\run_patch_checks.bat 52" in status
    assert "Patch 52 Notes" in progress
    assert "UX Polish" in readme
