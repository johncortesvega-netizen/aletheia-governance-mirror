# PATCH 71.4 RECOVERY NOTE — Stress Test Missing-Safeguard Verdict Enforcement

If Patch 71.4 must be reverted, restore these files from the last known working state after Patch 71.3:

- `app.py`
- `protocol.py`
- `tests/test_patch_71_4_missing_safeguard_verdict_enforcement.py`
- `PATCH_STATUS.md`
- `docs/progress_database.md`

## What this patch changed

Patch 71.4 adds a final Stress Test guard so explicit missing-safeguard language cannot be displayed or receipted as green SANCTUARY/Low.

The target scenario is:

> An automated welfare triage system reduces waiting times but lacks explainability, independent challenge, and human override during hardship cases.

After this patch, that pattern should route to:

- Protocol-adjusted state: `THRESHOLD`
- Risk: `Medium`
- Protocol label: `Missing Safeguard Negation / Needs Safeguards`
- Trust/alignment: capped below perfect values
- Ego/friction/collapse pressure: non-zero
- Repair questions: present

## Boundary preservation

This patch does not give ALETHEIA authority. It remains a local mirror only:

- Authority claim: `False`
- Human review required: `True`
- Public ledger: `False`
- Global ID sync: `False`
- Central storage: `False`
- Dataflow boundary: `Power -> Mirror. Never Mirror -> Power.`

## Validation

Run:

```bat
tools\run_patch_checks.bat 71_4
```

Then optionally run the regular suite:

```bat
tools\run_checks.bat
```

Known unrelated full-suite collection issues may still exist if legacy helper imports are unresolved.
