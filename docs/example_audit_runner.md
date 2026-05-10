# Patch 54 — Example Audit Runner / Demo Inputs

Patch 54 adds a small, opt-in demo input library so first-time users can see how ALETHEIA behaves without searching for an external governance document.

## Purpose

Demo inputs help users test the workflow quickly:

- load a sample AI policy
- load a sample DAO governance charter
- load a sample public policy scenario
- run Mirror Check only after an explicit user click
- compare the generated report to the public sample reports

## Safe Demo Rule

Demo material must never run automatically.

The default state remains user input. A demo only becomes active when the user deliberately selects a demo and clicks the load button.

## Included Demo Inputs

- `examples/demo_inputs/sample_ai_policy.txt`
- `examples/demo_inputs/sample_dao_governance.txt`
- `examples/demo_inputs/sample_public_policy.txt`

## Boundary

These inputs are fictional examples for interface testing and learning. They are not legal advice, policy recommendations, evidence sources, or governance decisions.

ALETHEIA reflects. Humans review. Power stays accountable.
