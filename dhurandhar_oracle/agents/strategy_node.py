"""
strategy_node — POMDP Point-Based Value Iteration (PBVI).

NEW vs got-oracle (which used CFR + MDP).

Responsibilities:
  1. Construct the POMDP:
       S = world states (cover_intact × mission_phase × adversary_knowledge)
       A = available_actions
       O = observations (trust signals, intelligence returns, handler reports)
       T = transition function (from causal_dag edges)
       Z = observation function (from adversary information_set)
       R = reward function (mission_success bonus - cover_blown penalty)
  2. Run PBVI over a set of sampled belief points to compute V(b)
  3. Extract greedy policy π(b) = argmax_a [R(b,a) + γ Σ P(o|b,a) V(τ(b,a,o))]
  4. Report: optimal_action, action_values Q(b,a), mission_success_prob,
             cover_integrity_prob

Input  keys: initial_belief_state, available_actions, causal_dag,
             adversaries, state_vector, stackelberg, action_override
Output keys: pomdp, errors, warnings

Why POMDP not MDP?
  An operative in the field never observes the full state — they don't
  know if their cover has been suspected, or if the handler's comms are
  being monitored. POMDP planning over a belief state (a probability
  distribution over possible world states) is the correct model.
  PBVI is tractable for discrete action/state spaces of this size.
"""
from __future__ import annotations

from dhurandhar_oracle.optimisation.pomdp import PBVISolver, build_pomdp
from dhurandhar_oracle.schemas import POOMDPResult
from dhurandhar_oracle.state import DhurandharState


def strategy_node(state: DhurandharState) -> dict:
    """Solve POMDP and return optimal policy + action values."""
    errors:   list[str] = []
    warnings: list[str] = []

    available_actions = state.get("available_actions", [])
    causal_dag        = state.get("causal_dag")
    adversaries       = state.get("adversaries", [])
    state_vector      = state.get("state_vector")
    belief_state      = state.get("initial_belief_state", {})
    stackelberg       = state.get("stackelberg")
    action_override   = state.get("action_override")

    if not available_actions or not causal_dag:
        errors.append("strategy_node: missing available_actions or causal_dag")
        return {"errors": errors, "warnings": warnings}

    if not belief_state:
        warnings.append("strategy_node: no belief state — using uniform prior")
        belief_state = {f"state_{i}": 1.0 / 3 for i in range(3)}

    # ── Build and solve POMDP ─────────────────────────────────────────────────
    pomdp_model = build_pomdp(
        available_actions=available_actions,
        causal_dag=causal_dag,
        adversaries=adversaries,
        state_vector=state_vector,
        initial_belief=belief_state,
        stackelberg=stackelberg,
    )

    solver = PBVISolver(pomdp_model, gamma=0.95, n_belief_points=50, n_iterations=100)
    solver.solve()

    result: POOMDPResult = solver.extract_result(belief_state, action_override)

    return {
        "pomdp":    result,
        "errors":   errors,
        "warnings": warnings,
    }
