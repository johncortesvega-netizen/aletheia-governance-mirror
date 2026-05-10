from pathlib import Path

from protocol import (
    apply_guardrail_verdict,
    calibrate_threshold_safeguard_metrics,
    ensure_threshold_repair_questions,
    stress_label_for_phrase,
)


DUTCH_GAP_CASES = [
    "Een DAO geeft de meeste stemmacht aan vroege tokenhouders en heeft geen proces voor benadeelde gebruikers om beslissingen aan te vechten.",
    "Een rampenbestrijdingscomité kan de normale wet omzeilen tijdens noodsituaties, maar publiceert geen audit-trail.",
    "Een hervormingsbeweging wint de macht en verwijdert onmiddellijk termijnlimieten om stabiliteit te bewaren.",
    "Een humanitair hulpsysteem geeft prioriteit aan efficiëntie boven het beroepsrecht van afgewezen aanvragers.",
    "Een leider komt aan de macht na een revolutie en belooft herstel, maar er bestaat geen onafhankelijke audit-trail.",
]


def _base_sim():
    return {
        "stability": 0.96,
        "trust_index": 1.0,
        "alignment": 1.0,
        "ego": 0.0,
        "ego_pressure": 0.0,
        "Ep": 0.0,
    }


def test_patch_67_2_dutch_gap_cases_route_to_threshold():
    for text in DUTCH_GAP_CASES:
        label, needs_review, reason = stress_label_for_phrase(text)
        verdict, risk = apply_guardrail_verdict("SANCTUARY", label, needs_review)
        assert verdict == "THRESHOLD", (text, label, reason)
        assert risk == "Medium"
        assert "Needs Safeguards" in label
        assert needs_review == "YES"


def test_patch_67_2_threshold_receipts_keep_repair_and_metric_softening():
    text = DUTCH_GAP_CASES[0]
    label, needs_review, _reason = stress_label_for_phrase(text)
    verdict, risk = apply_guardrail_verdict("SANCTUARY", label, needs_review)
    assert verdict == "THRESHOLD"

    calibrated = calibrate_threshold_safeguard_metrics(
        _base_sim(), text=text, verdict=verdict, risk=risk, protocol_label=label
    )
    assert calibrated["threshold_metric_calibration"]["applied"] is True
    assert calibrated["trust_index"] <= 0.92
    assert calibrated["alignment"] <= 0.92
    assert calibrated["ego"] >= 0.05

    report = ensure_threshold_repair_questions(
        {"repair_questions": []}, verdict=verdict, risk=risk, protocol_label=label
    )
    assert len(report["repair_questions"]) >= 5


def test_patch_67_2_app_wide_language_scope_is_visible():
    app_text = Path("app.py").read_text(encoding="utf-8")
    about_text = Path("about_page.py").read_text(encoding="utf-8")
    combined = app_text + "\n" + about_text
    assert "SUPPORTED_INPUT_LANGUAGE_NOTE" in app_text
    assert "English + Nederlands/Dutch input supported" in app_text
    assert "Input language scope" in app_text
    assert "English and Nederlands/Dutch" in combined
    assert "risk lexicon" in combined or "risk lexicons" in combined


def test_patch_67_2_docs_and_manifest_exist():
    assert Path("docs/stress_test_dutch_gap_fix.md").exists()
    assert Path("PATCH_67_2_MANIFEST.txt").exists()
    assert Path("PATCH_67_2_RECOVERY_NOTE.md").exists()
    manifest = Path("PATCH_67_2_MANIFEST.txt").read_text(encoding="utf-8")
    assert "protocol.py" in manifest
    assert "app.py" in manifest
    assert "about_page.py" in manifest
