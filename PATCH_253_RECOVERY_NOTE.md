# PATCH 253 RECOVERY NOTE — World Lens Bridge Removal

If World Lens fails after applying this patch, restore the previous `app.py` and `ui/pages/world_lens.py` from Patch 252/your last working commit.

Most likely failure mode:
- `RuntimeError: World Lens page dependency map is incomplete: ...`

If that appears, add the missing helper/constant to `WORLD_LENS_DEPENDENCIES` and pass it from `world_lens_dependency_map(...)`.

Validation commands:

```cmd
python -m py_compile app.py ui\pages\world_lens.py
python -m pytest
python -m streamlit run app.py
```

Manual checks:
- World Lens opens.
- Optional context note works.
- Semantic regional flags render.
- Grid basis selector works.
- Internal World Lens tabs render.
- Report Packet renders/downloads.
- Evidence Lab state still feeds World Lens.
