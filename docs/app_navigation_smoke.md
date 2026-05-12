# Patch 47 — App Navigation + Smoke Test Cleanup

## Purpose

Patch 47 makes the visible app path explicit and testable.

The app should expose the v0.1 mirror stack in a stable order:

1. Mirror Check
2. Stress Test
3. Boundary Cases
4. AI Integrity Mirror
5. Evidence Lab
6. World Lens
7. Protocol Guide
8. Why ALETHEIA

## Navigation Rule

Every tab reflects, explains, stress-tests, or documents.

No tab may command, enforce, validate spiritual authority, replace legal review, replace human judgment, activate Global ID, select a real 9k, remove a leader, issue an automatic reset, or make final governance decisions.

## Module Map

| Tab | Purpose |
|---|---|
| Mirror Check | Document and proposal review for capture risk, safeguards, repair questions, and local witness receipts. |
| Stress Test | Scenario simulation for stability, trust, alignment, ego pressure, grievances, friction, safeguards, and collapse risk. |
| Boundary Cases | Ethical edge-case calibration for consent, free agency, basic rights, reset misuse, ambient capture, and self-audit scenarios. |
| AI Integrity Mirror | Static review of pasted AI outputs, prompts, agent specs, and code snippets for authority-boundary and governance-integrity risk. |
| Evidence Lab | Evidence status, public-data audit support, and the Extraordinary Claim Protocol for unverified exceptional claims. |
| World Lens | Non-sovereign population-impact simulation and selected-year comparison using simulated threshold language only. |
| Protocol Guide | Consolidated v0.1 module map, safe-language rules, shared protocol state, and limitations. |
| Why ALETHEIA | Public-facing explanation of the project, the Eternal Baseline, module purpose, limitations, and research direction. |

## Smoke Test Scope

Patch 47 does not add new governance authority or new doctrine. It hardens UI discoverability and confirms the main app files still compile after the navigation update.

The patch-specific check is:

```bat
tools\run_patch_checks.bat 47
```

The safe full local check remains:

```bat
tools\run_checks.bat
```
