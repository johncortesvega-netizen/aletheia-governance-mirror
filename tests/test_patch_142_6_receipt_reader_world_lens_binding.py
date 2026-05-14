from __future__ import annotations

import io
import zipfile

from ui.receipt_reader import parse_receipt_standard_view, parse_uploaded_receipt_file


WORLD_LENS_MIXED_RECEIPT = """
# ALETHEIA World Lens Receipt

## Scope

- Selected year: **2023**
- World Lens source state: **Full empirical scored master**
- Evidence allocation status: **full 9k evidence view**
- Allocated country rows: **172**
- Active selected-year seats: **9,000**

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

GENERIC LOCAL WITNESS RECEIPT FOLLOWS
Module: Simulation
Protocol label: Missing Safeguard Negation / Needs Safeguards
Protocol-adjusted state: THRESHOLD
Trust index: 0.8000
"""

STRESS_RECEIPT_JSON = '{"module":"Simulation","metrics":{"integrity":0.569,"friction":0.149,"collapse_probability":0.265,"trust_index":0.8,"alignment":0.78,"ego":0.15},"verdict":{"protocol_adjusted_state":"THRESHOLD","risk":"Medium","protocol_label":"Missing Safeguard Negation / Needs Safeguards"},"repair_questions":["Who can pause or review the executive power?"]}'


class Upload:
    def __init__(self, name: str, payload: bytes):
        self.name = name
        self._payload = payload

    def getvalue(self) -> bytes:
        return self._payload


def test_world_lens_receipt_binds_to_world_lens_section_not_embedded_simulation_fallback():
    view = parse_receipt_standard_view(WORLD_LENS_MIXED_RECEIPT)
    fields = view["fields"]
    world = view["world_lens_fields"]

    assert view["receipt_kind"] == "World Lens"
    assert view["module_family"] == "World Lens"
    assert view["native_state"] == "WORLD_LENS_EVIDENCE_VIEW"
    assert fields["module_source"] == "World Lens"
    assert fields["protocol_label"] == "full 9k evidence view"
    assert fields["protocol_label"] != "Missing Safeguard Negation / Needs Safeguards"
    assert fields["integrity"] == "0.447"
    assert fields["collapse_probability"] == "0.441"
    assert world["selected_year"] == "2023"
    assert world["active_selected_year_seats"] == "9,000"
    assert world["trust_raw_survey_coverage"] == "0.0"
    assert world["trust_prior_coverage"] == "1.0"
    assert len(world["taxonomy_distribution"]) == 3
    assert any(row["Metric"] == "Weighted Integrity" for row in view["metric_rows"])
    assert not any(row["Metric"] == "Trust Index" for row in view["metric_rows"])
    assert "not a Mirror Check scenario receipt" in view["plain_language_explanation"]


def test_batch_zip_uses_actual_receipts_not_batch_index_for_first_view():
    payload = io.BytesIO()
    with zipfile.ZipFile(payload, "w") as archive:
        archive.writestr("batch_index.txt", "Native State,Count\nTHRESHOLD,1\n")
        archive.writestr("receipt_01.txt", "Module: Simulation\nProtocol-adjusted state: THRESHOLD\nRisk: Medium\nProtocol label: Text fallback\n")
        archive.writestr("receipt_01.json", STRESS_RECEIPT_JSON)

    parsed = parse_uploaded_receipt_file(Upload("batch.zip", payload.getvalue()))
    assert parsed["kind"] == "batch_zip"
    assert parsed["receipt_count"] == 1
    first_name, first_view = parsed["views"][0]
    assert first_name == "receipt_01.json"
    assert first_view["fields"]["module_source"] == "Simulation"
    assert first_view["fields"]["protocol_label"] == "Missing Safeguard Negation / Needs Safeguards"
    assert first_view["fields"]["trust"] == "0.8000"


def test_receipt_reader_patch_142_6_keeps_boundary_language():
    view = parse_receipt_standard_view(WORLD_LENS_MIXED_RECEIPT)
    combined = "\n".join([
        view["plain_language_explanation"],
        view["non_certification_note"],
        view["core_logic_text"],
        view["summary"],
    ]).lower()
    for forbidden in ["certifies", "approves", "rejects", "enforces", "is final truth"]:
        assert forbidden not in combined
    assert "not certification" in combined
    assert "human review remains required" in combined
