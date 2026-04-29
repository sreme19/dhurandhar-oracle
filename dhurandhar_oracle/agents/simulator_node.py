"""
simulator_node — Monte Carlo mission rollouts.

Same technique as got-oracle (vectorised NumPy Bernoulli sampling),
adapted for intelligence-ops metrics.

Responsibilities:
  1. Simulate `n_rollouts` missions under the *actual* action (from outcome data)
  2. Simulate `n_rollouts` missions under the *optimal* action (from POMDP)
  3. Compute p_mission_success, p_cover_blown, and 95% Wilson CIs for each
  4. Identify the single highest-impact causal edge (key_lever)

Metrics:
  - p_mission_success: fraction of rollouts where terminal state = success
  - p_cover_blown:     fraction where cover_integrity drops below threshold
  (replaces got-oracle's p_survival / p_throne)

Input  keys: causal_dag, pomdp, action_override, state_vector
Output keys: simulation_actual, simulation_optimal, errors, warnings
"""
from __future__ import annotations

import numpy as np

from dhurandhar_oracle.schemas import SimulationOutput
from dhurandhar_oracle.state import DhurandharState

_N_ROLLOUTS          = 2_000
_COVER_THRESHOLD     = 3.0   # cover_integrity below this → blown
_RNG_SEED            = 42


def simulator_node(state: DhurandharState) -> dict:
    """Run Monte Carlo rollouts for actual and optimal actions."""
    errors:   list[str] = []
    warnings: list[str] = []

    causal_dag    = state.get("causal_dag")
    pomdp         = state.get("pomdp")
    state_vector  = state.get("state_vector")
    action_override = state.get("action_override")

    if not causal_dag or not state_vector:
        errors.append("simulator_node: missing causal_dag or state_vector")
        return {"errors": errors, "warnings": warnings}

    optimal_action = (
        action_override
        if action_override
        else (pomdp.optimal_action if pomdp else None)
    )

    # TODO: load actual_action from outcomes JSON
    actual_action = action_override or (pomdp.optimal_action if pomdp else None)

    if not optimal_action:
        warnings.append("simulator_node: no optimal_action from POMDP — skipping simulation")
        return {"errors": errors, "warnings": warnings}

    rng = np.random.default_rng(_RNG_SEED)

    sim_actual  = _rollout(actual_action,  causal_dag, state_vector, rng, _N_ROLLOUTS)
    sim_optimal = _rollout(optimal_action, causal_dag, state_vector, rng, _N_ROLLOUTS)

    return {
        "simulation_actual":  sim_actual,
        "simulation_optimal": sim_optimal,
        "errors":             errors,
        "warnings":           warnings,
    }


def _rollout(
    action: str,
    causal_dag,
    state_vector,
    rng: np.random.Generator,
    n: int,
) -> SimulationOutput:
    """Run `n` Monte Carlo rollouts through the causal DAG."""
    # Walk the DAG from `action` node, sampling each edge
    success_flags = np.zeros(n, dtype=bool)
    cover_blown   = np.zeros(n, dtype=bool)

    edges = causal_dag.edges
    action_edges = [e for e in edges if e.cause == action]

    key_lever: str | None = None
    max_impact = 0.0

    for i in range(n):
        cover_ok = True
        mission_ok = True
        active = {action}

        # BFS through DAG
        frontier = list(action_edges)
        while frontier:
            edge = frontier.pop()
            if rng.random() < edge.strength:
                active.add(edge.effect)
                # TODO: map effect names to mission/cover outcome flags
                if "cover_blown" in edge.effect or "identity_exposed" in edge.effect:
                    cover_ok = False
                if "mission_fail" in edge.effect or "operative_captured" in edge.effect:
                    mission_ok = False
                # Push downstream
                frontier.extend([e for e in edges if e.cause == edge.effect])

        success_flags[i] = mission_ok
        cover_blown[i]   = not cover_ok

    p_success   = float(success_flags.mean())
    p_cover     = float(cover_blown.mean())

    # Wilson CI for p_success
    from scipy.stats import norm as _norm
    z = _norm.ppf(0.975)
    denom  = 1 + z ** 2 / n
    centre = (p_success + z ** 2 / (2 * n)) / denom
    margin = z * (p_success * (1 - p_success) / n + z ** 2 / (4 * n ** 2)) ** 0.5 / denom
    ci_low  = max(0.0, centre - margin)
    ci_high = min(1.0, centre + margin)

    # Key lever: edge with highest strength leading to terminal outcome
    if action_edges:
        key_edge = max(action_edges, key=lambda e: e.strength)
        key_lever = f"{key_edge.cause} → {key_edge.effect}  (p={key_edge.strength:.2f})"

    mode = "mission_success" if p_success >= 0.5 else "mission_failure"
    if p_cover >= 0.5:
        mode = "cover_blown"

    return SimulationOutput(
        action=action,
        p_mission_success=round(p_success, 4),
        p_cover_blown=round(p_cover, 4),
        ci_low=round(ci_low, 4),
        ci_high=round(ci_high, 4),
        n_rollouts=n,
        mode_outcome=mode,
        key_lever=key_lever,
    )
