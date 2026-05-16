from __future__ import annotations

from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

ROOT = Path(__file__).resolve().parents[1]


def read(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8")


def test_start_here_uses_side_by_side_nested_expanders() -> None:
    source = read("ui/unit_preview.py")

    assert 'with container.expander("Start here: try this first", expanded=False):' in source
    assert 'start_columns = container.columns(2, gap="large")' in source
    assert 'start_columns[0].expander("What ALETHEIA looks for", expanded=False)' in source
    assert 'start_columns[1].expander("Seven failure-mode review signals", expanded=False)' in source
    assert "Open these review-lens notes only when you want extra orientation" in source


def test_start_here_expanders_do_not_change_engine_boundaries() -> None:
    source = read("ui/unit_preview.py")

    assert "get_unit_preview_start_here_markdown()" in source
    assert "get_unit_preview_what_aletheia_looks_for_markdown()" in source
    assert "get_unit_preview_failure_mode_markdown()" in source
    assert "not verdicts" in source
    assert "full_report" not in source
    assert "repair_prompts_from_report" not in source
