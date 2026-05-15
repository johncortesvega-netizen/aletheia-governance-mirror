# PATCH 31 RECOVERY NOTE — World Lens Empirical Alignment

## Purpose

Patch 31 aligns World Lens report packets with the newer ALETHEIA diagnostic language without pretending country-year empirical data is the same thing as Mirror Check policy/scenario text.

The important correction is:

- Evidence Lab empirical scoring **does feed World Lens**.
- World Lens remains an empirical country-year view.
- Mirror Check text diagnostics such as Cognitive Resilience, Education Defense, contextual capture, and hard-capture trace require policy/scenario text and are therefore explicitly marked as not assessed when only empirical country-year indicators are available.

## Files touched

- `core/empirical.py`
- `core_empirical.py`
- `app.py`
- `tests/test_patch_31_world_lens_empirical_alignment.py`
- `PATCH_31_RECOVERY_NOTE.md`

## Behavioral change

Empirical scored rows and World Lens report exports now include alignment/scope fields such as:

- `mirror_logic_version`
- `diagnostic_scope`
- `empirical_world_lens_connection`
- `scenario_text_diagnostic_scope`
- `scenario_text_scope_note`
- `cognitive_resilience_signal`
- `education_defense_signal`
- `hard_capture_trace`
- `empirical_capture_pressure_signal`
- `empirical_trust_gap_signal`
- `empirical_governance_risk_signal`
- `world_lens_interpretation_warning`

The text-scenario fields are explicit `not_assessed_*` values for country-year rows. This prevents silent disconnects while preserving the Evidence Lab → World Lens pipeline.

## Hard boundaries preserved

Patch 31 does **not** add:

- Global ID sync
- public ledger
- push-warning authority layer
- automatic enforcement
- centralized truth authority
- user/person classification as malicious

World Lens remains a mirror over empirical evidence, not an authority verdict.

## Test command

```cmd
set PYTHONPATH=.
python -m pytest tests/test_patch_31_world_lens_empirical_alignment.py -q
```

Expected:

```text
5 passed
```

## Recovery

If this patch causes problems, revert the five touched files above. The empirical scoring core remains based on the pre-existing WGI/V-Dem/trust/country-year pipeline; Patch 31 only adds scope labeling and empirical alignment fields.
