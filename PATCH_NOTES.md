# Patch S2 — Semantic Integration for Stress Test + Evidence Lab

Changed file:
- `app.py`

## What changed

### Stress Test
- Added semantic-derived stress triggers for Scan-my-idea runs.
- The semantic scanner now translates language relationships into review questions, without changing Stress Test metrics or internal taxonomy labels.
- New expander after Repair Questions:
  - `Semantic stress triggers — subordinate to Stress Test`
- Detects and explains:
  - identity-gated access
  - grip language near access/basic-service terms
  - soft claims without concrete safeguards
  - obligation/permanence outweighing reversibility
  - visible safeguards that still require operational verification

### Evidence Lab
- Added an optional top expander:
  - `Semantic claim/mechanism evidence check`
- Lets the user paste a claim/policy sentence and get:
  - semantic pressure panel
  - claim/mechanism counts
  - evidence implications
  - human-review questions
- Does not score or alter the country-year empirical table.

## Boundary rule
The semantic scanner remains subordinate. It does not certify, approve, reject, enforce, or replace the module reading.

## Syntax check
Passed:
```bash
python -m py_compile app.py
```
