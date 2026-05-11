
from pathlib import Path


def test_patch_71_6_tree_central_glow_blob_removed():
    app_text = Path("app.py").read_text(encoding="utf-8")

    assert "TREE_VISUAL_CENTRAL_GLOW_REMOVED = True" in app_text
    assert "central glow/blob intentionally removed" in app_text
    assert 'cy="{175 - glow_height / 2}"' not in app_text
    assert 'ry="{glow_height}"' not in app_text
    assert "glow_height = 34 + int(alignment * 46)" not in app_text


def test_patch_71_6_tree_keeps_canopy_trunk_caption_and_state_logic():
    app_text = Path("app.py").read_text(encoding="utf-8")

    # Keep the actual tree structure and state-color logic.
    assert "def render_pulse_tree" in app_text
    assert "canopy_scale = 0.70 + (score * 0.18)" in app_text
    assert "canopy_y_offset" in app_text
    assert "canopy_sag" in app_text
    assert '<path d="M124 214 C126 178' in app_text
    assert "TREE_VISUAL_CAPTION_CLASS" in app_text
    assert "Visual tree score is explanatory; receipt integrity remains the protocol metric." in app_text

    for state in ["SANCTUARY", "THRESHOLD", "ASYLUM", "QUESTION_PROMPT"]:
        assert state in app_text


def test_patch_71_6_no_scoring_or_receipt_logic_claimed_changed():
    manifest = Path("PATCH_71_6_MANIFEST.txt").read_text(encoding="utf-8")
    recovery = Path("PATCH_71_6_RECOVERY_NOTE.md").read_text(encoding="utf-8")
    combined = manifest + "\n" + recovery

    assert "visual-only" in combined
    assert "No scoring" in combined
    assert "No receipt" in combined
    assert "No authority-boundary" in combined
    assert "Public ledger: `False`" in recovery
    assert "Global ID sync: `False`" in recovery
    assert "Central storage: `False`" in recovery


def test_patch_71_6_manifest_status_and_progress_docs_present():
    for path in [
        "PATCH_71_6_MANIFEST.txt",
        "PATCH_71_6_RECOVERY_NOTE.md",
        "PATCH_STATUS.md",
        "docs/progress_database.md",
    ]:
        assert Path(path).exists(), path

    status = Path("PATCH_STATUS.md").read_text(encoding="utf-8")
    progress = Path("docs/progress_database.md").read_text(encoding="utf-8")

    assert "Patch 71.6" in status
    assert "Patch 71.6" in progress
    assert "Tree Central Glow Removal" in status + progress
