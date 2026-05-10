from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def read(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8")


def test_v1_finalization_docs_exist_and_mark_release_complete():
    required = [
        "docs/v02_roadmap.md",
        "docs/feature_backlog.md",
        "docs/out_of_scope_future_modules.md",
        "docs/report_export_polish.md",
        "docs/manual_evidence_attachment.md",
        "docs/rubric_weighting_confidence.md",
        "docs/deployment_prep.md",
        "docs/v1_release_complete.md",
    ]
    for rel in required:
        assert (ROOT / rel).exists(), rel
    v1 = read("docs/v1_release_complete.md")
    assert "ALETHEIA v1.0" in v1
    assert "finished public mvp" in v1.lower()
    assert "ALETHEIA reflects" in v1
    assert "Humans review" in v1


def test_v1_finalization_preserves_non_authority_boundary():
    combined = "\n".join(
        read(path)
        for path in [
            "docs/v1_release_complete.md",
            "docs/v02_roadmap.md",
            "docs/out_of_scope_future_modules.md",
            "docs/deployment_prep.md",
        ]
    ).lower()
    for phrase in [
        "real global id sync",
        "real 9k selection",
        "world leader logic",
        "automatic reset",
        "public ledger authority",
        "neural validation",
        "religious validation",
        "automated enforcement",
    ]:
        assert phrase in combined


def test_patch_status_and_progress_mark_56_60_current():
    status = read("PATCH_STATUS.md")
    progress = read("docs/progress_database.md")
    assert "56–60" in status or "56-60" in status
    assert "v1 Finalization Bundle" in status
    assert "tools\\run_patch_checks.bat 56_60" in status
    assert "Patch 56–60" in progress
    assert "v1.0 public MVP complete" in progress


def test_readme_about_and_app_reference_v1_release():
    readme = read("README.md")
    about = read("about_page.py")
    app = read("app.py")
    assert "ALETHEIA v1.0" in readme
    assert "docs/v1_release_complete.md" in readme
    assert "v1.0 complete" in about.lower() or "v1.0 release complete" in about.lower()
    assert "APP_VERSION = \"v1.0-governance-mirror-final\"" in app
    assert "docs/v02_roadmap.md" in app
