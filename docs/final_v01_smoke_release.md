# ALETHEIA v0.1 — Final Smoke Release

Status: Patch 53
Purpose: final release-level smoke check before public v0.1 packaging.

## Release smoke boundary

This document verifies that the v0.1 release package is internally coherent and still framed as a governance mirror for human review. It does not add new doctrine, no scoring authority, no governance authority, no Global ID sync, no real 9k selection, no World Leader logic, no automatic reset, no public ledger, no neural validation, no religious validation, no legal authority, no medical authority, or no automated enforcement.

Core line:

> ALETHEIA reflects. Humans review. Power stays accountable.

## Required release materials

The release smoke check expects these materials to exist:

- `README.md`
- `docs/baseline_v01.md`
- `docs/eternal_baseline.md`
- `docs/protocol_guide.md`
- `docs/limitations.md`
- `docs/ethics.md`
- `docs/public_release_notes.md`
- `docs/v01_release_package.md`
- `docs/release_candidate_checklist.md`
- `docs/sample_reports.md`
- `docs/patch_workflow.md`
- `docs/progress_database.md`
- `PATCH_STATUS.md`

## Required examples

The release smoke check expects these examples to exist:

- `examples/example_policy_audit.md`
- `examples/example_boundary_case.md`
- `examples/example_self_audit.md`
- `examples/example_witness_receipt.md`

## Required developer workflow

The release smoke check expects these commands to remain available:

```bat
tools\run_checks.bat
tools\run_patch_checks.bat 53
```

The safe default check should run current maintained patch tests and compile checks, then report legacy inventory as non-blocking.

## Safe-language constraints

Release-facing language may say:

- potential risk detected
- human review required
- safeguard missing
- evidence gap found
- this claim is unverified
- simulated threshold signal
- local witness receipt

Release-facing language must not claim that ALETHEIA can:

- decide with final authority
- remove leaders
- validate spiritual authority
- replace human judgment
- activate Global ID
- run a real 9k selection
- trigger an automatic reset
- operate a public ledger
- perform neural validation
- enforce policy

## Final v0.1 smoke checklist

Before calling the package v0.1-ready, confirm:

1. Patch 53 test passes.
2. `tools\run_checks.bat` passes.
3. The app starts with `streamlit run app.py`.
4. Navigation exposes Mirror Check, Stress Test, Boundary Cases, Evidence Lab, World Lens, Protocol Guide, and Why ALETHEIA.
5. Examples can be opened and reviewed.
6. README explains what ALETHEIA is and what it is not.
7. Limitations and ethics pages are visible.
8. Local witness receipt language remains local-only and non-authoritative.
9. Legacy tests are documented rather than silently ignored.
10. No release document frames ALETHEIA as a throne.

## Final release interpretation

A responsible reading is:

> This model suggests a governance-risk pattern worth examining.

Not:

> This model has final authority.
