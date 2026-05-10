"""
ALETHEIA RECOVERY NOTE
Patch 16.1: Mirror Check Wording Polish

Purpose:
    Polish Mirror Check wording after Patch 16 without changing input flow,
    parsing, verdicts, scoring, witness hashing, or actor decoupling behavior.

Scope:
    Content-level UI contract checks only. This test must not execute Streamlit.

Rollback:
    Remove this test file and revert the small app.py wording edits.
"""

from pathlib import Path


APP_PATH = Path(__file__).resolve().parents[1] / "app.py"
APP_TEXT = APP_PATH.read_text(encoding="utf-8")


def test_mirror_check_uses_clearer_warmer_header_and_intro():
    assert "Mirror Check — Gentle Risk Review" in APP_TEXT
    assert "Bring one idea at a time." in APP_TEXT
    assert "ALETHEIA checks how power moves" in APP_TEXT
    assert "You keep the judgment." in APP_TEXT


def test_mirror_check_expander_uses_plain_language_functions():
    assert "What Mirror Check looks for" in APP_TEXT
    assert "Care alignment" in APP_TEXT
    assert "Does the idea protect people?" in APP_TEXT
    assert "Power language" in APP_TEXT
    assert "Does soft wording hide control?" in APP_TEXT
    assert "Witness receipt" in APP_TEXT
    assert "A local record you hold." in APP_TEXT


def test_mirror_check_action_wording_is_short_and_not_commanding():
    assert "Share one idea" in APP_TEXT
    assert "Write or paste the idea you want reviewed" in APP_TEXT
    assert "Review idea" in APP_TEXT
    assert "Reading the idea and preparing the review..." in APP_TEXT
    assert "Your idea is ready for review. You are the source; ALETHEIA is the mirror." in APP_TEXT


def test_mirror_check_old_stiffer_wording_is_gone():
    assert "Scenario Care & Risk Review" not in APP_TEXT
    assert "Ask a governance question" not in APP_TEXT
    assert "Review this idea" not in APP_TEXT
    assert "preparing the audit" not in APP_TEXT
