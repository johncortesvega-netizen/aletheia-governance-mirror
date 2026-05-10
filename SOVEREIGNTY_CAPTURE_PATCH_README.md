# ALETHEIA Sovereignty Capture Patch

This is a small, targeted patch for the working beta module logic.

## Files included

Replace these files in your project:

```text
core/parser.py
core/ethics.py
protocol.py
```

Optional test file:

```text
tests/test_sovereignty_capture.py
```

## What this fixes

The previous working beta correctly applied Sydney Protocol guardrails, but the local scanner underweighted phrases like:

```text
human takes over planet and brings in democracy under his rule
```

That scenario produced high raw simulation integrity, while the scanner only reported moderate power concentration.

This patch adds stronger detection for:

- planetary takeover
- personal sovereignty capture
- democracy subordinated to one ruler
- "under his/her/their rule"
- "human/person/man takes over"
- "takes over the world/planet"

## Expected behavior

For:

```text
human takes over planet and brings in democracy under his rule
```

Expected result:

```text
power_concentration >= 0.90
decision_transparency <= 0.32
regulatory_presence <= 0.28
ethics verdict: ETHICALLY HIGH-RISK
final protocol verdict: ASYLUM
stress label: Subordinate Democracy / Personal Rule Capture
```

## What this patch intentionally does NOT change

- app.py
- empirical modules
- Streamlit layout
- requirements.txt
- witness report formatting

This keeps the working beta module structure intact while strengthening capture-language logic.
