from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def read(rel: str) -> str:
    return (ROOT / rel).read_text(encoding="utf-8")


def test_patch_104_boundary_privacy_files_exist():
    required = [
        "docs/BOUNDARY.md",
        "docs/hosting_limits.md",
        "core/boundary.py",
        "core/privacy_panel.py",
        "PATCH_104_MANIFEST.txt",
        "PATCH_104_RECOVERY_NOTE.md",
    ]
    for rel in required:
        assert (ROOT / rel).exists(), rel


def test_patch_104_boundary_language_is_non_authoritative_and_bounded():
    text = "\n".join(
        read(rel)
        for rel in [
            "docs/BOUNDARY.md",
            "README.md",
            "CONTRIBUTING.md",
            "docs/architecture.md",
            "PATCH_STATUS.md",
            "docs/progress_database.md",
        ]
    )

    required_phrases = [
        "mirror, not a throne",
        "ALETHEIA surfaces signals. Humans keep the judgment.",
        "does not certify truth, safety, legality, ethics, privacy, security, or legitimacy",
        "internal governance-risk readings",
        "not verdicts or certifications",
        "Human judgment required",
        "No authority",
    ]
    for phrase in required_phrases:
        assert phrase in text

    forbidden_phrases = [
        "ALETHEIA guarantees privacy",
        "certified private",
        "certified secure",
        "ALETHEIA is a final truth system",
        "ALETHEIA provides automated approval",
    ]
    for phrase in forbidden_phrases:
        assert phrase.lower() not in text.lower()


def test_patch_104_local_first_hosted_caveat_is_precise():
    text = "\n".join(
        read(rel)
        for rel in [
            "docs/BOUNDARY.md",
            "docs/privacy_boundary.md",
            "docs/hosting_limits.md",
            "README.md",
            "CONTRIBUTING.md",
        ]
    )

    required_phrases = [
        "local-first by design",
        "For sensitive audits, run ALETHEIA locally",
        "hosted deployments may have platform-level logs",
        "outside ALETHEIA's application code",
        "no built-in telemetry",
        "analytics SDKs",
        "trackers",
        "backend upload endpoint",
        "public ledger sync",
        "Global ID sync",
        "central user-input storage",
        "not a privacy guarantee",
    ]
    for phrase in required_phrases:
        assert phrase in text

    overclaims = [
        "All processing happens locally in your browser/session",
        "Local processing only",
    ]
    lower = text.lower()
    for phrase in overclaims:
        assert phrase.lower() not in lower


def test_patch_104_helper_modules_are_importable_and_safe():
    from core.boundary import get_boundary_text
    from core.privacy_panel import get_privacy_panel_text

    footer = get_boundary_text("footer")
    compact = get_boundary_text("compact")
    full = get_boundary_text("full", root=ROOT)
    privacy = get_privacy_panel_text()

    assert "Mirror, not throne" in footer
    assert "Human judgment required" in compact
    assert "hosted use has platform limits" in compact
    assert "ALETHEIA — Boundary Statements" in full
    assert "Hosted deployments" in full
    assert "local-first by design" in privacy
    assert "No external AI/model calls" in privacy
    assert "platform-level logs" in privacy


def test_patch_104_manifest_and_recovery_are_behavior_preserving():
    text = "\n".join(
        read(rel)
        for rel in [
            "PATCH_104_MANIFEST.txt",
            "PATCH_104_RECOVERY_NOTE.md",
            "PATCH_STATUS.md",
            "docs/progress_database.md",
        ]
    ).lower()

    required_phrases = [
        "behavior changes:\n- none",
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
    ]
    for phrase in required_phrases:
        assert phrase in text
