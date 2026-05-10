import zipfile
from io import BytesIO
from pathlib import Path

from core.witness import (
    MAX_BATCH_RECEIPTS,
    build_local_witness_batch_zip,
    build_local_witness_receipt,
    parse_witness_batch_input,
)


def _receipt(text: str, verdict: str = "THRESHOLD"):
    return build_local_witness_receipt(
        module="Mirror Check",
        input_text=text,
        processed_text=text,
        input_status="USER_INPUT",
        scan={"scan_mode": "Local Scan"},
        sim={"stability": 0.7, "trust_index": 0.8, "alignment": 0.75, "ego": 0.1, "collapse_risk": False},
        report={"integrity": 0.7, "friction": 0.1, "collapse_probability": 0.2, "trust_friction": 0.1, "repair_questions": ["What safeguard is missing?"]},
        verdict=verdict,
        risk="Medium" if verdict == "THRESHOLD" else "High",
        protocol_label=verdict,
        app_version="test",
        generated_at_utc="2026-05-09T00:00:00Z",
    )


def test_batch_parser_accepts_numbered_separator_and_line_lists():
    text = """
    1. A city uses open data and appeal.
    2. A society is run by AI only, with no human input.
    ---
    A system cannot be questioned and has no appeal path.
    """
    items = parse_witness_batch_input(text)
    assert items == [
        "A city uses open data and appeal.",
        "A society is run by AI only, with no human input.",
        "A system cannot be questioned and has no appeal path.",
    ]

    line_items = parse_witness_batch_input("one phrase\ntwo phrase\nthree phrase")
    assert line_items == ["one phrase", "two phrase", "three phrase"]


def test_batch_parser_caps_at_fifty_items():
    text = "\n".join(f"{i}. Scenario {i}" for i in range(1, 61))
    items = parse_witness_batch_input(text)
    assert len(items) == MAX_BATCH_RECEIPTS
    assert items[0] == "Scenario 1"
    assert items[-1] == "Scenario 50"


def test_batch_zip_contains_all_receipts_and_indexes():
    receipts = [_receipt("A city uses appeal."), _receipt("No appeal path.", verdict="ASYLUM")]
    archive_bytes, index = build_local_witness_batch_zip(
        receipts,
        module="Mirror Check",
        app_version="test",
        generated_at_utc="2026-05-09T00:00:00Z",
    )
    assert index["receipt_type"] == "ALETHEIA_LOCAL_WITNESS_BATCH_INDEX"
    assert index["receipt_count"] == 2
    assert len(index["hashes"]["batch_index_sha256"]) == 64

    with zipfile.ZipFile(BytesIO(archive_bytes)) as zf:
        names = set(zf.namelist())
        assert "batch_index.txt" in names
        assert "batch_index.json" in names
        assert "receipt_01.txt" in names
        assert "receipt_01.json" in names
        assert "receipt_02.txt" in names
        assert "receipt_02.json" in names
        assert "ALETHEIA LOCAL WITNESS RECEIPT" in zf.read("receipt_01.txt").decode("utf-8")
        assert "ALETHEIA LOCAL WITNESS BATCH INDEX" in zf.read("batch_index.txt").decode("utf-8")


def test_app_exposes_batch_testing_copy_and_zip_download():
    app_text = Path("app.py").read_text()
    assert "Batch Testing — 50 phrases max" in app_text
    assert "Paste batch phrases or questions" in app_text
    assert "Download full batch archive (.zip)" in app_text
    assert "aletheia_mirror_check_batch_witness_receipts.zip" in app_text
