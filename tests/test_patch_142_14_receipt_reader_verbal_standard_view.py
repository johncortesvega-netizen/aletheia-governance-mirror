from __future__ import annotations

from pathlib import Path

from ui.receipt_reader import _render_single_view, parse_receipt_standard_view


MIRROR_RECEIPT = """
ALETHEIA LOCAL WITNESS RECEIPT
Module: Mirror Check

VERDICT SIGNAL
Protocol-adjusted state: SANCTUARY
Risk: Low
Protocol label: Generic Local Scan

CORE METRICS
Integrity: 0.7311
Friction: 0.0000
Collapse probability: 0.0730
Trust index: 0.9800
Alignment: 0.9500
Ego: 0.0009

SILENT OPERATOR REPAIR QUESTIONS
- What appeal path exists for people affected by this proposal?

MACHINE-READABLE RECEIPT JSON
{
  "active_modules": ["Mirror Check"],
  "module": "Mirror Check",
  "metrics": {
    "integrity": 0.7311,
    "friction": 0.0,
    "collapse_probability": 0.073,
    "trust_index": 0.98,
    "alignment": 0.95,
    "ego": 0.0009
  },
  "repair_questions": ["What appeal path exists for people affected by this proposal?"],
  "verdict": {
    "protocol_adjusted_state": "SANCTUARY",
    "risk": "Low",
    "protocol_label": "Generic Local Scan"
  }
}
"""

STRESS_RECEIPT = """
ALETHEIA LOCAL WITNESS RECEIPT
Module: Simulation

VERDICT SIGNAL
Protocol-adjusted state: THRESHOLD
Risk: Medium
Protocol label: Missing Safeguard Negation / Needs Safeguards

CORE METRICS
Integrity: 0.5800
Friction: 0.1200
Collapse probability: 0.2200
Trust index: 0.8000
Alignment: 0.7800
Ego: 0.1500

MACHINE-READABLE RECEIPT JSON
{
  "active_modules": ["Simulation"],
  "module": "Simulation",
  "metrics": {
    "integrity": 0.58,
    "friction": 0.12,
    "collapse_probability": 0.22,
    "trust_index": 0.8,
    "alignment": 0.78,
    "ego": 0.15
  },
  "verdict": {
    "protocol_adjusted_state": "THRESHOLD",
    "risk": "Medium",
    "protocol_label": "Missing Safeguard Negation / Needs Safeguards"
  }
}
"""

QUESTION_PROMPT_RECEIPT = """
ALETHEIA LOCAL WITNESS RECEIPT
Module: Mirror Check

VERDICT SIGNAL
Protocol-adjusted state: QUESTION_PROMPT
Protocol label: Audit Question / Review Tool

MACHINE-READABLE RECEIPT JSON
{
  "active_modules": ["Mirror Check"],
  "module": "Mirror Check",
  "metrics": {},
  "verdict": {
    "protocol_adjusted_state": "QUESTION_PROMPT",
    "protocol_label": "Audit Question / Review Tool"
  }
}
"""

WORLD_LENS_RECEIPT = """# ALETHEIA World Lens Receipt

- Selected year: **2024**
- World Lens source state: **Full empirical scored master**
- Evidence allocation status: **full 9k evidence view**
- Allocated country rows: **172**
- Active selected-year seats: **9,000**
- Weighted integrity: **0.446**
- Weighted friction: **0.306**
- Weighted collapse probability: **0.443**
- Average empirical coverage: **84.7%**

| source | rows_present | rows_missing | coverage |
| --- | --- | --- | --- |
| Trust raw survey | 0 | 172 | 0.0 |
| Trust prior | 172 | 0 | 1.0 |
"""


class DummyContainer:
    def __init__(self):
        self.events: list[tuple[str, object]] = []

    def markdown(self, text: str) -> None:
        self.events.append(("markdown", text))

    def write(self, text: object) -> None:
        self.events.append(("write", text))

    def caption(self, text: str) -> None:
        self.events.append(("caption", text))

    def table(self, data: object) -> None:
        self.events.append(("table", data))

    def info(self, text: str) -> None:
        self.events.append(("info", text))

    def expander(self, label: str, expanded: bool = False):
        self.events.append(("expander", label))
        return self

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc, tb):
        return False

    def rendered_text(self) -> str:
        return "\n".join(str(value) for _, value in self.events)


def test_verbal_brief_precedes_native_values_and_uses_mirror_voice():
    view = parse_receipt_standard_view(MIRROR_RECEIPT)
    dummy = DummyContainer()
    _render_single_view(dummy, view)
    rendered = dummy.rendered_text()

    assert "The mirror reflects a Sanctuary pattern" in rendered
    assert "This Standard View explains the receipt without creating a new verdict" in rendered
    assert "Trust Index: 0.9800" in rendered
    assert "Observation: Trust is recorded at 0.9800" in rendered
    assert "Native receipt values" in rendered


def test_repair_questions_are_human_review_questions():
    view = parse_receipt_standard_view(MIRROR_RECEIPT)
    dummy = DummyContainer()
    _render_single_view(dummy, view)
    rendered = dummy.rendered_text()

    assert "Human-review questions" in rendered
    assert "To strengthen this reading before relying on it, consider:" in rendered
    assert "Repair questions found in uploaded receipt" not in rendered


def test_stress_threshold_uses_verbal_review_checkpoint_language():
    view = parse_receipt_standard_view(STRESS_RECEIPT)
    dummy = DummyContainer()
    _render_single_view(dummy, view)
    rendered = dummy.rendered_text()

    assert "The mirror reflects a Threshold pattern" in rendered
    assert "safeguards, appeal paths, transparency" in rendered
    assert "Scenario Receipt State: THRESHOLD" in rendered
    assert "Native scenario receipt values" in rendered


def test_question_prompt_keeps_review_tool_mode_without_metric_table_dump():
    view = parse_receipt_standard_view(QUESTION_PROMPT_RECEIPT)
    dummy = DummyContainer()
    _render_single_view(dummy, view)
    rendered = dummy.rendered_text()

    assert "The mirror reflects a review-tool prompt" in rendered
    assert "Not applicable — QUESTION_PROMPT receipts are review-tool prompts" in rendered
    assert "Native receipt values" not in rendered


def test_world_lens_verbal_brief_stays_evidence_bundle_oriented():
    view = parse_receipt_standard_view(WORLD_LENS_RECEIPT)
    dummy = DummyContainer()
    _render_single_view(dummy, view)
    rendered = dummy.rendered_text()

    assert "The mirror reflects a selected-year World Lens evidence view for 2024" in rendered
    assert "without creating a country verdict, certification, or new score" in rendered
    assert "Native World Lens values" in rendered


def test_patch_142_14_manifest_and_recovery_note_exist():
    root = Path(__file__).resolve().parents[1]
    assert (root / "PATCH_142_14_MANIFEST.txt").exists()
    assert (root / "PATCH_142_14_RECOVERY_NOTE.md").exists()
