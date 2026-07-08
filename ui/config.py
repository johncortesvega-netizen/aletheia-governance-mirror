"""Static app-level display configuration.

Patch 267 extracts only low-risk UI/config copy from ``app.py``.
Behavior-sensitive constants for scoring, taxonomy, allocation, receipts, and
World Lens validity remain with their current runtime owners.
"""

APP_VERSION = "v1.0-original-governance-mirror-p6"
SUPPORTED_INPUT_LANGUAGE_NOTE = (
    "Language scope: ALETHEIA is English-first. Dutch/Nederlands examples may be used for batch testing, "
    "but this is not a general app-wide language-compatibility claim. Human review remains required."
)
