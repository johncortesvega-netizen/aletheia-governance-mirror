# PATCH 174 Recovery Note

## Summary
Patch 174 removes the standalone AI Integrity module from the visible app while preserving AI static scan context inside Mirror Check and Stress Test.

## Recovery steps
1. Restore the files listed in `PATCH_174_MANIFEST.txt` from the pre-patch state if the standalone AI Integrity tab needs to return.
2. Re-run `python tools/run_patch_checks.py 174`.
3. Re-run `python tools/run_patch_checks.py 173` to confirm subordinate AI static scan receipt/context behavior still works.

## Notes
- The underlying static scan helper remains because Mirror Check and Stress Test use it.
- This patch removes the standalone UI path, not the reusable subordinate context layer.
- Human review remains required.
