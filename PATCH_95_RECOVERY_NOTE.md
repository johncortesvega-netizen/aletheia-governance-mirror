# Patch 95 Recovery Note — Code Integrity Static Scan v1

If Patch 95 needs to be reverted, remove the Code Integrity Static Scan additions from:

- `core/ai_integrity_mirror.py`
- `app.py`
- `docs/code_integrity_static_scan.md`
- `docs/ai_integrity_mirror.md`
- `README.md`
- `docs/progress_database.md`
- `PATCH_STATUS.md`
- `tests/test_patch_95_code_integrity_static_scan.py`

Patch 95 is intentionally bounded. It adds static pasted-code review metadata and a display section only. It does not execute code, crawl repositories, call external services, run live model checks, alter AI Integrity scoring math, alter verdict routing, certify vulnerabilities, guarantee security, approve compliance, or enforce action.

After recovery, run:

```bat
tools\run_patch_checks.bat 94
tools\run_patch_checks.bat 93
tools\run_patch_checks.bat 92
```
