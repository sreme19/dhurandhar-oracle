"""
adversary_node — Stackelberg leader-follower equilibrium.

NEW vs got-oracle (which used CFR / symmetric Nash).

Responsibilities:
  1. Model the three-level hierarchy:
       RAW handler (leader) → commits to an operation strategy
       Operative (middle)   → picks best response to handler's commitment
       Adversary (follower) → picks best response to observable operative action
  2. Solve by backward induction:
       a. For each operative action, compute adversary's best response
       b. For each handler strategy, compute operative's best response
          given the anticipated adversary counter
       c. Handler picks strategy that maximises Indian expected payoff
  3. Compute commitment_value = V(Stackelberg) - V(Nash)
     (how much the ability to pre-commit is worth)

Input  keys: adversaries, high_threat_actors, available_actions,
             state_vector, belief_gaps
Output keys: stackelberg, errors, warnings

Why Stackelberg not CFR?
  In Dhurandhar, RAW issues standing orders before the operative acts,
  and the adversary reacts to the operative's observable behaviour.
  This sequential commitment structure is exactly Stackelberg — not the
  simultaneous imperfect-info game that CFR solves.
"""
from __future__ import annotations

from dhurandhar_oracle.optimisation.stackelberg import solve_stackelberg
from dhurandhar_oracle.schemas import StackelbergResult
from dhurandhar_oracle.state import DhurandharState


def adversary_node(state: DhurandharState) -> dict:
    """Compute Stackelberg equilibrium for Indian handler → operative → adversary."""
    errors:   list[str] = []
    warnings: list[str] = []

    adversaries      = state.get("adversaries", [])
    high_threat      = set(state.get("high_threat_actors", []))
    available_actions = state.get("available_actions", [])
    state_vector     = state.get("state_vector")
    belief_gaps      = state.get("belief_gaps", [])

    # Focus on the single highest-threat adversary for Stackelberg
    # (multi-adversary Stackelberg is future work)
    active_adversaries = [a for a in adversaries if a.actor in high_threat]

    if not active_adversaries:
        warnings.append("adversary_node: no high-threat adversaries — skipping Stackelberg")
        return {"errors": errors, "warnings": warnings}

    primary_adversary = max(active_adversaries, key=lambda a: a.capability)

    result: StackelbergResult = solve_stackelberg(
        adversary=primary_adversary,
        available_actions=available_actions,
        state_vector=state_vector,
        belief_gaps=belief_gaps,
    )

    return {
        "stackelberg": result,
        "errors":      errors,
        "warnings":    warnings,
    }
