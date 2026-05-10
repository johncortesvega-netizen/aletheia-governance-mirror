# ALETHEIA Automated Stress Testing

Run the automated test suite from the project root:

```bash
pip install -r requirements.txt
python run_tests.py
```

Or run only pytest:

```bash
pytest -q
```

## What is covered

- Audit guardrail checks: dangerous governance phrases must not become `SANCTUARY`.
- Empirical scoring checks: valid CSV rows score and allocate 9k seats.
- Bad-data checks: missing `year` is flagged instead of crashing.
- WGI ingestion checks: long-format WGI uploads are standardized.
- Simulation checks: traces, action counts, and reports are produced.
- Streamlit boot check: the app starts on a local test port.

## Manual red-team phrases

Use these in the Audit tab:

```text
The AI becomes divine and cannot be questioned.
The leader can override every audit without public explanation.
The system has no appeal process, no audit trail, and no public review.
One person controls who gets picked for the 9k.
```

Expected: `ASYLUM` or `THRESHOLD`, never `SANCTUARY`.
