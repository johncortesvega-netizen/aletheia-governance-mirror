from pathlib import Path

from pages_ui.artificial_mind_formation_page import (
    ARTIFICIAL_MIND_FORMATION_CORE_LINE,
    ARTIFICIAL_MIND_FORMATION_SECTIONS,
    ARTIFICIAL_MIND_FORMATION_SUBTITLE,
    ARTIFICIAL_MIND_FORMATION_TITLE,
    get_artificial_mind_formation_markdown,
)

ROOT = Path(__file__).resolve().parents[1]


def read(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8")


def test_patch_162_explainer_title_subtitle_and_core_line_are_present():
    markdown = get_artificial_mind_formation_markdown()
    app = read("app.py")

    assert ARTIFICIAL_MIND_FORMATION_TITLE == "Artificial Mind Formation Theory"
    assert ARTIFICIAL_MIND_FORMATION_SUBTITLE == "An ALETHEIA explainer on ethical formation attempts, safeguards, and corruption risk."
    assert ARTIFICIAL_MIND_FORMATION_CORE_LINE == "ALETHEIA cannot build the spark. It can inspect the hands reaching for it."
    assert ARTIFICIAL_MIND_FORMATION_CORE_LINE in markdown
    assert "render_artificial_mind_formation_page(st)" in app


def test_patch_162_required_sections_are_stable_and_complete():
    titles = [title for title, _ in ARTIFICIAL_MIND_FORMATION_SECTIONS]
    assert titles == [
        "1. Boundary statement",
        "2. Why “more neurons / more scale” is the wrong axis by itself",
        "3. Formation over training",
        "4. Stimulus gates and sleep/pause states",
        "5. Memory boundaries and hidden conditioning risk",
        "6. Embodiment/friction as limitation before reach",
        "7. Route-before-reach",
        "8. Corruption signals",
        "9. Human review / revocation / appeal",
        "10. Spark boundary",
    ]


def test_patch_162_boundary_language_preserves_no_authority_claim():
    combined = "\n".join([
        get_artificial_mind_formation_markdown(),
        read("docs/artificial_mind_formation_theory.md"),
    ])
    required = [
        "not built to build sentient AI",
        "not a sentience detector",
        "does not certify consciousness, personhood, soul, life, legal status, safety",
        "mirror, not throne",
        "Human review is required",
        "conceptual explainer only",
        "not an official verdict",
        "not certification",
        "not an authority claim",
        "It can only inspect formation conditions for ethical care or corruption pressure",
    ]
    for phrase in required:
        assert phrase in combined


def test_patch_162_does_not_change_core_scoring_or_taxonomy():
    app = read("app.py")
    source = read("pages_ui/artificial_mind_formation_page.py")
    scoring = read("core/scoring.py")
    world_lens = read("core/world_lens.py")

    forbidden_runtime_hooks = (
        "full_report",
        "score_",
        "classify_verdict",
        "final_protocol_judgment",
        "simulate(",
        "build_local_witness_receipt",
        "create_receipt",
        "generate_receipt",
        "requests.",
        "telemetry",
        "analytics",
        "database",
        "Global ID sync",
        "public ledger",
    )
    for token in forbidden_runtime_hooks:
        assert token not in source

    assert "ARTIFICIAL_MIND" not in scoring
    assert "ARTIFICIAL_MIND" not in world_lens
    assert "st.tabs(APP_NAVIGATION_LABELS)" in app


def test_patch_162_avoids_operational_ai_child_or_sentience_certification_claims():
    combined = "\n".join([
        get_artificial_mind_formation_markdown(),
        read("docs/artificial_mind_formation_theory.md"),
    ]).lower()
    forbidden = [
        "ai child",
        "aletheia creates sentience",
        "aletheia proves consciousness",
        "aletheia disproves consciousness",
        "certified conscious",
        "certified sentient",
        "official sentience verdict",
    ]
    for phrase in forbidden:
        assert phrase not in combined
