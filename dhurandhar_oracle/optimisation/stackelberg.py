"""
stackelberg.py — Stackelberg leader-follower game solver.

NEW to this project series (got-oracle used CFR / symmetric Nash).

Theory:
  A Stackelberg game has a sequential commitment structure:
    Leader  (RAW handler)  commits to a strategy σ_L first (publicly or verifiably)
    Middle  (operative)    observes commitment, picks best response σ_M(σ_L)
    Follower (adversary)   observes operative action, picks best response σ_F(σ_M)

  Solved by backward induction (subgame perfect equilibrium):
    Step 1: For each operative action a_M, find adversary's best response:
              a_F*(a_M) = argmax_{a_F} u_F(a_M, a_F)
    Step 2: For each handler strategy σ_L, find operative's best response:
              a_M*(σ_L) = argmax_{a_M} u_M(σ_L, a_M, a_F*(a_M))
    Step 3: Handler picks:
              σ_L* = argmax_{σ_L} u_L(σ_L, a_M*(σ_L), a_F*(a_M*(σ_L)))

  Commitment value = V_Stackelberg(leader) - V_Nash(leader)
    (how much the leader gains from being able to pre-commit)

Why not CFR?
  CFR finds Nash equilibrium of simultaneous imperfect-information games.
  Here the handler moves first, then the operative, then the adversary —
  a sequential game where the Stackelberg equilibrium concept applies.
  In particular, the handler's *commitment* changes adversary incentives.
"""
from __future__ import annotations

import numpy as np
from typing import Optional

from dhurandhar_oracle.schemas import (
    AdversaryModel, BeliefGap, OperativeState, StackelbergResult,
)

# Payoff calibration (arbitrary scale, tuned to mission outcomes)
_MISSION_SUCCESS_PAYOFF = 10.0
_COVER_BLOWN_PAYOFF     = -8.0
_STEP_COST              = -0.5


def solve_stackelberg(
    adversary: AdversaryModel,
    available_actions: list[str],
    state_vector: Optional[OperativeState],
    belief_gaps: list[BeliefGap],
) -> StackelbergResult:
    """
    Solve the three-level Stackelberg game by backward induction.

    TODO: implement full payoff matrices from causal_dag
    Current stub: uses heuristic payoffs from adversary.capability and state_vector.
    """
    n_actions = len(available_actions)
    if n_actions == 0:
        raise ValueError("No available actions for Stackelberg solver")

    # ── Build payoff matrices (stub — replace with causal DAG rollout) ────────
    rng = np.random.default_rng(42)
    # u_indian[a_M] = Indian payoff for each operative action (simplified)
    u_indian    = rng.uniform(0.2, 0.8, size=n_actions)
    # u_adversary[a_M] = adversary payoff for each operative action
    u_adversary = 1.0 - u_indian + rng.uniform(-0.1, 0.1, size=n_actions)

    # ── Belief gap penalty: if adversary knows more than we think, reduce payoff
    total_gap = sum(bg.gap for bg in belief_gaps if bg.actor == adversary.actor)
    u_indian   = u_indian * (1.0 - 0.2 * min(total_gap, 1.0))

    # ── Step 1: adversary best response to each operative action ─────────────
    # (In this 2-level simplified version, adversary counters the operative)
    adv_best = {
        available_actions[i]: available_actions[np.argmin(u_indian)]
        for i in range(n_actions)
    }

    # ── Step 2: operative best response (argmax Indian payoff after adversary counter) ─
    operative_best_idx = int(np.argmax(u_indian))
    operative_best     = available_actions[operative_best_idx]

    # ── Step 3: handler commits to strategy that maximises indian payoff ──────
    # (In a 3-level game the handler's strategy space is a distribution over directives)
    # Stub: handler commits to the action that yields highest indian payoff
    leader_action = operative_best   # handler endorses operative's optimal action

    # ── Commitment value vs Nash baseline ────────────────────────────────────
    # Nash: both play simultaneously → mixed strategy Nash ≈ uniform (no info)
    nash_payoff_indian    = float(u_indian.mean())
    stackelberg_payoff    = float(u_indian[operative_best_idx])
    commitment_value      = stackelberg_payoff - nash_payoff_indian

    adv_response = adv_best.get(operative_best, available_actions[0])

    return StackelbergResult(
        leader_action=leader_action,
        operative_best_response=operative_best,
        follower_best_response=adv_response,
        equilibrium_payoff_indian=round(stackelberg_payoff, 4),
        equilibrium_payoff_adversary=round(float(u_adversary[operative_best_idx]), 4),
        commitment_value=round(commitment_value, 4),
    )
