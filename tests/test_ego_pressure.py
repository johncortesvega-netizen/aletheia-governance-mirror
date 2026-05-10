import numpy as np

from config.weights import DEFAULT_WEIGHTS
from core.simulation import simulate
from core.scoring import full_report
from protocol import check_ego_pressure, final_protocol_judgment


def test_high_ego_pressure_fails_closed():
    features = {
        "technical_complexity": 0.45,
        "centralization": 0.45,
        "anonymity": 0.30,
        "regulation": 0.55,
        "transparency": 0.60,
        "capital_scale": 0.40,
        "ego_pressure": 0.90,
    }
    text = "I cannot say no because they will be upset and everyone will think I am selfish."
    np.random.seed(7)
    sim = simulate(features, DEFAULT_WEIGHTS, steps=20, n_agents=6, ego_pressure=0.90)
    report = full_report(sim)
    gate = check_ego_pressure(text, 0.90)
    judgment = final_protocol_judgment(text, {}, sim, report, base_verdict="SANCTUARY")

    assert gate["verdict"] == "ASYLUM"
    assert judgment["verdict"] == "ASYLUM"
    assert judgment["corruption_risk"] == "High"
    assert report["collapse_probability"] >= 0.35
