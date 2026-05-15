from __future__ import annotations

from ui.receipt_reader import (
    _interpret_metric,
    _native_values_rows,
    _render_single_view,
    _summary_for_state,
    _verbal_brief,
    parse_receipt_standard_view,
)


BASE_JSON = '''
ALETHEIA LOCAL WITNESS RECEIPT
Module: {module}

VERDICT SIGNAL
Protocol-adjusted state: {state}
Risk: {risk}
Protocol label: {label}

CORE METRICS
Integrity: {integrity}
Friction: {friction}
Collapse probability: {collapse}
Trust index: {trust}
Alignment: {alignment}
Ego: {ego}

SILENT OPERATOR REPAIR QUESTIONS
- Who can challenge this reading before reliance?

MACHINE-READABLE RECEIPT JSON
{{
  "active_modules": ["{module}"],
  "module": "{module}",
  "metrics": {{
    "integrity": {integrity},
    "friction": {friction},
    "collapse_probability": {collapse},
    "trust_index": {trust},
    "alignment": {alignment},
    "ego": {ego}
  }},
  "verdict": {{
    "protocol_adjusted_state": "{state}",
    "risk": "{risk}",
    "protocol_label": "{label}"
  }}
}}
'''

WORLD_LENS_RECEIPT = '''# ALETHEIA World Lens Receipt

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
'''

QUESTION_PROMPT_RECEIPT = '''
ALETHEIA LOCAL WITNESS RECEIPT
Module: Mirror Check
Protocol-adjusted state: QUESTION_PROMPT
Risk: Not scored
Protocol label: Audit Question / Review Tool
'''


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


def _receipt(state: str, module: str = "Mirror Check") -> str:
    risk = {"SANCTUARY": "Low", "THRESHOLD": "Medium", "ASYLUM": "High"}[state]
    label = {
        "SANCTUARY": "Generic Local Scan",
        "THRESHOLD": "Missing Safeguard Negation / Needs Safeguards",
        "ASYLUM": "MEI7 Ethics Gate / Asylum",
    }[state]
    return BASE_JSON.format(
        module=module,
        state=state,
        risk=risk,
        label=label,
        integrity="0.9200" if state == "SANCTUARY" else "0.5800" if state == "THRESHOLD" else "0.2800",
        friction="0.0800" if state == "SANCTUARY" else "0.1200" if state == "THRESHOLD" else "0.3400",
        collapse="0.0800" if state == "SANCTUARY" else "0.2200" if state == "THRESHOLD" else "0.8300",
        trust="0.8880" if state == "SANCTUARY" else "0.8000" if state == "THRESHOLD" else "0.6200",
        alignment="0.8652" if state == "SANCTUARY" else "0.7800" if state == "THRESHOLD" else "0.5369",
        ego="0.0800" if state == "SANCTUARY" else "0.1500" if state == "THRESHOLD" else "0.3683",
    )


def test_verbal_briefs_cover_core_receipt_states_without_new_authority():
    cases = [
        (parse_receipt_standard_view(_receipt("SANCTUARY")), "The mirror reflects a Sanctuary pattern"),
        (parse_receipt_standard_view(_receipt("THRESHOLD", module="Simulation")), "The mirror reflects a Threshold pattern"),
        (parse_receipt_standard_view(_receipt("ASYLUM", module="Simulation")), "The mirror reflects an Asylum-pressure pattern"),
        (parse_receipt_standard_view(QUESTION_PROMPT_RECEIPT), "The mirror reflects a review-tool prompt"),
        (parse_receipt_standard_view(WORLD_LENS_RECEIPT), "The mirror reflects a selected-year evidence view"),
    ]
    for view, expected in cases:
        brief = _verbal_brief(view)
        assert expected in brief
        assert "certify" not in brief.lower()
        assert "final truth" not in brief.lower()


def test_metric_observations_are_verbal_but_bounded_to_uploaded_receipt():
    assert "Trust is high in the uploaded receipt" in _interpret_metric("trust", "0.9800", "SANCTUARY")
    assert "robust" in _interpret_metric("integrity", "0.9200", "SANCTUARY")
    assert "Collapse pressure is low" in _interpret_metric("collapse_probability", "0.0800", "SANCTUARY")
    assert "receipt evidence" in _interpret_metric("ego", "0.0800", "SANCTUARY")
    assert "not a prediction" in _interpret_metric("collapse_probability", "0.0800", "SANCTUARY")


def test_rendered_standard_view_uses_reader_brief_human_review_questions_and_native_values_expander():
    view = parse_receipt_standard_view(_receipt("SANCTUARY"))
    dummy = DummyContainer()
    _render_single_view(dummy, view)
    markdowns = [value for kind, value in dummy.events if kind == "markdown"]
    writes = [str(value) for kind, value in dummy.events if kind == "write"]
    expanders = [value for kind, value in dummy.events if kind == "expander"]

    assert "### Reader Brief" in markdowns
    assert "### Human-review questions" in markdowns
    assert "Native receipt values" in expanders
    assert any("The mirror reflects a Sanctuary pattern" in value for value in writes)
    assert any("To strengthen this reading before relying on it" in value for value in writes)


def test_native_values_remain_available_without_replacing_uploaded_values():
    view = parse_receipt_standard_view(_receipt("SANCTUARY"))
    rows = _native_values_rows(view)
    values = {(row["Field"], row["Value"]) for row in rows}

    assert ("Native State", "SANCTUARY") in values
    assert ("Trust Index", "0.8880") in values
    assert ("Integrity", "0.9200") in values
    assert ("Collapse Pressure", "0.0800") in values


def test_reader_briefs_are_less_repetitive_and_keep_no_command_boundary():
    sanctuary = _summary_for_state("SANCTUARY", {
        "risk_state": "Low",
        "trust": "0.9800",
        "integrity": "0.7311",
        "friction": "0.0000",
        "collapse_probability": "0.0730",
    })
    asylum = _summary_for_state("ASYLUM", {})

    assert sanctuary.startswith("Reader brief:")
    assert "Use this as a reflection for review" in sanctuary
    assert "final command" in sanctuary
    assert "does not approve, reject, enforce, or certify" in asylum
