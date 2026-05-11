
from pathlib import Path


def test_patch_71_8_result_card_uses_two_line_review_band_helper():
    app_text = Path("app.py").read_text(encoding="utf-8")

    assert 'result_helper = f"Safety risk: {risk}"' in app_text
    assert 'result_helper += f"<br>Review band: {review_band_label}"' in app_text
    assert 'metric_card("Result state", result_display, result_helper)' in app_text

    # The old one-line helper caused awkward wrapping in the card.
    assert 'Safety risk: {risk} · Review band: {review_band_label}' not in app_text


def test_patch_71_8_keeps_review_band_display_only_scope():
    app_text = Path("app.py").read_text(encoding="utf-8")

    assert "def review_band_for_state" in app_text
    assert '"Needs Repair"' in app_text
    assert '"Needs Review"' in app_text
    assert '"Near Sanctuary"' in app_text

    # No receipt schema change in this small polish patch.
    assert "review_band" not in Path("core/witness.py").read_text(encoding="utf-8")


def test_patch_71_8_manifest_recovery_and_progress_docs_present():
    for path in [
        "PATCH_71_8_MANIFEST.txt",
        "PATCH_71_8_RECOVERY_NOTE.md",
        "PATCH_STATUS.md",
        "docs/progress_database.md",
    ]:
        assert Path(path).exists(), path

    manifest = Path("PATCH_71_8_MANIFEST.txt").read_text(encoding="utf-8")
    assert "app.py" in manifest
    assert "tests/test_patch_71_8_stress_review_band_card_polish.py" in manifest

    status = Path("PATCH_STATUS.md").read_text(encoding="utf-8")
    progress = Path("docs/progress_database.md").read_text(encoding="utf-8")
    assert "Patch 71.8" in status
    assert "Patch 71.8" in progress
    assert "Stress Test Review Band Card Polish" in status + progress
