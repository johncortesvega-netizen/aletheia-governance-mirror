# Patch 268 — Native Multipage Decision

Status: decision-only patch. No Streamlit native multipage migration is performed.

## Decision

Keep the current controlled router for now.

Patch 263 already moved top-level navigation and dispatch into `ui/main.py`. That split made `app.py` thinner while preserving ALETHEIA's current navigation contract. After reviewing the current state after Patches 263–267, Streamlit native multipage does not yet provide enough maintainability benefit to justify the migration risk.

## Reasoning

### Controlled router strengths

- Preserves the current top-level module order exactly.
- Keeps the Receipt Reader under `Why ALETHEIA → Support utilities` instead of promoting it to a primary page.
- Keeps protocol-sensitive framing in one explicit dispatch surface.
- Avoids a second navigation model while shell, state, and config extraction are still settling.
- Keeps active tests simple: one canonical router owner, `ui/main.py`.

### Native multipage risks right now

- It would likely require a root `pages/` directory and new page-level entrypoints.
- It could make Receipt Reader look like a primary module rather than a support utility.
- It may weaken the current controlled ordering/default-page contract.
- It could introduce cross-page session-state lifecycle regressions before state ownership is fully stabilized.
- It would force many tests to change at once for little immediate user-visible benefit.

### Hybrid option

Hybrid remains a possible future option, but not yet. A future hybrid could use native pages for stable, low-risk informational modules while keeping protocol-sensitive flows inside the controlled router. That decision should happen only after the state/config surfaces are stable and after exact navigation tests exist for every migrated page.

## Patch 268 boundary

This patch intentionally does not:

- create a root `pages/` directory;
- move Streamlit page entrypoints;
- rename navigation labels;
- change default page selection;
- change `key="aletheia_active_module"`;
- change Receipt Reader placement;
- change session-state ownership;
- change scoring, taxonomy, Z-axis, receipt, Evidence Lab, World Lens, Mirror Check, or Stress Test behavior.

## Future migration gate

A future native multipage or hybrid migration may be reconsidered only if it satisfies all of the following:

1. The current navigation labels, order, default, and Receipt Reader placement remain protected by active tests.
2. The migration reduces complexity compared with `ui/main.py`, not merely moves complexity into separate page entrypoints.
3. Session-state lifecycle behavior is protected by focused tests.
4. Protocol framing is not weakened.
5. The migration can be done in small patches with a green active suite after each patch.

## Next patch candidates

Preferred next step: continue with a narrow documentation or test-governance cleanup if needed, or perform another safe extraction only when there is an exact owner and exact-content test.

Do not start native multipage migration as Patch 269 unless the migration plan is first written as a separate prep patch.
