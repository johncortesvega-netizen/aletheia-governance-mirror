from __future__ import annotations

import io
import json
import zipfile
from pathlib import Path

from ui.receipt_reader import _batch_receipt_index_rows, parse_uploaded_receipt_file


class Upload:
    def __init__(self, name: str, payload: bytes):
        self.name = name
        self._payload = payload

    def getvalue(self) -> bytes:
        return self._payload


def _receipt_json(index: int, state: str, risk: str, protocol_label: str) -> str:
    metrics = {} if state == "QUESTION_PROMPT" else {
        "integrity": 0.58 + index / 1000,
        "friction": 0.12,
        "collapse_probability": 0.22,
        "trust_index": 0.8,
        "alignment": 0.78,
        "ego": 0.15,
    }
    return json.dumps(
        {
            "active_modules": ["Mirror Check"],
            "module": "Mirror Check",
            "metrics": metrics,
            "repair_questions": [] if state == "QUESTION_PROMPT" else ["What appeal path exists?"],
            "verdict": {
                "protocol_adjusted_state": state,
                "risk": risk,
                "protocol_label": protocol_label,
            },
        },
        indent=2,
    )


def _batch_zip() -> bytes:
    buffer = io.BytesIO()
    with zipfile.ZipFile(buffer, "w") as archive:
        archive.writestr("batch_index.txt", "index only; not a receipt")
        archive.writestr("receipt_01.json", _receipt_json(1, "QUESTION_PROMPT", "Not scored", "Audit Question / Review Tool"))
        archive.writestr("receipt_02.json", _receipt_json(2, "THRESHOLD", "Medium", "Missing Safeguard Negation / Needs Safeguards"))
        archive.writestr("receipt_03.json", _receipt_json(3, "ASYLUM", "High", "MEI7 Ethics Gate / Asylum"))
    return buffer.getvalue()


def test_batch_reader_builds_one_index_row_per_receipt_without_rescoring():
    parsed = parse_uploaded_receipt_file(Upload("mirror_check_batch.zip", _batch_zip()))

    assert parsed["kind"] == "batch_zip"
    assert parsed["bundle_type"] == "receipt_batch"
    assert parsed["receipt_count"] == 3
    assert parsed["distribution"] == {"QUESTION_PROMPT": 1, "THRESHOLD": 1, "ASYLUM": 1}

    rows = _batch_receipt_index_rows(parsed)
    assert len(rows) == 3
    assert [row["#"] for row in rows] == ["1", "2", "3"]
    assert [row["File"] for row in rows] == ["receipt_01.json", "receipt_02.json", "receipt_03.json"]
    assert rows[0]["Native State"] == "QUESTION_PROMPT"
    assert rows[0]["Review Pressure"] == "Not scored / review-tool mode"
    assert rows[0]["Protocol Label"] == "Audit Question / Review Tool"
    assert rows[0]["Integrity"] == "Not applicable"
    assert rows[0]["Collapse"] == "Not applicable"
    assert rows[0]["Trust Index"] == "Not applicable"
    assert rows[1]["Native State"] == "THRESHOLD"
    assert rows[1]["Repairs"] == "1"
    assert rows[2]["Protocol Label"] == "MEI7 Ethics Gate / Asylum"


def test_batch_reader_ui_has_receipt_index_and_selectable_inspection():
    helper = Path("ui/receipt_reader.py").read_text(encoding="utf-8")
    assert "### Receipt Index" in helper
    assert "One compact row per uploaded receipt" in helper
    assert "Inspect receipt" in helper
    assert "Inspect selected receipt" in helper
    assert "Inspect first receipt" not in helper
    for forbidden in ["rescore", "merge verdicts", "create a new receipt"]:
        assert forbidden in helper


def test_patch_142_9_manifest_and_recovery_note_exist():
    root = Path(__file__).resolve().parents[1]
    assert (root / "PATCH_142_9_MANIFEST.txt").exists()
    assert (root / "PATCH_142_9_RECOVERY_NOTE.md").exists()
