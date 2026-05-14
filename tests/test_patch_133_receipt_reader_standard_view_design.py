from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def read(rel: str) -> str:
    return (ROOT / rel).read_text(encoding="utf-8")


def test_patch_133_files_exist():
    required = [
        "docs/receipt_reader_standard_view.md",
        "tests/test_patch_133_receipt_reader_standard_view_design.py",
        "PATCH_133_MANIFEST.txt",
        "PATCH_133_RECOVERY_NOTE.md",
    ]
    for rel in required:
        assert (ROOT / rel).exists(), rel


def test_receipt_reader_design_defines_native_first_standard_second():
    doc = read("docs/receipt_reader_standard_view.md")
    required = [
        "Receipt Reader - Standard View",
        "Native receipt values are the source of truth",
        "native values first and standard review bands second",
        "Standard View is an interpretation and interoperability layer only",
        "SANCTUARY",
        "THRESHOLD",
        "ASYLUM",
        "QUESTION_PROMPT",
        "QUESTION_PROMPT | Not scored / review-tool mode",
    ]
    for phrase in required:
        assert phrase in doc


def test_receipt_reader_design_mapping_is_interoperability_not_certification():
    doc = read("docs/receipt_reader_standard_view.md")
    required = [
        "SANCTUARY | Low review pressure",
        "THRESHOLD | Elevated review pressure",
        "ASYLUM | High review pressure / escalation review required",
        "This mapping is for interoperability, not certification.",
        "Human review remains required.",
    ]
    for phrase in required:
        assert phrase in doc


def test_receipt_reader_design_has_hard_boundaries_and_limits():
    doc = read("docs/receipt_reader_standard_view.md").lower()
    required = [
        "does not rescore",
        "must not infer values",
        "must not guess",
        "must not modify receipt schema",
        "no scoring",
        "receipt schema",
        "external-call",
        "telemetry",
        "storage",
        "certification",
        "enforcement",
        "privacy-guarantee",
        "final-truth",
    ]
    for phrase in required:
        assert phrase in doc

    forbidden_claims = [
        "compliance certified",
        "certifies compliance",
        "privacy guaranteed",
        "guarantees privacy",
        "automatic enforcement",
        "final truth guaranteed",
    ]
    for phrase in forbidden_claims:
        assert phrase not in doc


def test_patch_133_status_docs_record_design_only_scope():
    combined = "\n".join(
        read(rel)
        for rel in [
            "PATCH_133_MANIFEST.txt",
            "PATCH_133_RECOVERY_NOTE.md",
            "PATCH_STATUS.md",
            "docs/progress_database.md",
            "docs/patch_index.md",
            "docs/architecture.md",
            "docs/public_trust_package.md",
        ]
    ).lower()
    required = [
        "patch 133",
        "receipt reader",
        "standard view",
        "design",
        "documentation/design only",
        "no runtime receipt reader ui",
        "no parser",
        "no scoring",
        "no receipt schema",
        "no new risk states",
        "no external calls",
        "no telemetry",
        "no storage",
        "no final-truth claim",
        "human review remains required",
    ]
    for phrase in required:
        assert phrase in combined
