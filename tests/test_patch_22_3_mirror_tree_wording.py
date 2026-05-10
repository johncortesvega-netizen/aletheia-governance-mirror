from pathlib import Path

APP = Path(__file__).resolve().parents[1] / "app.py"
TEXT = APP.read_text(encoding="utf-8")


def test_mirror_tree_uses_current_name():
    assert 'title="Mirror Reading Tree"' in TEXT
    assert 'title="Chat Audit Pulse Tree"' not in TEXT


def test_empty_state_copy_is_plain_and_current():
    assert "No reading yet. Share one idea above to generate a Mirror Reading Tree." in TEXT
    assert "generate the Sanctuary / Threshold / Asylum result and Pulse Tree" not in TEXT
