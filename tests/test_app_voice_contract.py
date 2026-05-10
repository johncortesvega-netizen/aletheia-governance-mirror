"""
ALETHEIA RECOVERY NOTE
Patch 10: App Voice Alignment

Purpose:
    Verify that user-facing app wording moved toward a clearer, warmer,
    more intuitive voice without changing production logic.

Scope:
    Content-level UI contract checks only. This test must not execute Streamlit.

Rollback:
    Remove this test file and revert app.py wording changes.
"""

from pathlib import Path


APP_PATH = Path(__file__).resolve().parents[1] / "app.py"
APP_TEXT = APP_PATH.read_text(encoding="utf-8")


def test_voice_uses_plain_intuitive_simulation_labels():
    assert "Stress Test — Scenario Lab" in APP_TEXT
    assert "Start with your own scenario" in APP_TEXT
    assert "You lead." in APP_TEXT
    assert "Write or paste your scenario" in APP_TEXT
    assert "⚡ Run review" in APP_TEXT


def test_voice_keeps_mirror_not_throne_boundary_simple():
    assert "ALETHEIA helps you check whether power stays visible" in APP_TEXT
    assert "It is a mirror, not a throne." in APP_TEXT
    assert "does not rule, vote, command, or replace people" in APP_TEXT
    assert "does not give orders or final judgments" in APP_TEXT


def test_voice_replaces_stiffer_patch_08_phrases():
    assert "Demo mode is on. These results are only an example." in APP_TEXT
    assert "Your input is being reviewed. You are the source; ALETHEIA is the mirror." in APP_TEXT
    assert "Names and titles will be removed before review." in APP_TEXT
    assert "No review has run yet." in APP_TEXT
    assert "Silent Operator repair questions" not in APP_TEXT


def test_receipt_wording_stays_local_and_non_authoritative():
    assert "Creates a local receipt you hold." in APP_TEXT
    assert "It is not published, synced, or treated as authority." in APP_TEXT
    assert "Download receipt" in APP_TEXT
