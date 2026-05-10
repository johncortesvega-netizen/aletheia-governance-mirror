"""
ALETHEIA RECOVERY NOTE
Patch 17: Mirror Check Local Witness Receipt

Purpose:
    Verify that Mirror Check uses the same local, user-held witness receipt
    pattern as Stress Test without changing verdicts, scoring, parsing, or
    witness hashing logic.

Scope:
    Content-level UI contract checks only. This test must not execute Streamlit.

Rollback:
    Remove this test file and revert the Patch 17 block in app.py.
"""

from pathlib import Path


APP_PATH = Path(__file__).resolve().parents[1] / "app.py"
APP_TEXT = APP_PATH.read_text(encoding="utf-8")


def test_mirror_check_uses_local_witness_receipt_builder():
    assert 'module="Mirror Check"' in APP_TEXT
    assert "mirror_receipt = build_local_witness_receipt(" in APP_TEXT
    assert "mirror_receipt_text = render_local_witness_receipt_text(mirror_receipt)" in APP_TEXT
    assert 'file_name="aletheia_mirror_check_local_witness_receipt.txt"' in APP_TEXT


def test_mirror_check_receipt_preserves_raw_and_processed_inputs():
    assert 'input_text=latest.get("raw_query", latest["query"])' in APP_TEXT
    assert 'processed_text=latest["query"]' in APP_TEXT
    assert 'input_status=latest.get("input_source", "USER_INPUT")' in APP_TEXT


def test_mirror_check_receipt_records_invisibility_filter():
    assert 'mirror_invisibility_applied = isinstance(invisibility_note, dict)' in APP_TEXT
    assert 'invisibility_applied=mirror_invisibility_applied' in APP_TEXT


def test_mirror_check_receipt_keeps_local_only_wording():
    assert "Creates a local receipt you hold. It is not published, synced, or treated as authority." in APP_TEXT
    assert '"⬇️ Download receipt"' in APP_TEXT
