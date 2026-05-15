from __future__ import annotations

import io
import zipfile
from pathlib import Path

from ui.receipt_reader import parse_uploaded_receipt_file


WORLD_LENS_RECEIPT_MD = """# ALETHEIA World Lens Receipt

## Scope

- Selected year: **2024**
- World Lens source state: **Full empirical scored master**
- Evidence allocation status: **full 9k evidence view**
- Allocated country rows: **172**
- Active selected-year seats: **9,000**
- Rows excluded / diagnostic: **33**
- Hidden zero-seat diagnostic rows: **33**

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
| WGI | 172 | 0 | 1.0 |
| V-Dem | 169 | 3 | 0.9826 |

## Internal taxonomy distribution

| empirical_pattern_display | raw_verdict | countries | seats | avg_integrity | avg_collapse_probability | avg_empirical_coverage | seat_share | internal_taxonomy_label | humility_note |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| High-risk internal reading | ASYLUM | 72 | 2943 | 0.3054 | 0.5956 | 0.85 | 0.327 | ASYLUM | High-risk taxonomy label; requires human review and does not enforce action. |
| Low-risk internal reading | SANCTUARY | 39 | 1238 | 0.7224 | 0.1783 | 0.8423 | 0.1376 | SANCTUARY | Internal taxonomy label only; not a final safety, final Sanctuary, or authority claim. |
| Review / threshold reading | THRESHOLD | 61 | 4819 | 0.5011 | 0.3748 | 0.8475 | 0.5354 | THRESHOLD | Review-state taxonomy label; requires human interpretation and safeguard review. |
"""

WORLD_LENS_SUMMARY_JSON = """{
  "selected_year": 2024,
  "weighted_integrity": 0.4455880333333333,
  "weighted_friction": 0.3062790444444445,
  "weighted_collapse_probability": 0.4427573666666667,
  "diagnostic_scope": "empirical_country_year_evidence"
}
"""


class Upload:
    def __init__(self, name: str, payload: bytes):
        self.name = name
        self._payload = payload

    def getvalue(self) -> bytes:
        return self._payload


def _zip_payload() -> bytes:
    payload = io.BytesIO()
    with zipfile.ZipFile(payload, "w") as archive:
        archive.writestr("aletheia_world_lens_receipt_2024.md", WORLD_LENS_RECEIPT_MD)
        archive.writestr("aletheia_world_lens_receipt_2024_summary.json", WORLD_LENS_SUMMARY_JSON)
        archive.writestr("aletheia_world_lens_receipt_2024_coverage.csv", "source,coverage\nTrust raw survey,0.0\n")
    return payload.getvalue()


def test_world_lens_zip_inspects_actual_md_receipt_not_summary_json():
    parsed = parse_uploaded_receipt_file(Upload("aletheia_world_lens_receipt_2024.zip", _zip_payload()))

    assert parsed["kind"] == "batch_zip"
    assert parsed["receipt_count"] == 1
    assert parsed["distribution"] == {"WORLD_LENS_EVIDENCE_VIEW": 1}

    first_name, first_view = parsed["views"][0]
    assert first_name == "aletheia_world_lens_receipt_2024.md"
    assert "summary" not in first_name.lower()
    assert first_view["module_family"] == "World Lens"
    assert first_view["native_state"] == "WORLD_LENS_EVIDENCE_VIEW"

    fields = first_view["fields"]
    world = first_view["world_lens_fields"]
    assert fields["module_source"] == "World Lens"
    assert fields["protocol_label"] == "full 9k evidence view"
    assert fields["integrity"] == "0.446"
    assert fields["friction"] == "0.306"
    assert fields["collapse_probability"] == "0.443"
    assert world["selected_year"] == "2024"
    assert world["active_selected_year_seats"] == "9,000"
    assert world["trust_raw_survey_coverage"] == "0.0"
    assert world["trust_prior_coverage"] == "1.0"

    values = {row["Metric"]: row["Value"] for row in first_view["metric_rows"]}
    assert values["Weighted Integrity"] == "0.446"
    assert values["Weighted Friction"] == "0.306"
    assert values["Weighted Collapse Pressure"] == "0.443"
    assert values["Average Empirical Coverage"] == "84.7%"
    assert values["Active Selected-Year Seats"] == "9,000"


def test_world_lens_zip_selection_does_not_introduce_authority_claims():
    parsed = parse_uploaded_receipt_file(Upload("aletheia_world_lens_receipt_2024.zip", _zip_payload()))
    _, view = parsed["views"][0]
    combined = "\n".join([
        view["core_logic_text"],
        view["summary"],
        view["non_certification_note"],
        view["parsing_limits"],
    ]).lower()

    assert "not as certification" in combined
    assert "human review remains required" in combined
    for forbidden in ["certifies", "approves", "rejects", "enforces", "final truth claim"]:
        assert forbidden not in combined


def test_patch_142_7_manifest_and_recovery_note_exist():
    root = Path(__file__).resolve().parents[1]
    assert (root / "PATCH_142_7_MANIFEST.txt").exists()
    assert (root / "PATCH_142_7_RECOVERY_NOTE.md").exists()
