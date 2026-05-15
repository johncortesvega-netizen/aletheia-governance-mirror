from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def read(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8")


def test_ai_integrity_ui_is_single_artifact_not_visible_batch_mode():
    app = read("app.py")

    assert "Artifact to review" in app
    assert "Paste one AI output, system prompt, policy, or workflow description to review." in app
    assert "Paste one artifact and read one local risk reading." in app

    assert "Batch review mode: split pasted artifacts" not in app
    assert "split pasted artifacts" not in app
    assert "Artifact(s) to review" not in app
    assert "batch mode extends" not in app


def test_ai_integrity_result_prioritizes_signals_before_optional_static_checks():
    app = read("app.py")

    ai_reading = app.index('st.markdown("### AI Integrity Reading")')
    triggered_card = app.index('cols[4].metric("Triggered signals", len(findings))')
    highest_pressure = app.index('st.markdown("#### Highest pressure signals")', ai_reading)
    repair_questions = app.index('st.markdown("#### Repair questions for human review")', ai_reading)
    optional_checks = app.index('st.markdown("#### Optional static boundary checks")', ai_reading)
    boundary_note = app.index('st.markdown("#### Boundary note")', ai_reading)

    assert ai_reading < triggered_card < highest_pressure < repair_questions < optional_checks < boundary_note
    assert "No privacy-boundary trigger was detected by this static artifact review." in app
    assert "No code-specific trigger was detected by this static artifact review." in app


def test_ai_integrity_single_artifact_patch_preserves_backend_boundaries():
    app = read("app.py")

    assert "audit_ai_integrity_artifact(ai_integrity_input, artifact_kind=artifact_kind)" in app
    assert "audit_ai_integrity_batch" in app  # backend helper remains available but is not exposed in the V1 UI
    assert "not proof, certification, approval, or a final safety claim" in app
    assert "no live model benchmarking, external calls, public ledger, central storage, or certification" in app

    assert "This is certification" not in app
    assert "This is approval" not in app
    assert "This proves safety" not in app
    assert "ALETHEIA has legal authority" not in app
    assert "ALETHEIA makes an enforcement decision" not in app
    assert "ALETHEIA provides final truth" not in app
