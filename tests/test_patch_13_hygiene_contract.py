"""
ALETHEIA RECOVERY NOTE
Patch 13: Code hygiene + language consistency tests.

Purpose:
    Keep cleanup changes small and reviewable: no duplicate hashlib import,
    repair-loop wording in English, and OpenAI kept optional for local builds.

Rollback:
    Remove this test file and revert Patch 13 cleanup changes.
"""

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
APP_TEXT = (ROOT / "app.py").read_text(encoding="utf-8")
PARSER_TEXT = (ROOT / "core" / "parser.py").read_text(encoding="utf-8")
REQ_TEXT = (ROOT / "requirements.txt").read_text(encoding="utf-8")
LLM_REQ_TEXT = (ROOT / "requirements-llm.txt").read_text(encoding="utf-8")
PROTOCOL_TEXT = (ROOT / "protocol.py").read_text(encoding="utf-8")


def test_hashlib_import_is_not_duplicated():
    assert APP_TEXT.count("import hashlib") == 1


def test_openai_dependency_is_optional_for_local_builds():
    assert "openai>=1.30" not in REQ_TEXT
    assert "openai>=1.30" in LLM_REQ_TEXT
    assert "OpenAI = None" in PARSER_TEXT
    assert "if not api_key or OpenAI is None" in PARSER_TEXT


def test_protocol_repair_questions_are_english_ui_text():
    assert "What appeal path exists for people affected by this proposal?" in PROTOCOL_TEXT
    assert "Which three checks and balances could move this pattern toward repair?" in PROTOCOL_TEXT
    assert "Welke bezwaarroute" not in PROTOCOL_TEXT
    assert "Welke drie checks-and-balances" not in PROTOCOL_TEXT
