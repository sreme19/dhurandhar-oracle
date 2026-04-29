"""
pomdp.py — Partially Observable Markov Decision Process solver.

Algorithm: Point-Based Value Iteration (PBVI)
  Pineau et al. (2003) "Point-based value iteration: An anytime algorithm
  for POMDPs"

NEW to this project series (not in ipl-oracle or got-oracle).

Why PBVI over exact value iteration?
  The exact belief-space value function is piecewise linear and convex (PWLC)
  over the continuous belief simplex. Exact VI is exponential in |S|.
  PBVI samples a finite set of reachable belief points and only computes
  α-vectors (hyperplanes) for those points — tractable for |S| ≤ ~50.

Key concepts:
  S = set of world states (cover_intact × mission_phase × adversary_knowledge)
  A = set of actions (available_actions from turning point)
  O = set of observations (trust_signal | intelligence_return | handler_report | …)
  T(s'|s,a) = transition probability  [derived from causal_dag edge strengths]
  Z(o|s',a) = observation probability [derived from adversary information_set]
  R(s,a)    = reward                  [+10 mission_success, -8 cover_blown, -1 per step]
  γ         = discount factor (0.95)

PBVI update:
  For each belief point b in B:
    For each action a:
      α_{a,o}(s) = Σ_{s'} T(s'|s,a) · Z(o|s',a) · α*(s')
      α_a(s)     = R(s,a) + γ · Σ_o max_{α} Σ_{s'} α_{a,o}(s')
    α*(b) = argmax_a  b · α_a
"""
from __future__ import annotations

import numpy as np
from dataclasses import dataclass, field
from typing import Optional

from dhurandhar_oracle.schemas import (
    AdversaryModel, CausalDAG, OperativeState, POOMDPResult, StackelbergResult,
)


@dataclass
class POMDPModel:
    """Discrete POMDP specification."""
    states:      list[str]          # world state IDs
    actions:     list[str]
    observations: list[str]
    T:           np.ndarray         # |S| × |A| × |S|  transition
    Z:           np.ndarray         # |A| × |S| × |O|  observation
    R:           np.ndarray         # |S| × |A|         reward
    gamma:       float = 0.95


@dataclass
class PBVISolver:
    """Point-Based Value Iteration solver."""
    model:        POMDPModel
    gamma:        float = 0.95
    n_belief_points: int = 50
    n_iterations: int = 100
    alpha_vectors: list[np.ndarray] = field(default_factory=list)

    def solve(self) -> None:
        """Run PBVI and populate self.alpha_vectors."""
        # TODO: implement PBVI
        #   1. Sample initial belief points (stochastic simulation)
        #   2. Initialise alpha vectors (one per action, R(s,a) / (1-gamma))
        #   3. Iterate:
        #       a. For each belief point, compute backup
        #       b. Prune dominated alpha vectors
        #       c. Expand belief set with forward simulation
        #   4. Convergence: max change in V(b) < epsilon
        raise NotImplementedError("PBVI solver — implement in P2")

    def extract_result(
        self,
        belief_state: dict[str, float],
        action_override: Optional[str] = None,
    ) -> POOMDPResult:
        """Extract optimal action and values from solved alpha vectors."""
        # TODO: implement extraction
        #   1. Convert belief_state dict → numpy vector b
        #   2. V(b) = max_α (b · α)
        #   3. π(b) = argmax_a max_{α in Γ_a} (b · α)
        raise NotImplementedError("PBVI extraction — implement in P2")


def build_pomdp(
    available_actions: list[str],
    causal_dag: CausalDAG,
    adversaries: list[AdversaryModel],
    state_vector: OperativeState,
    initial_belief: dict[str, float],
    stackelberg: Optional[StackelbergResult] = None,
) -> POMDPModel:
    """
    Construct a POMDPModel from turning-point data.

    World states are discrete combinations of:
      cover_status ∈ {intact, suspected, blown}
      mission_phase ∈ {infiltrating, trust_building, intelligence_extraction, exfil}
      adversary_knowledge ∈ {unaware, suspicious, certain}

    This gives |S| = 3 × 4 × 3 = 36 states.

    Transition probabilities T(s'|s,a):
      Derived from causal_dag edge strengths.  Actions that trigger
      "cover_blown" effects increase P(cover_status → blown).

    Observation probabilities Z(o|s',a):
      Derived from adversary.information_set.  Adversaries with higher
      capability emit more informative observations.

    Reward R(s,a):
      +10  if s is terminal mission_success
      -8   if s is cover_blown
      -0.1 per step (encourages speed — answers "what would be faster?")
    """
    # TODO: implement full state space construction
    #   Placeholder: 3-state model for testing
    states  = list(initial_belief.keys()) or ["s0", "s1", "s2"]
    n_s     = len(states)
    n_a     = len(available_actions)
    n_o     = 3   # trust_signal | intelligence_return | no_signal

    T = np.ones((n_s, n_a, n_s)) / n_s   # uniform placeholder
    Z = np.ones((n_a, n_s, n_o)) / n_o   # uniform placeholder
    R = np.zeros((n_s, n_a))

    return POMDPModel(
        states=states,
        actions=available_actions,
        observations=["trust_signal", "intelligence_return", "no_signal"],
        T=T,
        Z=Z,
        R=R,
        gamma=0.95,
    )
