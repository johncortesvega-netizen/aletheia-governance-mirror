import pandas as pd

from core.empirical import (
    prepare_empirical_frame,
    public_upload_diagnostics,
    build_master_from_public_uploads,
)


def _trust_df():
    return pd.DataFrame(
        {
            "Entity": ["Albania", "Albania", "Netherlands", "Northern Ireland"],
            "Code": ["ALB", "ALB", "NLD", ""],
            "Year": [1998, 2004, 2022, 2022],
            "Trust in others": [24.3, 23.2, 66.7, 40.0],
            "Trust in others (Annotations)": ["", "", "", "missing iso3"],
        }
    )


def _population_df():
    return pd.DataFrame(
        {
            "country": ["Albania", "Netherlands"],
            "iso3": ["ALB", "NLD"],
            "year": [2024, 2024],
            "population": [2700000, 18000000],
        }
    )


def test_patch_72_10_maps_owid_self_reported_trust_columns():
    prepared = prepare_empirical_frame(_trust_df())

    assert {"country", "iso3", "year", "wvs_generalized_trust"}.issubset(prepared.columns)
    assert prepared.loc[0, "country"] == "Albania"
    assert prepared.loc[0, "iso3"] == "ALB"
    assert int(prepared.loc[0, "year"]) == 1998
    assert abs(float(prepared.loc[0, "wvs_generalized_trust"]) - 0.243) < 0.000001
    assert abs(float(prepared.loc[2, "wvs_generalized_trust"]) - 0.667) < 0.000001
    assert "_aletheia_trust_upload_note" in prepared.columns
    assert "trust_in_others" in prepared["_aletheia_trust_upload_note"].dropna().iloc[0]
    assert "0-100 normalized to 0-1" in prepared["_aletheia_trust_upload_note"].dropna().iloc[0]


def test_patch_72_10_preserves_already_normalized_trust_values():
    df = pd.DataFrame(
        {
            "country": ["A"],
            "iso3": ["AAA"],
            "year": [2020],
            "Trust in others": [0.42],
        }
    )
    prepared = prepare_empirical_frame(df)

    assert abs(float(prepared.loc[0, "wvs_generalized_trust"]) - 0.42) < 0.000001
    assert "0-1 preserved" in prepared["_aletheia_trust_upload_note"].dropna().iloc[0]


def test_patch_72_10_public_upload_diagnostics_reports_trust_transform():
    diagnostics = public_upload_diagnostics(trust_df=_trust_df())

    trust_row = diagnostics.loc[diagnostics["upload"] == "Trust/ALETHEIA"].iloc[0]
    assert int(trust_row["rows_with_signal"]) == 4
    assert "trust_in_others -> wvs_generalized_trust" in str(trust_row["transform_note"])
    assert "0-100 normalized to 0-1" in str(trust_row["transform_note"])


def test_patch_72_10_master_builder_merges_auto_normalized_trust():
    master = build_master_from_public_uploads(population_df=_population_df(), trust_df=_trust_df())

    assert "wvs_generalized_trust" in master.columns
    alb = master[(master["iso3"] == "ALB") & (master["year"] == 1998)]
    nld = master[(master["iso3"] == "NLD") & (master["year"] == 2022)]
    assert not alb.empty
    assert not nld.empty
    assert abs(float(alb.iloc[0]["wvs_generalized_trust"]) - 0.243) < 0.000001
    assert abs(float(nld.iloc[0]["wvs_generalized_trust"]) - 0.667) < 0.000001


def test_patch_72_10_fallback_module_has_same_normalizer():
    import core_empirical

    prepared = core_empirical.prepare_empirical_frame(_trust_df())
    assert abs(float(prepared.loc[0, "wvs_generalized_trust"]) - 0.243) < 0.000001
    assert "_aletheia_trust_upload_note" in prepared.columns


def test_patch_72_10_manifest_recovery_and_status_present():
    from pathlib import Path

    for path in [
        "PATCH_72_10_MANIFEST.txt",
        "PATCH_72_10_RECOVERY_NOTE.md",
        "PATCH_STATUS.md",
        "docs/progress_database.md",
    ]:
        assert Path(path).exists(), path

    manifest = Path("PATCH_72_10_MANIFEST.txt").read_text(encoding="utf-8")
    recovery = Path("PATCH_72_10_RECOVERY_NOTE.md").read_text(encoding="utf-8")
    status = Path("PATCH_STATUS.md").read_text(encoding="utf-8")
    progress = Path("docs/progress_database.md").read_text(encoding="utf-8")

    assert "Trust Upload Auto-Normalizer" in manifest
    assert "tools\\run_patch_checks.bat 72_10" in recovery
    assert "Patch 72.10" in status
    assert "Patch 72.10" in progress
    assert "Trust Upload Auto-Normalizer" in status + progress
