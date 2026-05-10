# ALETHEIA v1 Cleanup Notes

This package has been cleaned and consolidated toward the README/product description.

## Security and release hygiene

- Removed local `.env` from the distributable package.
- Removed Android release keystore from the distributable package.
- Removed Python cache artifacts.
- Added `.env.example` for local configuration.
- Expanded `.gitignore` to prevent accidental secret/cache commits.
- Re-enabled CORS/XSRF protection in the devcontainer Streamlit command.

## Architecture consolidation

- `core/protocol.py` is now the canonical Sydney Protocol engine.
- Root-level `protocol.py` is now a compatibility wrapper.
- `core/empirical.py` is now the canonical empirical evidence/9k ingestion module.
- Root-level `core_empirical.py` is now a compatibility wrapper.
- UI assets are now under `assets/`.

## Validation added

New tests cover protocol guardrails, final protocol judgment, 9k allocation, empirical scoring, and a minimal local end-to-end audit pipeline.

Run:

```bash
python run_tests.py
```

## Remaining recommended work

- Split the large Streamlit `app.py` into `ui/` tab modules.
- Add more deterministic reference scenarios for Sanctuary/Threshold/Asylum labels.
- Add example public WGI/population files under `examples/`.
- Expand `paper/methodology.md` into a formal reproducibility note.
