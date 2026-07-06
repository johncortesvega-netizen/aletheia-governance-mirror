# Patch S2.1 — Stress Test compact layout

Changed file:
- `app.py`

## What changed
- Stress Test primary reading now stays visually above detailed diagnostic machinery.
- Secondary metrics, tree visual, stability/trust/alignment plot, action chart, and test voices table are now inside a collapsed expander:
  - `Stress Test visuals and agent traces`
- Added a caption clarifying that the visuals are diagnostic only and do not create a separate decision or authority claim.

## What did not change
- No Stress Test scoring changes.
- No semantic scanner logic changes.
- No receipt schema changes.
- No Mirror Check / Evidence Lab changes.

## Expected UI effect
After running a Stress Test, the user should see:
1. Protocol reading and main metrics
2. Why this result?
3. Repair questions
4. Semantic pressure signals
5. Optional visuals in a collapsed expander

This keeps the human-review path visible first and hides the machinery until requested.
