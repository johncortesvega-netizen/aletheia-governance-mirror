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

COVERAGE_CSV = "source,rows_present,rows_missing,coverage\nTrust raw survey,0,172,0.0\nTrust prior,172,0,1.0\n"
LARGEST_ALLOCATIONS_CSV = "country,iso3,seats,integrity,collapse_probability\nIndia,IND,1584,0.41,0.46\nUnited States,USA,377,0.685,0.202\n"


class Upload:
    def __init__(self, name: str, payload: bytes):
        self.name = name
        self._payload = payload

    def getvalue(self) -> bytes:
        return self._payload


def _world_lens_bundle_payload() -> bytes:
    payload = io.BytesIO()
    with zipfile.ZipFile(payload, "w") as archive:
        archive.writestr("aletheia_world_lens_receipt_2024.md", WORLD_LENS_RECEIPT_MD)
        archive.writestr("aletheia_world_lens_receipt_2024_summary.json", WORLD_LENS_SUMMARY_JSON)
        archive.writestr("aletheia_world_lens_receipt_2024_coverage.csv", COVERAGE_CSV)
        archive.writestr("aletheia_world_lens_receipt_2024_largest_allocations.csv", LARGEST_ALLOCATIONS_CSV)
    return payload.getvalue()


def test_world_lens_zip_is_evidence_bundle_not_multi_receipt_batch():
    parsed = parse_uploaded_receipt_file(Upload("aletheia_world_lens_receipt_2024.zip", _world_lens_bundle_payload()))

    assert parsed["kind"] == "batch_zip"
    assert parsed["bundle_type"] == "world_lens_evidence_bundle"
    assert parsed["receipt_count"] == 1
    assert parsed["distribution"] == {"WORLD_LENS_EVIDENCE_VIEW": 1}

    first_name, first_view = parsed["views"][0]
    assert first_name == "aletheia_world_lens_receipt_2024.md"
    assert "summary" not in first_name.lower()
    assert first_view["module_family"] == "World Lens"
    assert first_view["fields"]["integrity"] == "0.446"
    assert first_view["fields"]["friction"] == "0.306"
    assert first_view["fields"]["collapse_probability"] == "0.443"


def test_world_lens_bundle_keeps_summary_and_csv_as_supporting_evidence():
    parsed = parse_uploaded_receipt_file(Upload("aletheia_world_lens_receipt_2024.zip", _world_lens_bundle_payload()))
    details = parsed["bundle_details"]

    assert len(details["summary_files"]) == 1
    summary = details["summary_files"][0]
    assert summary["filename"] == "aletheia_world_lens_receipt_2024_summary.json"
    assert summary["selected_year"] == 2024
    assert summary["active_selected_year_seats"] == 9000
    assert summary["trust_raw_coverage"] == 0.0
    assert summary["trust_prior_coverage"] == 1.0

    tables = {table["filename"]: table for table in details["evidence_tables"]}
    assert "aletheia_world_lens_receipt_2024_coverage.csv" in tables
    assert "aletheia_world_lens_receipt_2024_largest_allocations.csv" in tables
    assert tables["aletheia_world_lens_receipt_2024_coverage.csv"]["row_count"] == 2
    assert tables["aletheia_world_lens_receipt_2024_largest_allocations.csv"]["preview_rows"][0]["country"] == "India"


def test_world_lens_evidence_bundle_does_not_claim_certification_or_rescore():
    parsed = parse_uploaded_receipt_file(Upload("aletheia_world_lens_receipt_2024.zip", _world_lens_bundle_payload()))
    _, view = parsed["views"][0]
    combined = "\n".join([
        view["core_logic_text"],
        view["summary"],
        view["non_certification_note"],
        view["parsing_limits"],
    ]).lower()

    assert "not as certification" in combined
    assert "human review remains required" in combined
    for forbidden in ["certifies", "approves", "rejects", "enforces", "official authority", "final truth claim"]:
        assert forbidden not in combined


def test_patch_142_8_manifest_and_recovery_note_exist():
    root = Path(__file__).resolve().parents[1]
    assert (root / "PATCH_142_8_MANIFEST.txt").exists()
    assert (root / "PATCH_142_8_RECOVERY_NOTE.md").exists()
