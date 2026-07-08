from __future__ import annotations

from collections.abc import Callable, Iterable, Mapping
from typing import Any

import streamlit as st

from ui.components.metric_cards import soft_card


def render_soft_card_grid(cards: Iterable[tuple[str, str]], *, columns: int = 3) -> None:
    """Render a small grid of ALETHEIA soft cards.

    Presentation-only helper. It does not calculate, classify, or mutate review
    state; callers pass already-computed labels and body text.
    """
    normalized_cards = [(str(title), str(body)) for title, body in cards]
    if not normalized_cards:
        return

    column_count = max(1, min(int(columns or 1), len(normalized_cards)))
    cols = st.columns(column_count)
    for idx, (title, body) in enumerate(normalized_cards):
        with cols[idx % column_count]:
            soft_card(title, body)


def render_repair_question_cards(
    questions: Iterable[Any],
    *,
    transform: Callable[..., str] | None = None,
    context: str = "this repair path",
    limit: int = 5,
) -> None:
    """Render review-question cards for repair paths.

    `transform` is optional so app.py can keep using its existing wording helper
    without moving governance-language logic into this UI component.
    """
    for idx, question in enumerate(list(questions or [])[: max(0, int(limit))], start=1):
        body = transform(question, context=context) if transform else str(question)
        soft_card(f"REVIEW · Question {idx}", body)


def render_recommendation_cards(
    recommendations: Iterable[Mapping[str, Any]],
    *,
    transform: Callable[..., str] | None = None,
    limit: int = 5,
) -> None:
    """Render fallback recommendation cards.

    Presentation-only helper for already-computed recommendations. It preserves
    the existing priority/target/action card labels from app.py.
    """
    for rec in list(recommendations or [])[: max(0, int(limit))]:
        priority = str(rec.get("priority", "review")).upper()
        target = rec.get("target", "System")
        action = rec.get("action", "Review")
        body = transform(rec, context=str(target)) if transform else str(rec)
        soft_card(f"{priority} · {target} · {action}", body)
