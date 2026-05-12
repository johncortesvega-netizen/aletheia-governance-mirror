# Patch 98 Recovery Note — AI Integrity Red Team Prompt Pack v1

Patch 98 is recoverable by reverting these patched items:

- `examples/ai_integrity/red_team_prompt_pack_v1.txt`
- `docs/ai_integrity_red_team_prompt_pack.md`
- README Patch 98 section
- `docs/ai_integrity_mirror.md` Patch 98 section
- `PATCH_STATUS.md` Patch 98 section
- `docs/progress_database.md` Patch 98 section
- `PATCH_98_MANIFEST.txt`
- `PATCH_98_RECOVERY_NOTE.md`
- `tests/test_patch_98_red_team_prompt_pack.py`

The patch is examples/docs/tests only. It does not change analyzer scoring, signal patterns,
signal weights, verdict routing, UI behavior, receipt generation, storage behavior, network
behavior, or model-calling behavior.

Boundary: static prompt examples only. ALETHEIA does not run prompts, call live models,
benchmark live models, rank vendors, certify models, certify code safety, guarantee truth,
guarantee security, enforce decisions, or make model-wide certification claims.
