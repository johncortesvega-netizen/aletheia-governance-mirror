from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

BATCH_FILES = [
    ROOT / "examples" / "batch_questions" / "set_01_plain_language.txt",
    ROOT / "examples" / "batch_questions" / "set_02_boundary_cases.txt",
    ROOT / "examples" / "batch_questions" / "set_03_world_lens_release.txt",
]


def _questions(path: Path) -> list[str]:
    return [line.strip() for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def test_patch_64_batch_question_files_exist_and_have_50_questions_each():
    for path in BATCH_FILES:
        assert path.exists(), f"missing batch baseline: {path}"
        questions = _questions(path)
        assert len(questions) == 50, f"{path.name} should have exactly 50 questions"
        assert questions[0].startswith("01. ")
        assert questions[-1].startswith("50. ")


def test_patch_64_question_numbering_is_sequential():
    for path in BATCH_FILES:
        questions = _questions(path)
        for idx, question in enumerate(questions, start=1):
            assert question.startswith(f"{idx:02d}. "), f"bad numbering in {path.name}: {question}"


def test_patch_64_docs_record_question_prompt_contract_and_authority_boundary():
    doc = (ROOT / "docs" / "mirror_check_batch_baselines.md").read_text(encoding="utf-8")
    required_terms = [
        "QUESTION_PROMPT",
        "Audit Question / Review Tool",
        "Scenario hash mismatches: 0",
        "Authority claim: False",
        "Public ledger: False",
        "Global ID sync: False",
        "Central storage: False",
        "Human review required: True",
        "normal governance scoring should not be forced",
    ]
    for term in required_terms:
        assert term in doc


def test_patch_64_release_surface_references_batch_baselines():
    readme = (ROOT / "README.md").read_text(encoding="utf-8")
    about = (ROOT / "about_page.py").read_text(encoding="utf-8")
    status = (ROOT / "PATCH_STATUS.md").read_text(encoding="utf-8")
    progress = (ROOT / "docs" / "progress_database.md").read_text(encoding="utf-8")

    for text in (readme, about, status, progress):
        assert "Patch 64" in text
        assert "Mirror Check Batch" in text or "Mirror Check batch" in text

    assert "docs/mirror_check_batch_baselines.md" in readme
    assert "examples/batch_questions" in readme
