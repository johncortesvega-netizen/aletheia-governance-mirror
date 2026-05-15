# ALETHEIA Reviewer Quick Start

This is the 5-minute path for a first-time reviewer. It is designed to make ALETHEIA easier to inspect without asking you to trust ALETHEIA.

## 1. Read the 60-second boundary

Start at the top of `README.md`:

> ALETHEIA is a mirror, not a throne. It shows governance-risk signals for human review — nothing more.

That sentence is the project boundary. If a module, receipt, or document appears to turn ALETHEIA into a decider, certification engine, enforcement system, or final authority, treat that as a review concern.

## 2. Open the app through Aletheia Unit Preview

Aletheia Unit Preview is the app-side front door. It helps new users decide whether to use Mirror Check, Stress Test, AI Integrity Mirror, Evidence Lab, World Lens, or Receipt Reader before entering the full work surface.

## 3. Pick one review path

Do not try to inspect everything at once. Choose one path:

- **Mirror Check:** governance text, authority drift, appealability, and capture pressure.
- **Stress Test:** scenario pressure and safeguard review.
- **AI Integrity Mirror:** static AI artifacts only, not live models or vendors.
- **World Lens:** selected-year country evidence views, not country certification.
- **Receipt Reader:** uploaded ALETHEIA receipts in Standard View without rescoring.

## 4. Run locally for sensitive review

```bash
python -m venv .venv
. .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
streamlit run app.py
```

The repository is designed without built-in telemetry, trackers, analytics SDKs, backend upload endpoints, public ledger sync, Global ID sync, or central user-input storage. Hosted deployments can still have platform-level logs outside ALETHEIA's application-code boundary.

## 5. Inspect one receipt

Download a receipt from one module, then check:

- `NOTICE`
- `AUTHORITY BOUNDARY`
- `VERDICT SIGNAL`
- `CORE METRICS`
- `MACHINE-READABLE RECEIPT JSON`
- repair or human-review questions

Receipt Reader may translate the receipt into Standard View. It must not rescore, override, regenerate, or merge verdicts.

## 6. Review the limits before trusting numbers

Read `docs/validation_and_precision.md`. Numerical readings are internal review aids, not independent validation, certification, or final truth. Decimal precision supports repeatability and receipt comparison; it is not a claim of scientific certainty.

## 7. Review without trusting

Use `docs/how_to_review_aletheia_without_trusting_it.md` for direct checks: local run, no-telemetry review, protocol baseline self-audit, receipt comparison, signal-rule inspection, and boundary inspection.

ALETHEIA reflects. Humans review. Power stays accountable.
