import numpy as np


def _clamp01(value):
    return float(np.clip(float(value or 0.0), 0.0, 1.0))


def nonlinear_ego_penalty(ego_pressure, *, exponent=1.5, weight=0.55):
    """Return a bounded tipping-point penalty for ego pressure.

    Patch 23B: small ego pressure should remain reviewable, while high
    pressure should degrade integrity sharply. This keeps the Sydney Protocol
    reading aligned with the formula: Intelligence + Power - Ego = Stability.
    """
    ep = _clamp01(ego_pressure)
    return round(_clamp01(weight * (ep ** exponent)), 4)


# ---------------------------------------------------------------------------
# compute_scores — backwards compatible + extended
# ---------------------------------------------------------------------------

def compute_scores(sim):
    """
    Returns:
        integrity  — 0-1, overall system health
        friction   — 0-1, ego-driven resistance to cooperation

    Both are backwards compatible with the original interface.
    """
    ep = float(sim.get("ego_pressure", sim.get("Ep", 0.0)) or 0.0)
    ep = _clamp01(ep)
    base_integrity = sim["stability"] * 0.60 + sim["alignment"] * 0.25 + sim["trust_index"] * 0.15
    ego_penalty = nonlinear_ego_penalty(ep)
    integrity = base_integrity - ego_penalty
    friction  = (
        sim["ego"] * (1 - sim["alignment"]) * (1 - sim.get("trust_index", 0.5) * 0.3)
        + 0.25 * ep
        + 0.45 * ego_penalty
    )
    return round(float(np.clip(integrity, 0, 1)), 4), round(float(np.clip(friction, 0, 1)), 4)


# ---------------------------------------------------------------------------
# collapse_probability — derived from stability trace shape
# ---------------------------------------------------------------------------

def collapse_probability(sim):
    """
    Estimates probability of systemic collapse as a float 0-1.
    Uses:
      - Whether tipping point was reached
      - Trend slope of last 10 steps
      - Final ego vs alignment gap
    """
    trace = sim["stability_trace"]
    if not trace:
        return 0.5

    # Slope of last 10 steps (negative = declining)
    last = trace[-10:]
    slope = (last[-1] - last[0]) / max(len(last) - 1, 1)

    # Base probability from final stability
    base = 1.0 - sim["stability"]

    # Adjust for trend
    trend_penalty = max(0, -slope * 3.0)

    # Ego-alignment gap
    ego_gap = max(0, sim["ego"] - sim["alignment"]) * 0.4

    # Trust deficit
    trust_penalty = max(0, 0.5 - sim.get("trust_index", 0.5)) * 0.3

    # Tipping point hit
    tipping_bonus = 0.25 if sim.get("collapse_risk") else 0.0

    ep = _clamp01(sim.get("ego_pressure", sim.get("Ep", 0.0)) or 0.0)
    ego_penalty = nonlinear_ego_penalty(ep)
    # Patch 23B: collapse probability should respond sharply near the ego
    # tipping point instead of growing only linearly.
    ep_penalty = 0.20 * ep + 0.60 * ego_penalty

    prob = base * 0.35 + trend_penalty + ego_gap + trust_penalty + tipping_bonus + ep_penalty
    return round(float(np.clip(prob, 0, 1)), 3)


# ---------------------------------------------------------------------------
# trust_friction — how much distrust is slowing cooperation
# ---------------------------------------------------------------------------

def trust_friction(sim):
    """Trust-adjusted friction: higher when low trust + high ego."""
    t = sim.get("trust_index", 0.5)
    e = sim["ego"]
    a = sim["alignment"]
    ep = _clamp01(sim.get("ego_pressure", sim.get("Ep", 0.0)) or 0.0)
    tf = e * (1 - a) + (1 - t) * 0.4 + 0.18 * ep + 0.35 * nonlinear_ego_penalty(ep)
    return round(float(np.clip(tf, 0, 1)), 3)


# ---------------------------------------------------------------------------
# intervention_recommendations — actionable output per audit
# ---------------------------------------------------------------------------

def intervention_recommendations(sim, integrity, friction):
    """
    Returns a list of dicts:
        { "priority": "high"|"medium"|"low", "target": str, "action": str, "reason": str }
    """
    recs = []
    profiles = sim.get("agent_profiles", [])
    cp = collapse_probability(sim)

    # --- Ego Pressure / social capture ---
    ep = float(sim.get("ego_pressure", sim.get("Ep", 0.0)) or 0.0)
    if ep > 0.75:
        recs.append({
            "priority": "critical",
            "target":   "Consent baseline",
            "action":   "Cool-down phase and consent reset",
            "reason":   f"Ego Pressure={ep:.2f}. External social pressure is too high for a fair choice."
        })

    # --- Collapse risk ---
    if sim.get("collapse_risk"):
        step = sim.get("tipping_step", "?")
        recs.append({
            "priority": "critical",
            "target":   "System",
            "action":   "Emergency alignment intervention",
            "reason":   f"Stability crossed collapse threshold at step {step}. Immediate governor action required."
        })

    # --- High ego actors ---
    high_ego = [p for p in profiles if p["E"] > 0.65]
    for p in high_ego:
        recs.append({
            "priority": "high",
            "target":   p["name"].capitalize(),
            "action":   "Ego suppression — impose accountability mechanisms",
            "reason":   f"Ego={p['E']:.2f}, ideology={p['ideology']}. Driving systemic friction."
        })

    # --- Trust deficits ---
    low_trust = [p for p in profiles if p["trust"] < 0.38]
    for p in low_trust:
        recs.append({
            "priority": "high",
            "target":   p["name"].capitalize(),
            "action":   "Trust-building protocol — transparency measures",
            "reason":   f"Trust index={p['trust']:.2f}. Bilateral agreements recommended."
        })

    # --- Grievance accumulation ---
    grieving = [p for p in profiles if p["grievances"] > 2]
    for p in grieving:
        recs.append({
            "priority": "medium",
            "target":   p["name"].capitalize(),
            "action":   "Grievance resolution mechanism",
            "reason":   f"{p['grievances']} unresolved grievances. Risk of defection."
        })

    # --- Low alignment trend ---
    align_trace = sim.get("alignment_trace", [])
    if len(align_trace) >= 10:
        align_slope = align_trace[-1] - align_trace[-10]
        if align_slope < -0.05:
            recs.append({
                "priority": "high",
                "target":   "System",
                "action":   "Alignment floor enforcement — raise divine_floor parameter",
                "reason":   f"Alignment declining at {align_slope:.3f}/step. Shared-values erosion."
            })

    # --- Action imbalance: too much exploit ---
    counts = sim.get("action_counts", {})
    total  = sum(counts.values()) or 1
    exploit_rate = counts.get("exploit", 0) / total
    if exploit_rate > 0.35:
        recs.append({
            "priority": "high",
            "target":   "System",
            "action":   "Incentive redesign — penalise defection, reward cooperation",
            "reason":   f"{exploit_rate:.0%} of all actions were exploitative. Elite capture risk."
        })

    # --- Low integrity but stable ---
    if integrity < 0.45 and not sim.get("collapse_risk"):
        recs.append({
            "priority": "medium",
            "target":   "System",
            "action":   "Intelligence investment — raise capacity baseline",
            "reason":   f"Integrity={integrity:.2f}. System stable but underperforming."
        })

    # --- Good state ---
    if not recs:
        recs.append({
            "priority": "low",
            "target":   "System",
            "action":   "Maintain current conditions",
            "reason":   f"Integrity={integrity:.2f}, friction={friction:.2f}. System within healthy bounds."
        })

    # Sort: critical > high > medium > low
    order = {"critical": 0, "high": 1, "medium": 2, "low": 3}
    recs.sort(key=lambda r: order.get(r["priority"], 9))
    return recs


# ---------------------------------------------------------------------------
# full_report — convenience wrapper for app.py
# ---------------------------------------------------------------------------

def full_report(sim):
    """
    Single call that returns everything app.py needs to display.
    """
    integrity, friction = compute_scores(sim)
    cp                  = collapse_probability(sim)
    tf                  = trust_friction(sim)
    recs                = intervention_recommendations(sim, integrity, friction)

    return {
        "integrity":          integrity,
        "friction":           friction,
        "collapse_probability": cp,
        "trust_friction":     tf,
        "recommendations":    recs,
    }
