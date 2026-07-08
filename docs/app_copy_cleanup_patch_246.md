# Patch 246 — App-wide Copy Cleanup Pass

## Purpose

Patch 246 performs a conservative copy-editing pass across the active app surfaces after modularization. The goal is to remove stale wording, authority-sounding phrasing, and confusing placement language without changing the ALETHEIA concept or runtime behavior.

## What changed

- Replaced leftover rebrand wording such as `Patrol guide panels` with `Protocol guide panels`.
- Tightened Receipt Reader placement copy so it reads as a support utility location, not a self-referential announcement.
- Replaced several authority-adjacent phrases:
  - `final internal label` → `final judgment` or `internal review label`, depending on context.
  - `good or bad` → `safe, unsafe, trustworthy, or untrustworthy`.
  - `final truth` in metric/helper contexts → `truth measurement` or `final truth claim`.
  - `command layer` → `authority layer` where the meaning is governance-boundary language.
- Reduced misleading visual-card wording:
  - `sanctuary blueprint` → `boundary blueprint`.
  - `Command Dossier` → `Reference Dossier`.
- Cleaned Evidence Lab and semantic-panel wording from `proof` language toward `evidence` language where appropriate.

## Boundary

This is a UI-copy and documentation patch only.

No scanner logic, scoring, MEI7 gate, Z-axis logic, Stress Test metrics, Evidence Lab calculations, World Lens math, receipt schema, telemetry, storage behavior, module routing, or authority-boundary behavior was changed.

## Validation

Validated with:

```cmd
python -m py_compile app.py ui/pages/*.py ui/components/*.py
python -m pytest
```

Expected result: active pytest suite remains green.
