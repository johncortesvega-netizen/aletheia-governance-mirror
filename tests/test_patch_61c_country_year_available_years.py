from pathlib import Path

import pandas as pd

from core.world_lens import (
    country_available_years,
    country_year_status_message,
    safe_country_year_index,
)

ROOT = Path(__file__).resolve().parents[1]


def test_country_available_years_are_scoped_to_selected_country_only():
    df = pd.DataFrame(
        [
            {"country": "Netherlands", "iso3": "NLD", "year": 2024, "empirical_identity_valid": True},
            {"country": "Netherlands", "iso3": "NLD", "year": 2020, "empirical_identity_valid": True},
            {"country": "Netherlands", "iso3": "NLD", "year": 1996, "empirical_identity_valid": True},
            {"country": "France", "iso3": "FRA", "year": 2023, "empirical_identity_valid": True},
            {"country": "France", "iso3": "FRA", "year": 2001, "empirical_identity_valid": True},
        ]
    )
    assert country_available_years(df, "NLD") == [2024, 2020, 1996]
    assert country_available_years(df, "FRA") == [2023, 2001]
    assert 2023 not in country_available_years(df, "NLD")


def test_invalid_or_missing_country_years_do_not_fallback_to_global_range():
    df = pd.DataFrame(
        [
            {"country": "Netherlands", "iso3": "NLD", "year": 2024, "empirical_identity_valid": False},
            {"country": "France", "iso3": "FRA", "year": 2023, "empirical_identity_valid": True},
        ]
    )
    assert country_available_years(df, "NLD") == []
    assert country_available_years(df, "MISSING") == []


def test_country_year_status_message_is_country_specific():
    msg = country_year_status_message("Netherlands", "NLD", [2024, 2023, 2022])
    assert "Available years for Netherlands · NLD" in msg
    assert "2022–2024" in msg
    gap_msg = country_year_status_message("Example", "EXM", [2024, 2020, 1996])
    assert "2024, 2020, 1996" in gap_msg
    empty_msg = country_year_status_message("NoData", "NOD", [])
    assert "No available country-year data" in empty_msg


def test_app_and_docs_expose_no_silent_fallback_boundary():
    app_text = (ROOT / "app.py").read_text(encoding="utf-8")
    doc_text = (ROOT / "docs" / "country_year_explorer.md").read_text(encoding="utf-8")
    assert "country_available_years" in app_text
    assert "safe_country_year_index" in app_text
    assert "does not silently fall back to a global/default year" in app_text
    assert "No silent fallback" in doc_text
    assert safe_country_year_index(2020, [2024, 2020]) == 1
    assert safe_country_year_index(1999, [2024, 2020]) == 0
