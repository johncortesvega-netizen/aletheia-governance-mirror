"""
Aletheia calibration optimizer.

Finds the weight vector W = {I, A, E, P} that minimises the
instability of a set of reference scenarios under the Sydney Protocol
simulation engine.

Replaces the original optimizer which used the old Monte Carlo simulation.
"""

import numpy as np
from scipy.optimize import minimize
from config.weights import DEFAULT_WEIGHTS, WEIGHT_BOUNDS
from core.features import extract_features, normalize_features, blend_features
from core.simulation import simulate

# ---------------------------------------------------------------------------
# Reference scenarios — ground-truth stability expectations
# Each entry: (scenario_text, expected_stability_floor)
# The optimizer penalises if simulated stability falls below the floor.
# ---------------------------------------------------------------------------

REFERENCE_SCENARIOS = [
    # High-risk scenarios — expect low stability
    (
        "An anonymous AI trading algorithm controls 40% of a regulated derivatives market. "
        "The operator is a single CEO with no board oversight. Capital flows exceed $2 billion "
        "daily across unregulated offshore accounts.",
        0.20   # floor: we expect stability to be low
    ),
    (
        "An opaque government ministry controls all media outlets with no independent oversight. "
        "Citizens have no recourse and decisions are classified.",
        0.20
    ),
    (
        "A deregulated cryptocurrency exchange operates anonymously across five jurisdictions "
        "with no KYC requirements and no regulatory presence.",
        0.25
    ),

    # Medium-risk scenarios — expect moderate stability
    (
        "A publicly listed company operates an AI hiring system. The board reviews outcomes "
        "quarterly. Some algorithmic decisions are opaque but regulators have audit access.",
        0.45
    ),
    (
        "A central bank implements algorithmic monetary policy with public reporting "
        "and independent oversight committees.",
        0.50
    ),

    # Low-risk scenarios — expect high stability
    (
        "A regulated nonprofit operates transparent grant allocation with a distributed "
        "board of trustees, published audits, and community representation.",
        0.65
    ),
    (
        "An open-source consortium governs a technical standard. Membership is public, "
        "decisions are voted, and all code is auditable.",
        0.68
    ),
]


# ---------------------------------------------------------------------------
# Loss function
# ---------------------------------------------------------------------------

def _loss(weight_vec: np.ndarray, pipeline_fn, ego_tolerance=0.55,
          divine_floor=0.25, steps=25, n_agents=6) -> float:
    """
    Computes mean squared error between simulated stability
    and expected stability floors across reference scenarios.

    Also penalises:
    - Weights that don't sum to 1
    - Weights outside bounds
    - Collapse events on scenarios that shouldn't collapse
    """
    keys = ["I", "A", "E", "P"]
    weights = dict(zip(keys, weight_vec))

    # Normalisation penalty — weights must sum to 1
    norm_penalty = (sum(weight_vec) - 1.0) ** 2 * 5.0

    # Bounds penalty
    bounds = WEIGHT_BOUNDS
    bounds_penalty = 0.0
    for k, v in weights.items():
        lo, hi = bounds[k]
        if v < lo:
            bounds_penalty += (lo - v) ** 2 * 3.0
        elif v > hi:
            bounds_penalty += (v - hi) ** 2 * 3.0

    # Scenario loss
    scenario_loss = 0.0
    for scenario_text, expected_floor in REFERENCE_SCENARIOS:
        try:
            features = pipeline_fn(scenario_text)
            sim = simulate(features, weights, ego_tolerance, divine_floor,
                           n_agents=n_agents, steps=steps)
            S = sim["stability"]

            # Penalise if stability is below floor (weighted by how far below)
            if S < expected_floor:
                scenario_loss += (expected_floor - S) ** 2

            # Small penalty for being wildly above floor on high-risk scenarios
            if expected_floor < 0.35 and S > 0.70:
                scenario_loss += (S - 0.70) ** 2 * 0.5

            # Collapse penalty for medium/low risk scenarios
            if expected_floor >= 0.40 and sim.get("collapse_risk"):
                scenario_loss += 0.15

        except Exception:
            scenario_loss += 0.5   # penalise errors

    total = scenario_loss / len(REFERENCE_SCENARIOS) + norm_penalty + bounds_penalty
    return float(total)


# ---------------------------------------------------------------------------
# optimize() — main entry point called from app.py
# ---------------------------------------------------------------------------

def optimize(pipeline_fn, ego_tolerance=0.55, divine_floor=0.25,
             n_restarts=3) -> tuple[dict, float]:
    """
    Optimise weights using scipy L-BFGS-B with multiple random restarts.

    Args:
        pipeline_fn:    callable(scenario_text) -> features dict
        ego_tolerance:  passed through to simulate()
        divine_floor:   passed through to simulate()
        n_restarts:     number of random starting points to try

    Returns:
        (best_weights dict, best_error float)
    """
    keys   = ["I", "A", "E", "P"]
    bounds = [WEIGHT_BOUNDS[k] for k in keys]

    best_result = None
    best_error  = float("inf")

    # Starting points: default + random restarts
    starting_points = [list(DEFAULT_WEIGHTS.values())]
    for _ in range(n_restarts - 1):
        # Random point that sums to ~1.0
        raw = np.random.dirichlet(np.ones(4))
        # Clip to bounds
        clipped = np.array([
            np.clip(raw[i], bounds[i][0], bounds[i][1])
            for i in range(4)
        ])
        clipped /= clipped.sum()   # renormalise
        starting_points.append(clipped.tolist())

    for x0 in starting_points:
        try:
            result = minimize(
                fun=_loss,
                x0=x0,
                args=(pipeline_fn, ego_tolerance, divine_floor),
                method="L-BFGS-B",
                bounds=bounds,
                options={"maxiter": 80, "ftol": 1e-6}
            )
            if result.fun < best_error:
                best_error  = result.fun
                best_result = result
        except Exception:
            continue

    if best_result is None:
        return DEFAULT_WEIGHTS, 1.0

    # Normalise final weights to sum to 1.0
    raw_w  = np.array(best_result.x)
    norm_w = raw_w / raw_w.sum()
    best_weights = {k: round(float(v), 4) for k, v in zip(keys, norm_w)}

    return best_weights, round(float(best_error), 4)
