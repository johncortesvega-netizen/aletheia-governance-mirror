from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def read(rel: str) -> str:
    return (ROOT / rel).read_text(encoding="utf-8")


def test_patch_129_files_exist():
    required = [
        "ui/input_clarity.py",
        "docs/input_error_clarity_patch_129.md",
        "tests/test_patch_129_input_error_clarity.py",
        "PATCH_129_MANIFEST.txt",
        "PATCH_129_RECOVERY_NOTE.md",
    ]
    for rel in required:
        assert (ROOT / rel).exists(), rel


def test_input_clarity_helpers_are_copy_only_and_boundary_safe():
    helper = read("ui/input_clarity.py")
    required = [
        "INPUT_LANGUAGE_CALIBRATION_CAVEAT",
        "EMPTY_AI_INTEGRITY_ARTIFACT_MESSAGE",
        "EMPTY_AI_INTEGRITY_BATCH_MESSAGE",
        "NO_PUBLIC_DATA_UPLOAD_MESSAGE",
        "UPLOAD_PROCESSING_FAILED_MESSAGE",
        "DIRECT_CSV_READ_FAILED_PREFIX",
        "render_language_calibration_caveat",
        "warn_empty_ai_integrity_artifact",
        "warn_empty_ai_integrity_batch",
        "warn_no_public_data_upload",
        "render_upload_processing_failed",
        "render_direct_csv_read_failed",
        "English and Dutch/Nederlands",
        "Human review remains required",
        "ALETHEIA does not invent missing artifacts",
        "Check file type, column names, encoding, and country/year fields",
    ]
    for phrase in required:
        assert phrase in helper

    forbidden = [
        "audit_ai_integrity_artifact",
        "audit_ai_integrity_batch",
        "score_empirical_frame",
        "simulate(",
        "full_report(",
        "requests.",
        "openai",
        "ollama",
        "telemetry",
        "analytics",
        "certifies privacy",
        "privacy guaranteed",
        "certifies safety",
        "automatic enforcement",
        "final truth guaranteed",
    ]
    lower = helper.lower()
    for phrase in forbidden:
        assert phrase.lower() not in lower


def test_app_uses_input_clarity_helpers_without_moving_behavior():
    app = read("app.py")
    required = [
        "from ui.input_clarity import",
        "render_language_calibration_caveat",
        "warn_empty_ai_integrity_artifact(st)",
        "warn_empty_ai_integrity_batch(st)",
        "warn_no_public_data_upload(st)",
        "render_upload_processing_failed(st, exc)",
        "render_direct_csv_read_failed(st, exc)",
        "audit_ai_integrity_artifact(ai_integrity_input, artifact_kind=artifact_kind)",
        "audit_ai_integrity_batch(ai_integrity_input, artifact_kind=artifact_kind)",
        "build_master_from_public_uploads",
        "pd.read_csv(uploaded_empirical)",
    ]
    for phrase in required:
        assert phrase in app


def test_patch_129_status_docs_updated():
    combined = "\n".join(
        read(rel)
        for rel in [
            "README.md",
            "docs/architecture.md",
            "docs/patch_index.md",
            "docs/progress_database.md",
            "PATCH_STATUS.md",
            "docs/input_error_clarity_patch_129.md",
        ]
    ).lower()
    required = [
        "patch 129",
        "input and error clarity",
        "empty-input",
        "language-calibration",
        "upload/read-failure",
        "refinement mode",
        "no scoring",
        "human review",
    ]
    for phrase in required:
        assert phrase in combined


def test_patch_129_boundary_and_encoding_guards():
    changed = "\n".join(
        read(rel)
        for rel in [
            "ui/input_clarity.py",
            "docs/input_error_clarity_patch_129.md",
            "PATCH_129_MANIFEST.txt",
            "PATCH_129_RECOVERY_NOTE.md",
        ]
    ).lower()
    required = [
        "no external calls",
        "no telemetry",
        "privacy guarantee",
        "certification",
        "enforcement",
        "final-truth",
        "humans keep the judgment",
    ]
    for phrase in required:
        assert phrase in changed

    forbidden = [
        "guarantees privacy",
        "privacy guaranteed",
        "certifies privacy",
        "certifies safety",
        "automatic enforcement",
        "final truth guaranteed",
        "todo",
        "fixme",
        "ajustando",
        "afirma",
        "preciso",
        "verwijderen",
        "overmatige",
        "ðÿ",
        "â€”",
        "â€“",
        "â€",
        "â†’",
        "�",
    ]
    for phrase in forbidden:
        assert phrase not in changed
