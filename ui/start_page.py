"""Legacy compatibility wrapper for the pre-app gate.

Patch 138 retires the old Start Page UI. The single active entry surface is
Aletheia Unit Preview. This wrapper remains only so older imports do not revive
or flash the retired Start Page.
"""
from __future__ import annotations

from ui.unit_preview import UNIT_PREVIEW_SESSION_KEY as START_GATE_SESSION_KEY
from ui.unit_preview import render_unit_preview


def render_start_page(container=None) -> bool:
    """Delegate legacy Start Page calls to Aletheia Unit Preview."""
    return render_unit_preview(container)
