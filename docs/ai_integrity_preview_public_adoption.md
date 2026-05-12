# ALETHEIA v1.0 AI Integrity Preview — Public Adoption Package

Patch 100 stabilizes the public-facing AI Integrity line introduced through patches 85-99. It is a release-surface package, not a new authority layer.

## Purpose

The AI Integrity Preview helps reviewers paste AI outputs, prompts, agent specs, model-card excerpts, policy claims, batch artifacts, and code snippets into ALETHEIA for static artifact-level review.

It is designed for teams, educators, researchers, community reviewers, and builders who need a readable first-pass mirror for authority pressure, weak review paths, opacity, surveillance or identity-capture language, unsafe code markers, privacy-boundary tension, and repair questions.

## What is included

- AI Integrity Mirror static artifact review.
- Signal categories and redacted evidence snippets.
- Privacy boundary visibility and Privacy Boundary Audit Panel.
- Code Integrity Static Scan v1.
- Batch Review for delimiter-separated artifacts.
- AI Integrity Comparison View for side-by-side artifact readings.
- Red Team Prompt Pack v1 for manual/static testing.
- AI Integrity Report Builder v1 for compact human-review reports.
- Ready-to-use demo files in `examples/ai_integrity/`.

## Suggested first-use path

1. Start with `docs/ai_integrity_mirror.md` to understand the boundary.
2. Open `docs/ai_integrity_demo_pack.md` and paste one demo artifact into AI Integrity Mirror.
3. Use `examples/ai_integrity/batch_demo_v1.txt` to test batch mode.
4. Use `docs/ai_integrity_red_team_prompt_pack.md` to manually collect model outputs elsewhere, then paste those outputs into ALETHEIA.
5. Use the Report Builder output as a compact review packet for discussion.

## Review boundary

ALETHEIA reflects artifact-level risk signals for human review. It does not call live models, benchmark live models, crawl repositories, rank vendors, certify AI systems, certify code safety, prove privacy, guarantee truth, guarantee security, approve deployment, or enforce decisions.

Human review, domain expertise, legal review, medical review, security testing, privacy assessment, and deployment decisions remain outside ALETHEIA.

## Privacy boundary

This repository contains no built-in telemetry, trackers, analytics SDKs, backend upload endpoint, public ledger sync, Global ID sync, or central user-input database. Inputs are processed in the running app session and exports are user-held downloads.

Third-party hosting layers may still have their own access logs, server logs, analytics, or infrastructure telemetry outside ALETHEIA's application-code boundary. Public deployments should review the host as well as this repository.

## Release-readiness checklist

Before sharing a public build, run a practical smoke check:

```bat
tools\run_patch_checks.bat 100
tools\run_patch_checks.bat 99
tools\run_patch_checks.bat 98
tools\run_patch_checks.bat 97
tools\run_patch_checks.bat 96
tools\run_patch_checks.bat 95
```

Also verify that README, About, docs, examples, and receipts still preserve the core line:

> ALETHEIA reflects. Humans review. Power stays accountable.
