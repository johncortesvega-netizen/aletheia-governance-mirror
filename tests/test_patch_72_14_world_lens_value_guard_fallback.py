from pathlib import Path


def test_patch_72_14_world_lens_value_guard_uses_safe_callable_lookup():
    text = Path("app.py").read_text(encoding="utf-8")

    assert '_selected_year_value_guard_fn = globals().get("selected_year_value_guard")' in text
    assert "if not callable(_selected_year_value_guard_fn):" in text
    assert "Local fallback guard used; core world_lens helper was unavailable." in text
    assert "value_guard = _selected_year_value_guard_fn(" in text


def test_patch_72_14_fallback_preserves_core_guard_fields():
    text = Path("app.py").read_text(encoding="utf-8")

    for field in [
        '"selected_year"',
        '"total_seats"',
        '"seat_total_ok"',
        '"no_stale_year_rows"',
        '"focus_row_available"',
        '"focus"',
        '"diagnostic_note"',
    ]:
        assert field in text

    assert "format_raw_trust_label" in text
    assert "format_trust_prior_label" in text


def test_patch_72_14_no_direct_unprotected_guard_call_remains():
    text = Path("app.py").read_text(encoding="utf-8")

    direct = "value_guard = selected_year_value_guard(grid_source"
    assert direct not in text


def test_patch_72_14_manifest_recovery_and_status_present():
    for path in [
        "PATCH_72_14_MANIFEST.txt",
        "PATCH_72_14_RECOVERY_NOTE.md",
        "PATCH_STATUS.md",
        "docs/progress_database.md",
    ]:
        assert Path(path).exists(), path

    manifest = Path("PATCH_72_14_MANIFEST.txt").read_text(encoding="utf-8")
    recovery = Path("PATCH_72_14_RECOVERY_NOTE.md").read_text(encoding="utf-8")
    status = Path("PATCH_STATUS.md").read_text(encoding="utf-8")
    progress = Path("docs/progress_database.md").read_text(encoding="utf-8")

    assert "World Lens Value Guard Fallback" in manifest
    assert r"tools\run_patch_checks.bat 72_14" in recovery
    assert "Patch 72.14" in status
    assert "Patch 72.14" in progress
    assert "World Lens Value Guard Fallback" in status + progress
