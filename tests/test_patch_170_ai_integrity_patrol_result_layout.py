from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def test_patch_170_ai_integrity_patrol_result_panels_are_present():
    text = (ROOT / "app.py").read_text(encoding="utf-8")
    assert "# Patch 170: AI Integrity Patrol result panels are collapsed by default" in text
    assert 'patrol_result_row_1 = st.columns(2, gap="large")' in text
    assert 'patrol_result_row_2 = st.columns(2, gap="large")' in text
    assert 'patrol_result_row_3 = st.columns(2, gap="large")' in text
    assert 'patrol_result_row_4 = st.columns(2, gap="large")' in text


def test_patch_170_ai_integrity_patrol_panels_are_collapsed_by_default():
    text = (ROOT / "app.py").read_text(encoding="utf-8")
    panel_titles = [
        "How to read this result",
        "Highest pressure signals",
        "Triggered signals by category",
        "Evidence snippets by category",
        "Repair questions for human review",
        "Optional static boundary checks",
        "Boundary note",
        "Local AI Integrity receipt",
    ]
    for title in panel_titles:
        assert f'with st.expander("{title}", expanded=False):' in text


def test_patch_170_ai_integrity_keeps_no_authority_boundaries():
    text = (ROOT / "app.py").read_text(encoding="utf-8")
    assert "static governance-integrity risk reading for review, not proof, certification, approval, or a final safety claim" in text
    assert "This is not a privacy guarantee, compliance approval, hosting audit, or proof that no data is collected." in text
    assert "This is not a security guarantee, vulnerability certification, compliance approval, or proof that code is safe." in text
    assert "ALETHEIA does not claim final Sanctuary" in text


def test_patch_170_ai_integrity_engine_and_receipt_calls_are_preserved():
    text = (ROOT / "app.py").read_text(encoding="utf-8")
    assert "ai_result = audit_ai_integrity_artifact(ai_integrity_input, artifact_kind=artifact_kind)" in text
    assert "build_ai_integrity_receipt_context(" in text
    assert "build_local_witness_receipt(" in text
    assert "render_ai_integrity_receipt_context_text(ai_receipt_context)" in text
    assert 'key="ai_integrity_receipt_download"' in text
