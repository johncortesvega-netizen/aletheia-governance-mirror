# Privacy Boundary

Patch 89 makes ALETHEIA's privacy-by-design boundary visible in the app, About page, README, and local project ledgers.

## Plain statement

ALETHEIA's repository includes no built-in telemetry, trackers, analytics SDKs, backend upload endpoint, public ledger sync, Global ID sync, or central user-input database.

Inputs are processed in the running app session. Receipts are user-held downloads. ALETHEIA does not intentionally collect, sell, transmit, or centrally store pasted text, uploaded files, AI Integrity artifacts, or generated receipts.

## Deployment caution

If ALETHEIA is deployed through a third-party host, that hosting layer may have its own server logs, access logs, crash logs, request metadata, or operational monitoring outside ALETHEIA's application code. Those host-level systems are not part of ALETHEIA's repository and should be reviewed before making public deployment claims.

## Boundary language to use

Use:

> Privacy by design: ALETHEIA includes no built-in telemetry, trackers, analytics SDKs, backend upload endpoint, public ledger sync, Global ID sync, or central user-input database. Inputs are processed in-session and receipts are user-held downloads.

Do not use:

> ALETHEIA can guarantee that no infrastructure, browser, network, or hosting provider logs anything.

## Why this matters

The privacy boundary supports adoption and trust without turning ALETHEIA into a certification authority. The promise is limited to the app code and repository design: local/session processing, no intentional collection, no tracking layer, no central storage, and no authority claim.

## Verification cues

Patch 89 includes static tests that check for the visible privacy language and scan Python application files for common telemetry, analytics, backend-upload, and external-call imports.

Boundary preserved: no scoring-math change, no verdict-routing change, no AI Integrity rubric change, no live model benchmarking, no external API integration, no repository crawler, no storage layer, no public ledger, no Global ID sync, no enforcement, no certification, and no authority claim.

## Verification command

```bat
tools\run_patch_checks.bat 89
```


## Patch 104 clarification: local-first, not hosted privacy guarantee

ALETHEIA is local-first by design. That means the repository/application boundary avoids built-in telemetry, analytics SDKs, trackers, backend upload endpoints, public ledger sync, Global ID sync, and central user-input storage.

This does **not** mean every hosted deployment can guarantee that no infrastructure logs exist. Streamlit Cloud or another hosting provider may maintain server logs, access logs, request metadata, crash logs, operational monitoring, or rate-limit records outside ALETHEIA's application code.

For sensitive audits, use the local repository. Treat hosted deployments as public-demo or light-review surfaces unless the hosting environment has been separately reviewed by humans.

Related documents:

- `docs/BOUNDARY.md`
- `docs/hosting_limits.md`


This is not a privacy guarantee. Human review remains required.
