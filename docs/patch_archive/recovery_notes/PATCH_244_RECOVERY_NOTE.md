# Patch 244 Recovery Note — World Lens Page Extraction

If World Lens fails after applying this patch, restore only:

- `app.py`

from the previous working patch and remove `ui/pages/world_lens.py` if desired.

This patch is intended as a page-extraction only. If a failure appears, it is likely related to the transitional namespace bridge or a missed dependency in the extracted page body, not to World Lens math.

No data, receipt, scoring, scanner, MEI7, Z-axis, 9k allocation, or authority-boundary behavior should be changed by this patch.
