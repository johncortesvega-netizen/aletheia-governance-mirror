from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]

QUESTION_BANKS = {
    "examples/batch_questions/repair_questions_v2_nl.txt": "NL",
    "examples/batch_questions/formal_doctrine_repair_questions_nl.txt": "NL",
    "examples/batch_questions/plain_language_questions_nl.txt": "NL",
    "examples/batch_questions/boundary_case_questions_nl.txt": "NL",
    "examples/batch_questions/world_lens_release_questions_nl.txt": "NL",
}

SCENARIO_BATCHES = {
    "examples/batch_scenarios/stress_test_scenarios_en_v1.txt": {
        "language": "EN",
        "distribution": "THRESHOLD 46 / ASYLUM 4 / SANCTUARY 0",
    },
    "examples/batch_scenarios/stress_test_scenarios_nl_v1.txt": {
        "language": "NL",
        "distribution": "THRESHOLD 50 / ASYLUM 0 / SANCTUARY 0",
    },
    "examples/batch_scenarios/governance_language_stress_test_en.txt": {
        "language": "EN",
        "distribution": "THRESHOLD 29 / ASYLUM 21 / SANCTUARY 0",
    },
}

LEGACY_TO_OFFICIAL = {
    "examples/batch_questions/set_01_plain_language.txt": "examples/batch_questions/plain_language_questions_nl.txt",
    "examples/batch_questions/set_02_boundary_cases.txt": "examples/batch_questions/boundary_case_questions_nl.txt",
    "examples/batch_questions/set_03_world_lens_release.txt": "examples/batch_questions/world_lens_release_questions_nl.txt",
    "examples/batch_scenarios/stress_test_scenarios_v1.txt": "examples/batch_scenarios/stress_test_scenarios_en_v1.txt",
    "examples/batch_scenarios/stress_test_advanced_en_v1.txt": "examples/batch_scenarios/governance_language_stress_test_en.txt",
}


def _numbered_nonempty_lines(path: Path) -> list[str]:
    lines = [line.strip() for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]
    return lines


def _assert_numbered_50_line_file(relative_path: str) -> None:
    path = ROOT / relative_path
    assert path.exists(), f"Missing official batch file: {relative_path}"
    lines = _numbered_nonempty_lines(path)
    assert len(lines) == 50, f"{relative_path} should contain exactly 50 non-empty lines"
    for index, line in enumerate(lines, start=1):
        assert line.startswith(f"{index:02d}. "), f"{relative_path} line {index} is not numbered correctly"


def test_patch_71_official_question_banks_exist_and_have_50_numbered_questions():
    for relative_path in QUESTION_BANKS:
        _assert_numbered_50_line_file(relative_path)


def test_patch_71_official_scenario_batches_exist_and_have_50_numbered_scenarios():
    for relative_path in SCENARIO_BATCHES:
        _assert_numbered_50_line_file(relative_path)


def test_patch_71_catalog_registers_all_official_files_and_expected_modes():
    catalog = (ROOT / "docs" / "batch_file_catalog.md").read_text(encoding="utf-8")
    assert "QUESTION_PROMPT" in catalog
    assert "Audit Question / Review Tool" in catalog
    assert "Simulation / Stress Test" in catalog
    assert "no authority claim" in catalog.lower()
    assert "no public ledger" in catalog.lower()
    assert "no Global ID sync" in catalog
    assert "no central storage" in catalog.lower()

    for relative_path, language in QUESTION_BANKS.items():
        assert relative_path in catalog
        assert f"| `{relative_path}` | {language} | 50 |" in catalog
        assert "50 `QUESTION_PROMPT`; metrics suppressed" in catalog

    for relative_path, metadata in SCENARIO_BATCHES.items():
        assert relative_path in catalog
        assert metadata["distribution"] in catalog
        assert f"| `{relative_path}` | {metadata['language']} | 50 |" in catalog


def test_patch_71_legacy_aliases_are_mapped_but_not_used_as_public_primary_refs():
    catalog = (ROOT / "docs" / "batch_file_catalog.md").read_text(encoding="utf-8")
    for legacy, official in LEGACY_TO_OFFICIAL.items():
        assert legacy in catalog
        assert official in catalog

    public_text = "\n".join(
        [
            (ROOT / "README.md").read_text(encoding="utf-8"),
            (ROOT / "about_page.py").read_text(encoding="utf-8"),
        ]
    )
    for legacy in LEGACY_TO_OFFICIAL:
        assert legacy not in public_text
    for official in list(QUESTION_BANKS) + list(SCENARIO_BATCHES):
        assert official in public_text or Path(official).name in public_text


def test_patch_71_manifest_recovery_status_and_progress_are_present():
    assert (ROOT / "PATCH_71_MANIFEST.txt").exists()
    assert (ROOT / "PATCH_71_RECOVERY_NOTE.md").exists()
    assert "Patch 71" in (ROOT / "PATCH_STATUS.md").read_text(encoding="utf-8")
    assert "Patch 71" in (ROOT / "docs" / "progress_database.md").read_text(encoding="utf-8")
    assert "docs/batch_file_catalog.md" in (ROOT / "PATCH_71_MANIFEST.txt").read_text(encoding="utf-8")
