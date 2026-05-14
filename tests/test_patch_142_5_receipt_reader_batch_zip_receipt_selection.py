from __future__ import annotations

import io
import json
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


class FakeUpload:
    def __init__(self, name: str, data: bytes):
        self.name = name
        self._data = data

    def getvalue(self) -> bytes:
        return self._data


def _receipt_json(state: str = "THRESHOLD", risk: str = "Medium") -> str:
    return json.dumps(
        {
            "active_modules": ["Simulation"],
            "module": "Simulation",
            "metrics": {
                "integrity": 0.569,
                "friction": 0.149,
                "collapse_probability": 0.265,
                "trust_index": 0.8,
                "alignment": 0.78,
                "ego": 0.15,
            },
            "repair_questions": [
                "What explanation path lets affected people understand how the automated triage decision was made?"
            ],
            "verdict": {
                "protocol_adjusted_state": state,
                "risk": risk,
                "protocol_label": "Missing Safeguard Negation / Needs Safeguards",
            },
        },
        indent=2,
    )


def _receipt_text() -> str:
    return """ALETHEIA LOCAL WITNESS RECEIPT
Module: Simulation
VERDICT SIGNAL
Protocol-adjusted state: THRESHOLD
Risk: Medium
Protocol label: Missing Safeguard Negation / Needs Safeguards
CORE METRICS
Integrity: 0.5690
Friction: 0.1490
Collapse probability: 0.2650
Trust index: 0.8000
Alignment: 0.7800
Ego: 0.1500
"""


def _batch_zip() -> bytes:
    buffer = io.BytesIO()
    with zipfile.ZipFile(buffer, "w") as archive:
        archive.writestr("batch_index.txt", "ALETHEIA LOCAL WITNESS BATCH INDEX\nReceipt count: 1\n01. THRESHOLD / Medium")
        archive.writestr("batch_index.json", json.dumps({"receipt_count": 1, "module": "Simulation"}))
        archive.writestr("receipt_01.txt", _receipt_text())
        archive.writestr("receipt_01.json", _receipt_json())
    return buffer.getvalue()


def test_patch_142_5_batch_zip_uses_actual_receipts_not_batch_index_for_inspection():
    from ui.receipt_reader import parse_uploaded_receipt_file

    parsed = parse_uploaded_receipt_file(FakeUpload("batch.zip", _batch_zip()))

    assert parsed["kind"] == "batch_zip"
    assert parsed["receipt_count"] == 1
    assert parsed["distribution"] == {"THRESHOLD": 1}
    assert parsed["risk_distribution"] == {"Medium": 1}
    assert parsed["module_distribution"] == {"Simulation": 1}
    first_name, first_view = parsed["views"][0]
    assert first_name == "receipt_01.json"
    assert "batch_index" not in first_name
    assert first_view["fields"]["protocol_label"] == "Missing Safeguard Negation / Needs Safeguards"
    assert first_view["fields"]["trust"] == "0.8000"
    assert first_view["fields"]["alignment"] == "0.7800"
    assert first_view["fields"]["integrity"] == "0.5690"
    assert first_view["repair_questions"][0].startswith("What explanation path")


def test_patch_142_5_batch_zip_reader_mentions_batch_index_is_not_inspected_as_receipt():
    helper = (ROOT / "ui/receipt_reader.py").read_text(encoding="utf-8")
    assert "Batch index files are used only as indexes" in helper
    assert "Inspect first receipt" in helper
    assert "_is_batch_index_name" in helper
    assert "_receipt_sort_key" in helper


def test_patch_142_5_docs_and_manifest_exist():
    required = [
        "PATCH_142_5_MANIFEST.txt",
        "PATCH_142_5_RECOVERY_NOTE.md",
        "tests/test_patch_142_5_receipt_reader_batch_zip_receipt_selection.py",
    ]
    for rel in required:
        assert (ROOT / rel).exists(), rel
