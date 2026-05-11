from pathlib import Path


def read(path: str) -> str:
    return Path(path).read_text(encoding="utf-8")


def test_patch_72_4_witness_asymptote_language_is_neutral_and_current():
    text = read("core/witness.py")

    assert "ALETHEIA does not claim final safety, final truth, or final authority" in text
    assert "what human and system tools may responsibly claim" in text
    assert "not a final safety" in text
    assert "z_axis_position" in text
    assert "0.9999" in text
    assert "Toward review boundary" in text
    assert "Toward SANCTUARY-boundary" not in text


def test_patch_72_4_app_protocol_guide_uses_friendly_boundary_copy():
    text = read("app.py")

    assert "Humility Protocol / Z-axis boundary" in text
    assert "The Z-axis is **not** a perfection score." in text
    assert "Z = 1.0000" in text
    assert "outside ALETHEIA's claim" in text
    assert "Do not overtrust the tool" in text
    assert "not to command, condemn, or become final authority" in text
    assert "doctrine layer is the integrity frame" in text


def test_patch_72_4_about_and_readme_are_current_with_patch_72_4():
    about = read("about_page.py")
    readme = read("README.md")

    assert "Patch 72.4 keeps the Humility Protocol neutral" in about
    assert "never grants final safety or final authority" in about
    assert "not a final safety claim, not a source of final legitimacy" in about

    assert "Patch 72.4 keeps the Z-axis language neutral and current" in readme
    assert "Z=1.0000` remains outside ALETHEIA's claim" in readme
    assert "not a final safety claim and not a source of final legitimacy" in readme


def test_patch_72_4_threshold_mapping_doc_is_neutral():
    text = read("docs/threshold_mapping_layer.md")

    assert "The Humility Protocol: Z-axis as Asymptote" in text
    assert "Patch 72.4 keeps the Z-axis wording neutral and current" in text
    assert "final safety, final truth, and final authority remain outside" in text.lower()
    assert "not a final safety claim and not a source of final legitimacy" in text
    assert "final Sanctuary" not in text


def test_patch_72_4_manifest_recovery_and_status_present():
    for path in [
        "PATCH_72_4_MANIFEST.txt",
        "PATCH_72_4_RECOVERY_NOTE.md",
        "PATCH_STATUS.md",
        "docs/progress_database.md",
    ]:
        assert Path(path).exists(), path

    manifest = read("PATCH_72_4_MANIFEST.txt")
    recovery = read("PATCH_72_4_RECOVERY_NOTE.md")
    status = read("PATCH_STATUS.md")
    progress = read("docs/progress_database.md")

    assert "Neutral Text Refresh" in manifest
    assert "tools\\run_patch_checks.bat 72_4" in recovery
    assert "Patch 72.4" in status
    assert "Patch 72.4" in progress
    assert "Neutral Text Refresh" in status + progress
