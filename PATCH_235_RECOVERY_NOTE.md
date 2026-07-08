# PATCH 235 RECOVERY NOTE

If Receipt Reader is missing from the navigation after Patch 226/234, apply this patch.

This patch adds `🧾 Receipt Reader` to `APP_NAVIGATION_LABELS` and renders `render_receipt_reader_standard_view(st)` as its own single-module navigation surface.

If problems occur, revert only `app.py` to the previous committed state. No data migrations are involved.
