from pathlib import Path

from core.witness import build_local_witness_receipt, render_local_witness_receipt_text

ROOT = Path(__file__).resolve().parents[1]


def read(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8")


def sample_payload():
    return {
        "scan": {"power_concentration": 0.7, "decision_transparency": 0.2, "scan_mode": "local"},
        "sim": {"stability": 0.41, "trust_index": 0.35, "alignment": 0.4, "ego": 0.72},
        "report": {"integrity": 0.32, "friction": 0.66, "repair_questions": ["Which appeal path is missing?"]},
    }


def test_local_witness_receipt_v2_doc_and_prompt_define_boundaries():
    doc = read("docs/local_witness_receipt.md")
    prompt = read("prompts/local_witness_receipt_prompt.md")
    for text in [doc, prompt]:
        for phrase in [
            "Local Witness Receipt v2",
            "document fingerprint",
            "report fingerprint",
            "public ledger: No",
            "Global ID sync: No",
            "central storage: No",
            "authority claim: No",
            "human review required: Yes",
        ]:
            assert phrase in text
    assert "This receipt creates authority" in prompt
    assert "You must not say" in prompt


def test_receipt_builder_includes_v2_hashes_versions_and_authority_boundary():
    payload = sample_payload()
    receipt = build_local_witness_receipt(
        module="Mirror Check",
        input_text="A proposal removes appeals.",
        processed_text="A proposal removes appeals.",
        scan=payload["scan"],
        sim=payload["sim"],
        report=payload["report"],
        verdict="THRESHOLD",
        risk="Medium",
        protocol_label="Needs Safeguards",
        app_version="test-app",
        rubric_version="test-rubric",
        prompt_version="test-prompt",
        active_modules=["Mirror Check", "Evidence Lab"],
        generated_at_utc="2026-05-10T00:00:00Z",
    )
    assert receipt["receipt_version"] == "local-witness-v2"
    assert receipt["rubric_version"] == "test-rubric"
    assert receipt["prompt_version"] == "test-prompt"
    assert receipt["active_modules"] == ["Mirror Check", "Evidence Lab"]
    for key in [
        "document_fingerprint_sha256",
        "processed_document_fingerprint_sha256",
        "report_fingerprint_sha256",
        "audit_receipt_sha256",
    ]:
        assert len(receipt["hashes"][key]) == 64
    boundary = receipt["authority_boundary"]
    assert boundary["stored_locally"] is True
    assert boundary["public_ledger"] is False
    assert boundary["global_id_sync"] is False
    assert boundary["central_storage"] is False
    assert boundary["authority_claim"] is False
    assert boundary["human_review_required"] is True


def test_receipt_text_surfaces_v2_boundary_language():
    payload = sample_payload()
    receipt = build_local_witness_receipt(
        module="Mirror Check",
        input_text="A proposal removes appeals.",
        processed_text="A proposal removes appeals.",
        scan=payload["scan"],
        sim=payload["sim"],
        report=payload["report"],
        app_version="test-app",
        rubric_version="test-rubric",
        prompt_version="test-prompt",
        active_modules=["Mirror Check", "Evidence Lab"],
        generated_at_utc="2026-05-10T00:00:00Z",
    )
    text = render_local_witness_receipt_text(receipt)
    for phrase in [
        "Receipt version: local-witness-v2",
        "Rubric version: test-rubric",
        "Prompt version: test-prompt",
        "Active modules: Mirror Check, Evidence Lab",
        "Document fingerprint SHA-256",
        "Report fingerprint SHA-256",
        "AUTHORITY BOUNDARY",
        "Public ledger: False",
        "Global ID sync: False",
        "Central storage: False",
        "Authority claim: False",
        "Human review required: True",
    ]:
        assert phrase in text


def test_app_readme_status_and_about_surface_patch_41():
    app = read("app.py")
    readme = read("README.md")
    about = read("about_page.py")
    status = read("PATCH_STATUS.md")
    progress = read("docs/progress_database.md")
    for text in [app, readme, about, status, progress]:
        assert "Local Witness Receipt v2" in text
    assert "tools\\run_patch_checks.bat 41" in progress
    assert "docs/local_witness_receipt.md" in readme
    assert "prompts/local_witness_receipt_prompt.md" in readme
