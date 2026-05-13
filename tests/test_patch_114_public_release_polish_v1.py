from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def read(rel: str) -> str:
    return (ROOT / rel).read_text(encoding="utf-8")


def test_patch_114_files_exist():
    required = [
        "docs/public_release_polish_v1.md",
        "tests/test_patch_114_public_release_polish_v1.py",
        "PATCH_114_MANIFEST.txt",
        "PATCH_114_RECOVERY_NOTE.md",
    ]
    for rel in required:
        assert (ROOT / rel).exists(), rel


def test_public_release_polish_sets_public_entry_path_and_wording():
    doc = read("docs/public_release_polish_v1.md")
    required = [
        "**Patch:** 114",
        "Public entry path",
        "docs/BOUNDARY.md",
        "docs/privacy_boundary.md",
        "docs/hosting_limits.md",
        "docs/signal_detection.md",
        "docs/SIGNAL_DICTIONARY.md",
        "docs/beginner_ux.md",
        "docs/public_trust_package.md",
        "docs/public_review_checklist.md",
        "free, open-source governance mirror",
        "internal governance-risk readings and repair prompts",
        "not verdicts or certifications",
        "direct repository and documentation links",
        "local-first",
        "hosted deployments may have platform-level logs",
        "ALETHEIA surfaces signals. Humans keep the judgment.",
    ]
    for phrase in required:
        assert phrase in doc


def test_public_docs_point_to_release_polish_and_preserve_boundaries():
    combined = "\n".join(
        read(rel)
        for rel in [
            "README.md",
            "docs/public_release_notes.md",
            "docs/public_trust_package.md",
            "docs/patch_index.md",
            "docs/architecture.md",
            "examples/Trust_Package_README.md",
            "PATCH_STATUS.md",
            "docs/progress_database.md",
            "PATCH_114_MANIFEST.txt",
            "PATCH_114_RECOVERY_NOTE.md",
        ]
    ).lower()
    required = [
        "patch 114",
        "public release polish v1",
        "docs/public_release_polish_v1.md",
        "public entry path",
        "no app.py change",
        "no runtime behavior change",
        "no scoring",
        "no verdict-routing",
        "no signal-pattern",
        "no signal-weight",
        "no receipt schema",
        "no module-routing",
        "no external calls",
        "no live model calls",
        "no telemetry",
        "no analytics",
        "no central storage",
        "no global id sync",
        "no public ledger sync",
        "no privacy guarantee",
        "no certification",
        "no enforcement",
        "no final truth",
        "humans keep the judgment",
    ]
    for phrase in required:
        assert phrase in combined


def test_patch_114_no_accidental_internal_notes_or_placeholders():
    changed = "\n".join(
        read(rel)
        for rel in [
            "docs/public_release_polish_v1.md",
            "docs/public_release_notes.md",
            "docs/public_trust_package.md",
            "docs/patch_index.md",
            "PATCH_114_MANIFEST.txt",
            "PATCH_114_RECOVERY_NOTE.md",
        ]
    )
    forbidden = [
        "Ajustando",
        "afirmação",
        "Preciso",
        "Verwijderen",
        "overmatige",
        "placeholder",
        "TODO",
        "FIXME",
    ]
    for phrase in forbidden:
        assert phrase not in changed
