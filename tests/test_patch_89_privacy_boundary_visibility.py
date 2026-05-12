from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]


def read(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8")


def test_patch_89_privacy_copy_is_visible_in_app_and_about_page():
    app = read("app.py")
    about = read("about_page.py")

    for text in [app, about]:
        lowered = text.lower()
        assert "privacy by design" in lowered
        assert "no built-in telemetry" in lowered
        assert "trackers" in lowered
        assert "analytics sdks" in lowered
        assert "backend upload endpoint" in lowered
        assert "central user-input database" in lowered

    assert "hosting providers may still have their own server logs" in app.lower()
    assert "third-party host" in about


def test_patch_89_ai_integrity_surface_mentions_no_central_artifact_storage():
    app = read("app.py")
    docs = read("docs/ai_integrity_mirror.md")

    assert "central storage of pasted AI Integrity artifacts" in app
    assert "Pasted AI Integrity artifacts are processed in the running app session" in docs
    assert "third-party hosting layers may still keep their own access logs" in docs


def test_patch_89_repository_docs_and_ledgers_capture_safe_privacy_claim():
    for path in [
        "README.md",
        "docs/privacy_boundary.md",
        "PATCH_STATUS.md",
        "docs/progress_database.md",
        "PATCH_89_MANIFEST.txt",
        "PATCH_89_RECOVERY_NOTE.md",
    ]:
        assert (ROOT / path).exists(), path

    combined = "\n".join(
        read(path)
        for path in [
            "README.md",
            "docs/privacy_boundary.md",
            "PATCH_STATUS.md",
            "docs/progress_database.md",
            "PATCH_89_MANIFEST.txt",
            "PATCH_89_RECOVERY_NOTE.md",
        ]
    )
    lowered = combined.lower()
    for phrase in [
        "patch 89",
        "privacy boundary",
        "no built-in telemetry",
        "backend upload endpoint",
        "public ledger sync",
        "global id sync",
        "central user-input database",
        "third-party host",
        r"tools\run_patch_checks.bat 89",
    ]:
        assert phrase.lower() in lowered


def test_patch_89_no_common_telemetry_or_backend_upload_imports_in_app_code():
    banned_patterns = [
        r"^\s*import\s+requests\b",
        r"^\s*from\s+requests\b",
        r"^\s*import\s+httpx\b",
        r"^\s*from\s+httpx\b",
        r"urllib\.request",
        r"urlopen\(",
        r"posthog",
        r"sentry_sdk",
        r"mixpanel",
        r"amplitude",
        r"firebase",
        r"supabase",
        r"streamlit_js_eval",
        r"^\s*import\s+sqlite3\b",
        r"MongoClient",
        r"create_engine\(",
    ]
    application_files = [
        path
        for path in ROOT.rglob("*.py")
        if ".git" not in path.parts
        and "tests" not in path.parts
        and "__pycache__" not in path.parts
    ]

    offenders = []
    for path in application_files:
        text = path.read_text(encoding="utf-8", errors="ignore")
        for pattern in banned_patterns:
            if re.search(pattern, text, flags=re.IGNORECASE | re.MULTILINE):
                offenders.append(f"{path.relative_to(ROOT)}::{pattern}")

    assert not offenders, "Unexpected telemetry/backend-upload/storage imports: " + "; ".join(offenders)
