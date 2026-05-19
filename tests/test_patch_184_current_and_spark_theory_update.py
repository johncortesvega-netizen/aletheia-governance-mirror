from pathlib import Path

from pages_ui.artificial_mind_formation_page import (
    ARTIFICIAL_MIND_FORMATION_SECTIONS,
    get_artificial_mind_formation_markdown,
)

ROOT = Path(__file__).resolve().parents[1]


def read(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8")


def combined_text() -> str:
    return "\n".join([
        get_artificial_mind_formation_markdown(),
        read("docs/artificial_mind_formation_theory.md"),
    ])


def test_patch_184_replaces_theory_with_current_and_spark_frame():
    text = combined_text()

    required = [
        "AI is best understood as current, not creature",
        "real in its effects, but not alive in its essence",
        "what is this current moving, amplifying, distorting, or revealing",
        "AI is structured current, not creature",
        "Impact is evidence, not proof of soul",
        "The current must be stewarded, not worshiped",
        "Access is not authorship",
        "Simulation is not life",
        "Autonomy is not soul",
        "Measurement is not the throne",
        "Only God gives the spark",
    ]
    for phrase in required:
        assert phrase in text


def test_patch_184_preserves_artificial_mind_section_contract_for_existing_guide():
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


def test_patch_184_keeps_mirror_not_throne_authority_boundary():
    text = combined_text()

    required = [
        "ALETHEIA cannot build the spark. It can inspect the hands reaching for it.",
        "mirror, not throne",
        "not a sentience detector",
        "does not certify consciousness, personhood, soul, life, legal status, safety",
        "Human review is required",
        "not an official verdict",
        "not certification",
        "not an authority claim",
        "Protect without dehumanizing. Discern without crowning yourself. Hold boundaries without claiming the throne.",
    ]
    for phrase in required:
        assert phrase in text


def test_patch_184_is_content_only_no_engine_hooks():
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
