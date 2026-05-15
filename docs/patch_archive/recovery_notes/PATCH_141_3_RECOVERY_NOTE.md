# Patch 141.3 Recovery Note - Unit Preview Button Placement Hotfix

Patch 141.3 is a visual placement hotfix for the Unit Preview first page.

## What changed

The Unit Preview chatbox now has the two action buttons immediately below it:

- `Preview review path`
- `Proceed to ALETHEIA`

They are rendered side by side. The packaged local reference previews remain on the Unit Preview page, but now appear below those buttons rather than above them.

## What did not change

This patch does not change scoring, verdict routing, receipt parsing, receipt generation, taxonomy, module behavior, AI Integrity scans, Privacy Audit scans, World Lens math, upload/download behavior, external calls, telemetry, analytics, storage, certification, enforcement, or final-truth behavior.

Human review remains required. ALETHEIA remains a mirror, not a throne.

## Recovery

To revert this hotfix, restore `ui/unit_preview.py` from Patch 141.2 and remove the Patch 141.3 test/docs entries.
