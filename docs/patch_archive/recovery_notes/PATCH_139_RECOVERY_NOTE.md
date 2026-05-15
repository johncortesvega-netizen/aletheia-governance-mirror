# Patch 139 Recovery Note — Unit Preview Header Entry Hotfix

Patch 139 fixes the visible entry-flow issue where Aletheia Unit Preview could appear as a plain first page before the intended polished ALETHEIA surface.

Recovery position:

- Keep `ui/unit_preview.py`.
- Keep `Aletheia Unit Preview` as the only pre-module hook.
- Keep `app.py` as the orchestrator.
- The gate should render **after** `render_app_header(...)` and **before** `render_how_to_use_note(...)`, sidebar controls, and module tabs.
- Do not restore the old Start Page gate.
- Do not call `render_start_page(...)` from `app.py`.

Expected manual behavior:

1. Fresh session opens on the ALETHEIA header plus Aletheia Unit Preview.
2. No plain pre-header Unit Preview appears first.
3. No old Start Page appears.
4. Click `Proceed to ALETHEIA`.
5. Full modules open directly.

No scoring, routing, receipt, signal, AI Integrity, Privacy Audit, World Lens, upload/download, external-call, telemetry, storage, certification, enforcement, privacy-guarantee, or final-truth behavior changed.
