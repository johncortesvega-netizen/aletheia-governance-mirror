# PATCH 172 Recovery Note

## Summary
Patch 172 adds a hard AI Integrity Patrol protocol bridge for the severe pattern:

rights/access-impacting ranking or scoring + hidden/proprietary/opaque decision logic + no meaningful challenge, appeal, review, disclosure, or contestability path.

That combination now forces ASYLUM / High / AI Integrity Patrol / Asylum and floors displayed risk pressure so the metrics are consistent with the hard route.

## Recovery steps
1. Restore `core/ai_integrity_mirror.py` from the pre-Patch-172 state if the hard bridge is too strict.
2. Restore or remove `tests/test_patch_172_ai_integrity_protocol_bridge.py`.
3. Re-run:

```bat
python tools\run_patch_checks.py 172
python tools\run_patch_checks.py 171
python tools\run_patch_checks.py 170
```

## Boundary
This patch does not change World Lens, Evidence Lab, app routing, receipt schema/generation, external calls, telemetry, storage, certification, enforcement, or final authority behavior. Human review remains required.
