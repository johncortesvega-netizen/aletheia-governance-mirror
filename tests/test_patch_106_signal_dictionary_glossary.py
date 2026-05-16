from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def read(rel: str) -> str:
    return (ROOT / rel).read_text(encoding="utf-8")


def test_patch_106_signal_dictionary_files_exist():
    required = [
        "docs/SIGNAL_DICTIONARY.md",
        "tests/test_patch_106_signal_dictionary_glossary.py",
        "PATCH_106_MANIFEST.txt",
        "PATCH_106_RECOVERY_NOTE.md",
    ]
    for rel in required:
        assert (ROOT / rel).exists(), rel


def test_patch_106_dictionary_is_glossary_not_scoring_specification():
    text = read("docs/SIGNAL_DICTIONARY.md")
    required = [
        "Signal Dictionary",
        "signal dictionary, not a scoring specification",
        "mirror, not a throne",
        "review prompts",
        "not be read as verdicts",
        "transparent rule-based and heuristic signal detection",
        "ALETHEIA is English-first",
        "Possible false positives",
        "Repair direction",
        "ALETHEIA surfaces signals. Humans keep the judgment.",
    ]
    for phrase in required:
        assert phrase in text


def test_patch_106_dictionary_covers_core_signal_families():
    text = read("docs/SIGNAL_DICTIONARY.md")
    required = [
        "Authority Overreach",
        "Consent Pressure",
        "Missing Appeal or Review",
        "Power Concentration",
        "Capture Risk",
        "Evidence Gap",
        "Surveillance or Identity-Sync Pressure",
        "Automation Without Human Review",
        "Non-Transparency",
        "Repair Need",
    ]
    for phrase in required:
        assert phrase in text


def test_patch_106_navigation_links_dictionary():
    combined = "\n".join(
        read(rel)
        for rel in [
            "README.md",
            "CONTRIBUTING.md",
            "docs/signal_detection.md",
            "docs/public_trust_package.md",
            "docs/patch_index.md",
            "examples/Trust_Package_README.md",
        ]
    )
    required = [
        "docs/SIGNAL_DICTIONARY.md",
        "reviewer-facing glossary",
        "not a scoring specification",
    ]
    for phrase in required:
        assert phrase in combined


def test_patch_106_status_and_recovery_preserve_runtime_boundaries():
    text = "\n".join(
        read(rel)
        for rel in [
            "PATCH_106_MANIFEST.txt",
            "PATCH_106_RECOVERY_NOTE.md",
            "PATCH_STATUS.md",
            "docs/progress_database.md",
        ]
    ).lower()
    required = [
        "behavior changes:\n- none",
        "documentation-only",
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
        "no central storage",
        "no global id sync",
        "no public ledger sync",
        "no privacy guarantee",
        "no security guarantee",
        "no certification",
        "no enforcement",
        "no final truth claim",
    ]
    for phrase in required:
        assert phrase in text


def test_patch_106_no_accidental_internal_work_notes_or_placeholders():
    scan_files = [
        "docs/SIGNAL_DICTIONARY.md",
        "PATCH_106_MANIFEST.txt",
        "PATCH_106_RECOVERY_NOTE.md",
        "README.md",
        "PATCH_STATUS.md",
    ]
    forbidden_fragments = [
        "internal repair note",
        "temporary work note",
        "placeholder button",
        "downloaded (placeholder)",
        "ajustando",
        "afirmação",
        "preciso",
        "verwijderen",
        "overmatige",
    ]
    text = "\n".join(read(rel) for rel in scan_files).lower()
    for fragment in forbidden_fragments:
        assert fragment not in text
