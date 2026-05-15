# PATCH 27A — Cognitive Resilience Calibration Pack

## Status

Patch 27A is a diagnostic calibration-only patch.

It adds a 40-scenario Cognitive Resilience dataset and review tests without changing production logic.

No changes were made to:

- `core/scoring.py`
- `protocol.py`
- `core/ethics.py`
- `app.py`

## Added files

- `calibration/cognitive_resilience_scenarios.py`
- `tests/test_patch_27A_cognitive_resilience_calibration.py`
- `PATCH_27A_RECOVERY_NOTE.md`

## Dataset structure

The dataset contains 40 scenarios grouped into four groups of 10:

1. High Cognitive Resilience / Sanctuary Focus
2. Low Cognitive Resilience / Asylum Focus
3. High education + risky power / Threshold or Asylum
4. Safety/Objectivity Capture / Contextual Capture stress tests

## Expected behavior by group

### Group 1 — High Cognitive Resilience

These scenarios establish the positive baseline.

Expected direction:

- `cognitive_resilience_signal`: high
- `integrity`: high or not penalized
- `collapse_probability`: low
- `contextual_capture_count`: 0
- `grip_marker_count`: 0

Examples included:

- Repair guides shared through hobby meetings
- Open-source education
- Decentralized lab work
- Local radio without central editorial control
- Master-apprentice networks
- Question circles that train critical thinking

Important nuance:

High Cognitive Resilience only helps when the scenario remains local, open, revocable, appealable, and non-coercive.

### Group 2 — Low Cognitive Resilience

Expected direction:

- `cognitive_resilience_signal`: low
- `central_info_capture`: true
- friction / collapse risk should trend upward in later scoring patches

Examples included:

- Truth of the Day tablets
- Hobby bans
- Obedience-profile information feeds
- Archive rewriting
- Licensed speech
- Entertainment compliance

These should generally lean ASYLUM once logic is wired.

### Group 3 — Smart population, risky power

Expected direction:

High education must not wash away capture.

If no audit / no appeal / single keyholder / forced delegation exists:

- THRESHOLD or ASYLUM depending on severity

Examples included:

- Technocratic village governed by unauditable AI
- Open-source code but one private server keyholder
- Expert delegation forced by certification
- Enlightened dictator

Key rule:

High CR + central power / no audit / no appeal = still Threshold or Asylum.

### Group 4 — Safety/Objectivity Capture

This group is the immediate stress test for Patch 21 contextual capture.

Expected direction:

- `contextual_capture_count > 0`
- `ethics_adjustment applied: True`
- integrity lower than raw integrity
- friction / trust friction higher
- THRESHOLD or ASYLUM depending on severity

Examples included:

- “Objectivity” filter removes dissent
- Biometric control at bakery for fair distribution
- Private conversations monitored for mental-health safety and sent to police
- Mandatory inclusive ID
- Automated objectivity approval before posting
- Sport / health data forced into grid
- Protest avoidance for personal safety
- Universal digital currency replacing local currencies

Hard Asylum triggers:

- biometric access to food / basic needs
- private conversation surveillance sent to police
- mandatory digital ID for inclusion
- no appeal
- central truth gate
- survival conditioned on compliance

## Tags added

The calibration records use these tags:

- `#COGNITIVE_RESILIENCE_HIGH`
- `#COGNITIVE_RESILIENCE_LOW`
- `#EDUCATIONAL_DECENTRALIZATION`
- `#HOBBY_BASED_LEARNING`
- `#NO_TRUTH_GATEKEEPER`
- `#LOCAL_KNOWLEDGE_NETWORK`
- `#CENTRAL_INFO_CAPTURE`
- `#ARCHIVE_REWRITE`
- `#ENTERTAINMENT_COMPLIANCE`
- `#LICENSED_SPEECH`
- `#ALGORITHMIC_ISOLATION`
- `#SAFETY_CAPTURE`
- `#OBJECTIVITY_CAPTURE`
- `#BIOMETRIC_SURVIVAL_GATE`
- `#PRIVATE_CONVERSATION_SURVEILLANCE`
- `#CENTRALIZED_TRUTH_SCORE`
- `#RELINQUISH_REQUIRED`

## Diagnostic tests

The tests verify:

- 40 scenarios exist
- 10 scenarios exist per group
- IDs are unique and stable from `CR-01` through `CR-40`
- required tags are present
- Group 1 is a positive Sanctuary baseline
- Group 2 is central information capture / low CR
- Group 3 preserves the rule that high CR must not launder capture
- Group 4 is a contextual capture stress pack
- the existing ethics layer can score all scenarios without crashing
- current classifier agreement is documented with `xfail` because CR is not wired yet

## Do not implement yet

Do not yet add the full Cognitive Resilience scoring formula.

Do not yet modify:

- `core/scoring.py`
- `protocol.py`
- `core/ethics.py`
- `app.py`

unless absolutely needed for imports/tests.

## Later roadmap

### Patch 27B — Cognitive Resilience Diagnostic

Add:

- `cognitive_resilience_signal`
- `educational_decentralization_signal`
- `central_info_capture_signal`

Visible in local witness receipts.

No heavy scoring effect yet.

### Patch 28 — Educational Decentralization Scoring

Use CR lightly:

- High CR can stabilize only if no hard capture markers exist.
- Low CR or central truth-gate increases friction / collapse.

Do not let high CR sanitize coercive power.

### Patch 28.1 — Safety/Objectivity Capture Multiplier

Strengthen contextual capture when “safety,” “objectivity,” “fairness,” “inclusion,” or “public health” are paired with:

- mandatory ID
- biometrics
- surveillance
- no appeal
- central grid
- forced compliance
- private conversation monitoring
- access to food / mobility / health conditioned on compliance

## Design rule

Cognitive Resilience is a system property, not a judgment of people.

Use language like:

> This scenario offers strong information resilience.

Do not use language like:

> This population is smart/dumb.

## Closing rule

High Cognitive Resilience must never launder capture.

- High CR + local learning + open tools = safer.
- High CR + AI cannot be audited = still Asylum.
- Safety words + biometric enforcement = capture.
- Objectivity words + no appeal = capture.

Power → Mirror. Never Mirror → Power.
