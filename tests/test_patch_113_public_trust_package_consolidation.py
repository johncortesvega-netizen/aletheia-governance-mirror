from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def read(rel: str) -> str:
    return (ROOT / rel).read_text(encoding="utf-8")


def test_patch_113_files_exist():
    required = [
        "docs/public_trust_package.md",
        "docs/public_review_checklist.md",
        "docs/patch_index.md",
        "examples/Trust_Package_README.md",
        "tests/test_patch_113_public_trust_package_consolidation.py",
        "PATCH_113_MANIFEST.txt",
        "PATCH_113_RECOVERY_NOTE.md",
    ]
    for rel in required:
        assert (ROOT / rel).exists(), rel


def test_public_trust_package_is_central_map_and_not_certification():
    trust = read("docs/public_trust_package.md")
    required = [
        "Patch 113 — Public Trust Package Consolidation",
        "central review map",
        "mirror, not a throne",
        "What this package is not",
        "not a trust guarantee",
        "security audit",
        "privacy guarantee",
        "compliance approval",
        "ethics certification",
        "final truth",
        "Recommended review order",
        "Boundary and authority",
        "Privacy and hosted-use posture",
        "Signal detection and limits",
        "Architecture and maintainability",
        "Beginner path",
        "Patch history",
        "Public-review checklist",
        "docs/public_review_checklist.md",
        "docs/privacy_audit_panel_v1.md",
        "docs/beginner_ux.md",
        "ALETHEIA surfaces signals. Humans keep the judgment.",
    ]
    for phrase in required:
        assert phrase in trust


def test_public_review_checklist_covers_required_review_domains():
    checklist = read("docs/public_review_checklist.md")
    required = [
        "not a certification",
        "Boundary check",
        "Privacy and hosting check",
        "Signal-basis check",
        "Evidence and repair check",
        "Contributor and patch check",
        "Public trust check",
        "mirror, not throne",
        "human review",
        "privacy guarantee",
        "telemetry",
        "analytics",
        "central storage",
        "Global ID sync",
        "public ledger sync",
        "external model calls",
        "rule-based and heuristic limits",
        "English-first language-scope",
        "readings rather than verdicts or certifications",
        "more human review",
    ]
    for phrase in required:
        assert phrase in checklist


def test_patch_index_has_clean_structural_sequence_through_113():
    index = read("docs/patch_index.md")
    for patch in range(102, 114):
        assert f"| {patch} |" in index
    required = [
        "Public trust package consolidated and public review checklist added",
        "Documentation/navigation only",
        "docs/public_trust_package.md",
        "docs/public_review_checklist.md",
        "These organize review evidence. They do not create certification",
    ]
    for phrase in required:
        assert phrase in index


def test_readme_status_progress_and_architecture_record_patch_113_boundaries():
    combined = "\n".join(
        read(rel)
        for rel in [
            "README.md",
            "docs/architecture.md",
            "docs/patch_index.md",
            "docs/public_trust_package.md",
            "docs/public_review_checklist.md",
            "examples/Trust_Package_README.md",
            "PATCH_STATUS.md",
            "docs/progress_database.md",
            "PATCH_113_MANIFEST.txt",
            "PATCH_113_RECOVERY_NOTE.md",
        ]
    ).lower()
    required = [
        "patch 113",
        "public trust package consolidation",
        "documentation/navigation only",
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
        "no compliance approval",
        "no certification",
        "no enforcement",
        "no final truth",
        "humans keep the judgment",
    ]
    for phrase in required:
        assert phrase in combined


def test_patch_113_no_accidental_internal_notes_or_placeholders():
    changed = "\n".join(
        read(rel)
        for rel in [
            "docs/public_trust_package.md",
            "docs/public_review_checklist.md",
            "docs/patch_index.md",
            "examples/Trust_Package_README.md",
            "PATCH_113_MANIFEST.txt",
            "PATCH_113_RECOVERY_NOTE.md",
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
        "trust guarantee",
    ]
    # The exact phrase "not a trust guarantee" is allowed; positive claims are not.
    normalized = changed.replace("not a trust guarantee", "not-a-trust-guarantee")
    for phrase in forbidden:
        assert phrase not in normalized
