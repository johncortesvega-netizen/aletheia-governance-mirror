# Public Demo / Deployment Prep

Status: v1.0 public MVP prep
Purpose: Prepare ALETHEIA for safe public demo deployment

## Candidate Deployment Targets

- local Streamlit run
- Streamlit Community Cloud
- Hugging Face Spaces
- GitHub repository release

## Local Run

```bat
streamlit run app.py
```

## Safe Check Before Demo

```bat
tools\run_checks.bat
```

## Public Demo Warnings

Any public demo should state:

- ALETHEIA is a governance-risk review prototype
- outputs are diagnostic and correctable
- uploads should not include private, sensitive, or confidential data
- reports are not legal advice, policy commands, enforcement, religious validation, or final judgments
- human review remains required

## Privacy Boundary

v1.0 should not deploy with:

- central citizen database
- Global ID sync
- public ledger authority
- neural data
- memory extraction
- automated enforcement
- real voting or leader-selection systems

## Demo Data

Use fictional demo inputs under `examples/demo_inputs/` unless the user explicitly provides their own public or safe test document.

Demos must load only by explicit user choice.
