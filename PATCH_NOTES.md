# PATCH NOTES

## Patch 253 — World Lens Bridge Removal

World Lens was the final large page still using a broad `globals()` bridge. This patch replaces that handoff with an explicit dependency map so later cleanup can remove injected helpers one by one.

This is a modularization boundary cleanup only. It does not change World Lens output, Evidence Lab state sharing, 9k allocation, report packets, semantic pressure, scoring, or receipt behavior.
