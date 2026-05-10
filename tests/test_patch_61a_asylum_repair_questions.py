from pathlib import Path

from protocol import (
    ensure_asylum_repair_questions,
    protocol_repair_questions,
    requires_asylum_repair_questions,
)


def test_asylum_repair_questions_include_human_review_paths():
    questions = protocol_repair_questions(
        "ASYLUM",
        "Malicious Leadership / Asylum",
        "High",
    )
    joined = "\n".join(questions).lower()
    assert len(questions) >= 6
    assert "appeal" in joined
    assert "basic rights" in joined
    assert "human review" in joined or "independent reviewer" in joined
    assert "non-coercive" in joined


def test_high_risk_empty_report_gets_repair_questions():
    report = {"integrity": 0.84, "repair_questions": []}
    patched = ensure_asylum_repair_questions(
        report,
        verdict="ASYLUM",
        risk="High",
        protocol_label="Malicious Leadership / Asylum",
        scan={"power_concentration": 0.88},
    )
    assert patched is not report
    assert patched["repair_questions"]
    assert patched["repair_questions_source"] == "patch_61A_asylum_repair_questions"


def test_power_concentration_trigger_is_mirror_only():
    assert requires_asylum_repair_questions(
        verdict="THRESHOLD",
        risk="Medium",
        protocol_label="Manual stress test",
        scan={"power_concentration": 0.80},
    )
    patched = ensure_asylum_repair_questions(
        {},
        verdict="THRESHOLD",
        risk="Medium",
        protocol_label="Manual stress test",
        scan={"power_concentration": 0.80},
    )
    joined = "\n".join(patched["repair_questions"]).lower()
    assert "aletheia becoming the authority" in joined
    assert "without retaliation" in joined


def test_patch_files_document_safe_boundary():
    root = Path(__file__).resolve().parents[1]
    doc = (root / "docs" / "asylum_repair_calibration.md").read_text(encoding="utf-8")
    recovery = (root / "PATCH_61A_RECOVERY_NOTE.md").read_text(encoding="utf-8")
    app = (root / "app.py").read_text(encoding="utf-8")
    assert "does not add enforcement" in doc.lower()
    assert "human review" in recovery.lower()
    assert "ensure_asylum_repair_questions" in app
