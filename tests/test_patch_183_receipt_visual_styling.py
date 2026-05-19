from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
APP = ROOT / "app.py"


def test_patch_183_version_marks_third_visual_pass():
    text = APP.read_text(encoding="utf-8")
    assert 'APP_VERSION = "v1.0-ai-patrol-sky-theme-p3"' in text


def test_patch_183_receipt_visual_css_tokens_present():
    text = APP.read_text(encoding="utf-8")
    assert "Patch 183: receipt visual styling pass" in text
    assert ".receipt-sky-panel" in text
    assert ".receipt-boundary-strip" in text
    assert ".receipt-boundary-pill" in text
    assert ".receipt-hash-pill" in text
    assert ".receipt-code-frame" in text
    assert "border-left: 6px solid var(--gold)" in text
    assert "position: absolute;" in text


def test_patch_183_local_and_mirror_receipts_have_visual_cards_without_schema_changes():
    text = APP.read_text(encoding="utf-8")
    assert "visual-only receipt framing; receipt payload and schema remain unchanged" in text
    assert "visual-only Mirror Check receipt framing; receipt payload and schema remain unchanged" in text
    assert "Download text only. This visual card does not change the receipt content, schema, or authority boundary." in text
    assert "Local only" in text
    assert "User-held text file" in text
    assert "Human review required" in text
    assert "build_local_witness_receipt(" in text
    assert "build_mirror_receipt_for_entry(latest)" in text
    assert "render_local_witness_receipt_text" in text


def test_patch_183_receipt_documentation_and_world_lens_framing_present():
    text = APP.read_text(encoding="utf-8")
    assert "visual-only example framing for receipt documentation" in text
    assert "Local Witness Receipt v2" in text
    assert "SHA-256 fingerprints" in text
    assert "visual-only World Lens receipt download framing; ZIP contents remain unchanged" in text
    assert "Complete World Lens receipt" in text
    assert "Evidence alignment required" in text
    assert "Not policy authority" in text
    assert "_build_world_lens_receipt_zip()" in text


def test_patch_183_status_and_recovery_artifacts_present():
    for path in [
        "PATCH_183_MANIFEST.txt",
        "PATCH_183_RECOVERY_NOTE.md",
        "PATCH_183_DELETE_LIST.txt",
        "PATCH_STATUS.md",
        "docs/progress_database.md",
    ]:
        assert (ROOT / path).exists(), path
    status = (ROOT / "PATCH_STATUS.md").read_text(encoding="utf-8")
    progress = (ROOT / "docs" / "progress_database.md").read_text(encoding="utf-8")
    assert "Patch 183 — AI Patrol Receipt Visual Styling" in status
    assert "Patch 183 — AI Patrol Receipt Visual Styling" in progress
