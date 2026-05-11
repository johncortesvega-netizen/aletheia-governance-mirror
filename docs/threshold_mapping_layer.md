# Threshold Mapping Layer

Patch 72 adds a receipt-only mapping layer for THRESHOLD readings.

The canonical taxonomy remains:

```text
SANCTUARY / THRESHOLD / ASYLUM
```

The mapping layer does **not** create `THRESHOLD-` or `THRESHOLD+` as new verdicts. It records direction inside a THRESHOLD or boundary reading so the middle zone is less opaque.

## Purpose

The layer maps the movement between captured logic and distributed resilience:

- **Toward ASYLUM**: care, safety, access, or protection language is coupled to concentrated control, surveillance, weak correction, ID pressure, or a central truth gate.
- **Balanced THRESHOLD**: mixed governance pressure; neither capture nor distributed repair clearly dominates.
- **Toward SANCTUARY**: human review, appealability, transparency, distributed verification, and repair capacity outweigh central-control pressure.

## Receipt fields

The local witness receipt now includes:

- `threshold_mapping_layer.threshold_direction`
- `threshold_mapping_layer.z_axis_position`
- `threshold_mapping_layer.integrity_gap`
- `threshold_mapping_layer.repair_index`
- `threshold_mapping_layer.component_readings`
- `threshold_mapping_layer.asylum_pressure_signals`
- `threshold_mapping_layer.sanctuary_growth_signals`

The readable receipt prints this section between **Raw Metrics Before Ethics** and **Scanner Features**.

## Component readings

| Component | Threshold - pressure | Threshold + growth |
| --- | --- | --- |
| Power balance | Central truth gate or one-source-of-truth pressure | Distributed verification with multiple witnesses and inspectable evidence |
| Correction | No, weak, or non-time-bound appeal path | Open, time-bound appeal or review with human review |
| Access | Access or care conditional on behavior, ID, obedience, or surveillance | Basic needs protected without coercive access conditions |

## Boundary

This layer is descriptive only. It does not change scoring, verdict routing, receipt authority, storage, public ledger behavior, Global ID sync, central storage, or enforcement posture.

ALETHEIA remains a mirror, not a throne.
