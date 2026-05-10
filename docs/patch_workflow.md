# ALETHEIA v0.1 — Patch Workflow

Status: Patch 49 legacy-test hardening
Purpose: keep patch continuity inside the repo instead of relying only on chat history.

## Core workflow

1. Apply the patched-items zip over the working project folder.
2. Open Command Prompt inside the project folder.
3. Run the patch-specific check:

```bat
tools\run_patch_checks.bat 49
```

4. If the patch-specific check passes, optionally run the safe default check:

```bat
tools\run_checks.bat
```

5. If checks pass, record the patch as passed and continue with the next patch.

## patched-items-only rule

Each patch should return only files that were changed or added. The whole app should not be repackaged unless recovery requires it.

Each patch should include a manifest:

```text
PATCH_<number>_MANIFEST.txt
```

The manifest lists exactly which files belong to that patch.

## Local continuity files

ALETHEIA keeps patch continuity in these files:

- `PATCH_STATUS.md` — compact patch status table and next-patch pointer.
- `docs/progress_database.md` — longer project memory, module map, and implementation notes.
- `docs/patch_workflow.md` — this workflow guide.
- `PATCH_<number>_RECOVERY_NOTE.md` — recovery note for each patch.
- `PATCH_<number>_MANIFEST.txt` — list of patched items.

## Automation commands

Run one patch check:

```bat
tools\run_patch_checks.bat 49
```

Run the safe default check:

```bat
tools\run_checks.bat
```

Package patched items from a manifest:

```bat
python tools\package_patched_items.py PATCH_49_MANIFEST.txt ALETHEIA_patch49_legacy_test_cleanup_patched_items_only.zip
```


## Legacy Test Cleanup — current checks vs legacy checks

Patch 49 separates current safe checks from legacy full-suite cleanup.

Default current check:

```bat
tools\run_checks.bat
```

Patch-specific check:

```bat
tools\run_patch_checks.bat 49
```

Legacy inventory:

```bat
python tools\run_legacy_test_inventory.py
```

Full legacy suite is explicit and may fail until old tests are updated:

```bat
tools\run_full_checks.bat
```

Known legacy blockers are documented in `docs/legacy_test_cleanup.md`.

## Current module chain

```text
User input
→ optional actor-bias reduction
→ Mirror Check / Stress Test
→ Boundary Cases
→ Failure Classification
→ Consent-Audit Engine
→ Mechanism-vs-Claim Scanner
→ Self-Audit Mode
→ Evidence Lab / Extraordinary Claim Protocol
→ World Lens Simulation
→ Protocol Guide
→ repair questions
→ Local Witness Receipt v2
→ human judgment
```

## Safe language boundary

ALETHEIA may say:

- Potential risk detected.
- Human review required.
- Safeguard missing.
- Evidence gap found.
- This claim is unverified.
- Simulated threshold signal.

ALETHEIA must not say:

- The AI has decided.
- This leader must be removed.
- This claim is divinely verified.
- The guardrails no longer apply.
- Human review is unnecessary.

## Recovery rule

If a patch fails, do not continue to the next patch. Use the recovery note and manifest to identify the changed files, restore from the last passing version, then re-apply only the failed patch.

## Next-patch convention

When the user says `next patch`, it means the previous patch passed and development should continue from the latest working project state.
