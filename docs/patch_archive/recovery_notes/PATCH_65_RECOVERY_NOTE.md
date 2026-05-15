# Patch 65 — Stress Test Prompting Guide + Batch Baseline

Status: Ready for local verification.

Patch 65 adds a Stress Test prompting guide, a 50-scenario Stress Test batch baseline, and an explicit local-only Stress Test batch runner in the Simulation tab.

The patch is diagnostic only:

- no public ledger
- no Global ID sync
- no central storage
- no authority claim
- no automated enforcement
- human review remains required

Check:

```bat
tools\run_patch_checks.bat 65
```
