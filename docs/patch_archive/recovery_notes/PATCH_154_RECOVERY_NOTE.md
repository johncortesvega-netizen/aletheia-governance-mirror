# PATCH 154 RECOVERY NOTE — Unit Preview Start Here Nested Review Expanders

Patch 154 is a UI/copy layout refinement of Patch 153.

## What changed

The Start Here expander still contains the safe first path, but the review-lens material is now hidden behind two optional side-by-side expanders:

- What ALETHEIA looks for
- Seven failure-mode review signals

This prevents the Start Here panel from becoming too text-heavy while keeping the failure-mode language available at the front door.

## What did not change

- No scoring logic changed.
- No routing logic changed.
- No receipt schema changed.
- No protocol logic changed.
- No Receipt Reader logic changed.
- No new tab was added.

## Recovery

If the layout is visually worse on a narrow screen, revert `ui/unit_preview.py` to Patch 153 and keep the failure-mode language in Receipt Reader/docs only.
