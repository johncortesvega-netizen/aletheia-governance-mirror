# ALETHEIA PATCH 19A RECOVERY NOTE

Patch: 19A  
Name: Mirror Check Calibration Scenario Pack  
Type: Diagnostic tests only

## Intent

Add a reviewable calibration pack before changing Mirror Check logic.

This patch documents what ALETHEIA should do for known scenario bands:

- Sanctuary
- Threshold
- Asylum
- Out of scope

It also adds a multi-phrase calibration prompt helper so reviewers can test many phrases at once without changing production app behavior.

## Touched files

- `calibration/mirror_check_scenarios.py`
- `tests/test_mirror_check_calibration_scenarios.py`
- `PATCH_19A_RECOVERY_NOTE.md`

## Do not touch

- `app.py`
- `protocol.py`
- `core/scoring.py`
- `core/simulation.py`
- `core/parser.py`
- `core/witness.py`
- `core/empirical.py`
- verdict logic
- scoring formulas
- witness hashing
- UI flow

## Why xfail is used

The calibration target test is marked `xfail(strict=False)` on purpose.

That means known calibration gaps are visible as expected diagnostic gaps, but they do **not** turn the normal test screen red. Patch 19B can then fix the logic and later convert these diagnostic expectations into strict passing tests.

## How to test many phrases at once

Use `parse_calibration_prompt_block(...)` from `calibration/mirror_check_scenarios.py`.

Supported formats:

```text
1. First scenario.
2. Second scenario.
```

or:

```text
First scenario.
---
Second scenario.
```

## Validation

```bash
python -m py_compile app.py protocol.py core/scoring.py core/parser.py core/witness.py core/empirical.py calibration/mirror_check_scenarios.py
python -m pytest tests -q
```

## Rollback

Remove:

- `calibration/mirror_check_scenarios.py`
- `tests/test_mirror_check_calibration_scenarios.py`
- `PATCH_19A_RECOVERY_NOTE.md`

No production rollback should be needed.
