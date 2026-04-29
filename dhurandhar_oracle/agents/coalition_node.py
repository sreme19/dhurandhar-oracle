"""
coalition_node — Shapley values over the Indian handler / asset network.

Runs IN PARALLEL with intel_network_node (LangGraph fan-out from state_node).

Responsibilities:
  1. Build the coalition of Indian-side actors from alliance_snapshot
     (in_coalition=True edges where source is Indian operative/handler)
  2. Compute Shapley values — each actor's marginal contribution to
     mission_success_probability
  3. Compute defection incentives — would an asset gain by switching sides?
     (key for mole detection cross-check with HMM)

Input  keys: alliance_snapshot, state_vector
Output keys: shapley, errors, warnings

TODO: calibrate coalition characteristic function v(S) against
  mission_success_prob from the simulator once it's implemented.
"""
from __future__ import annotations

from dhurandhar_oracle.optimisation.shapley import shapley_exact, defection_incentive
from dhurandhar_oracle.state import DhurandharState
from dhurandhar_oracle.schemas import ShapleyResult

_MAX_EXACT_PLAYERS = 8   # O(N·2^N) — fall back to Monte Carlo above this


def coalition_node(state: DhurandharState) -> dict:
    """Compute Shapley values for the Indian asset coalition."""
    errors:   list[str] = []
    warnings: list[str] = []

    alliance_snapshot = state.get("alliance_snapshot", [])
    coalition_edges   = [e for e in alliance_snapshot if e.in_coalition]

    if not coalition_edges:
        warnings.append("coalition_node: no in-coalition edges — returning empty Shapley")
        return {
            "shapley": ShapleyResult(values={}, defection_incentives={}),
            "errors": errors, "warnings": warnings,
        }

    actors = list({e.target for e in coalition_edges})

    # TODO: replace stub characteristic function with Monte Carlo mission sim
    def char_fn(subset: frozenset[str]) -> float:
        """Stub: coalition value = sum of edge strengths for actors in subset."""
        return sum(
            e.strength for e in coalition_edges
            if e.target in subset
        )

    if len(actors) <= _MAX_EXACT_PLAYERS:
        phi = shapley_exact(actors, char_fn)
    else:
        warnings.append(f"coalition_node: {len(actors)} actors — using Monte Carlo Shapley")
        from dhurandhar_oracle.optimisation.shapley import shapley_approx
        phi = shapley_approx(actors, char_fn, n_samples=2000)

    defections = {a: defection_incentive(a, actors, char_fn, phi[a]) for a in actors}

    return {
        "shapley": ShapleyResult(values=phi, defection_incentives=defections),
        "errors":  errors,
        "warnings": warnings,
    }
