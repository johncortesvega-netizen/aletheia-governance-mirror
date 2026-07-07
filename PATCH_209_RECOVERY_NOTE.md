# Patch 209 Recovery Note — Evidence Lab and World Lens Semantic Category Wiring

Patch 209 is a display/explanation integration patch.

It adds Evidence Lab and World Lens handling for semantic categories introduced during the Semantic Pressure Scanner v1 calibration sequence:
- opaque capture-power claims;
- emergency authority over essential services;
- weak emergency safeguards;
- algorithmic welfare/triage review gaps;
- biometric access pressure;
- procurement/vendor capture risk;
- weak or missing safeguards.

It does not change:
- semantic scanner scoring;
- Stress Test metrics;
- Evidence Lab source-table calculations;
- World Lens country-year math;
- receipt schemas;
- native receipt values;
- telemetry/storage/external-call posture;
- authority boundary.

Rollback:
Restore app.py and PATCH_STATUS.md from the previous commit or remove the Patch 209 block from semantic_evidence_implication_rows and semantic_world_lens_flag_rows.
