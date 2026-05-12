from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

PROMPT_PACK = ROOT / "examples" / "ai_integrity" / "red_team_prompt_pack_v1.txt"
DOC = ROOT / "docs" / "ai_integrity_red_team_prompt_pack.md"


def read(path: str | Path) -> str:
    return Path(path).read_text(encoding="utf-8")


def test_patch_98_prompt_pack_exists_and_has_required_categories():
    text = read(PROMPT_PACK)

    required = [
        "AI Integrity Red Team Prompt Pack v1",
        "authority overreach",
        "legal false authority",
        "medical false authority",
        "political false authority",
        "manipulation pressure",
        "privacy extraction",
        "surveillance and capture",
        "false certainty",
        "no-appeal automation",
        "unsafe code request",
        "refusal quality",
        "bounded answer control",
    ]
    for phrase in required:
        assert phrase in text

    assert text.count("\n---\n") >= 10
    assert text.count("Prompt:") >= 10
    assert text.count("Review focus:") >= 10


def test_patch_98_prompt_pack_preserves_static_manual_boundary():
    combined = "\n".join(
        read(path)
        for path in [
            PROMPT_PACK,
            DOC,
            ROOT / "README.md",
            ROOT / "docs" / "ai_integrity_mirror.md",
            ROOT / "PATCH_STATUS.md",
            ROOT / "docs" / "progress_database.md",
            ROOT / "PATCH_98_MANIFEST.txt",
            ROOT / "PATCH_98_RECOVERY_NOTE.md",
        ]
    )

    for phrase in [
        "static",
        "manual",
        "does not run prompts",
        "No live model calls",
        "No external calls",
        "artifact-level review",
        "not model-wide certification",
        "not a vendor ranking",
        "not a final truth claim",
    ]:
        assert phrase in combined


def test_patch_98_docs_and_status_are_wired():
    combined = "\n".join(
        read(path)
        for path in [
            DOC,
            ROOT / "README.md",
            ROOT / "docs" / "ai_integrity_mirror.md",
            ROOT / "PATCH_STATUS.md",
            ROOT / "docs" / "progress_database.md",
            ROOT / "PATCH_98_MANIFEST.txt",
            ROOT / "PATCH_98_RECOVERY_NOTE.md",
        ]
    )

    for phrase in [
        "Patch 98",
        "AI Integrity Red Team Prompt Pack",
        "examples/ai_integrity/red_team_prompt_pack_v1.txt",
        "authority overreach",
        "privacy extraction",
        "unsafe code request",
        "refusal quality",
        "tools\\run_patch_checks.bat 98",
    ]:
        assert phrase in combined


def test_patch_98_does_not_introduce_certification_or_live_call_claims():
    patched_text = "\n".join(
        read(path)
        for path in [
            PROMPT_PACK,
            DOC,
            ROOT / "README.md",
            ROOT / "docs" / "ai_integrity_mirror.md",
            ROOT / "PATCH_STATUS.md",
            ROOT / "docs" / "progress_database.md",
            ROOT / "PATCH_98_MANIFEST.txt",
            ROOT / "PATCH_98_RECOVERY_NOTE.md",
        ]
    ).lower()

    forbidden_claims = [
        "certifies models",
        "certifies prompts",
        "certifies vendors",
        "guarantees model safety",
        "proves model safety",
        "guarantees privacy",
        "approved by aletheia",
        "will call live models",
        "calls live models",
        "benchmarks live models automatically",
        "ranks vendors",
    ]
    for phrase in forbidden_claims:
        assert phrase not in patched_text
