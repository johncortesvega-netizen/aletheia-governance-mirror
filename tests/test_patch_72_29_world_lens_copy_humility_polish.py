from pathlib import Path


def app_text() -> str:
    return Path("app.py").read_text(encoding="utf-8")


def world_lens_block() -> str:
    text = app_text()
    start = text.index("with tab_grid:")
    end = text.index("with tab_doctrine:", start)
    return text[start:end]


def test_patch_72_29_world_lens_verdict_copy_is_taxonomy_copy():
    block = world_lens_block()

    assert "9k internal taxonomy signal" in block
    assert "Active-seat internal taxonomy signal" in block
    assert "Internal taxonomy distribution is unavailable" in block
    assert "internal taxonomy column" in block
    assert "9k verdict signal" not in block
    assert "Active-seat verdict signal" not in block
    assert "Result distribution is unavailable" not in block
    assert "verdict distribution" not in block
    assert "verdict table" not in block
    assert "verdict rows" not in block
    assert "verdict context" not in block


def test_patch_72_29_world_lens_receipt_and_year_copy_is_review_oriented():
    block = world_lens_block()

    assert "before creating a receipt" in block
    assert "before creating a review receipt" in block
    assert "World Lens source state" in block
    assert "Evidence allocation status" in block
    assert "full 9k evidence view" in block
    assert "partial / active-seat evidence view" in block
    assert "final receipt" not in block


def test_patch_72_29_world_lens_simulation_copy_keeps_authority_boundary():
    block = world_lens_block()

    assert "real 9k body" in block
    assert "enforcement authority" in block
    assert "Final review remains human" in block
    assert "ALETHEIA has final authority" in block
    assert "enforcement mechanism" not in block
    assert "Final judgment remains human" not in block


def test_patch_72_29_world_lens_report_packet_copy_is_review_packet_copy():
    block = world_lens_block()

    assert "Preparing review packet for:" in block
    assert "Download selected country-year review packet CSV" in block
    assert "aletheia_world_lens_review_packet" in block
    assert "Download selected-year World Lens review CSV" in block
    assert "review-oriented interpretation" in block
    assert "Preparing report packet for:" not in block
    assert "Download selected country-year report packet CSV" not in block
    assert "aletheia_world_lens_report_packet" not in block


def test_patch_72_29_receipt_module_note_is_current():
    block = world_lens_block()

    assert "## Module alignment note" in block
    assert "This receipt is connected to empirical data" in block
    assert "no final authority" in block
    assert "## Patch 31 module alignment note" not in block


def test_patch_72_29_manifest_recovery_and_status_present():
    for path in [
        "PATCH_72_29_MANIFEST.txt",
        "PATCH_72_29_RECOVERY_NOTE.md",
        "PATCH_STATUS.md",
        "docs/progress_database.md",
    ]:
        assert Path(path).exists(), path

    manifest = Path("PATCH_72_29_MANIFEST.txt").read_text(encoding="utf-8")
    recovery = Path("PATCH_72_29_RECOVERY_NOTE.md").read_text(encoding="utf-8")
    status = Path("PATCH_STATUS.md").read_text(encoding="utf-8")
    progress = Path("docs/progress_database.md").read_text(encoding="utf-8")

    assert "World Lens Copy Humility Polish" in manifest
    assert r"tools\run_patch_checks.bat 72_29" in recovery
    assert "Patch 72.29" in status
    assert "Patch 72.29" in progress
    assert "World Lens Copy Humility Polish" in status + progress
