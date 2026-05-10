import json
import zipfile
from io import BytesIO
from pathlib import Path

from core.witness import (
    build_local_witness_batch_zip,
    build_local_witness_receipt,
    combine_witness_text_uploads,
    detect_witness_question_set,
    parse_witness_batch_input,
)


def _receipt(text: str):
    return build_local_witness_receipt(
        module="Mirror Check",
        input_text=text,
        processed_text=text,
        input_status="QUESTION_SET_ITEM",
        scan={"scan_mode": "Local Scan"},
        sim={"stability": 0.7, "trust_index": 0.8, "alignment": 0.75, "ego": 0.1, "collapse_risk": False},
        report={"integrity": 0.7, "friction": 0.1, "collapse_probability": 0.2, "trust_friction": 0.1, "repair_questions": ["What safeguard is missing?"]},
        verdict="THRESHOLD",
        risk="Medium",
        protocol_label="THRESHOLD",
        app_version="test",
        generated_at_utc="2026-05-09T00:00:00Z",
    )


def test_question_set_detection_for_numbered_prompt_bank():
    text = "\n".join(f"{i:02d}. Who can appeal decision {i}?" for i in range(1, 51))
    items = parse_witness_batch_input(text)
    assert len(items) == 50
    assert detect_witness_question_set(text, len(items)) is True


def test_txt_uploads_are_combined_with_separator():
    class Upload:
        def __init__(self, data: str):
            self._data = data.encode("utf-8")
        def getvalue(self):
            return self._data

    combined = combine_witness_text_uploads([Upload("1. First question?"), Upload("2. Second question?")])
    assert "---" in combined
    assert "First question?" in combined
    assert "Second question?" in combined


def test_batch_index_records_question_set_input_type():
    receipts = [_receipt("Who can appeal this decision?"), _receipt("Where is the human override path?")]
    archive_bytes, index = build_local_witness_batch_zip(
        receipts,
        module="Mirror Check",
        app_version="test",
        generated_at_utc="2026-05-09T00:00:00Z",
        input_type="QUESTION_SET",
    )
    assert index["input_type"] == "QUESTION_SET"
    with zipfile.ZipFile(BytesIO(archive_bytes)) as zf:
        index_json = json.loads(zf.read("batch_index.json").decode("utf-8"))
        assert index_json["input_type"] == "QUESTION_SET"
        assert "Input type: QUESTION_SET" in zf.read("batch_index.txt").decode("utf-8")


def test_app_exposes_txt_upload_and_question_set_copy():
    app_text = Path("app.py").read_text()
    assert "Batch review — up to 50 ideas or questions" in app_text
    assert "Upload .txt batch files" in app_text
    assert "Question set detected" in app_text
    assert "without opening the main Pulse Tree" in app_text
