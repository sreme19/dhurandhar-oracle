"""
voi_node — Value of Information ranking.

NEW vs got-oracle.

Responsibilities:
  1. For each IntelligenceTarget, compute VoI = H(belief) - E[H(belief | obs)]
     where belief is the current POMDP belief state distribution
  2. Rank targets by VoI bits descending
  3. Penalise by access_difficulty to get effort-adjusted priority
  4. Answer: "What should Rizwan / Hamza gather next?"

Input  keys: intelligence_targets, initial_belief_state, hmm_results
Output keys: voi_result, errors, warnings

Algorithm:
  - Current belief H = -Σ p·log2(p) over belief_state distribution
  - For each target, estimate posterior belief after observing it
    (simplified: uniform update weighted by target.mission_relevance)
  - VoI = H(prior) - E[H(posterior)]
  - Effort-adjusted score = VoI / access_difficulty

TODO: replace simplified posterior estimate with a proper POMDP
  observation model once strategy_node PBVI is implemented.
"""
from __future__ import annotations

from dhurandhar_oracle.optimisation.voi import compute_voi_ranking
from dhurandhar_oracle.schemas import VoIResult
from dhurandhar_oracle.state import DhurandharState


def voi_node(state: DhurandharState) -> dict:
    """Rank intelligence targets by Value of Information."""
    errors:   list[str] = []
    warnings: list[str] = []

    intel_targets = state.get("intelligence_targets", [])
    belief_state  = state.get("initial_belief_state", {})

    if not intel_targets:
        warnings.append("voi_node: no intelligence targets defined — skipping VoI")
        return {
            "voi_result": VoIResult(rankings=[], top_target="", total_entropy_bits=0.0),
            "errors": errors, "warnings": warnings,
        }

    if not belief_state:
        warnings.append("voi_node: no belief state defined — using uniform prior")
        belief_state = {"unknown": 1.0}

    voi_result = compute_voi_ranking(intel_targets, belief_state)

    return {
        "voi_result": voi_result,
        "errors":     errors,
        "warnings":   warnings,
    }
