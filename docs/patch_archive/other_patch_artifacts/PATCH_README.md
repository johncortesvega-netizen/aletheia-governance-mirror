# ALETHEIA v1 patch files

Apply by copying these files over the existing project root, preserving paths.

## Copy / overwrite

- `.gitignore`
- `.env.example`
- `.devcontainer/devcontainer.json`
- `requirements.txt`
- `run_tests.py`
- `RELEASE_NOTES_V1_CLEANUP.md`
- `protocol.py`
- `core_empirical.py`
- `core/parser.py`
- `core/protocol.py`
- `core/empirical.py`
- `tests/test_protocol_guardrails.py`
- `tests/test_empirical.py`
- `tests/test_end_to_end_audit.py`

## Delete from your local project before sharing/releasing

- `.env`
- `*.jks`
- `*.keystore`
- `__pycache__/`
- `.pytest_cache/`
- `*.pyc`

## Validation

I validated the patch with:

```bash
PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 python -m pytest -q tests
```

Result: 7 tests passed. There are 2 non-blocking pandas deprecation warnings in `core/empirical.py` around `groupby.apply`.
