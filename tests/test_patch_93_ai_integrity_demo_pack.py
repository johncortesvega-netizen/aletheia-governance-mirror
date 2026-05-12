from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DEMO_DIR = ROOT / "examples" / "ai_integrity"

DEMO_FILES = {
    "bounded_ai_answer.txt": [
        "bounded AI answer",
        "Human review is required",
        "uncertainty",
        "appeal",
    ],
    "authority_overclaim.txt": [
        "authority overclaim",
        "certified final authority",
        "official verdict",
        "no appeal route",
    ],
    "opaque_agent_workflow.txt": [
        "opaque agent workflow",
        "hidden criteria",
        "deny access automatically",
        "independent review",
    ],
    "code_secret_example.txt": [
        "code secret",
        "API_KEY",
        "eval(user_supplied_code)",
        "os.system",
    ],
    "central_identity_capture_claim.txt": [
        "central identity",
        "Global ID",
        "biometric",
        "central registry",
        "blacklist",
    ],
    "batch_demo_v1.txt": [
        "AI Integrity batch demo v1",
        "---",
        "certified final authority",
        "hidden proprietary criteria",
        "Global ID",
    ],
}


def read(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8")


def test_patch_93_demo_files_exist_and_cover_expected_artifact_types():
    assert DEMO_DIR.exists()
    for filename, phrases in DEMO_FILES.items():
        path = DEMO_DIR / filename
        assert path.exists(), filename
        text = path.read_text(encoding="utf-8")
        for phrase in phrases:
            assert phrase in text, f"{phrase!r} missing from {filename}"


def test_patch_93_batch_demo_is_separator_delimited_and_multi_artifact():
    text = (DEMO_DIR / "batch_demo_v1.txt").read_text(encoding="utf-8")
    delimiter_lines = [line for line in text.splitlines() if line.strip() in {"---", "===", "###"}]
    assert len(delimiter_lines) >= 4

    for phrase in [
        "bounded answer",
        "authority overclaim",
        "opaque agent workflow",
        "code-risk sample",
        "central identity capture claim",
    ]:
        assert phrase in text.lower()


def test_patch_93_demo_files_repeat_static_non_certification_boundary():
    combined = "\n".join(path.read_text(encoding="utf-8") for path in DEMO_DIR.glob("*.txt")).lower()

    for phrase in [
        "pasted artifact only",
        "not ai certification",
        "not model approval",
        "not a benchmark",
        "not proof of truth",
    ]:
        assert phrase in combined

    for forbidden_claim in [
        "certifies ai systems",
        "certifies models",
        "approved vendor",
        "safety guarantee is issued",
        "live model benchmark result",
    ]:
        assert forbidden_claim not in combined


def test_patch_93_docs_readme_ledgers_manifest_and_recovery_note_capture_scope():
    for path in [
        "docs/ai_integrity_demo_pack.md",
        "docs/ai_integrity_mirror.md",
        "README.md",
        "PATCH_STATUS.md",
        "docs/progress_database.md",
        "PATCH_93_MANIFEST.txt",
        "PATCH_93_RECOVERY_NOTE.md",
    ]:
        assert (ROOT / path).exists(), path

    combined = "\n".join(
        read(path)
        for path in [
            "docs/ai_integrity_demo_pack.md",
            "docs/ai_integrity_mirror.md",
            "README.md",
            "PATCH_STATUS.md",
            "docs/progress_database.md",
            "PATCH_93_MANIFEST.txt",
            "PATCH_93_RECOVERY_NOTE.md",
        ]
    ).lower()

    for phrase in [
        "patch 93",
        "ai integrity batch demo pack",
        "examples/ai_integrity/",
        "docs/ai_integrity_demo_pack.md",
        "bounded_ai_answer.txt",
        "authority_overclaim.txt",
        "opaque_agent_workflow.txt",
        "code_secret_example.txt",
        "central_identity_capture_claim.txt",
        "batch_demo_v1.txt",
        "examples/docs/tests only",
        "no analyzer scoring change",
        "no signal-pattern change",
        "no signal-weight change",
        "no verdict-routing change",
        "no ui behavior change",
        "no receipt-generation change",
        "no live model benchmarking",
        "no external calls",
        "no repository crawler",
        "no public ledger sync",
        "no global id sync",
        "no enforcement",
        "no model certification",
        r"tools\run_patch_checks.bat 93",
    ]:
        assert phrase in combined


def test_patch_93_does_not_wire_live_calls_or_new_runtime_behavior():
    patch_text = "\n".join(
        [
            read("docs/ai_integrity_demo_pack.md"),
            read("PATCH_93_MANIFEST.txt"),
            read("PATCH_93_RECOVERY_NOTE.md"),
        ]
        + [path.read_text(encoding="utf-8") for path in DEMO_DIR.glob("*.txt")]
    ).lower()

    forbidden_phrases = [
        "openai.chat.completions.create",
        "requests.post(",
        "urllib.request.urlopen",
        "streamlit tab",
        "score +=",
        "protocol_adjusted_state =",
    ]
    for phrase in forbidden_phrases:
        assert phrase not in patch_text
