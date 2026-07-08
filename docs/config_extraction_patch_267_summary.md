# Patch 267 summary — Safe Config Extraction

Patch 267 creates the first narrow config/static-data modules:

- `ui/config.py` owns `APP_VERSION` and `SUPPORTED_INPUT_LANGUAGE_NOTE`.
- `ui/examples.py` owns `APP_UX_POLISH_SUMMARY` and `DEMO_INPUT_FILES`.

No behavior-sensitive constants move in this patch. Allocation, taxonomy, scoring, receipt semantics, World Lens validity gates, navigation labels, and demo scenario maps remain with their current owners.

Next patch candidate: Native Multipage Decision documentation, or a very narrow second config extraction only if a specific static surface has exact-content tests.
