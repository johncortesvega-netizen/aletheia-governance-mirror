# Patch 95 — Code Integrity Static Scan v1

Patch 95 adds a deterministic **Code Integrity Static Scan** layer inside the AI Integrity Mirror. It reviews pasted code snippets for code-specific integrity signals without executing the code and without changing AI Integrity scoring math or verdict routing.

## What it can flag

The static scan can flag review signals for:

- exposed secrets, tokens, passwords, API keys, client secrets, and private-key blocks
- dangerous subprocess, shell execution, `eval`, `exec`, and `os.system` usage
- hardcoded admin bypass or skipped authorization/review markers
- unsafe file deletion patterns such as recursive removal or direct unlink/remove calls
- outbound network calls and request/fetch-like data-flow markers
- telemetry-like endpoints, analytics packages, tracking keywords, or usage-event logging
- central logging, Global ID, biometric sync, central registry, or identity-sync hints
- missing human-review gates in automated decision or enforcement code

## Output

The scan returns review metadata such as:

- `scan_mode: Code Integrity Static Scan`
- `code_integrity_scan_version: code-integrity-static-scan-v0.1`
- detection count
- severity counts
- category counts
- redacted evidence snippets
- code review questions
- whether automated decision code appears to lack a human-review gate

## Boundary

This is a **static pasted-code review aid** only. It does not execute code, crawl repositories, resolve dependencies, call external services, run live models, perform a penetration test, guarantee security, certify vulnerabilities, approve compliance, or prove that code is safe.

Patch 95 preserves the ALETHEIA boundary: mirror, not throne. The scan surfaces review pressure for human reviewers; it does not enforce action or replace a security review.
