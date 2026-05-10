"""
ALETHEIA RECOVERY NOTE
Patch 14: Empirical Parity + Warning Guard

Purpose:
    Keep the packaged empirical module aligned with the root-level fallback and
    guard against pandas groupby.apply deprecation debt returning silently.

Rollback:
    Remove this test file and restore core/empirical.py from Patch 13.
"""

from pathlib import Path

import numpy as np
import pandas as pd

from core.empirical import score_empirical_frame


ROOT = Path(__file__).resolve().parents[1]


def test_empirical_module_has_no_groupby_apply_deprecation_pattern():
    source = (ROOT / "core" / "empirical.py").read_text(encoding="utf-8")
    assert ".groupby(" in source
    import re
    assert not re.search(r"\.groupby\([^\n]*\)(?:\s|\n)*\.apply\(", source)


def test_empirical_trust_prior_is_preserved_and_used_when_survey_trust_missing():
    df = pd.DataFrame(
        [
            {
                "country": "Trustland",
                "iso3": "TRL",
                "year": 2024,
                "population": 1_000_000,
                "wgi_voice_accountability": 0.70,
                "wgi_political_stability": 0.65,
                "wgi_government_effectiveness": 0.66,
                "wgi_regulatory_quality": 0.64,
                "wgi_rule_of_law": 0.67,
                "wgi_control_corruption": 0.63,
                "vdem_executive_constraints": 0.72,
                "vdem_democracy": 0.74,
                "wvs_generalized_trust": np.nan,
                "empirical_trust_prior": 0.81,
                "capital_scale": 0.40,
            }
        ]
    )

    scored = score_empirical_frame(df)

    assert "empirical_trust_prior" in scored.columns
    assert float(scored.loc[0, "empirical_trust_prior"]) == 0.81
    assert "trust prior" in scored.loc[0, "evidence_used"]


def test_scored_empirical_output_preserves_source_columns_for_review():
    df = pd.DataFrame(
        [
            {
                "country": "Review Republic",
                "iso3": "RVR",
                "year": 2024,
                "population": 2_000_000,
                "wgi_voice_accountability": 0.60,
                "wgi_political_stability": 0.55,
                "wgi_government_effectiveness": 0.58,
                "wgi_regulatory_quality": 0.57,
                "wgi_rule_of_law": 0.59,
                "wgi_control_corruption": 0.56,
                "vdem_executive_constraints": 0.61,
                "vdem_democracy": 0.62,
                "wvs_generalized_trust": 0.44,
                "capital_scale": 0.35,
                "conflict_events": 3,
                "regime_breakdown": 0,
            }
        ]
    )

    scored = score_empirical_frame(df)

    for column in [
        "wgi_voice_accountability",
        "wgi_political_stability",
        "vdem_democracy",
        "wvs_generalized_trust",
        "conflict_events",
        "regime_breakdown",
    ]:
        assert column in scored.columns
