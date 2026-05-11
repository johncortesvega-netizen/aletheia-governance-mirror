from pathlib import Path


def test_patch_72_2_adds_input_signature_helper():
    app_text = Path("app.py").read_text(encoding="utf-8")

    assert "def mirror_active_input_signature(text_value: str) -> str:" in app_text
    assert 'hashlib.sha256((text_value or "").strip().encode("utf-8")).hexdigest()' in app_text
    assert "prevents an old assessment/receipt from staying active after" in app_text


def test_patch_72_2_stores_active_signature_after_explicit_review():
    app_text = Path("app.py").read_text(encoding="utf-8")

    assert "st.session_state.audit_active_input_signature = mirror_active_input_signature(st.session_state.audit_chat_query)" in app_text
    assert app_text.index("st.session_state.audit_active_input_signature = mirror_active_input_signature") > app_text.index("if run_chat:")


def test_patch_72_2_latest_reading_requires_current_input_match():
    app_text = Path("app.py").read_text(encoding="utf-8")

    assert "latest_matches_current_input = (" in app_text
    assert "current_input_signature == latest_input_signature" in app_text
    assert "active_input_signature == latest_input_signature" in app_text
    assert "if latest_matches_current_input:" in app_text


def test_patch_72_2_changed_input_closes_previous_assessment_and_hides_receipt_flow():
    app_text = Path("app.py").read_text(encoding="utf-8")

    assert "The input has changed. The previous assessment is closed for this draft." in app_text
    assert "Click Review idea to create a new reading and receipt." in app_text
    assert "Last closed reading" in app_text

    latest_block = app_text[app_text.index("# Latest result appears immediately after the question box"):app_text.index("with tab_doctrine:")]
    marker = "The input has changed. The previous assessment is closed for this draft."
    closed_branch = latest_block[latest_block.index(marker):latest_block.index("previous_items =")]
    assert "build_mirror_receipt_for_entry(latest)" not in closed_branch
    assert "Download receipt" not in closed_branch
    assert "render_chat_judgment(" not in closed_branch


def test_patch_72_2_manifest_recovery_docs_present():
    for path in [
        "PATCH_72_2_MANIFEST.txt",
        "PATCH_72_2_RECOVERY_NOTE.md",
        "PATCH_STATUS.md",
        "docs/progress_database.md",
    ]:
        assert Path(path).exists(), path

    manifest = Path("PATCH_72_2_MANIFEST.txt").read_text(encoding="utf-8")
    recovery = Path("PATCH_72_2_RECOVERY_NOTE.md").read_text(encoding="utf-8")
    status = Path("PATCH_STATUS.md").read_text(encoding="utf-8")
    progress = Path("docs/progress_database.md").read_text(encoding="utf-8")

    assert "app.py" in manifest
    assert "tests/test_patch_72_2_mirror_check_input_change_reset.py" in manifest
    assert "tools\\run_patch_checks.bat 72_2" in recovery
    assert "Patch 72.2" in status
    assert "Patch 72.2" in progress
    assert "Mirror Check Input Change Reset" in status + progress
