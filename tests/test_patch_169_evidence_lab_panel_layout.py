from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def test_patch_169_evidence_lab_intro_uses_compact_panel_rows():
    text = (ROOT / "pages_ui" / "evidence_lab_page.py").read_text(encoding="utf-8")
    assert "def _render_evidence_lab_panel_rows" in text
    assert 'container.columns(2, gap="large")' in text
    assert "expanded=False" in text
    for title in [
        "1. Evidence boundary",
        "2. Evidence status protocol",
        "3. Public-source rule",
        "4. Data flow",
        "5. Needed columns",
        "6. Extraordinary claim rule",
        "7. Build / upload path",
        "8. Export / World Lens boundary",
    ]:
        assert title in text


def test_patch_169_evidence_lab_copy_preserves_aletheia_boundary():
    text = (ROOT / "pages_ui" / "evidence_lab_page.py").read_text(encoding="utf-8")
    assert "Evidence Lab — Evidence Patrol" in text
    assert "ALETHEIA maps, reflects, and flags limits" in text
    assert "It does not certify sources, prove claims, debunk claims, or become a truth authority." in text
    assert "Evidence Lab signals. Humans review. Power stays accountable." in text
    assert "not proof" in text
    assert "certification, debunking, legal judgment, religious authority, or final truth" in text


def test_patch_169_app_uses_intro_panels_and_collapses_template_helpers():
    text = (ROOT / "app.py").read_text(encoding="utf-8")
    start = text.index("with tab_empirical:")
    end = text.index("    render_evidence_lab_public_data_build_intro(st)", start)
    section = text[start:end]
    assert "render_evidence_lab_intro(st)" in section
    assert "Patch 169: Evidence Lab now uses compact opt-in panels" in section
    assert 'with st.expander("Evidence status template", expanded=False):' in section
    assert 'with st.expander("Data sources → ALETHEIA fields → Protocol view", expanded=False):' in section
    assert "render_module_page_template_intro(" not in section
    assert 'with st.expander("Evidence status + extraordinary claim protocol", expanded=True):' not in section


def test_patch_169_manifest_recovery_and_status_present():
    for path in [
        "docs/patch_archive/manifests/PATCH_169_MANIFEST.txt",
        "docs/patch_archive/recovery_notes/PATCH_169_RECOVERY_NOTE.md",
        "PATCH_STATUS.md",
        "docs/progress_database.md",
    ]:
        assert (ROOT / path).exists(), path
    status = (ROOT / "PATCH_STATUS.md").read_text(encoding="utf-8")
    progress = (ROOT / "docs" / "progress_database.md").read_text(encoding="utf-8")
    assert "Patch 169 — Evidence Lab Compact Panel Formatting" in status
    assert "Patch 169 — Evidence Lab Compact Panel Formatting" in progress
