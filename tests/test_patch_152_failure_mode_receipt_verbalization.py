from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def read(rel: str) -> str:
    return (ROOT / rel).read_text(encoding="utf-8")


def test_receipt_reader_renders_failure_mode_layer_for_every_single_view():
    text = read("ui/receipt_reader.py")
    assert "FAILURE_MODE_REVIEW_SIGNALS" in text
    assert "def _render_failure_mode_review_signals" in text
    assert "_render_failure_mode_review_signals(container)" in text
    assert "### Failure-mode review signals" in text
    assert "internal review signals, not proof" in text
    assert "of wrongdoing, illegality, deception, or final truth" in text


def test_all_required_failure_mode_names_are_present_in_receipt_reader_and_docs():
    combined = "\n".join(
        read(rel)
        for rel in [
            "ui/receipt_reader.py",
            "README.md",
            "about_page.py",
            "pages_ui/about_page.py",
            "docs/receipt_reader_standard_view.md",
            "docs/SIGNAL_DICTIONARY.md",
        ]
    )
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


def test_failure_mode_copy_preserves_boundary_and_no_new_tab_claim():
    combined = "\n".join(
        read(rel)
        for rel in [
            "README.md",
            "about_page.py",
            "pages_ui/about_page.py",
            "docs/receipt_reader_standard_view.md",
        ]
    )
    assert "not verdicts" in combined
    assert "Human review remains required" in combined
    assert "does not rescore" in combined
    reader_text = read("ui/receipt_reader.py")
    assert "not proof" in reader_text
    assert "of wrongdoing, illegality, deception, or final truth" in reader_text
    assert "Receipt Reader repeats this verbal layer for all uploaded receipts" in combined
