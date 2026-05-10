# Patch 36 — Patch Automation Toolkit

Status: automation support patch.

## Added

- `tools/run_checks.bat` — one-command full local check runner for Command Prompt.
- `tools/run_patch_checks.bat` — patch-specific check runner.
- `tools/package_patched_items.py` — manifest-based packager for patched-items-only zips.
- `docs/progress_database.md` — local progress database for patch status, roadmap decisions, and next steps.
- `PATCH_STATUS.md` — short current patch sequence and next-patch queue.
- `PATCH_36_MANIFEST.txt` — manifest of this patch's changed files.
- `tests/test_patch_36_patch_automation.py` — regression checks for automation files.

## No production logic changes

This patch does not change audit scoring, doctrine outputs, Global Grid logic, witness receipts, or governance behavior.

## Commands

Run all checks:

```bat
tools\run_checks.bat
```

Run this patch's checks:

```bat
tools\run_patch_checks.bat 36
```

Package patched items from a manifest:

```bat
python tools\package_patched_items.py PATCH_36_MANIFEST.txt ALETHEIA_patch36_patched_items_only.zip
```
