from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def read(rel: str) -> str:
    return (ROOT / rel).read_text(encoding="utf-8")


def test_patch_105_navigation_files_exist():
    required = [
        "docs/patch_index.md",
        "docs/public_trust_package.md",
        "examples/Trust_Package_README.md",
        "PATCH_105_MANIFEST.txt",
        "PATCH_105_RECOVERY_NOTE.md",
    ]
    for rel in required:
        assert (ROOT / rel).exists(), rel


def test_patch_105_patch_index_orients_without_certifying():
    text = read("docs/patch_index.md")
    required = [
        "Patch History",
        "mirror, not a throne",
        "Patch history is evidence for review, not proof of truth, safety, legality, ethics, privacy, security, or legitimacy",
        "Structural sequence after external review",
        "102",
        "103",
        "104",
        "105",
        "documentation, boundaries, privacy posture, and contributor navigation come before a larger `app.py` refactor",
        "Boundary and authority",
        "Privacy and hosted-use caveats",
        "Signal detection and review limits",
        "AI Integrity Mirror",
        "Patch-file naming convention",
        "ALETHEIA surfaces signals. Humans keep the judgment.",
    ]
    for phrase in required:
        assert phrase in text


def test_patch_105_public_trust_package_is_review_map_not_guarantee():
    text = "\n".join(
        read(rel)
        for rel in [
            "docs/public_trust_package.md",
            "examples/Trust_Package_README.md",
            "README.md",
            "CONTRIBUTING.md",
            "docs/architecture.md",
        ]
    )
    required = [
        "trust package, not a trust guarantee",
        "does not certify truth, safety, legality, ethics, privacy, security, or legitimacy",
        "docs/BOUNDARY.md",
        "docs/privacy_boundary.md",
        "docs/hosting_limits.md",
        "docs/signal_detection.md",
        "docs/architecture.md",
        "docs/patch_index.md",
        "PATCH_STATUS.md",
        "docs/progress_database.md",
        "local-first by design",
        "Hosted deployments may have platform-level logs outside ALETHEIA's application-code boundary",
        "review path, not a certification",
    ]
    for phrase in required:
        assert phrase in text


def test_patch_105_status_and_recovery_preserve_runtime_boundaries():
    text = "\n".join(
        read(rel)
        for rel in [
            "PATCH_105_MANIFEST.txt",
            "PATCH_105_RECOVERY_NOTE.md",
            "PATCH_STATUS.md",
            "docs/progress_database.md",
        ]
    ).lower()
    required = [
        "behavior changes:\n- none",
        "no runtime behavior change",
        "no scoring change",
        "no verdict-routing change",
        "no signal-pattern change",
        "no signal-weight change",
        "no receipt schema change",
        "no streamlit page wiring change",
        "no app.py refactor",
        "no external calls",
        "no live model calls",
        "no telemetry",
        "no analytics",
        "no backend upload endpoint",
        "no central storage",
        "no global id sync",
        "no public ledger sync",
        "no privacy guarantee",
        "no security guarantee",
        "no certification",
        "no enforcement",
        "no final truth claim",
        "human review remains required",
    ]
    for phrase in required:
        assert phrase in text


def test_patch_105_no_accidental_work_notes_or_placeholders():
    scan_files = [
        "docs/patch_index.md",
        "docs/public_trust_package.md",
        "examples/Trust_Package_README.md",
        "PATCH_105_MANIFEST.txt",
        "PATCH_105_RECOVERY_NOTE.md",
    ]
    forbidden_fragments = [
        "internal repair note",
        "temporary work note",
        "placeholder button",
        "TODO: patch later",
        "downloaded (placeholder)",
    ]
    text = "\n".join(read(rel) for rel in scan_files)
    for fragment in forbidden_fragments:
        assert fragment.lower() not in text.lower()
