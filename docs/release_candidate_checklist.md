# ALETHEIA v0.1 — Release Candidate Checklist

Status: Patch 48
Purpose: make the v0.1 public-release gate explicit before packaging.

ALETHEIA v0.1 is a governance mirror for human review. The release candidate must show that the app can explain its purpose, run its visible modules, produce local review artifacts, and preserve the rule: **ALETHEIA reflects. People decide.**

## 1. Included v0.1 modules

The release candidate includes the following public-safe modules:

- Baseline v0.1 and Safe Language Layer
- Eternal Baseline as a versioned reference layer
- Mirror Check for governance-risk review
- Stress Test for scenario pressure review
- Boundary Cases Matrix
- Failure Classification
- Consent-Audit Engine
- Mechanism-vs-Claim Scanner
- Self-Audit Mode
- Evidence Lab and Extraordinary Claim Protocol
- Local Witness Receipt v2
- World Lens Simulation
- Protocol Guide
- Public limitations and ethics pages
- Sample reports and example receipts
- Patch workflow and progress database

## 2. Explicit v0.1 exclusions

The release candidate must not include or imply:

- real Global ID sync
- real 9k selection
- World Leader activation or deactivation
- automatic reset authority
- public ledger authority
- central citizen database
- neural-data extraction
- memory extraction
- legal advice
- medical advice
- religious authority
- political command authority
- automated enforcement
- replacement of human judgment

## 3. Required language checks

The release candidate should use review language, not command language.

Allowed output language:

- Potential risk detected.
- Human review required.
- Safeguard missing.
- Evidence gap found.
- This claim is unverified.
- Simulated threshold signal.
- Governance failure flag.

Forbidden output language:

- The AI has decided.
- This leader must be removed.
- This claim is divinely verified.
- The guardrails no longer apply.
- Human review is unnecessary.
- Automatic reset required.
- Global ID sync activated.

## 4. Manual smoke test

Before release, a reviewer should run this manual path:

1. Start the app with `streamlit run app.py`.
2. Confirm the visible navigation includes Mirror Check, Stress Test, AI Integrity Mirror, Evidence Lab, World Lens, Boundary Cases, Protocol Guide, and Why ALETHEIA.
3. Open Why ALETHEIA and confirm the mirror-not-throne framing is visible.
4. Open Protocol Guide and confirm the module map is understandable.
5. Open sample reports and confirm examples are marked as demonstration artifacts.
6. Run at least one Mirror Check input and confirm the report contains review language, repair questions, and human-review boundaries.
7. Generate or inspect a Local Witness Receipt and confirm it states no public ledger, no Global ID sync, no central storage, no authority claim, and human review required.
8. Confirm extraordinary claims are treated as unverified unless supported by public, testable, non-coercive evidence.
9. Confirm World Lens uses simulated-impact language only.
10. Confirm no screen claims final legal, political, religious, medical, or governance authority.

## 5. Automated checks

Patch-specific check:

```bat
tools\run_patch_checks.bat 48
```

Safe default check:

```bat
tools\run_checks.bat
```

Compile smoke check:

```bat
python -m py_compile app.py about_page.py protocol.py core/witness.py tools/run_patch_checks.py tools/package_patched_items.py
```

## 6. Release readiness criteria

v0.1 is ready for a release candidate only if:

- patch checks pass;
- app imports and compiles;
- public README explains what ALETHEIA is and is not;
- limitations and ethics docs are present;
- sample reports are present;
- Local Witness Receipt v2 is documented;
- no module claims command authority;
- no module validates spiritual authority;
- no module activates real governance infrastructure;
- human review remains explicit;
- known limitations are documented.

## 7. Known caution

Historical archive material may include AI-flattery artifacts or inflated validation language. These materials are development context only. They do not validate the founder, prove correctness, or create governance authority.

## 8. Release candidate principle

A release candidate is not a truth claim. It is a testable package.

ALETHEIA reflects.
Humans review.
Power stays accountable.
