# ---------------------------------------------------------------------------
# Default weights for the stability formula:
#   S = W_I * I  +  W_A * A  -  W_E * E  +  W_P * P
#
# Design principles:
#   - Alignment (A) is the strongest positive driver — cooperation is primary
#   - Intelligence (I) second — capacity matters
#   - Ego (E) is the primary negative driver — self-interest destabilises
#   - Power (P) has a small positive effect — influence enables coordination
#
# These are used as the starting point for calibration.
# The optimizer will adjust them; don't hard-code these into formulas.
# ---------------------------------------------------------------------------

DEFAULT_WEIGHTS = {
    "I": 0.30,   # Intelligence / cognitive capacity
    "A": 0.40,   # Alignment / cooperation
    "E": 0.20,   # Ego / self-interest (used as penalty, sign applied in formula)
    "P": 0.10,   # Power / influence
}

# Sanity check — weights should sum to 1.0
assert abs(sum(DEFAULT_WEIGHTS.values()) - 1.0) < 1e-6, (
    f"DEFAULT_WEIGHTS must sum to 1.0, got {sum(DEFAULT_WEIGHTS.values())}"
)

# ---------------------------------------------------------------------------
# Weight bounds for the optimizer
# ---------------------------------------------------------------------------

WEIGHT_BOUNDS = {
    "I": (0.10, 0.50),
    "A": (0.25, 0.55),
    "E": (0.10, 0.40),
    "P": (0.05, 0.25),
}

# ---------------------------------------------------------------------------
# Named presets — alternative starting configurations
# ---------------------------------------------------------------------------

WEIGHT_PRESETS = {
    "default": DEFAULT_WEIGHTS,

    # High-ego environment (e.g. deregulated markets, authoritarian systems)
    "high_ego_context": {
        "I": 0.25,
        "A": 0.30,
        "E": 0.35,
        "P": 0.10,
    },

    # High-trust cooperative environment (e.g. Nordic governance, multilateral treaties)
    "cooperative_context": {
        "I": 0.30,
        "A": 0.50,
        "E": 0.12,
        "P": 0.08,
    },

    # Power-concentrated environment (e.g. state capitalism, oligarchic systems)
    "power_concentrated": {
        "I": 0.25,
        "A": 0.25,
        "E": 0.25,
        "P": 0.25,
    },
}
