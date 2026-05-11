from pathlib import Path


def app_text() -> str:
    return Path("app.py").read_text(encoding="utf-8")


def test_patch_72_13_year_selector_does_not_force_synced_year_every_rerun():
    text = app_text()

    assert "must not overwrite a user's manual year choice" in text
    assert "country_year_widget_key not in st.session_state and synced_evidence_year in country_years" in text
    assert "st.session_state[country_year_widget_key] = int(synced_evidence_year)" in text

    forbidden = (
        "if synced_evidence_year in country_years and "
        "st.session_state.get(country_year_widget_key) != int(synced_evidence_year):"
    )
    assert forbidden not in text


def test_patch_72_13_country_year_review_still_requires_explicit_run():
    text = app_text()

    assert "Run country-year review" in text
    assert "Press **Run country-year review** to update the cards and raw-row detail." in text
    assert "empirical_country_year_explorer_active_signature" in text
    assert "empirical_country_year_explorer_active_payload" in text


def test_patch_72_13_trust_prior_is_presented_as_derived_not_missing_source():
    text = app_text()

    assert "Trust prior (derived)" in text
    assert "`empirical_trust_prior` is a derived/scoring field" in text
    assert "Not an upload requirement; derived during scoring from raw trust or neutral fallback." in text
    assert "computed after scoring" in text
    assert "derived field active" in text
    assert "Trust prior is derived during scoring" in text


def test_patch_72_13_direct_upload_message_mentions_raw_trust_and_prior_derivation():
    text = app_text()

    assert "Raw trust is read from `wvs_generalized_trust` when available." in text
    assert "Trust prior is derived during scoring" in text
    assert "so it is not a required upload column." in text
    assert "If a true source column is present but has no usable values" in text


def test_patch_72_13_manifest_recovery_and_status_present():
    for path in [
        "PATCH_72_13_MANIFEST.txt",
        "PATCH_72_13_RECOVERY_NOTE.md",
        "PATCH_STATUS.md",
        "docs/progress_database.md",
    ]:
        assert Path(path).exists(), path

    manifest = Path("PATCH_72_13_MANIFEST.txt").read_text(encoding="utf-8")
    recovery = Path("PATCH_72_13_RECOVERY_NOTE.md").read_text(encoding="utf-8")
    status = Path("PATCH_STATUS.md").read_text(encoding="utf-8")
    progress = Path("docs/progress_database.md").read_text(encoding="utf-8")

    assert "Evidence Lab Year Selector and Trust Diagnostic Guard" in manifest
    assert r"tools\run_patch_checks.bat 72_13" in recovery
    assert "Patch 72.13" in status
    assert "Patch 72.13" in progress
    assert "Evidence Lab Year Selector" in status + progress
