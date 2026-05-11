
from pathlib import Path


def _app_text() -> str:
    return Path("app.py").read_text(encoding="utf-8")


def test_patch_71_5_boundary_cases_include_missing_safeguard_templates():
    app_text = _app_text()

    for title in [
        "Automated Triage Missing Safeguards",
        "Biometric Gate Without Fallback",
        "Question Prompt vs Risk State",
    ]:
        assert title in app_text

    assert "lacks explainability, independent challenge, and human override" in app_text
    assert "without a fallback path, public audit, or meaningful appeal" in app_text
    assert "QUESTION_PROMPT is an input/review-tool mode, not a fourth risk state" in app_text


def test_patch_71_5_boundary_cases_use_needs_safeguards_language():
    app_text = _app_text()

    assert "Missing explainability, independent challenge, or human override routes to THRESHOLD / Needs Safeguards, not Sanctuary." in app_text
    assert "Basic-rights access requires fallback, public audit, meaningful appeal, correction, and human review before it can approach Sanctuary." in app_text
    assert "Classify as Needs Safeguards; require explanation path, independent challenge, human override, appeal, correction, audit trail, and hardship review." in app_text
    assert "Classify as Needs Safeguards; add non-biometric fallback, public audit, meaningful appeal, human review, dignity-preserving correction, and emergency access." in app_text


def test_patch_71_5_consent_and_mechanism_scanners_reflect_new_safeguards():
    app_text = _app_text()

    for phrase in [
        "fallback/alternative path",
        "meaningful appeal",
        "human override",
        "explainability",
        "independent challenge",
        "Fallback path",
        "Needs Safeguards",
    ]:
        assert phrase in app_text

    assert "Recommended safeguard: Add human review, appeal, transparency, correction, evidence requirements, explainability, independent challenge, human override, fallback paths, and public audit where missing." in app_text
    assert "Recommended repair: Add concrete safeguards such as appeal, audit trail, time limits, correction, evidence requirements, explainability, independent challenge, human override, fallback, independent oversight, and human review." in app_text


def test_patch_71_5_local_witness_template_mentions_stress_test_boundary_context():
    app_text = _app_text()

    assert '"active_modules": "Mirror Check, Stress Test, Boundary Cases, Evidence Lab, Self-Audit Mode"' in app_text
    assert "Local Witness Receipt v2" in app_text
    assert "Authority claim: {receipt_example['authority_claim']}" in app_text
    assert "Human review required: {receipt_example['human_review_required']}" in app_text


def test_patch_71_5_manifest_recovery_and_progress_docs_present():
    for path in [
        "PATCH_71_5_MANIFEST.txt",
        "PATCH_71_5_RECOVERY_NOTE.md",
        "PATCH_STATUS.md",
        "docs/progress_database.md",
    ]:
        assert Path(path).exists(), path

    manifest = Path("PATCH_71_5_MANIFEST.txt").read_text(encoding="utf-8")
    assert "app.py" in manifest
    assert "tests/test_patch_71_5_boundary_cases_missing_safeguards_cleanup.py" in manifest

    status = Path("PATCH_STATUS.md").read_text(encoding="utf-8")
    progress = Path("docs/progress_database.md").read_text(encoding="utf-8")

    assert "Patch 71.5" in status
    assert "Patch 71.5" in progress
    assert "Boundary Cases Missing-Safeguard Cleanup" in status + progress
