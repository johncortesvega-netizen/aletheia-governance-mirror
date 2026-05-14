# Patch 140 — Unit Preview Orientation Cleanup

Patch 140 keeps **Aletheia Unit Preview** as the hook and moves beginner orientation copy out of the full app surface.

## What changed

- The full app no longer repeats the `Start here: try this first` beginner expander after the user has already proceeded.
- The full app no longer repeats the static `How to use this` note after the user has already proceeded.
- Unit Preview now carries the orientation layer:
  - `How to use this` copy;
  - six short examples for Mirror Check, Stress Test, Boundary Cases, AI Integrity Mirror, Evidence Lab, and World Lens;
  - a compact `Start here: try this first` first-use checklist.
- Receipt Reader — Standard View is no longer presented as a main module tab. It is available as a support utility near the footer after the module work surface.

## Boundary

This is UI placement and copy organization only. It does not change scoring, routing, taxonomy, receipt schemas, receipt generation, signal regexes, signal weights, AI Integrity behavior, Privacy Audit behavior, World Lens math, uploads, downloads, external calls, telemetry, storage, certification, enforcement, privacy guarantees, or final-truth behavior.

## Intended user flow

1. Fresh session opens on the ALETHEIA header and Aletheia Unit Preview.
2. Unit Preview explains how to start and shows examples.
3. The user may preview a suggested path or proceed.
4. After proceed, the full app opens as the working surface.
5. Receipt Reader remains available as a support utility, not a core module tab.
