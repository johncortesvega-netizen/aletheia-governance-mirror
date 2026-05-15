# Patch 85 Recovery Note — AI Integrity Mirror Scaffold

Patch 85 adds a new **AI Integrity Mirror** tab and static analyzer.

## Restore / rollback

If this patch must be rolled back:

1. Remove the AI Integrity tab wiring from `app.py`:
   - `audit_ai_integrity_artifact` / `AI_INTEGRITY_RUBRIC_VERSION` import
   - `🤖 AI Integrity Mirror` navigation label
   - AI Integrity entries in the navigation map and Protocol Guide copy
   - the `with tab_ai_integrity:` block
2. Remove:
   - `core/ai_integrity_mirror.py`
   - `docs/ai_integrity_mirror.md`
   - `tests/test_patch_85_ai_integrity_mirror.py`
   - `PATCH_85_MANIFEST.txt`
   - `PATCH_85_RECOVERY_NOTE.md`
3. Revert Patch 85 entries from:
   - `PATCH_STATUS.md`
   - `docs/progress_database.md`

## Boundary reminder

AI Integrity Mirror is a static review mirror. It does not certify models, vendors, prompts, agents, outputs, or codebases. It does not certify AI systems, vendors, prompts, agents, codebases, or model outputs as safe. It does not perform live model benchmarking, external scanning, public-ledger publication, enforcement, or authority decisions.

## Local verification

```bat
tools\run_patch_checks.bat 85
```

Focused Python check:

```bat
python -m py_compile app.py core/ai_integrity_mirror.py
pytest tests/test_patch_85_ai_integrity_mirror.py
```
