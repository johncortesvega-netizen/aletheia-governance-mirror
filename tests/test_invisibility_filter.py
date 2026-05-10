"""
ALETHEIA RECOVERY NOTE
Patch 07: Invisibility Filter helper tests

Purpose:
    Verify actor decoupling without changing product behavior.

Scope:
    Tests core.parser.decouple_actor only.

Rollback:
    Remove this test file and the Patch 07 helper from core/parser.py.
"""

import sys
import types

# Test environment shim: core.parser imports streamlit for secrets access in the
# existing parser path. Patch 07 only tests the pure decouple_actor helper.
if "streamlit" not in sys.modules:
    streamlit_stub = types.SimpleNamespace(secrets={})
    sys.modules["streamlit"] = streamlit_stub

if "openai" not in sys.modules:
    openai_stub = types.SimpleNamespace(OpenAI=object)
    sys.modules["openai"] = openai_stub

from core.parser import decouple_actor


def test_decouple_actor_removes_named_actor_but_keeps_logic_terms():
    result = decouple_actor(
        "President Jane Doe proposes permanent authority with no appeal path."
    )

    assert result["invisibility_filter_applied"] is True
    assert "Jane Doe" not in result["decoupled_text"]
    assert "[ROLE_ACTOR]" in result["decoupled_text"]
    assert "permanent authority" in result["decoupled_text"]
    assert "no appeal path" in result["decoupled_text"]


def test_decouple_actor_redacts_contact_identifiers():
    result = decouple_actor(
        "Send the audit to john@example.com and @johncortesvega before review."
    )

    assert "john@example.com" not in result["decoupled_text"]
    assert "@johncortesvega" not in result["decoupled_text"]
    assert "[CONTACT]" in result["decoupled_text"]
    assert "[HANDLE]" in result["decoupled_text"]
    assert result["redaction_count"] == 2


def test_decouple_actor_is_noop_when_no_identifiers_are_present():
    text = "A local council creates appeal rights, public review, and sunset clauses."
    result = decouple_actor(text)

    assert result["decoupled_text"] == text
    assert result["invisibility_filter_applied"] is False
    assert result["redaction_count"] == 0
