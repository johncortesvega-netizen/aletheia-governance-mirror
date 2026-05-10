"""Patch 31 — World Lens empirical alignment tests.

World Lens is connected to Evidence Lab through empirical country-year rows.
This patch keeps that connection explicit while preventing Mirror Check text
scenario diagnostics from being silently implied by country-year indicator data.
"""

from __future__ import annotations

import importlib.util
from pathlib import Path

import pandas as pd

from core.empirical import apply_world_lens_diagnostic_alignment, score_empirical_frame


def _sample_empirical_row() -> pd.DataFrame:
    return pd.DataFrame(
        [
            {
                "country": "Netherlands",
                "iso3": "NLD",
                "year": 2024,
                "population": 18000000,
                "wgi_voice_accountability": 1.4,
                "wgi_political_stability": 0.9,
                "wgi_government_effectiveness": 1.7,
                "wgi_regulatory_quality": 1.6,
                "wgi_rule_of_law": 1.7,
                "wgi_control_corruption": 1.8,
                "vdem_executive_constraints": 0.86,
                "vdem_democracy": 0.82,
                "wvs_generalized_trust": 0.66,
            }
        ]
    )


def test_empirical_scoring_exports_world_lens_alignment_fields():
    scored = score_empirical_frame(_sample_empirical_row())
    assert len(scored) == 1

    row = scored.iloc[0]
    assert row["mirror_logic_version"] == "patch31-world-lens-empirical-alignment"
    assert row["diagnostic_scope"] == "empirical_country_year_evidence"
    assert "Evidence Lab empirical" in row["empirical_world_lens_connection"]
    assert row["scenario_text_diagnostic_scope"] == "not_assessed_without_policy_text"


def test_mirror_check_text_diagnostics_are_not_implied_from_country_year_data():
    scored = score_empirical_frame(_sample_empirical_row())
    row = scored.iloc[0]

    assert row["cognitive_resilience_signal"] == "not_assessed_from_empirical_country_year"
    assert row["education_defense_signal"] == "not_assessed_from_empirical_country_year"
    assert row["hard_capture_trace"] == "not_assessed_without_policy_text"
    assert row["high_cr_laundering_blocked"] == "not_applicable_without_policy_text"


def test_empirical_proxy_signals_are_still_available_for_world_lens():
    scored = score_empirical_frame(_sample_empirical_row())
    row = scored.iloc[0]

    assert row["empirical_capture_pressure_signal"] in {"low", "medium", "high", "unknown"}
    assert row["empirical_governance_risk_signal"] in {"low", "medium", "high", "unknown"}
    assert row["empirical_trust_gap_signal"] in {"low", "medium", "high", "unknown"}
    assert pd.notna(row["empirical_capture_pressure_score"])


def test_alignment_helper_preserves_operational_rows_and_adds_scope_columns():
    raw = pd.DataFrame(
        [
            {
                "country": "Example",
                "iso3": "EXP",
                "year": 2024,
                "integrity": 0.52,
                "collapse_probability": 0.31,
                "friction": 0.2,
                "centralization": 0.7,
                "transparency": 0.3,
                "regulation": 0.4,
                "empirical_trust_prior": 0.45,
            }
        ]
    )
    aligned = apply_world_lens_diagnostic_alignment(raw)

    assert aligned.loc[0, "country"] == "Example"
    assert aligned.loc[0, "diagnostic_scope"] == "empirical_country_year_evidence"
    assert aligned.loc[0, "empirical_capture_pressure_signal"] in {"medium", "high"}
    assert "not as a Mirror Check text scenario" in aligned.loc[0, "world_lens_interpretation_warning"]


def test_app_version_marks_patch_31_without_importing_streamlit_runtime():
    app_path = Path(__file__).resolve().parents[1] / "app.py"
    text = app_path.read_text(encoding="utf-8")
    assert 'APP_VERSION = "v9.6.11-patch31-world-lens-empirical-alignment"' in text
    assert "apply_world_lens_diagnostic_alignment" in text
