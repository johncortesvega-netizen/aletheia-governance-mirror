# How to Review ALETHEIA Without Trusting ALETHEIA

ALETHEIA's anti-capture posture should be inspected, not accepted on faith. This guide gives reviewers a direct path to challenge the project.

## 1. Clone and run locally

Run ALETHEIA locally before sensitive work:

```bash
git clone <repo-url>
cd aletheia-governance-mirror
pip install -r requirements.txt
streamlit run app.py
```

Local use lets you inspect files, receipts, and network behavior in your own environment.

## 2. Inspect telemetry, storage, and network claims

Search the repository for terms such as:

```text
telemetry
analytics
tracking
requests
http
backend upload
public ledger
Global ID
database
```

Confirm whether the implementation matches the public claim: no built-in telemetry, no analytics SDK, no backend upload endpoint, no public ledger sync, no Global ID sync, and no central user-input database in ALETHEIA's application code. Hosted platforms may still have their own logs.

## 3. Run the protocol baseline self-audit

```bash
python tools/run_protocol_baseline_self_audit.py
```

The self-audit compares watched files to the local baseline manifest. It is not a security guarantee, tamper-proof control, certification, automated approval, or final truth claim. Any difference is a human-review prompt.

## 4. Compare local receipts across repeated runs

Run the same input twice, download receipts, and compare:

- scenario hash;
- processed scenario hash;
- document fingerprint;
- audit receipt hash;
- verdict signal;
- metrics;
- repair questions;
- authority-boundary section.

Differences should be inspected by a person.

## 5. Inspect receipt boundaries

Every receipt should preserve local witness boundaries:

- user-held receipt;
- no public ledger;
- no Global ID sync;
- no central storage;
- no authority claim;
- human review required.

## 6. Review signal rules and heuristic maps directly

Inspect the module code and docs for signal definitions. Rule-based detection is transparent and reviewable, but bounded. It can miss irony, cultural context, coded language, long context, or unsupported languages.

## 7. Upload known test scenarios

Use inputs where you already know the risk pattern. Check whether ALETHEIA's reading is plausible, overconfident, under-sensitive, or wrong. Record false positives and false negatives.

## 8. Check that outputs avoid authority claims

ALETHEIA output should not certify, approve, reject, enforce, govern, punish, gatekeep, or claim final truth. If a module appears to do that, treat it as a defect.

## 9. Review World Lens source and coverage notes

For World Lens, inspect coverage, trust-prior notes, raw trust survey availability, WGI/V-Dem coverage, selected-year seats, and evidence-table CSVs. Do not treat World Lens as a country certification or government rating.

## 10. Report concerns

Open an issue or write a review note describing:

- the file/module inspected;
- the input used;
- the observed output;
- why it may violate mirror-not-throne boundaries;
- whether it is a behavior, documentation, UX, or repo-hygiene concern.

## Review stance

ALETHEIA reflects. Humans review. Power stays accountable.

Do not trust the statement. Inspect whether the repository, app, receipts, and tests behave that way.
