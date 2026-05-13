# ALETHEIA — Hosting Limits and Local-First Use

Patch 104 adds a clearer hosted-use boundary so public users do not mistake the hosted Streamlit demo for a privacy guarantee.

## Plain statement

ALETHEIA is local-first by design, but a hosted deployment is still hosted infrastructure.

The repository is designed without built-in telemetry, analytics SDKs, trackers, backend upload endpoints, Global ID sync, public ledger sync, or central user-input storage. Inputs are processed in the active app session and receipts are user-held downloads.

For sensitive audits, run ALETHEIA locally.

## Hosted-use caveat

When ALETHEIA is deployed on Streamlit Cloud or another platform, that platform may maintain server logs, access logs, request metadata, crash logs, infrastructure monitoring, rate-limit records, or operational diagnostics outside ALETHEIA's application code.

Those platform-level systems are not controlled by ALETHEIA and are not reviewed by ALETHEIA's repository tests.

## Streamlit-specific practical limits

Streamlit is useful for fast, accessible, Python-based review tools, but it has practical constraints:

- session state can reset or behave differently across deployments;
- free or shared hosting can have compute, memory, sleeping, or timeout limits;
- complex dashboards may work better on desktop than mobile;
- Streamlit does not by itself make a production authentication, compliance, or privacy regime;
- hosting providers may have infrastructure logs outside the app code;
- public demos are best treated as light review surfaces, not sensitive-data environments.

## Recommended use

Use the hosted app for public examples, non-sensitive text, demonstration, learning, and light review.

Use the local repository for sensitive audits:

```bash
git clone https://github.com/johncortesvega-netizen/aletheia-governance-mirror.git
cd aletheia-governance-mirror
pip install -r requirements.txt
streamlit run app.py
```

## Boundary language to use

Use:

> ALETHEIA is local-first by design. The repository includes no built-in telemetry, analytics SDKs, backend upload endpoint, public ledger sync, Global ID sync, or central user-input storage. For sensitive audits, run it locally. Hosted deployments may have platform-level logs outside ALETHEIA's code boundary.

Avoid:

> All processing always happens only on your device.

Avoid:

> No infrastructure can ever log anything.

Avoid:

> Hosted use is fully private by guarantee.

## Boundary preserved

This document does not add authentication, telemetry, storage, external calls, model calls, hosting integrations, or privacy certification. It makes the existing privacy/local-first boundary easier to understand.


This is not a privacy guarantee. Human review remains required.
