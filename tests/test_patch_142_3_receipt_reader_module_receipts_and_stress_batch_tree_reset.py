from pathlib import Path
import importlib

ROOT = Path(__file__).resolve().parents[1]


def read(rel: str) -> str:
    return (ROOT / rel).read_text(encoding="utf-8")


WORLD_LENS_RECEIPT = """
# ALETHEIA World Lens Receipt

## Scope

- Selected year: **2023**
- World Lens source state: **Full empirical scored master**
- Evidence allocation status: **full 9k evidence view**
- Allocated country rows: **172**
- Active selected-year seats: **9,000**
- Rows excluded / diagnostic: **33**
- Hidden zero-seat diagnostic rows: **33**

## Weighted metrics

- Weighted integrity: **0.447**
- Weighted friction: **0.304**
- Weighted collapse probability: **0.441**
- Average empirical coverage: **84.7%**

## Coverage

| source | rows_present | rows_missing | coverage |
| --- | --- | --- | --- |
| Trust raw survey | 0 | 172 | 0.0 |
| Trust prior | 172 | 0 | 1.0 |
| WGI | 172 | 0 | 1.0 |
| V-Dem | 169 | 3 | 0.9826 |

## Internal taxonomy distribution

| empirical_pattern_display | raw_verdict | countries | seats | avg_integrity | avg_collapse_probability | avg_empirical_coverage | seat_share | internal_taxonomy_label | humility_note |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| High-risk internal reading | ASYLUM | 70 | 2948 | 0.3076 | 0.5933 | 0.85 | 0.3276 | ASYLUM | High-risk taxonomy label; requires human review and does not enforce action. |
| Low-risk internal reading | SANCTUARY | 39 | 1206 | 0.7256 | 0.1765 | 0.8423 | 0.134 | SANCTUARY | Internal taxonomy label only; not a final safety, final Sanctuary, or authority claim. |
| Review / threshold reading | THRESHOLD | 63 | 4846 | 0.4991 | 0.3773 | 0.8476 | 0.5384 | THRESHOLD | Review-state taxonomy label; requires human interpretation and safeguard review. |
"""

AI_INTEGRITY_RECEIPT = """
AI INTEGRITY RECEIPT CONTEXT
Receipt header: AI Integrity Mirror — Static Artifact Review Receipt
AI Integrity receipt version: ai-integrity-receipt-polish-v0.5
Review mode: single static artifact
Artifact type: AI output
Internal taxonomy label: SANCTUARY
Risk reading: Low
Protocol label: AI Integrity Mirror / Low-Risk Internal Reading
Integrity reading: 0.92
Capture pressure: 0.08
Risk pressure: 0.0
Positive review signals: 4

STATIC REVIEW SCOPE
Scope: pasted artifact only. The reading does not test a live model, vendor, deployment, full repository, training data, hidden system prompt, or future behavior.

REPAIR QUESTIONS
- What independent reviewer could challenge this low-risk reading before real-world reliance?

GENERIC LOCAL WITNESS RECEIPT FOLLOWS
Module: AI Integrity Mirror
Risk: Low
Protocol-adjusted state: SANCTUARY
Trust index: 0.8880
SILENT OPERATOR REPAIR QUESTIONS
- What independent reviewer could challenge this low-risk reading before real-world reliance?
"""

STRESS_RECEIPT = """
ALETHEIA LOCAL WITNESS RECEIPT
Module: Simulation
VERDICT SIGNAL
Protocol-adjusted state: THRESHOLD
Risk: Medium
Protocol label: Missing Safeguard Negation / Needs Safeguards
CORE METRICS
Integrity: 0.5690
Friction: 0.1490
Collapse probability: 0.2650
Trust index: 0.8000
Alignment: 0.7800
Ego: 0.1500
SILENT OPERATOR REPAIR QUESTIONS
- What explanation path lets affected people understand how the automated triage decision was made?
"""


def test_receipt_reader_detects_world_lens_and_uses_world_lens_evidence_fields():
    reader = importlib.import_module("ui.receipt_reader")
    parsed = reader.parse_receipt_standard_view(WORLD_LENS_RECEIPT)
    fields = parsed["fields"]
    world = parsed["world_lens_fields"]

    assert parsed["receipt_kind"] == "World Lens"
    assert parsed["native_state"] == "WORLD_LENS_EVIDENCE_VIEW"
    assert fields["module_source"] == "World Lens"
    assert fields["integrity"] == "0.447"
    assert fields["friction"] == "0.304"
    assert fields["collapse_probability"] == "0.441"
    assert world["selected_year"] == "2023"
    assert world["active_selected_year_seats"] == "9,000"
    assert world["average_empirical_coverage"] == "84.7%"
    assert world["trust_raw_survey_coverage"] == "0.0"
    assert world["trust_prior_coverage"] == "1.0"
    assert "trust prior" in fields["trust"].lower()
    assert "Mirror Check scenario" in parsed["plain_language_explanation"]


def test_receipt_reader_detects_ai_integrity_context_without_live_model_claims():
    reader = importlib.import_module("ui.receipt_reader")
    parsed = reader.parse_receipt_standard_view(AI_INTEGRITY_RECEIPT)
    fields = parsed["fields"]
    ai = parsed["ai_integrity_fields"]

    assert parsed["receipt_kind"] == "AI Integrity Mirror"
    assert fields["module_source"] == "AI Integrity Mirror"
    assert fields["protocol_adjusted_state"] == "SANCTUARY"
    assert fields["risk_state"] == "Low"
    assert fields["integrity"] == "0.92"
    assert fields["friction"] == "0.08"
    assert ai["artifact_type"] == "AI output"
    assert "does not test a live model" in parsed["plain_language_explanation"]
    assert "certification" in parsed["non_certification_note"].lower()


def test_receipt_reader_detects_stress_test_simulation_receipts():
    reader = importlib.import_module("ui.receipt_reader")
    parsed = reader.parse_receipt_standard_view(STRESS_RECEIPT)
    fields = parsed["fields"]

    assert parsed["receipt_kind"] == "Stress Test"
    assert fields["module_source"] == "Simulation"
    assert parsed["native_state"] == "THRESHOLD"
    assert fields["risk_state"] == "Medium"
    assert fields["trust"] == "0.8000"
    assert "without re-running the scenario" in parsed["plain_language_explanation"]


def test_stress_batch_run_closes_single_scenario_tree_state():
    app = read("app.py")
    assert "Patch 142.3: a Stress Test batch is a separate workflow" in app
    assert "old tree does not remain below the batch" in app
    assert 'st.session_state.pop(stress_single_key, None)' in app
    assert '"last_report"' in app
    assert '"last_scan"' in app
    assert '"last_sim"' in app


def test_patch_142_3_boundaries_and_docs():
    helper = read("ui/receipt_reader.py")
    combined = "\n".join(
        read(rel)
        for rel in [
            "PATCH_142_3_MANIFEST.txt",
            "PATCH_142_3_RECOVERY_NOTE.md",
            "PATCH_STATUS.md",
            "docs/progress_database.md",
            "docs/patch_index.md",
        ]
    ).lower()
    for phrase in [
        "patch 142.3",
        "receipt reader module receipt calibration",
        "world lens",
        "ai integrity mirror",
        "stress test",
        "stress batch",
        "tree",
        "no scoring",
        "no verdict routing",
        "no receipt schema",
        "no receipt generation",
        "no ai integrity scan behavior",
        "no world lens math",
        "no external calls",
        "no telemetry",
        "no certification",
        "human review remains required",
    ]:
        assert phrase in combined

    forbidden_helper_calls = [
        "full_report(",
        "simulate(",
        "build_local_witness_receipt",
        "render_local_witness_receipt_text",
        "audit_ai_integrity",
        "scan_privacy_boundary_static",
        "requests.",
        "httpx.",
        "openai",
        "embedding",
        "telemetry",
        "analytics",
        "download_button",
    ]
    lower_helper = helper.lower()
    for phrase in forbidden_helper_calls:
        assert phrase.lower() not in lower_helper
