from __future__ import annotations

import io
import zipfile
from pathlib import Path

from ui.receipt_reader import (
    _curated_preview_rows,
    _preview_field_label,
    _render_single_view,
    parse_receipt_standard_view,
    parse_uploaded_receipt_file,
)


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

WORLD_LENS_RECEIPT_MD = """# ALETHEIA World Lens Receipt

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

ALL_ROWS_CSV = """country,iso3,year,seats_9k,internal_taxonomy_label,aletheia_empirical_integrity,aletheia_empirical_friction,aletheia_empirical_collapse_probability,empirical_completeness,empirical_trust_prior,coverage_gap_count,__source_wgi_voice_accountability
India,IND,2024,1609,THRESHOLD,0.4698,0.2399,0.3996,0.85,0.5,1,-0.07
"""


class Upload:
    def __init__(self, name: str, payload: bytes):
        self.name = name
        self._payload = payload

    def getvalue(self) -> bytes:
        return self._payload


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


class ExpanderDummy(DummyContainer):
    def expander(self, label: str, expanded: bool = False):
        self.events.append(("expander", label))
        return self

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc, tb):
        return False


def _world_lens_zip() -> bytes:
    payload = io.BytesIO()
    with zipfile.ZipFile(payload, "w") as archive:
        archive.writestr("aletheia_world_lens_receipt_2024.md", WORLD_LENS_RECEIPT_MD)
        archive.writestr("aletheia_world_lens_receipt_2024_all_rows.csv", ALL_ROWS_CSV)
    return payload.getvalue()


def test_mirror_check_standard_view_uses_bounded_receipt_copy():
    view = parse_receipt_standard_view(MIRROR_RECEIPT)
    rows = {row["Metric"]: row for row in view["metric_rows"]}

    dummy = DummyContainer()
    _render_single_view(dummy, view)
    headings = [value for kind, value in dummy.events if kind == "markdown"]

    assert "### Native Receipt State: SANCTUARY" in headings
    assert "Trust is high in the uploaded receipt" in rows["Trust Index"]["Interpretation"]
    assert "Alignment is high in the uploaded receipt" in rows["Alignment"]["Interpretation"]
    assert "low reading" in rows["Ego"]["Interpretation"].lower() or "very low" in rows["Ego"]["Interpretation"].lower()
    assert "records a Low risk reading" in view["summary"]
    assert "operating in a Low risk state" not in view["summary"]


def test_stress_test_standard_view_uses_scenario_receipt_copy():
    view = parse_receipt_standard_view(STRESS_RECEIPT)
    rows = {row["Metric"]: row for row in view["metric_rows"]}

    dummy = DummyContainer()
    _render_single_view(dummy, view)
    headings = [value for kind, value in dummy.events if kind == "markdown"]

    assert view["module_family"] == "Stress Test / Simulation"
    assert "### Scenario Receipt State: THRESHOLD" in headings
    assert "### Scenario Review Metrics" in headings
    assert "Collapse Pressure" in rows
    assert "Collapse pressure is reviewable" in rows["Collapse Pressure"]["Interpretation"]
    assert "Trust is solid" in rows["Trust Index"]["Interpretation"]


def test_world_lens_standard_view_uses_evidence_view_and_softened_collapse_label():
    view = parse_receipt_standard_view(WORLD_LENS_RECEIPT_MD)
    rows = {row["Metric"]: row for row in view["metric_rows"]}

    dummy = DummyContainer()
    _render_single_view(dummy, view)
    headings = [value for kind, value in dummy.events if kind == "markdown"]

    assert "### Evidence View: WORLD_LENS_EVIDENCE_VIEW" in headings
    assert "Weighted Collapse Pressure" in rows
    assert rows["Weighted Collapse Pressure"]["Value"] == "0.443"
    assert "native weighted collapse-probability field" in rows["Weighted Collapse Pressure"]["Interpretation"].lower()


def test_world_lens_curated_csv_preview_uses_short_display_labels():
    parsed = parse_uploaded_receipt_file(Upload("world_lens.zip", _world_lens_zip()))
    table = parsed["bundle_details"]["evidence_tables"][0]
    rows = _curated_preview_rows(table)
    preview_label = _preview_field_label(table)

    assert rows
    assert "Country" in rows[0]
    assert "State" in rows[0]
    assert "Integrity" in rows[0]
    assert "Collapse" in rows[0]
    assert "aletheia_empirical_collapse_probability" not in rows[0]
    assert "Country" in preview_label
    assert "aletheia_empirical_collapse_probability" not in preview_label


def test_patch_142_12_manifest_and_recovery_note_exist():
    root = Path(__file__).resolve().parents[1]
    assert (root / "PATCH_142_12_MANIFEST.txt").exists()
    assert (root / "PATCH_142_12_RECOVERY_NOTE.md").exists()
