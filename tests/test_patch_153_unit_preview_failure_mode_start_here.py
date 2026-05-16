from __future__ import annotations

from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from ui.unit_preview import (
    get_unit_preview_failure_mode_markdown,
    get_unit_preview_what_aletheia_looks_for_markdown,
)

ROOT = Path(__file__).resolve().parents[1]


def read(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8")


def test_start_here_has_side_by_side_failure_mode_expander_copy() -> None:
    source = read("ui/unit_preview.py")

    assert 'with container.expander("Start here: try this first", expanded=False):' in source
    assert 'start_columns = container.columns(2, gap="large")' in source
    assert "#### What ALETHEIA looks for" in source
    assert "#### Seven failure-mode review signals" in source
    assert "get_unit_preview_what_aletheia_looks_for_markdown()" in source
    assert "get_unit_preview_failure_mode_markdown()" in source


def test_start_here_failure_mode_language_is_complete_and_bounded() -> None:
    combined = (
        get_unit_preview_what_aletheia_looks_for_markdown()
        + "\n"
        + get_unit_preview_failure_mode_markdown()
    )

    assert "appear more legitimate, neutral, certain, or authoritative than the evidence supports" in combined
    assert "not verdicts or proof of wrongdoing" in combined
    assert "prompts for review" in combined
    for phrase in [
        "Authority drift",
        "Evidence inflation",
        "Flattery pressure",
        "Capture pressure",
        "Sanctification drift",
        "False neutrality",
        "No-appeal automation",
    ]:
        assert phrase in combined


def test_patch_153_preserves_behavior_boundary() -> None:
    manifest = read("PATCH_153_MANIFEST.txt")
    recovery = read("PATCH_153_RECOVERY_NOTE.md")
    combined = manifest + "\n" + recovery

    assert "ui/unit_preview.py" in manifest
    assert "No scoring change" in combined
    assert "No routing change" in combined
    assert "No receipt schema change" in combined
    assert "No new tab" in combined
