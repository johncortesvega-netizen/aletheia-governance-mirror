from __future__ import annotations

from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from ui.unit_preview import get_unit_preview_proceed_button_style

ROOT = Path(__file__).resolve().parents[1]


def read(path: str) -> str:
    direct = ROOT / path
    if direct.exists():
        return direct.read_text(encoding="utf-8")
    name = Path(path).name
    if name.endswith("_MANIFEST.txt"):
        return (ROOT / "docs" / "patch_archive" / "manifests" / name).read_text(encoding="utf-8")
    if name.endswith("_RECOVERY_NOTE.md"):
        return (ROOT / "docs" / "patch_archive" / "recovery_notes" / name).read_text(encoding="utf-8")
    return direct.read_text(encoding="utf-8")


def test_patch_150_makes_proceed_button_distinct_red_and_readable() -> None:
    css = get_unit_preview_proceed_button_style()
    source = read("ui/unit_preview.py")

    assert "button[kind=\"primary\"]" in css
    assert "#b91c1c" in css
    assert "#ffffff" in css
    assert "font-weight: 800" in css
    assert "get_unit_preview_proceed_button_style()" in source
    assert "Proceed to ALETHEIA" in source


def test_patch_150_adds_clean_ai_audit_loop_proof_copy_without_validation_claim() -> None:
    unit_preview = read("ui/unit_preview.py")
    evidence_doc = read("docs/for-reviewers/ai_audit_loop_evidence.md")
    combined = unit_preview + "\n" + evidence_doc

    assert "external AI output -> ALETHEIA-style mirror reading -> human review -> failure mode identified" in combined
    assert "capture pressure, evidence-boundary gaps, sanctification drift, and concealed flattery pressure" in combined
    assert "External AI agreement, disagreement, or self-correction is not validation of ALETHEIA" in combined
    assert "This is not:" in combined
    assert "official ALETHEIA receipt" in combined


def test_patch_150_adds_what_this_is_not_to_public_docs_and_about_page() -> None:
    readme = read("README.md")
    about = read("pages_ui/about_page.py")
    combined = readme + "\n" + about

    assert "## What this is / is not" in readme
    assert "What this is / is not" in about
    assert "a mirror for pressure, authority drift, evidence gaps, capture risk" in combined
    assert "a judge, oracle, certification engine, truth machine" in combined
    assert "Internal taxonomy labels such as **SANCTUARY**, **THRESHOLD**, and **ASYLUM**" in combined
    assert "do not claim truth, purity, safety, legitimacy, moral authority, or final status" in combined


def test_patch_150_strengthens_receipt_boundary_language_without_schema_change() -> None:
    witness = read("core/witness.py")
    ai_integrity = read("core/ai_integrity_mirror.py")
    app = read("app.py")
    combined = witness + "\n" + ai_integrity + "\n" + app

    assert "This receipt is a structured mirror reading" in combined
    assert "does not certify truth, safety, legality, legitimacy, morality, or institutional fitness" in combined
    assert "Human review remains required" in combined
    assert "may be incomplete, wrong, or sensitive to missing evidence" in combined
    assert "External AI agreement, disagreement, or self-correction is not validation of ALETHEIA" in combined
    assert "RECEIPT_BOUNDARY_NOTICE" in witness
    assert "AI_AUDIT_LOOP_RECEIPT_NOTICE" in witness


def test_patch_150_preserves_behavior_boundaries() -> None:
    manifest = read("PATCH_150_MANIFEST.txt")
    recovery = read("PATCH_150_RECOVERY_NOTE.md")
    combined = manifest + "\n" + recovery

    assert "ui/unit_preview.py" in manifest
    assert "core/witness.py" in manifest
    assert "README.md" in manifest
    assert "pages_ui/about_page.py" in manifest
    assert "No app scoring change" in combined
    assert "No routing change" in combined
    assert "No receipt schema change" in combined
    assert "No World Lens math change" in combined
    assert "Human review remains required" in combined
