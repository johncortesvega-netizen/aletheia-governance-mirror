import numpy as np

# ---------------------------------------------------------------------------
# Sydney Protocol Agent — persistent identity, trust ledger, memory
# ---------------------------------------------------------------------------

IDEOLOGY_PROFILES = {
    "cooperative":   {"base_A": 0.78, "base_E": 0.18, "exploit_bias": 0.05},
    "realist":       {"base_A": 0.48, "base_E": 0.45, "exploit_bias": 0.35},
    "aggressive":    {"base_A": 0.22, "base_E": 0.72, "exploit_bias": 0.70},
    "isolationist":  {"base_A": 0.32, "base_E": 0.38, "exploit_bias": 0.15},
    "mediator":      {"base_A": 0.68, "base_E": 0.22, "exploit_bias": 0.08},
}

def _assign_ideology(A, E):
    if A > 0.65 and E < 0.30:
        return "cooperative"
    if E > 0.62:
        return "aggressive"
    if A < 0.38 and E < 0.50:
        return "isolationist"
    if A > 0.55 and E < 0.42:
        return "mediator"
    return "realist"


class Agent:
    def __init__(self, agent_id, I, P, E, A, name="actor", Ep=0.0):
        self.id       = agent_id
        self.name     = name
        self.I        = float(np.clip(I, 0, 1))
        self.P        = float(np.clip(P, 0, 1))
        self.E        = float(np.clip(E, 0, 1))
        self.Ep       = float(np.clip(Ep, 0, 1))
        self.A        = float(np.clip(A, 0, 1))
        self.ideology = _assign_ideology(A, E)
        self.neighbors     = []
        self.trust_ledger  = {}   # {other_id: float 0-1}
        self.grievances    = {}   # {other_id: int count}
        self.alliances     = set()
        self.memory        = []   # last N actions
        self.history       = []   # (t, I, P, E, A, action) per step

    def avg_trust(self):
        vals = list(self.trust_ledger.values())
        return float(np.mean(vals)) if vals else 0.5

    def observe(self, system):
        return {
            "I":                round(self.I, 3),
            "P":                round(self.P, 3),
            "E":                round(self.E, 3),
            "Ep":               round(self.Ep, 3),
            "A":                round(self.A, 3),
            "global_stability": round(_compute_stability(system), 3),
            "avg_ego":          round(float(np.mean([a.E for a in system["agents"]])), 3),
            "avg_trust":        round(self.avg_trust(), 3),
            "recent_exploits":  self.memory.count("exploit"),
        }

    def update_trust(self, other_id, action):
        cur = self.trust_ledger.get(other_id, 0.5)
        delta = {"exploit": -0.14, "cooperate": 0.08,
                 "stabilize": 0.04, "isolate": -0.04}.get(action, 0)
        self.trust_ledger[other_id] = float(np.clip(cur + delta, 0, 1))
        if action == "exploit":
            self.grievances[other_id] = self.grievances.get(other_id, 0) + 1
            self.alliances.discard(other_id)
        elif action == "cooperate" and self.trust_ledger[other_id] > 0.65:
            self.alliances.add(other_id)


# ---------------------------------------------------------------------------
# Stability formula  (fixed vs. original broken version)
# ---------------------------------------------------------------------------

def _compute_stability(system):
    agents = system["agents"]
    if not agents:
        return 0.0
    agent_scores = [0.35 * a.I + 0.30 * a.A - 0.25 * a.E + 0.10 * a.P - 0.18 * a.Ep
                    for a in agents]
    avg_score = float(np.mean(agent_scores))
    avg_trust = float(np.mean([a.avg_trust() for a in agents]))
    return float(np.clip(avg_score * 0.75 + avg_trust * 0.25, 0, 1))


# ---------------------------------------------------------------------------
# Ideology-aware decision policy
# ---------------------------------------------------------------------------

def _policy(agent, obs):
    S   = obs["global_stability"]
    ide = agent.ideology

    # Global collapse — everyone cooperates
    if S < 0.25:
        return "cooperate"

    profile = IDEOLOGY_PROFILES[ide]
    exploit_p = profile["exploit_bias"]

    if ide == "cooperative":
        return "cooperate" if np.random.random() < 0.78 else "stabilize"

    if ide == "aggressive":
        if S > 0.38 and agent.P < 0.88:
            return "exploit" if np.random.random() < exploit_p else "cooperate"
        return "cooperate"

    if ide == "isolationist":
        return "isolate" if obs["avg_trust"] < 0.40 else "stabilize"

    if ide == "mediator":
        return "cooperate" if obs["avg_ego"] > 0.52 else "stabilize"

    # Realist
    if agent.P > 0.70 and agent.E > 0.50:
        return "exploit" if np.random.random() < exploit_p else "cooperate"
    if S < 0.42:
        return "cooperate"
    return "stabilize" if np.random.random() < 0.45 else "cooperate"


# ---------------------------------------------------------------------------
# Action execution
# ---------------------------------------------------------------------------

def _act(agent, action, system, ego_tolerance, divine_floor):
    agent.memory.append(action)
    if len(agent.memory) > 8:
        agent.memory.pop(0)

    if action == "exploit":
        agent.P  = np.clip(agent.P + 0.06, 0, 1)
        agent.A  = np.clip(agent.A - 0.06, divine_floor, 1)
        agent.E  = np.clip(agent.E + 0.04, 0, 1)
        for nb in agent.neighbors:
            nb.update_trust(agent.id, "exploit")

    elif action == "cooperate":
        agent.A  = np.clip(agent.A + 0.07, divine_floor, 1)
        agent.E  = np.clip(agent.E - 0.04, 0, 1)
        agent.I  = np.clip(agent.I + 0.01, 0, 1)
        for nb in agent.neighbors:
            nb.update_trust(agent.id, "cooperate")
            agent.update_trust(nb.id, "cooperate")

    elif action == "stabilize":
        agent.I  = np.clip(agent.I + 0.04, 0, 1)
        agent.A  = np.clip(agent.A + 0.02, divine_floor, 1)
        agent.E  = np.clip(agent.E - 0.01, 0, 1)
        for nb in agent.neighbors:
            nb.update_trust(agent.id, "stabilize")

    elif action == "isolate":
        agent.A  = np.clip(agent.A - 0.03, divine_floor, 1)
        agent.P  = np.clip(agent.P - 0.01, 0, 1)

    # Ego-tolerance clamp — Sydney Protocol enforcement
    if agent.E > ego_tolerance:
        agent.A = np.clip(agent.A - 0.03, divine_floor, 1)

    agent.history.append({
        "I": round(agent.I, 3), "P": round(agent.P, 3),
        "E": round(agent.E, 3), "A": round(agent.A, 3),
        "action": action
    })


# ---------------------------------------------------------------------------
# System initialisation from features dict
# ---------------------------------------------------------------------------

def _build_agents_from_features(features, weights, n_agents=6, ego_pressure=None):
    """
    Map scenario features onto a small agent ensemble.
    Different agents represent different stakeholder archetypes
    in the scenario (e.g. regulator, operator, market, public).
    """
    archetypes = [
        # (name,  I_bias,  P_bias,  E_bias,  A_bias)
        ("regulator",   0.10,  0.00,  -0.20,   0.20),
        ("operator",    0.00,  0.20,   0.15,  -0.05),
        ("market",     -0.05,  0.15,   0.20,  -0.10),
        ("public",     -0.10, -0.10,  -0.05,   0.10),
        ("tech_layer",  0.15,  0.05,   0.05,   0.00),
        ("capital",     0.05,  0.20,   0.25,  -0.15),
    ]

    base_I = 0.60 + 0.30 * features["technical_complexity"]
    base_P = 0.50 + 0.50 * features["centralization"]
    base_E = 0.40 + 0.50 * features["anonymity"]
    base_A = 0.50 + 0.50 * features["regulation"]
    if ego_pressure is None:
        ego_pressure = features.get("ego_pressure", features.get("Ep", 0.0))
    ego_pressure = float(np.clip(ego_pressure, 0, 1))

    agents = []
    for i, (name, dI, dP, dE, dA) in enumerate(archetypes[:n_agents]):
        noise = np.random.normal(0, 0.04, 4)
        a = Agent(
            agent_id=i,
            name=name,
            I=base_I + dI + noise[0],
            P=base_P + dP + noise[1],
            E=base_E + dE + noise[2] + 0.10 * ego_pressure,
            A=base_A + dA + noise[3] - 0.12 * ego_pressure,
            Ep=ego_pressure,
        )
        agents.append(a)

    # Wire neighbors (fully connected small graph)
    for a in agents:
        a.neighbors = [x for x in agents if x.id != a.id]
        for nb in a.neighbors:
            a.trust_ledger[nb.id] = float(np.clip(
                np.random.normal(0.5 + 0.15 * features["regulation"], 0.08), 0, 1
            ))

    return agents


# ---------------------------------------------------------------------------
# Main simulate() — drop-in replacement for the original
# ---------------------------------------------------------------------------

def simulate(features, weights, ego_tolerance=0.55, divine_floor=0.45,
             n_agents=6, steps=40, n=None, ego_pressure=None):
    """
    Runs a Sydney Protocol agent-based simulation from scenario features.

    Returns a dict compatible with the original interface PLUS new fields:
        trust_index      — system-wide average trust
        stability_trace  — S(t) list over simulation steps
        trust_trace      — trust(t) list
        ego_trace        — ego(t) list
        alignment_trace  — alignment(t) list
        agent_profiles   — final state of each archetype agent
        collapse_risk    — bool, True if S fell below 0.30 at any point
        tipping_step     — first step where S < 0.30, else None
        action_counts    — distribution of actions taken
    """
    if ego_pressure is None:
        ego_pressure = features.get("ego_pressure", features.get("Ep", 0.0))
    ego_pressure = float(np.clip(ego_pressure, 0, 1))
    agents = _build_agents_from_features(features, weights, n_agents, ego_pressure=ego_pressure)
    system = {"agents": agents}

    stability_trace  = []
    trust_trace      = []
    ego_trace        = []
    alignment_trace  = []
    ego_pressure_trace = []
    collapse_risk    = False
    tipping_step     = None
    action_counts    = {"exploit": 0, "cooperate": 0,
                        "stabilize": 0, "isolate": 0}

    for t in range(steps):
        actions = [_policy(a, a.observe(system)) for a in agents]
        for a, action in zip(agents, actions):
            _act(a, action, system, ego_tolerance, divine_floor)
            action_counts[action] += 1

        S     = _compute_stability(system)
        trust = float(np.mean([a.avg_trust() for a in agents]))
        ego   = float(np.mean([a.E for a in agents]))
        align = float(np.mean([a.A for a in agents]))
        ep    = float(np.mean([a.Ep for a in agents]))

        if ep > 0.0:
            S = float(np.clip(S - 0.22 * ep, 0, 1))
            trust = float(np.clip(trust - 0.16 * ep, 0, 1))
            align = float(np.clip(align - 0.18 * ep, 0, 1))

        stability_trace.append(round(S, 4))
        trust_trace.append(round(trust, 4))
        ego_trace.append(round(ego, 4))
        alignment_trace.append(round(align, 4))
        ego_pressure_trace.append(round(ep, 4))

        if S < 0.30 and not collapse_risk:
            collapse_risk = True
            tipping_step  = t

    final_S     = float(np.mean(stability_trace[-10:]))   # trailing mean
    final_ego   = float(np.mean(ego_trace[-10:]))
    final_align = float(np.mean(alignment_trace[-10:]))
    final_trust = float(np.mean(trust_trace[-10:]))

    agent_profiles = [
        {
            "name":      a.name,
            "ideology":  a.ideology,
            "I": round(a.I, 3), "P": round(a.P, 3),
            "E": round(a.E, 3), "Ep": round(a.Ep, 3), "A": round(a.A, 3),
            "trust":     round(a.avg_trust(), 3),
            "alliances": len(a.alliances),
            "grievances": sum(a.grievances.values()),
            "last_action": a.memory[-1] if a.memory else "—",
        }
        for a in agents
    ]

    return {
        # --- original interface (backwards compatible) ---
        "stability":    final_S,
        "ego":          final_ego,
        "alignment":    final_align,
        "ego_pressure": ego_pressure,
        "Ep": ego_pressure,
        "distribution": stability_trace,   # was list of floats

        # --- new fields ---
        "trust_index":     final_trust,
        "stability_trace": stability_trace,
        "trust_trace":     trust_trace,
        "ego_trace":       ego_trace,
        "alignment_trace": alignment_trace,
        "ego_pressure_trace": ego_pressure_trace,
        "agent_profiles":  agent_profiles,
        "collapse_risk":   collapse_risk,
        "tipping_step":    tipping_step,
        "action_counts":   action_counts,
        "steps":           steps,
    }
