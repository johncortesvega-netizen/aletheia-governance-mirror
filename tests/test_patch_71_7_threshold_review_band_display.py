
from pathlib import Path


def _app_text() -> str:
    return Path("app.py").read_text(encoding="utf-8")


def test_patch_71_7_adds_user_friendly_threshold_review_band_helper():
    app_text = _app_text()

    assert "REVIEW_BAND_LABELS" in app_text
    assert '"THRESHOLD_MINUS": "Needs Repair"' in app_text
    assert '"THRESHOLD": "Needs Review"' in app_text
    assert '"THRESHOLD_PLUS": "Near Sanctuary"' in app_text
    assert "def review_band_for_state" in app_text

    # Canonical taxonomy stays unchanged; these are display bands only.
    assert "Canonical taxonomy remains ASYLUM / THRESHOLD / SANCTUARY" in app_text


def test_patch_71_7_threshold_band_thresholds_are_display_only_and_intuitive():
    app_text = _app_text()

    assert "Closer to Asylum, but still repairable." in app_text
    assert "Mixed or incomplete safeguards require human review." in app_text
    assert "Mostly stable, but not fully safe yet." in app_text

    # Small patch: do not add new canonical protocol states.
    assert "THRESHOLD_MINUS" in app_text
    assert "THRESHOLD_PLUS" in app_text
    assert "protocol_adjusted_state" not in app_text[app_text.index("def review_band_for_state"):app_text.index("def review_band_for_state") + 2500]


def test_patch_71_7_stress_test_ui_shows_review_band_without_receipt_schema_change():
    app_text = _app_text()

    assert "Review band:" in app_text
    assert "review_band_for_state(verdict, report, sim)" in app_text
    assert "result_display += f\"<br><span" in app_text
    assert "review_band_for_state(verdict, stress_report, sim)" in app_text
    assert '"Review band": stress_review_band.get("label")' in app_text

    # This small patch should not modify the receipt schema directly.
    assert "review_band" not in Path("core/witness.py").read_text(encoding="utf-8")


def test_patch_71_7_manifest_recovery_and_progress_docs_present():
    for path in [
        "PATCH_71_7_MANIFEST.txt",
        "PATCH_71_7_RECOVERY_NOTE.md",
        "PATCH_STATUS.md",
        "docs/progress_database.md",
    ]:
        assert Path(path).exists(), path

    manifest = Path("PATCH_71_7_MANIFEST.txt").read_text(encoding="utf-8")
    assert "app.py" in manifest
    assert "tests/test_patch_71_7_threshold_review_band_display.py" in manifest

    status = Path("PATCH_STATUS.md").read_text(encoding="utf-8")
    progress = Path("docs/progress_database.md").read_text(encoding="utf-8")
    assert "Patch 71.7" in status
    assert "Patch 71.7" in progress
    assert "Threshold Review Band Display" in status + progress
