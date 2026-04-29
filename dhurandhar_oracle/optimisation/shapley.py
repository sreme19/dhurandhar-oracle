"""
shapley.py — Shapley values + defection incentive.

Ported from got-oracle/got_oracle/optimisation/shapley.py.
Same algorithm, new domain: coalition is the Indian handler/asset network
(Hamza, Aalam, Ajay Sanyal, ...) rather than GoT houses.

Public API:
  shapley_exact(actors, char_fn)        — O(N·2^N), exact
  shapley_approx(actors, char_fn, n)    — Monte Carlo approximation
  defection_incentive(actor, ...)       — gain from leaving the coalition
"""
from __future__ import annotations

import itertools
import math
import random
from typing import Callable


CharFn = Callable[[frozenset[str]], float]


def shapley_exact(
    actors: list[str],
    char_fn: CharFn,
) -> dict[str, float]:
    """
    Exact Shapley values via the formula:
      φᵢ = Σ_{S ⊆ N\{i}} |S|!(|N|-|S|-1)!/|N|! · [v(S∪{i}) - v(S)]
    Complexity: O(N·2^N) — use only for N ≤ 12.
    """
    n = len(actors)
    phi: dict[str, float] = {a: 0.0 for a in actors}

    for i, actor in enumerate(actors):
        others = [a for a in actors if a != actor]
        for size in range(len(others) + 1):
            for subset in itertools.combinations(others, size):
                S      = frozenset(subset)
                weight = (
                    math.factorial(len(S))
                    * math.factorial(n - len(S) - 1)
                    / math.factorial(n)
                )
                marginal = char_fn(S | {actor}) - char_fn(S)
                phi[actor] += weight * marginal

    return phi


def shapley_approx(
    actors: list[str],
    char_fn: CharFn,
    n_samples: int = 2000,
    seed: int = 42,
) -> dict[str, float]:
    """
    Monte Carlo Shapley approximation (Castro et al. 2009).
    Samples random permutations and computes marginal contributions.
    Complexity: O(n_samples · N).
    """
    rng = random.Random(seed)
    phi: dict[str, float] = {a: 0.0 for a in actors}

    for _ in range(n_samples):
        order   = actors[:]
        rng.shuffle(order)
        running = frozenset()
        for actor in order:
            marginal    = char_fn(running | {actor}) - char_fn(running)
            phi[actor] += marginal / n_samples
            running     = running | {actor}

    return phi


def defection_incentive(
    actor: str,
    all_actors: list[str],
    char_fn: CharFn,
    phi_in: float,
) -> float:
    """
    Defection incentive: how much the actor gains by leaving the coalition.
      incentive = φ_out - φ_in
    where φ_out is the Shapley value in a singleton coalition {actor}.
    Positive value = actor is better off defecting.
    """
    solo_coalition = frozenset({actor})
    phi_out        = char_fn(solo_coalition)
    return phi_out - phi_in
