from __future__ import annotations

import io
import zipfile
from pathlib import Path

from ui.receipt_reader import (
    _curated_preview_rows,
    _render_world_lens_bundle,
    parse_uploaded_receipt_file,
)


WORLD_LENS_RECEIPT_MD = """# ALETHEIA World Lens Receipt

## Scope

- Selected year: **2024**
- World Lens source state: **Full empirical scored master**
- Evidence allocation status: **full 9k evidence view**
- Allocated country rows: **172**
- Active selected-year seats: **9,000**

## Weighted metrics

- Weighted integrity: **0.446**
- Weighted friction: **0.306**
- Weighted collapse probability: **0.443**
- Average empirical coverage: **84.7%**

## Coverage

| source | rows_present | rows_missing | coverage |
| --- | --- | --- | --- |
| Trust raw survey | 0 | 172 | 0.0 |
| Trust prior | 172 | 0 | 1.0 |

## Internal taxonomy distribution

| empirical_pattern_display | raw_verdict | countries | seats | avg_integrity | avg_collapse_probability | avg_empirical_coverage | seat_share | internal_taxonomy_label | humility_note |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| High-risk internal reading | ASYLUM | 72 | 2943 | 0.3054 | 0.5956 | 0.85 | 0.327 | ASYLUM | High-risk taxonomy label; requires human review and does not enforce action. |
"""

WORLD_LENS_SUMMARY_JSON = """{
  "selected_year": 2024,
  "grid_source_state": "Full empirical scored master",
  "active_selected_year_seats": 9000,
  "allocated_country_rows": 172,
  "weighted_integrity": 0.4455880333333333,
  "weighted_friction": 0.3062790444444445,
  "weighted_collapse_probability": 0.4427573666666667,
  "average_empirical_coverage": 0.8473837209302322,
  "trust_raw_coverage": 0.0,
  "trust_prior_coverage": 1.0,
  "interpretation_warning": "Full selected-year 9k allocation."
}
"""

ALL_ROWS_CSV = """country,iso3,year,population,population_share,seats_9k,aletheia_empirical_integrity,aletheia_empirical_friction,aletheia_empirical_collapse_probability,empirical_pattern_display,raw_aletheia_verdict,empirical_completeness,raw_trust,empirical_trust_prior,coverage_gap_count,humility_note,__source_wgi_voice_accountability,__source_wgi_political_stability,__source_wgi_government_effectiveness,__source_wgi_regulatory_quality,__source_wgi_rule_of_law,__source_wgi_control_corruption,grid_selected_year,grid_source_state,internal_taxonomy_label
India,IND,2024,1450935791,0.17,1609,0.4698,0.2399,0.3996,Review / threshold reading,THRESHOLD,0.85,,0.5,1,Review-state taxonomy label; requires human interpretation.,-0.07,-0.78,0.40,-0.09,-0.03,-0.29,2024,Full empirical scored master,THRESHOLD
"""

COVERAGE_CSV = "source,rows_present,rows_missing,coverage\nTrust raw survey,0,172,0.0\nTrust prior,172,0,1.0\n"


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

    def selectbox(self, label: str, options: list[str], key: str | None = None) -> str:
        self.events.append(("selectbox", label))
        return options[0]

    def expander(self, label: str, expanded: bool = False):
        self.events.append(("expander", label))
        return self

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc, tb):
        return False


def _payload() -> bytes:
    payload = io.BytesIO()
    with zipfile.ZipFile(payload, "w") as archive:
        archive.writestr("aletheia_world_lens_receipt_2024.md", WORLD_LENS_RECEIPT_MD)
        archive.writestr("aletheia_world_lens_receipt_2024_summary.json", WORLD_LENS_SUMMARY_JSON)
        archive.writestr("aletheia_world_lens_receipt_2024_all_rows.csv", ALL_ROWS_CSV)
        archive.writestr("aletheia_world_lens_receipt_2024_coverage.csv", COVERAGE_CSV)
    return payload.getvalue()


def test_world_lens_bundle_renders_native_receipt_before_csv_tables():
    parsed = parse_uploaded_receipt_file(Upload("aletheia_world_lens_receipt_2024.zip", _payload()))
    assert parsed["bundle_type"] == "world_lens_evidence_bundle"

    dummy = DummyContainer()
    _render_world_lens_bundle(dummy, parsed)
    labels = [str(value) for kind, value in dummy.events if kind in {"markdown", "expander"}]

    native_index = next(i for i, value in enumerate(labels) if "Inspect native World Lens receipt" in value)
    csv_index = next(i for i, value in enumerate(labels) if "Supporting CSV Evidence Tables" in value)
    assert native_index < csv_index


def test_world_lens_supporting_table_inventory_is_compact_not_column_dump():
    parsed = parse_uploaded_receipt_file(Upload("aletheia_world_lens_receipt_2024.zip", _payload()))
    dummy = DummyContainer()
    _render_world_lens_bundle(dummy, parsed)

    table_events = [data for kind, data in dummy.events if kind == "table" and isinstance(data, list)]
    inventory = next(
        rows for rows in table_events
        if rows and isinstance(rows[0], dict) and rows[0].get("Table") in {"All Rows", "Coverage"}
    )
    assert all("Columns" not in row for row in inventory)
    assert all("Preview Fields" in row for row in inventory)
    assert all(len(str(row["Preview Fields"])) < 160 for row in inventory)


def test_world_lens_csv_preview_uses_curated_columns_by_default():
    parsed = parse_uploaded_receipt_file(Upload("aletheia_world_lens_receipt_2024.zip", _payload()))
    all_rows_table = next(
        table for table in parsed["bundle_details"]["evidence_tables"]
        if table["table_name"] == "All Rows"
    )
    curated = _curated_preview_rows(all_rows_table)
    assert curated
    first = curated[0]
    assert "country" in first
    assert "iso3" in first
    assert "aletheia_empirical_integrity" in first
    assert "aletheia_empirical_collapse_probability" in first
    assert "__source_wgi_voice_accountability" not in first
    assert len(first) <= 12


def test_patch_142_11_manifest_and_recovery_note_exist():
    root = Path(__file__).resolve().parents[1]
    assert (root / "PATCH_142_11_MANIFEST.txt").exists()
    assert (root / "PATCH_142_11_RECOVERY_NOTE.md").exists()
