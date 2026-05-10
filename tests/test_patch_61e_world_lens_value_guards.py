from pathlib import Path

import pandas as pd

from core.world_lens import selected_year_value_guard

ROOT = Path(__file__).resolve().parents[1]


def sample_grid() -> pd.DataFrame:
    rows = []
    # Deterministic 2024 selected-year fixture with a full 9k seat total.
    fixture = [
        ("India", "IND", 2024, 1609, "THRESHOLD", 0.421, 0.482, None, 0.5),
        ("China", "CHN", 2024, 1562, "ASYLUM", 0.301, 0.623, None, 0.5),
        ("United States", "USA", 2024, 377, "THRESHOLD", 0.602, 0.311, None, 0.5),
        ("Indonesia", "IDN", 2024, 314, "THRESHOLD", 0.488, 0.408, None, 0.5),
        ("Pakistan", "PAK", 2024, 279, "ASYLUM", 0.276, 0.631, None, 0.5),
        ("Nigeria", "NGA", 2024, 258, "ASYLUM", 0.312, 0.589, None, 0.5),
        ("Brazil", "BRA", 2024, 235, "THRESHOLD", 0.559, 0.337, None, 0.5),
        ("Netherlands", "NLD", 2024, 20, "SANCTUARY", 0.794, 0.121, None, 0.5),
    ]
    allocated_so_far = sum(r[3] for r in fixture)
    remainder = 9000 - allocated_so_far
    filler_count = 120
    base = remainder // filler_count
    extra = remainder % filler_count
    for country, iso3, year, seats, verdict, integrity, collapse, raw_trust, prior in fixture:
        rows.append(
            {
                "country": country,
                "iso3": iso3,
                "year": year,
                "seats_9k": seats,
                "aletheia_verdict": verdict,
                "aletheia_empirical_integrity": integrity,
                "aletheia_empirical_collapse_probability": collapse,
                "wvs_generalized_trust": raw_trust,
                "empirical_trust_prior": prior,
            }
        )
    for i in range(filler_count):
        rows.append(
            {
                "country": f"Filler {i:03d}",
                "iso3": f"X{i:02d}"[:3],
                "year": 2024,
                "seats_9k": base + (1 if i < extra else 0),
                "aletheia_verdict": "THRESHOLD",
                "aletheia_empirical_integrity": 0.45,
                "aletheia_empirical_collapse_probability": 0.44,
                "wvs_generalized_trust": None,
                "empirical_trust_prior": 0.5,
            }
        )
    # Add an older Netherlands row to prove the selected-year guard does not use stale rows.
    rows.append(
        {
            "country": "Netherlands",
            "iso3": "NLD",
            "year": 2023,
            "seats_9k": 21,
            "aletheia_verdict": "THRESHOLD",
            "aletheia_empirical_integrity": 0.111,
            "aletheia_empirical_collapse_probability": 0.777,
            "wvs_generalized_trust": 0.9,
            "empirical_trust_prior": 0.9,
        }
    )
    return pd.DataFrame(rows)


def test_selected_year_value_guard_locks_9000_seat_total_and_country_count():
    guard = selected_year_value_guard(sample_grid(), 2024, focus_iso3="NLD")
    assert guard["selected_year"] == 2024
    assert guard["total_seats"] == 9000
    assert guard["seat_total_ok"] is True
    assert guard["allocated_countries"] >= 100
    assert guard["full_selected_year_grid"] is True
    assert guard["no_stale_year_rows"] is True


def test_selected_year_value_guard_keeps_netherlands_2024_values_stable():
    focus = selected_year_value_guard(sample_grid(), 2024, focus_iso3="NLD")["focus"]
    assert focus["country"] == "Netherlands"
    assert focus["iso3"] == "NLD"
    assert focus["year"] == 2024
    assert focus["seats"] == 20
    assert focus["verdict"] == "SANCTUARY"
    assert round(focus["integrity"], 3) == 0.794
    assert round(focus["collapse_probability"], 3) == 0.121
    assert focus["raw_trust_label"] == "not available"
    assert focus["trust_prior_label"] == "0.500 neutral default"


def test_selected_year_value_guard_does_not_fallback_to_stale_year():
    guard = selected_year_value_guard(sample_grid(), 2023, focus_iso3="NLD")
    assert guard["selected_year"] == 2023
    assert guard["total_seats"] == 21
    assert guard["seat_total_ok"] is False
    assert guard["full_selected_year_grid"] is False
    assert guard["focus"]["year"] == 2023
    assert round(guard["focus"]["integrity"], 3) == 0.111


def test_patch_61e_docs_and_app_surface_value_guard():
    doc = (ROOT / "docs" / "world_lens_value_guards.md").read_text(encoding="utf-8")
    app = (ROOT / "app.py").read_text(encoding="utf-8")
    helper = (ROOT / "core" / "world_lens.py").read_text(encoding="utf-8")
    assert "selected-year rows are tied to the selected year only" in doc
    assert "World Lens value guard" in app
    assert "selected_year_value_guard" in helper
