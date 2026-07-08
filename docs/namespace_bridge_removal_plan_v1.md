# Namespace Bridge Removal Plan
**Patch:** 245  
**Companion document:** `docs/modularization_bridge_inventory_v1.md`

## Purpose

This plan defines how to remove the temporary `globals()` namespace bridge introduced during safe page extraction. The goal is not speed. The goal is behavior-preserving dependency clarity.

## Current bridge calls

```python
render_mirror_check_page(globals())
render_stress_test_page(globals())
render_evidence_lab_page(globals())
render_world_lens_page(globals())
```

## Removal principle

Replace one bridge at a time with explicit imports and explicit dependency passing. Each patch should be small enough that a UI regression can be traced to one page.

## Proposed patch sequence

### Patch 246 — Mirror Check Explicit Dependencies

- Replace `render_mirror_check_page(globals())` with explicit imports/arguments.
- Document Mirror Check session-state keys.
- Keep user-visible output unchanged.

### Patch 247 — Stress Test Explicit Dependencies

- Replace `render_stress_test_page(globals())`.
- Isolate demo scenario constants and stress helpers if needed.
- Keep sliders, demos, batch testing, semantic signals, tree visuals, and receipts unchanged.

### Patch 248 — Evidence Lab Explicit Dependencies

- Replace `render_evidence_lab_page(globals())`.
- Document Evidence Lab output state consumed by World Lens.
- Do not change evidence calculations.

### Patch 249 — World Lens Explicit Dependencies

- Replace `render_world_lens_page(globals())`.
- Last bridge removal due to 9k allocation, selected-year data, Evidence Lab handoff, internal tabs, report packet and export dependencies.

## Per-patch test protocol

For each bridge-removal patch:

```cmd
python -m py_compile app.py ui\pages\<target_page>.py
python -m pytest
python -m streamlit run app.py
```

Manual checks:

- target page opens;
- primary flow works;
- semantic pressure UI still renders where expected;
- no inactive modules render under the active module;
- receipts/downloads still work if applicable;
- World Lens and Evidence Lab state handoff is preserved where applicable.

## Stop conditions

Stop and patch before continuing if any of these occur:

- missing import/name error;
- visible raw HTML tags in user-facing cards;
- hidden inactive modules rendering as a long page;
- Receipt Reader placement becomes unclear again;
- active pytest fails;
- a page silently changes score/routing/receipt behavior.
