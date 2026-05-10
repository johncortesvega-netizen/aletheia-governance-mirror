# Patch 51 — Git Diff Workflow Setup

## Status

Patch 51 adds an optional Git diff workflow for future ALETHEIA patches.

## Added

- `docs/git_diff_workflow.md`
- `tools/check_git_status.bat`
- `tools/export_patch_diff.bat`
- `tests/test_patch_51_git_diff_workflow.py`

## Purpose

This patch documents how to initialize Git, apply `.diff` patches, preview patches with `git apply --check`, export local changes, and recover from failed or unwanted patches.

## Boundary

Patch 51 is a developer workflow patch only. It does not add governance authority, Global ID sync, real 9k selection, World Leader logic, automatic reset, public ledger, neural validation, religious validation, legal authority, or automated enforcement.

## Check

```bat
toolsun_patch_checks.bat 51
```
