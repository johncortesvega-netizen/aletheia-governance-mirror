# Patch 67.1 — Dutch Stress Test Lexicon + Threshold Receipt Enforcement

Patch 67.1 extends the Stress Test risk-sensitivity layer to Dutch governance scenarios.

## Problem

The English stress-test batch was correctly moved away from Sanctuary after Patch 66, but the Dutch version of the same scenario set was still too often classified as Sanctuary because the trigger lexicon was English-heavy.

## Fix

The Stress Test now recognizes Dutch governance-risk language for:

- noodbevoegdheden zonder einddatum or beroep
- biometrische identiteit tied to basisdiensten
- reputatiescores, gedragsscores, and automated labels
- ontbrekende data and fallback-waarde confusion
- geen audit-trail or geheim algoritme
- permanent verbannen, automatisch bevroren, or no correction path
- toestemming under practical pressure
- founder/oprichter or CEO control
- surveillance and indefinite data storage
- human review that cannot change the automated outcome

## Expected behavior

Dutch stress cases should become at least `THRESHOLD / Needs Safeguards` unless explicit safeguards are present.

For THRESHOLD outputs, ALETHEIA should add repair questions and prevent overly perfect trust/alignment metrics in the receipt layer.

For ASYLUM outputs, the stronger Asylum repair and metric calibration remains in place.

## Authority boundary

This patch does not add enforcement authority. The receipt boundary remains:

- Authority claim: False
- Human review required: True
- Public ledger: False
- Global ID sync: False
- Central storage: False

ALETHEIA reflects. People decide.
