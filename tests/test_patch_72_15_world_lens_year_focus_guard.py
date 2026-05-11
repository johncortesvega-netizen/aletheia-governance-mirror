from pathlib import Path


def app_text() -> str:
    return Path("app.py").read_text(encoding="utf-8")


def test_patch_72_15_world_lens_year_selector_does_not_force_synced_year_every_rerun():
    text = app_text()

    assert "seed the World Lens year from the Evidence Lab synced" in text
    assert "Do not force it back on every" in text
    assert '"grid_year_v2" not in st.session_state and synced_evidence_year_int in years' in text

    forbidden = (
        "if synced_evidence_year_int in years and "
        "st.session_state.get(\"grid_year_v2\") != synced_evidence_year_int:"
    )
    assert forbidden not in text


def test_patch_72_15_world_lens_focus_iso3_is_defined_before_value_guard():
    text = app_text()

    focus_line = 'focus_iso3 = str(st.session_state.get("aletheia_synced_iso3") or "NLD").upper().strip()'
    guard_call = "value_guard = _selected_year_value_guard_fn("
    assert focus_line in text
    assert text.index(focus_line) < text.index(guard_call)
    assert 'focus_iso3=focus_iso3 or "NLD"' in text


def test_patch_72_15_prototype_branch_has_own_allocation_heading():
    text = app_text()

    prototype_start = text.index('elif grid_mode == "Prototype region brackets":')
    prototype_slice = text[prototype_start:]
    assert 'allocation_heading = "Prototype verdict signal"' in prototype_slice
    assert 'st.markdown(f"### {allocation_heading}")' in prototype_slice
    assert prototype_slice.index('allocation_heading = "Prototype verdict signal"') < prototype_slice.index('st.markdown(f"### {allocation_heading}")')


def test_patch_72_15_manifest_recovery_and_status_present():
    for path in [
        "PATCH_72_15_MANIFEST.txt",
        "PATCH_72_15_RECOVERY_NOTE.md",
        "PATCH_STATUS.md",
        "docs/progress_database.md",
    ]:
        assert Path(path).exists(), path

    manifest = Path("PATCH_72_15_MANIFEST.txt").read_text(encoding="utf-8")
    recovery = Path("PATCH_72_15_RECOVERY_NOTE.md").read_text(encoding="utf-8")
    status = Path("PATCH_STATUS.md").read_text(encoding="utf-8")
    progress = Path("docs/progress_database.md").read_text(encoding="utf-8")

    assert "World Lens Year and Focus Guard" in manifest
    assert r"tools\run_patch_checks.bat 72_15" in recovery
    assert "Patch 72.15" in status
    assert "Patch 72.15" in progress
    assert "World Lens Year and Focus Guard" in status + progress
