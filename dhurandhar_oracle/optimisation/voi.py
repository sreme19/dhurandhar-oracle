"""
voi.py — Value of Information (VoI) computation.

NEW to this project series.

Theory:
  The Value of Information of intelligence target X, given current belief b, is:
    VoI(X) = H(b) - E_x[H(b | X=x)]
  where H is Shannon entropy and the expectation is over possible observations x.

  In information-theoretic terms: VoI is the mutual information I(b; X) —
  how many bits of uncertainty about the mission state would observing X remove.

  Effort-adjusted VoI: score = VoI(X) / access_difficulty(X)
  This answers "what should the operative gather *next*, considering cost?"

Simplification used here:
  We don't have a full observation model O(x|world_state).
  Instead we use the IntelligenceTarget.mission_relevance as a proxy for
  how much of the belief state's entropy is attributable to this target.
  VoI(X) ≈ H(b) × mission_relevance(X)  (proportional partition of entropy)

TODO: replace with proper POMDP observation model once strategy_node
  PBVI is implemented. The POMDP model has Z(o|s',a) which can be used
  to compute exact VoI as the mutual information between observations and states.
"""
from __future__ import annotations

import math

from dhurandhar_oracle.schemas import IntelligenceTarget, VoIEntry, VoIResult


def _shannon_entropy(belief: dict[str, float]) -> float:
    """Compute H(b) in bits."""
    h = 0.0
    for p in belief.values():
        if p > 0:
            h -= p * math.log2(p)
    return h


def compute_voi_ranking(
    targets: list[IntelligenceTarget],
    belief_state: dict[str, float],
) -> VoIResult:
    """
    Rank intelligence targets by (effort-adjusted) Value of Information.

    Args:
        targets:      List of IntelligenceTarget objects from the turning point
        belief_state: Current POMDP belief distribution {state_id: probability}

    Returns:
        VoIResult with ranked entries, top_target, and total entropy.
    """
    # TODO: replace approximate VoI with exact mutual information
    #   once POMDP Z matrix is available:
    #   VoI(X) = Σ_o P(o|b) · H(b) - Σ_o P(o|b) · H(b|o)
    #          = I(b ; X)

    total_entropy = _shannon_entropy(belief_state)

    entries: list[tuple[float, VoIEntry]] = []

    for target in targets:
        # Approximate VoI: fraction of total entropy this target explains
        voi_bits = total_entropy * target.mission_relevance

        # Effort-adjusted score (not used for rank directly but exposed)
        effort_adj = voi_bits / max(target.access_difficulty, 0.1)

        recommendation = _make_recommendation(target, voi_bits, effort_adj)

        entries.append((effort_adj, VoIEntry(
            intelligence_target=target.name,
            voi_bits=round(voi_bits, 4),
            priority_rank=0,   # set below
            effort_required=target.access_difficulty,
            recommendation=recommendation,
        )))

    # Rank by effort-adjusted VoI descending
    entries.sort(key=lambda x: -x[0])
    ranked = []
    for rank, (_, entry) in enumerate(entries, start=1):
        ranked.append(VoIEntry(
            intelligence_target=entry.intelligence_target,
            voi_bits=entry.voi_bits,
            priority_rank=rank,
            effort_required=entry.effort_required,
            recommendation=entry.recommendation,
        ))

    top = ranked[0].intelligence_target if ranked else ""

    return VoIResult(
        rankings=ranked,
        top_target=top,
        total_entropy_bits=round(total_entropy, 4),
    )


def _make_recommendation(
    target: IntelligenceTarget,
    voi_bits: float,
    effort_adj: float,
) -> str:
    if effort_adj >= 1.5:
        return f"High priority — gather immediately via: {', '.join(target.access_actions[:2])}"
    if effort_adj >= 0.5:
        return f"Medium priority — schedule after cover deepening"
    return f"Low priority — defer; access difficulty ({target.access_difficulty:.1f}) outweighs VoI ({voi_bits:.2f} bits)"
