from pathlib import Path

from core.world_lens import (
    format_raw_trust_label,
    format_trust_prior_label,
    trust_coverage_label,
)

ROOT = Path(__file__).resolve().parents[1]


def test_raw_trust_missing_is_explicit():
    assert format_raw_trust_label(None) == "not available"
    assert format_raw_trust_label(float("nan")) == "not available"


def test_neutral_trust_prior_is_labeled_as_default():
    assert format_trust_prior_label(0.5) == "0.500 neutral default"
    assert format_trust_prior_label(0.62) == "0.620"


def test_coverage_labels_distinguish_raw_from_fallback():
    raw, prior, note = trust_coverage_label(0.0, 1.0)
    assert raw == "0.0%"
    assert prior == "100.0%"
    assert "not observed survey trust coverage" in note
    assert "neutral 0.500 prior" in note


def test_app_and_docs_use_clear_world_lens_trust_wording():
    app_text = (ROOT / "app.py").read_text(encoding="utf-8")
    doc_text = (ROOT / "docs" / "world_lens_interpretation.md").read_text(encoding="utf-8")
    assert "Raw trust survey coverage" in app_text
    assert "Neutral trust-prior fallback coverage" in app_text
    assert "Raw trust: not available" in doc_text
    assert "Trust prior used: 0.500 neutral default" in doc_text
