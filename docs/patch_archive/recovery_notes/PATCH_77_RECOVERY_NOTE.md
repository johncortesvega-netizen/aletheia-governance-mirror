# Patch 77 Recovery Note - Capture Risk Signals Framework

Patch 77 is documentation/copy/test only. It makes ALETHEIA's anti-capture logic explicit without changing scoring, routing, receipt schemas, data processing, or app-engine behavior.

To recover or verify:

```bat
tools\run_patch_checks.bat 77
```

If the patch needs to be reverted, remove the Patch 77 files and restore the touched README/About/public-test-case/progress/status files from the previous working project zip.

Boundary preserved: ALETHEIA remains a mirror for human review. This patch does not add enforcement, adjudication, legal authority, political authority, religious authority, public ledger authority, Global ID sync, central storage, certification, punishment, or final judgment.
