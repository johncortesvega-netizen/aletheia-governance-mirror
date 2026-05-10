# Patch 66 — Stress Test Risk Sensitivity Calibration

Patch 66 raises Stress Test sensitivity for subtle governance-risk scenarios.

The Stress Test batch infrastructure was already working: it produced local Simulation receipts, kept authority claims false, required human review, and preserved local-only boundaries. The remaining issue was calibration: many stress scenarios with missing appeal, no term limits, biometric access pressure, forced consent, fallback-data confusion, founder control, surveillance, or no meaningful human review were still rendering as `SANCTUARY`.

## Rule

Stress Test should not treat a scenario as healthy merely because the raw simulation is numerically stable. If the scenario describes a governance-risk pattern without explicit safeguards, it should route to at least:

```text
THRESHOLD / Needs Safeguards
```

Hard capture patterns may still route to:

```text
ASYLUM / High
```

## Risk patterns added

Patch 66 adds soft stress-test sensitivity markers for:

- emergency power without limits
- predictive risk before action
- biometric or identity access pressure
- missing appeal or correction paths
- founder, CEO, board, token, or core-team control
- confidential criteria or proprietary decision systems
- consent under pressure
- vote-shaping, nudging, unity-pressure, or criticism suppression
- permanent emergency drift
- reputation, behavior, or civic scoring
- surveillance or indefinite data storage
- extraordinary authority claims
- blocked watchdogs or weak complaint paths
- fallback-data disclosure gaps
- population-weighting protection gaps
- civil-rights pause scenarios
- ethical language without mechanisms
- authority-boundary confusion
- family or community stability blind spots
- efficiency over appeal rights
- human review without power to correct the outcome

## Safe boundary

This patch does not make ALETHEIA an authority. It only changes the mirror signal.

Allowed language:

- Needs Safeguards
- Human review required
- Potential risk detected
- Repair questions required

Forbidden language:

- AI has decided
- Remove this leader
- Enforce this outcome
- Automatic reset required

## Expected batch effect

The official 50-scenario Stress Test baseline should now produce mostly `THRESHOLD` and `ASYLUM` outcomes rather than mostly `SANCTUARY` outcomes.

Expected distribution for the Patch 65 scenario batch after Patch 66:

```text
THRESHOLD: 46
ASYLUM: 4
SANCTUARY: 0
```

This is appropriate because the batch intentionally consists of governance stress scenarios, not healthy governance examples.
