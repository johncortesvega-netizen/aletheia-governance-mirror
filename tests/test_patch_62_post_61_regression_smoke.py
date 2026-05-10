from pathlib import Path

import pandas as pd

from protocol import (
    calibrate_malicious_leadership_metrics,
    ensure_asylum_repair_questions,
)
from core.world_lens import (
    country_available_years,
    country_year_status_message,
    format_raw_trust_label,
    format_trust_prior_label,
    selected_year_value_guard,
    trust_coverage_label,
)

ROOT = Path(__file__).resolve().parents[1]


def _clean_sim():
    return {
        "stability": 0.95,
        "trust_index": 1.0,
        "alignment": 1.0,
        "ego": 0.0079,
        "ego_pressure": 0.0,
        "Ep": 0.0,
        "trust_trace": [1.0, 1.0],
        "alignment_trace": [1.0, 1.0],
        "ego_trace": [0.0, 0.01],
    }


def _world_lens_fixture():
    rows = [
        {
            "country": "Netherlands",
            "iso3": "NLD",
            "year": 2024,
            "seats_9k": 20,
            "aletheia_verdict": "SANCTUARY",
            "aletheia_empirical_integrity": 0.794,
            "aletheia_empirical_collapse_probability": 0.121,
            "wvs_generalized_trust": None,
            "empirical_trust_prior": 0.5,
            "empirical_identity_valid": True,
        },
        {
            "country": "Netherlands",
            "iso3": "NLD",
            "year": 2020,
            "seats_9k": 19,
            "aletheia_verdict": "THRESHOLD",
            "aletheia_empirical_integrity": 0.500,
            "aletheia_empirical_collapse_probability": 0.300,
            "wvs_generalized_trust": 0.72,
            "empirical_trust_prior": 0.72,
            "empirical_identity_valid": True,
        },
        {
            "country": "France",
            "iso3": "FRA",
            "year": 2023,
            "seats_9k": 10,
            "aletheia_verdict": "THRESHOLD",
            "aletheia_empirical_integrity": 0.540,
            "aletheia_empirical_collapse_probability": 0.260,
            "wvs_generalized_trust": None,
            "empirical_trust_prior": 0.5,
            "empirical_identity_valid": True,
        },
    ]
    # Add enough selected-year filler rows to make a complete 9k grid while keeping Netherlands 2024 stable.
    remaining = 9000 - 20
    filler_count = 120
    base = remaining // filler_count
    extra = remaining % filler_count
    for idx in range(filler_count):
        rows.append(
            {
                "country": f"Filler {idx:03d}",
                "iso3": f"X{idx:02d}"[:3],
                "year": 2024,
                "seats_9k": base + (1 if idx < extra else 0),
                "aletheia_verdict": "THRESHOLD",
                "aletheia_empirical_integrity": 0.45,
                "aletheia_empirical_collapse_probability": 0.44,
                "wvs_generalized_trust": None,
                "empirical_trust_prior": 0.5,
                "empirical_identity_valid": True,
            }
        )
    return pd.DataFrame(rows)


def test_patch_62_simulation_regression_keeps_asylum_repair_and_metric_calibration():
    report = ensure_asylum_repair_questions(
        {"integrity": 0.8452, "repair_questions": []},
        verdict="ASYLUM",
        risk="High",
        protocol_label="Malicious Leadership / Asylum",
        scan={"power_concentration": 0.88},
    )
    joined = "\n".join(report["repair_questions"]).lower()
    assert "appeal" in joined
    assert "basic rights" in joined
    assert "human review" in joined or "independent reviewer" in joined
    assert "non-coercive" in joined

    calibrated = calibrate_malicious_leadership_metrics(
        _clean_sim(),
        text="evil penguin becomes world leader after a revolution",
        protocol_label="Malicious Leadership / Asylum",
        scan={"power_concentration": 0.88},
    )
    assert calibrated["malicious_leadership_metric_calibration"]["applied"] is True
    assert calibrated["trust_index"] <= 0.65
    assert calibrated["alignment"] <= 0.70
    assert calibrated["ego"] >= 0.20


def test_patch_62_world_lens_regression_keeps_country_year_and_trust_guards():
    df = _world_lens_fixture()
    assert country_available_years(df, "NLD") == [2024, 2020]
    assert country_available_years(df, "FRA") == [2023]
    assert 2023 not in country_available_years(df, "NLD")
    assert "Available years for Netherlands · NLD" in country_year_status_message("Netherlands", "NLD", [2024, 2020])

    assert format_raw_trust_label(None) == "not available"
    assert format_trust_prior_label(0.5) == "0.500 neutral default"
    raw_label, prior_label, note = trust_coverage_label(0.0, 1.0)
    assert raw_label == "0.0%"
    assert prior_label == "100.0%"
    assert "not observed survey trust coverage" in note


def test_patch_62_selected_year_value_guard_keeps_netherlands_2024_stable():
    guard = selected_year_value_guard(_world_lens_fixture(), 2024, focus_iso3="NLD")
    assert guard["selected_year"] == 2024
    assert guard["total_seats"] == 9000
    assert guard["seat_total_ok"] is True
    assert guard["full_selected_year_grid"] is True
    assert guard["no_stale_year_rows"] is True

    focus = guard["focus"]
    assert focus["country"] == "Netherlands"
    assert focus["iso3"] == "NLD"
    assert focus["year"] == 2024
    assert focus["seats"] == 20
    assert focus["verdict"] == "SANCTUARY"
    assert round(focus["integrity"], 3) == 0.794
    assert round(focus["collapse_probability"], 3) == 0.121
    assert focus["raw_trust_label"] == "not available"
    assert focus["trust_prior_label"] == "0.500 neutral default"


def test_patch_62_docs_and_status_record_post_61_regression_boundary():
    doc = (ROOT / "docs" / "post_61_regression_smoke.md").read_text(encoding="utf-8")
    status = (ROOT / "PATCH_STATUS.md").read_text(encoding="utf-8")
    progress = (ROOT / "docs" / "progress_database.md").read_text(encoding="utf-8")
    assert "Post-61 Regression Smoke Test" in doc
    assert "no Global ID sync" in doc
    assert "no enforcement" in doc
    assert "Patch 62" in status
    assert "Patch 62" in progress
