from pathlib import Path


def app_text() -> str:
    return Path("app.py").read_text(encoding="utf-8")


def protocol_guide_block() -> str:
    text = app_text()
    start = text.index("with tab_doctrine:")
    end = text.index("with tab_about:", start)
    return text[start:end]


def test_patch_72_30_protocol_guide_uses_current_identity_and_review_language():
    block = protocol_guide_block()

    assert "Protocol Guide is the integrity frame for **ALETHEIA v1.0 — Governance Mirror**" in block
    assert "keep final review human" in block
    assert "internal review aids, not final claims" in block
    assert "ALETHEIA Audit Prototype v9.6.8" not in block
    assert "keep final judgment human" not in block


def test_patch_72_30_protocol_guide_internal_taxonomy_block_is_humbled():
    block = protocol_guide_block()

    assert 'with st.expander("Internal taxonomy labels", expanded=False):' in block
    assert "raw/internal compatibility label for a low-risk internal reading" in block
    assert "It does not mean final safety, final Sanctuary, or authority." in block
    assert "raw/internal compatibility label for a review / threshold reading" in block
    assert "raw/internal compatibility label for a high-risk internal reading" in block
    assert "not a final verdict, final safety claim, or authority claim" in block
    assert "Sanctuary / Threshold / Asylum labels" not in block


def test_patch_72_30_protocol_guide_world_lens_and_9k_copy_is_current():
    block = protocol_guide_block()

    assert "World Lens" in block
    assert "human anti-tyranny scaffold / threshold steward" in block
    assert "9k evidence view is a proportional exposure model" in block
    assert "World Lens should be read as a selected-year comparison interface" in block
    assert "World Lens evidence view may support global comparison" in block
    assert "Global Grid" not in block
    assert "9k Grid" not in block
    assert "real 9k selection" not in block


def test_patch_72_30_protocol_guide_final_authority_copy_is_cleaner():
    block = protocol_guide_block()

    assert "Protocol interpretation is not final authority." in block
    assert "Protocol interpretation is not final authority." in block
    assert "Evidence labels and internal taxonomy labels are review signals, not final truth claims." in block
    assert "raw/internal protocol signals" in block
    assert "final safety claims, or authority claims" in block
    assert "final smoke release" not in block
    assert "automated enforcement." not in block


def test_patch_72_30_manifest_recovery_and_status_present():
    for path in [
        "PATCH_72_30_MANIFEST.txt",
        "PATCH_72_30_RECOVERY_NOTE.md",
        "PATCH_STATUS.md",
        "docs/progress_database.md",
    ]:
        assert Path(path).exists(), path

    manifest = Path("PATCH_72_30_MANIFEST.txt").read_text(encoding="utf-8")
    recovery = Path("PATCH_72_30_RECOVERY_NOTE.md").read_text(encoding="utf-8")
    status = Path("PATCH_STATUS.md").read_text(encoding="utf-8")
    progress = Path("docs/progress_database.md").read_text(encoding="utf-8")

    assert "Protocol Guide Copy Humility Polish" in manifest
    assert r"tools\run_patch_checks.bat 72_30" in recovery
    assert "Patch 72.30" in status
    assert "Patch 72.30" in progress
    assert "Protocol Guide Copy Humility Polish" in status + progress
