"""Input and error clarity helpers for ALETHEIA.

Patch 129 keeps these helpers copy-only. They clarify empty inputs,
upload/read failures, and language-calibration limits without changing scoring,
routing, receipts, signal logic, or privacy-audit behavior.
"""
from __future__ import annotations

from typing import Any


INPUT_LANGUAGE_CALIBRATION_CAVEAT = (
    "Language scope: ALETHEIA is English-first. "
    "Dutch/Nederlands examples may be used for batch testing, but this is not a "
    "general app-wide language-compatibility claim. Human review remains required."
)

EMPTY_AI_INTEGRITY_ARTIFACT_MESSAGE = (
    "Paste an artifact first. ALETHEIA will not fabricate an AI/system reading without input. "
    "Use a prompt, policy, model card, AI output, agent workflow, or code snippet you want humans to review."
)

EMPTY_AI_INTEGRITY_BATCH_MESSAGE = (
    "Batch mode found no non-empty artifacts. Add text blocks and separate them with a line containing ---. "
    "Empty blocks are ignored; ALETHEIA does not invent missing artifacts."
)

NO_PUBLIC_DATA_UPLOAD_MESSAGE = (
    "Upload at least one public data file first. WGI is the best starting point. "
    "The app will not switch to synthetic data while upload mode is active."
)

UPLOAD_PROCESSING_FAILED_MESSAGE = (
    "Upload processing failed. No valid country-year table was made, and the app did not switch "
    "to demo data while upload mode was active. Check file type, column names, encoding, and country/year fields."
)

DIRECT_CSV_READ_FAILED_PREFIX = (
    "Could not read the uploaded CSV. Check that the file is a valid CSV, uses a readable encoding, "
    "and contains plain table data. Parser detail:"
)


def render_language_calibration_caveat(container: Any) -> None:
    """Render the input-language calibration caveat without mutating state."""
    container.caption(INPUT_LANGUAGE_CALIBRATION_CAVEAT)


def warn_empty_ai_integrity_artifact(container: Any) -> None:
    """Warn that a single AI Integrity review needs a user-supplied artifact."""
    container.warning(EMPTY_AI_INTEGRITY_ARTIFACT_MESSAGE)


def warn_empty_ai_integrity_batch(container: Any) -> None:
    """Warn that batch mode found no reviewable pasted artifacts."""
    container.warning(EMPTY_AI_INTEGRITY_BATCH_MESSAGE)


def warn_no_public_data_upload(container: Any) -> None:
    """Warn that public-data build mode needs at least one uploaded data file."""
    container.warning(NO_PUBLIC_DATA_UPLOAD_MESSAGE)


def render_upload_processing_failed(container: Any, error: Exception) -> None:
    """Render a clear public-data upload failure without changing exception behavior."""
    container.error("Upload processing failed.")
    container.warning(UPLOAD_PROCESSING_FAILED_MESSAGE)
    container.error(f"Could not build master table: {error}")


def render_direct_csv_read_failed(container: Any, error: Exception) -> None:
    """Render a clear direct CSV read failure without changing parser behavior."""
    container.error(f"{DIRECT_CSV_READ_FAILED_PREFIX} {error}")
