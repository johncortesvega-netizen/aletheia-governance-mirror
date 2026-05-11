
from pathlib import Path


def test_patch_71_9_mirror_check_judgment_accepts_sim_for_review_band():
    app_text = Path("app.py").read_text(encoding="utf-8")

    assert "def render_chat_judgment(judgment: dict, source: str, report: dict, sim: dict | None = None)" in app_text
    assert "review_band = review_band_for_state(verdict, report, sim or {})" in app_text
    assert "review_band_label = review_band.get" in app_text
    assert "review_band_line" in app_text
    assert "<strong>Review band:</strong>" in app_text


def test_patch_71_9_mirror_check_latest_reading_passes_sim_to_judgment_card():
    app_text = Path("app.py").read_text(encoding="utf-8")

    assert 'render_chat_judgment(latest["judgment"], latest["source"], latest["report"], latest.get("sim"))' in app_text
    assert 'render_chat_judgment(latest["judgment"], latest["source"], latest["report"])' not in app_text


def test_patch_71_9_scope_is_display_only():
    app_text = Path("app.py").read_text(encoding="utf-8")

    assert "def review_band_for_state" in app_text
    assert '"Needs Repair"' in app_text
    assert '"Needs Review"' in app_text
    assert '"Near Sanctuary"' in app_text

    # This patch should not change receipt schema or canonical states.
    assert "review_band" not in Path("core/witness.py").read_text(encoding="utf-8")
    assert "Canonical taxonomy remains ASYLUM / THRESHOLD / SANCTUARY" in app_text


def test_patch_71_9_manifest_recovery_and_progress_docs_present():
    for path in [
        "PATCH_71_9_MANIFEST.txt",
        "PATCH_71_9_RECOVERY_NOTE.md",
        "PATCH_STATUS.md",
        "docs/progress_database.md",
    ]:
        assert Path(path).exists(), path

    manifest = Path("PATCH_71_9_MANIFEST.txt").read_text(encoding="utf-8")
    assert "app.py" in manifest
    assert "tests/test_patch_71_9_mirror_check_review_band_display.py" in manifest

    status = Path("PATCH_STATUS.md").read_text(encoding="utf-8")
    progress = Path("docs/progress_database.md").read_text(encoding="utf-8")
    assert "Patch 71.9" in status
    assert "Patch 71.9" in progress
    assert "Mirror Check Review Band Display" in status + progress
