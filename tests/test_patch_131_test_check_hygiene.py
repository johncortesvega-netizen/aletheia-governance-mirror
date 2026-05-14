import ast
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def read(rel: str) -> str:
    return (ROOT / rel).read_text(encoding="utf-8")


def read_bytes(rel: str) -> bytes:
    return (ROOT / rel).read_bytes()


def test_patch_131_files_exist():
    required = [
        "docs/test_check_hygiene.md",
        "tools/run_checks.py",
        "tests/test_patch_131_test_check_hygiene.py",
        "PATCH_131_MANIFEST.txt",
        "PATCH_131_RECOVERY_NOTE.md",
    ]
    for rel in required:
        assert (ROOT / rel).exists(), rel


def test_protocol_baseline_manifest_is_utf8_json_without_bom():
    raw = read_bytes("data/protocol_baseline_manifest.json")
    assert not raw.startswith(b"\xef\xbb\xbf")
    manifest = json.loads(raw.decode("utf-8"))
    assert manifest["created_for_patch"] == "131"
    assert "tests/test_patch_131_test_check_hygiene.py" in manifest["files"]
    assert "tools/run_checks.py" in manifest["files"]


def test_patch_131_docs_record_local_validation_commands():
    doc = read("docs/test_check_hygiene.md")
    required = [
        "set PATH=C:\\Users\\John\\AppData\\Local\\Python\\bin;C:\\Users\\John\\AppData\\Local\\Python\\pythoncore-3.14-64\\Scripts;%PATH%",
        "cd C:\\Users\\John\\Desktop\\aletheia-governance-mirror",
        "python tools\\run_patch_checks.py 131",
        "python tools\\run_patch_checks.py 130",
        "python tools\\run_patch_checks.py 129",
        "python tools\\run_protocol_baseline_self_audit.py",
        "python tools\\run_checks.py",
        "python -m streamlit run app.py",
    ]
    for phrase in required:
        assert phrase in doc


def test_patch_131_hygiene_docs_are_boundary_safe():
    combined_status = "\n".join(
        read(rel)
        for rel in [
            "docs/test_check_hygiene.md",
            "PATCH_131_MANIFEST.txt",
            "PATCH_131_RECOVERY_NOTE.md",
            "README.md",
            "docs/architecture.md",
            "docs/patch_index.md",
            "docs/progress_database.md",
            "PATCH_STATUS.md",
        ]
    ).lower()
    patch_131_materials = "\n".join(
        read(rel)
        for rel in [
            "docs/test_check_hygiene.md",
            "PATCH_131_MANIFEST.txt",
            "PATCH_131_RECOVERY_NOTE.md",
        ]
    ).lower()

    required = [
        "patch 131",
        "test and check hygiene",
        "release-candidate refinement mode",
        "no runtime behavior change",
        "no scoring",
        "no verdict-routing",
        "no receipt schema",
        "no signal-pattern",
        "no signal-weight",
        "no privacy audit scan behavior change",
        "no ai integrity scan behavior change",
        "no world lens math change",
        "no external calls",
        "no telemetry",
        "no analytics",
        "no storage",
        "humans keep the judgment",
    ]
    for phrase in required:
        assert phrase in combined_status

    forbidden_claim_patterns = [
        r"\bguarantees?\s+privacy\b",
        r"\bprivacy\s+guaranteed\b",
        r"\bcertif(?:y|ies|ied)\s+(?:privacy|safety|truth|integrity)\b",
        r"\bautomatic\s+enforcement\b",
        r"\bfinal\s+truth\s+guaranteed\b",
        r"\bproves?\s+final\s+truth\b",
    ]
    for pattern in forbidden_claim_patterns:
        assert not re.search(pattern, patch_131_materials), pattern


def test_patch_131_changed_docs_have_no_repair_notes_or_mojibake():
    changed = "\n".join(
        read(rel)
        for rel in [
            "docs/test_check_hygiene.md",
            "PATCH_131_MANIFEST.txt",
            "PATCH_131_RECOVERY_NOTE.md",
        ]
    )
    forbidden = [
        "todo",
        "fixme",
        "placeholder",
        "ajustando",
        "afirma",
        "preciso",
        "verwijderen",
        "overmatige",
        "Ã°Ã¿",
        "Ã¢â‚¬â€",
        "Ã¢â‚¬â€œ",
        "Ã¢â‚¬",
        "Ã¢â€ â€™",
        "\ufffd",
    ]
    lowered = changed.lower()
    for token in forbidden:
        assert token.lower() not in lowered


def test_tool_entry_points_parse_and_run_locally():
    for rel in [
        "tools/run_checks.py",
        "tools/run_patch_checks.py",
        "tools/run_current_suite.py",
        "tools/run_protocol_baseline_self_audit.py",
    ]:
        ast.parse(read(rel))

    tool = read("tools/run_checks.py")
    assert "tools/run_current_suite.py" in tool
    assert "tools/run_legacy_test_inventory.py" in tool
    assert "requests" not in tool
    assert "httpx" not in tool
    assert "urllib" not in tool
    assert "socket" not in tool
