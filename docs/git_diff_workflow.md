# ALETHEIA v0.1 — Git Diff Workflow

Patch 51 introduces an optional Git-based workflow so future patches can be shared as `.diff` files instead of full project zips or patched-items-only zip bundles.

This workflow is optional. The patched-items-only workflow remains valid.

## Purpose

The Git diff workflow helps reduce overwrite risk. Instead of replacing whole files, Git applies only the changed lines. If the local project has drifted too far from the expected version, Git stops and asks for review.

## First-time setup

Run these commands from Command Prompt inside the ALETHEIA project folder:

```bat
git init
git add .
git commit -m "ALETHEIA v0.1 baseline before diff workflow"
```

If Git is not installed, continue using patched-items-only zip files.

## Applying a future patch diff

When a future patch is delivered as a `.diff` file, copy it into the project folder and run:

```bat
git apply PATCH_52_example.diff
toolsun_patch_checks.bat 52
```

If the check passes, commit it:

```bat
git add .
git commit -m "Patch 52 example"
```

## Previewing a patch before applying

```bat
git apply --check PATCH_52_example.diff
```

If `--check` fails, do not apply the patch. Ask for a fresh patch based on the latest project zip or send the current diff/conflict context.

## Exporting your local changes

To export all uncommitted tracked changes into a diff file:

```bat
tools\export_patch_diff.bat PATCH_local_changes.diff
```

To inspect your current Git state:

```bat
tools\check_git_status.bat
```

## Recovery

If a patch was applied but should be reverted before commit:

```bat
git apply -R PATCH_52_example.diff
```

If changes are already committed, use normal Git recovery:

```bat
git log --oneline
git revert <commit_hash>
```

## Safety boundary

Git improves code-patch safety, but it does not make ALETHEIA authoritative.

Patch diffs are development artifacts only. They do not create governance authority, legal authority, spiritual validation, Global ID sync, public ledger, real 9k selection, World Leader logic, automatic reset, neural validation, or automated enforcement.

Core rule:

> ALETHEIA reflects. Humans review. Power stays accountable.
