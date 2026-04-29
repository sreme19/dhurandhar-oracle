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

from dhurandhar_oracle.optimisation.stackelberg import solve_stackelberg, solve_stackelberg_multi
from dhurandhar_oracle.schemas import StackelbergResult
from dhurandhar_oracle.state import DhurandharState


def adversary_node(state: DhurandharState) -> dict:
    """Compute Stackelberg equilibrium for Indian handler → operative → adversary.

    Multi-adversary extension: when multiple high-threat adversaries exist (e.g.
    PLA + ISI in Film 4), solve against each independently then aggregate payoffs
    as a capability-weighted convex combination. The operative best response is the
    action that maximises expected payoff across the adversary coalition.
    """
    errors:   list[str] = []
    warnings: list[str] = []

    adversaries       = state.get("adversaries", [])
    high_threat       = set(state.get("high_threat_actors", []))
    available_actions = state.get("available_actions", [])
    state_vector      = state.get("state_vector")
    belief_gaps       = state.get("belief_gaps", [])

    active_adversaries = [a for a in adversaries if a.actor in high_threat]

    # Fall back: if no actor is in high_threat (e.g. threat scoring not yet run),
    # use all adversaries above capability threshold 7.0
    if not active_adversaries:
        active_adversaries = [a for a in adversaries if a.capability >= 7.0]
        if active_adversaries:
            warnings.append(
                "adversary_node: no high_threat_actors set — using all adversaries "
                f"with capability >= 7.0 ({[a.actor for a in active_adversaries]})"
            )

    if not active_adversaries:
        warnings.append("adversary_node: no active adversaries — skipping Stackelberg")
        return {"errors": errors, "warnings": warnings}

    if len(active_adversaries) == 1:
        # Single-adversary path (unchanged behaviour)
        result: StackelbergResult = solve_stackelberg(
            adversary=active_adversaries[0],
            available_actions=available_actions,
            state_vector=state_vector,
            belief_gaps=belief_gaps,
        )
    else:
        # Multi-adversary: capability-weighted aggregation
        warnings.append(
            f"adversary_node: multi-adversary Stackelberg over "
            f"{[a.actor for a in active_adversaries]}"
        )
        result = solve_stackelberg_multi(
            adversaries=active_adversaries,
            available_actions=available_actions,
            state_vector=state_vector,
            belief_gaps=belief_gaps,
        )

    return {
        "stackelberg": result,
        "errors":      errors,
        "warnings":    warnings,
    }
