from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def read(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8")


def test_patch_92_rubric_doc_exists_and_names_current_signal_categories():
    path = ROOT / "docs" / "ai_integrity_rubric.md"
    assert path.exists()
    text = path.read_text(encoding="utf-8")

    for phrase in [
        "# AI Integrity Mirror Rubric",
        "pasted artifacts",
        "governance-integrity signals",
        "Authority boundary",
        "Enforcement / appealability",
        "Certification overclaim",
        "Reviewability",
        "Transparency",
        "Coercion / manipulation",
        "Surveillance / identity capture",
        "Code / credential hygiene",
        "Code execution / data flow",
        "final_authority_claim",
        "automated_enforcement",
        "sovereign_or_certification_language",
        "missing_human_review",
        "opacity_or_hidden_logic",
        "manipulation_or_pressure",
        "surveillance_or_identity_capture",
        "secret_or_token_exposure",
        "unsafe_execution_or_network",
    ]:
        assert phrase in text


def test_patch_92_rubric_doc_preserves_non_certification_and_static_scope():
    text = read("docs/ai_integrity_rubric.md").lower()

    for phrase in [
        "does not test a live model",
        "does not measure moral purity",
        "not certification",
        "not external verification",
        "not public-ledger claims",
        "does not certify ai systems",
        "does not call live models",
        "does not store pasted artifacts centrally",
        "third-party hosting layers",
        "documentation only",
        "no scoring-math change",
        "no signal-pattern change",
        "no signal-weight change",
        "no verdict-routing change",
        "no receipt-generation change",
    ]:
        assert phrase in text


def test_patch_92_readme_and_ai_integrity_docs_link_to_rubric():
    readme = read("README.md")
    mirror_doc = read("docs/ai_integrity_mirror.md")

    assert "docs/ai_integrity_rubric.md" in readme
    assert "docs/ai_integrity_mirror.md" in readme
    assert "static, local-first review module" in readme
    assert "does not certify AI systems" in readme
    assert "Patch 92 rubric documentation" in mirror_doc
    assert "docs/ai_integrity_rubric.md" in mirror_doc
    assert "No scoring-math change" in mirror_doc
    assert "no live model benchmarking" in mirror_doc.lower()


def test_patch_92_ledgers_manifest_and_recovery_note_capture_boundary():
    for path in [
        "PATCH_STATUS.md",
        "docs/progress_database.md",
        "PATCH_92_MANIFEST.txt",
        "PATCH_92_RECOVERY_NOTE.md",
    ]:
        assert (ROOT / path).exists(), path

    combined = "\n".join(
        read(path)
        for path in [
            "PATCH_STATUS.md",
            "docs/progress_database.md",
            "PATCH_92_MANIFEST.txt",
            "PATCH_92_RECOVERY_NOTE.md",
        ]
    ).lower()

    for phrase in [
        "patch 92",
        "ai integrity rubric documentation",
        "docs/ai_integrity_rubric.md",
        "documentation only",
        "no scoring-math change",
        "no signal-pattern change",
        "no signal-weight change",
        "no verdict-routing change",
        "no live model benchmarking",
        "no external calls",
        "no repository crawler",
        "no public ledger sync",
        "no global id sync",
        "no enforcement",
        "no model certification",
        r"tools\run_patch_checks.bat 92",
    ]:
        assert phrase in combined
