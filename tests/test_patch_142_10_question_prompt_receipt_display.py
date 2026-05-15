from __future__ import annotations

import io
import json
import zipfile
from pathlib import Path

from ui.receipt_reader import _batch_receipt_index_rows, parse_receipt_standard_view, parse_uploaded_receipt_file


class Upload:
    def __init__(self, name: str, payload: bytes):
        self.name = name
        self._payload = payload

    def getvalue(self) -> bytes:
        return self._payload


def _question_prompt_receipt() -> str:
    return json.dumps(
        {
            "active_modules": ["Mirror Check"],
            "module": "Mirror Check",
            "metrics": {},
            "repair_questions": ["Which part of this is a review question?"],
            "verdict": {
                "protocol_adjusted_state": "QUESTION_PROMPT",
                "risk": "Not scored",
                "protocol_label": "Audit Question / Review Tool",
            },
        },
        indent=2,
    )


def _batch_zip() -> bytes:
    buffer = io.BytesIO()
    with zipfile.ZipFile(buffer, "w") as archive:
        archive.writestr("batch_index.txt", "index only")
        archive.writestr("receipt_01.json", _question_prompt_receipt())
        archive.writestr("receipt_02.json", _question_prompt_receipt())
    return buffer.getvalue()


def test_question_prompt_detail_marks_metrics_not_applicable_not_missing():
    view = parse_receipt_standard_view(_question_prompt_receipt())

    assert view["native_state"] == "QUESTION_PROMPT"
    assert view["standard_band"] == "Not scored (review-tool mode)"
    assert view["metric_rows"] == [
        {
            "Metric": "Scored Metrics",
            "Value": "Not applicable",
            "Interpretation": "QUESTION_PROMPT receipts are review-tool prompts, not scored scenario receipts.",
        }
    ]
    assert "review-tool prompt" in view["summary"]


def test_question_prompt_batch_index_marks_suppressed_metrics_not_applicable():
    parsed = parse_uploaded_receipt_file(Upload("question_prompt_batch.zip", _batch_zip()))
    rows = _batch_receipt_index_rows(parsed)

    assert parsed["receipt_count"] == 2
    assert rows[0]["Native State"] == "QUESTION_PROMPT"
    assert rows[0]["Review Pressure"] == "Not scored / review-tool mode"
    assert rows[0]["Integrity"] == "Not applicable"
    assert rows[0]["Collapse"] == "Not applicable"
    assert rows[0]["Trust Index"] == "Not applicable"
    assert "Collapse Probability" not in rows[0]
    assert "Repair Questions" not in rows[0]
    assert rows[0]["Repairs"] == "1"


def test_question_prompt_ui_copy_explains_suppressed_metrics():
    helper = Path("ui/receipt_reader.py").read_text(encoding="utf-8")

    assert "QUESTION_PROMPT receipts intentionally suppress scored metrics" in helper
    assert "Not applicable — QUESTION_PROMPT receipts are review-tool prompts" in helper
    assert "QUESTION_PROMPT metrics are marked not applicable, not missing" in helper


def test_patch_142_10_manifest_and_recovery_note_exist():
    root = Path(__file__).resolve().parents[1]
    assert (root / "PATCH_142_10_MANIFEST.txt").exists()
    assert (root / "PATCH_142_10_RECOVERY_NOTE.md").exists()
