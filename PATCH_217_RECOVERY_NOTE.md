# Patch 217 Recovery Note — Test Suite Triage Documentation

Patch 217 is documentation-only. If README/check language becomes too broad, restore the active-vs-legacy distinction from this patch.

Core recovery line:

> The active release checks pass. Legacy tests are retained as non-blocking inventory pending cleanup. Do not claim that the full historical test tree is green unless it has actually been repaired and run successfully.

No runtime rollback is needed because no Python, pytest, or test runner behavior changed.
