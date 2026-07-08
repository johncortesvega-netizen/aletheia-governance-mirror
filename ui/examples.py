"""Static UI guidance and demo-input metadata.

Patch 267 keeps demo loading behavior in ``app.py``; this module owns only the
static lists consumed by that behavior.
"""

APP_UX_POLISH_SUMMARY = [
    "Start with Mirror Check when you have a document.",
    "Use Stress Test when you have a scenario.",
    "Use Evidence Lab when a claim needs source-quality review.",
    "Use World Lens when you need selected-year country evidence and allocation context.",
    "Use Boundary Cases as a reference layer when the ethical edge case is unclear.",
    "Use Protocol Guide when you need the operating rules and mirror boundaries.",
    "Receipt Reader: Why ALETHEIA → Support utilities → Receipt Reader — Standard View.",
]

DEMO_INPUT_FILES = [
    ("Sample AI policy", "examples/demo_inputs/sample_ai_policy.txt"),
    ("Sample DAO governance charter", "examples/demo_inputs/sample_dao_governance.txt"),
    ("Sample public policy scenario", "examples/demo_inputs/sample_public_policy.txt"),
]
