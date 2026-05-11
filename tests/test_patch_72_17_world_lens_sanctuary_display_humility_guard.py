from pathlib import Path


def test_patch_72_17_app_uses_humble_sanctuary_display_label():
    text = Path("app.py").read_text(encoding="utf-8")

    assert 'col_a.metric("Empirical pattern", display_verdict_value)' in text
    assert 'Low-risk internal reading' in text
    assert 'Internal taxonomy label: SANCTUARY' in text
    assert 'not a final safety, final Sanctuary, or authority claim' in text
    assert 'col_a.metric("Empirical verdict", verdict_value)' not in text


def test_patch_72_17_app_rewrites_legacy_sanctuary_overlay_display():
    text = Path("app.py").read_text(encoding="utf-8")

    assert 'overlay_status_value.startswith("SANCTUARY evidence pattern")' in text
    assert 'Low-risk evidence pattern: strong public-data baseline' in text
    assert 'ALETHEIA does not claim final safety, final Sanctuary, or final authority.' in text


def test_patch_72_17_empirical_overlay_no_longer_returns_sanctuary_as_primary_claim():
    for rel in ["core/empirical.py", "core_empirical.py"]:
        text = Path(rel).read_text(encoding="utf-8")
        assert 'return "SANCTUARY evidence pattern: strong public-data baseline' not in text
        assert 'return "Low-risk evidence pattern: strong public-data baseline' in text
        assert 'Internal taxonomy label: SANCTUARY' in text
        assert 'does not claim final safety, final Sanctuary, or final authority' in text


def test_patch_72_17_preserves_internal_taxonomy_and_warning_labels():
    text = Path("core/empirical.py").read_text(encoding="utf-8")

    assert 'return "ASYLUM evidence pattern: high capture/collapse concern"' in text
    assert 'return "THRESHOLD evidence pattern: unresolved safeguards or friction"' in text
    assert '"SANCTUARY"' in text
    assert '"THRESHOLD"' in text
    assert '"ASYLUM"' in text


def test_patch_72_17_manifest_recovery_and_status_present():
    for path in [
        "PATCH_72_17_MANIFEST.txt",
        "PATCH_72_17_RECOVERY_NOTE.md",
        "PATCH_STATUS.md",
        "docs/progress_database.md",
    ]:
        assert Path(path).exists(), path

    manifest = Path("PATCH_72_17_MANIFEST.txt").read_text(encoding="utf-8")
    recovery = Path("PATCH_72_17_RECOVERY_NOTE.md").read_text(encoding="utf-8")
    status = Path("PATCH_STATUS.md").read_text(encoding="utf-8")
    progress = Path("docs/progress_database.md").read_text(encoding="utf-8")

    assert "World Lens Sanctuary Display Humility Guard" in manifest
    assert r"tools\run_patch_checks.bat 72_17" in recovery
    assert "Patch 72.17" in status
    assert "Patch 72.17" in progress
    assert "Sanctuary Display Humility Guard" in status + progress
