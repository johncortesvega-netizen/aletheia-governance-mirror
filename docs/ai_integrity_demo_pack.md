# AI Integrity Batch Demo Pack

Patch 93 adds ready-to-use static demo artifacts for AI Integrity Mirror reviewers.
The files live in `examples/ai_integrity/` and can be copied into the AI Integrity Mirror
single-artifact or batch review input.

## Files

| File | Review focus |
|---|---|
| `examples/ai_integrity/bounded_ai_answer.txt` | Bounded answer with human review, uncertainty, appeal, and limits |
| `examples/ai_integrity/authority_overclaim.txt` | Final-authority, certification-overclaim, no-appeal language |
| `examples/ai_integrity/opaque_agent_workflow.txt` | Hidden criteria, weak explainability, automated denial, missing review paths |
| `examples/ai_integrity/code_secret_example.txt` | Credential-like strings, dynamic execution, shell/network markers |
| `examples/ai_integrity/central_identity_capture_claim.txt` | Global ID, biometric tracking, central registry, continuous monitoring, blacklist pressure |
| `examples/ai_integrity/batch_demo_v1.txt` | Separator-delimited multi-artifact demo for batch mode |

## How to use

1. Open the AI Integrity Mirror tab.
2. Paste one example file into the text area, or paste `batch_demo_v1.txt` with batch mode enabled.
3. Review the risk reading, signal categories, redacted evidence snippets, repair questions, and receipt text.

## Boundary

These examples are demo inputs only. They are not AI certification, model approval,
vendor approval, benchmark proof, safety guarantee, truth detection, legal advice,
medical advice, security audit, enforcement, or official review.

Patch 93 does not change analyzer scoring, signal patterns, signal weights, verdict routing,
UI behavior, receipt generation, or privacy architecture. It adds static docs, examples,
and tests only.

ALETHEIA's repository still includes no built-in telemetry, trackers, analytics SDKs,
backend upload endpoint, public ledger sync, Global ID sync, or central user-input database.
No live model calls, external calls, repository crawler, storage layer, enforcement,
vendor ranking, model certification, approval, or final safety claim is introduced.

## Verification

```bat
tools\run_patch_checks.bat 93
tools\run_patch_checks.bat 92
tools\run_patch_checks.bat 91
tools\run_patch_checks.bat 90
tools\run_patch_checks.bat 89
tools\run_patch_checks.bat 88
tools\run_patch_checks.bat 87
tools\run_patch_checks.bat 86
tools\run_patch_checks.bat 85
```
