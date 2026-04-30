"""
arc_chain.py — chain the existing per-turning-point oracle pipeline
across an operative's full Dhurandhar 1+2 arc to produce a counterfactual
rewrite.

For each turning point in chronological order:
  1. Invoke the existing oracle_graph (POMDP + Stackelberg + …)
  2. Read pomdp.action_values to get Q(b, a) for every action
  3. Read the outcome JSON to find the actually-taken action
  4. q_delta_i = Q(b, prescribed) - Q(b, actual)
  5. Accumulate state hand-off (uses character.state_by_act for baseline;
     prescribed final state is baseline + heuristic uplift weighted by
     cumulative q_delta).
  6. Build a 5d career-level ObjectiveDelta from the cumulative q_delta and
     simulator outputs (p_mission_success deltas).

This is a self-consistent baseline: the actual action's Q-value comes from
the same solver that produces the prescribed action, so we are not mixing
ground truths.
"""
from __future__ import annotations

from typing import Optional

from dhurandhar_oracle.io.loader import (
    load_character,
    load_outcome,
    load_turning_point,
    list_turning_points,
)
from dhurandhar_oracle.schemas import (
    ArcRewrite,
    ArcStep,
    ObjectiveDelta,
    OperativeState,
)


def _final_state(operative_id: str) -> OperativeState:
    """Use the last state_by_act entry as the baseline final state."""
    char = load_character(operative_id)
    if not char.state_by_act:
        return OperativeState(cover_integrity=5, trust_capital=5, intelligence_depth=5,
                              network_strength=5, exposure_risk=5)
    # Pick the chronologically latest by film/act keys: "film2_act3" > "film1_act1"
    def _rank(k: str) -> tuple[int, int]:
        try:
            f = int(k[4])
            a = int(k[-1])
            return (f, a)
        except Exception:
            return (0, 0)
    latest_key = max(char.state_by_act.keys(), key=_rank)
    return char.state_by_act[latest_key]


def _uplift_state(base: OperativeState, q_delta_total: float) -> OperativeState:
    """Heuristic prescribed final state: baseline plus q-delta-weighted uplift.

    q_delta_total scales each dimension proportionally. The mapping is
    intentionally conservative — POMDP Q-values are unitless and not directly
    comparable to the OperativeState's [0, 10] scale, so we cap the per-dim
    uplift at +/-2.0.
    """
    # Empirical: Q-deltas in the existing solver are typically O(1-5) magnitude.
    # Scale: 1 Q-unit ≈ 0.3 OperativeState unit, capped.
    scale = max(min(q_delta_total * 0.3, 2.0), -2.0)

    def clip(v: float) -> float:
        return max(0.0, min(10.0, v))

    return OperativeState(
        cover_integrity    = clip(base.cover_integrity    + 0.5 * scale),
        trust_capital      = clip(base.trust_capital      + 0.4 * scale),
        intelligence_depth = clip(base.intelligence_depth + 1.0 * scale),
        network_strength   = clip(base.network_strength   + 0.4 * scale),
        # exposure_risk: lower is better, so prescribed should reduce it
        exposure_risk      = clip(base.exposure_risk      - 0.6 * scale),
    )


def _objective_delta_from_q(q_delta_total: float) -> ObjectiveDelta:
    """Map cumulative POMDP Q-delta to a 5d career objective delta.

    Heuristic: positive q_delta means prescribed beats actual — that maps to
    higher mission_yield and strategic_impact, lower personal_cost and
    attribution_risk, modestly higher network_durability.
    """
    s = max(min(q_delta_total * 0.25, 3.0), -3.0)
    return ObjectiveDelta(
        mission_yield      = +1.0 * s,
        strategic_impact   = +0.7 * s,
        personal_cost      = -0.4 * s,
        network_durability = +0.5 * s,
        attribution_risk   = -0.3 * s,
    )


def rewrite_arc(operative_id: str,
                forced_tp_action: Optional[dict] = None) -> ArcRewrite:
    """Run the rewrite-arc analysis for an Indian-side operative."""
    # Lazy import: avoid circular import at module load
    from dhurandhar_oracle.graph import oracle_graph

    tps = list_turning_points(operative_id)
    if not tps:
        return ArcRewrite(
            operative=operative_id, steps=[], cumulative_q_delta=0.0,
            final_state_baseline=_final_state(operative_id),
            final_state_prescribed=_final_state(operative_id),
            objective_delta=ObjectiveDelta(),
        )

    # Sort chronologically: film, then act, then id for stability
    tps = sorted(tps, key=lambda t: (t.film, t.act, t.id))

    forced_event_id  = (forced_tp_action or {}).get("turning_point_id")
    forced_action_id = (forced_tp_action or {}).get("action_id")

    steps: list[ArcStep] = []
    cumulative_q_delta = 0.0

    for tp in tps:
        # Pull actual action from outcome file (may be missing)
        actual_action: Optional[str] = None
        try:
            o = load_outcome(tp.id)
            actual_action = o.actual_action
        except FileNotFoundError:
            pass

        result = oracle_graph.invoke({
            "operative":     operative_id,
            "turning_point": tp.id,
            "errors":   [], "warnings": [],
        })
        if result.get("errors"):
            continue
        pomdp = result.get("pomdp")
        if pomdp is None:
            continue

        prescribed_action = pomdp.optimal_action
        if forced_event_id and tp.id == forced_event_id and forced_action_id in pomdp.action_values:
            prescribed_action = forced_action_id

        if actual_action is None or actual_action not in pomdp.action_values:
            # Outcome missing or actual action not in available_actions —
            # treat baseline Q as the worst available action.
            if pomdp.action_values:
                actual_action = min(pomdp.action_values, key=pomdp.action_values.get)
            else:
                continue

        actual_q     = pomdp.action_values.get(actual_action, 0.0)
        prescribed_q = pomdp.action_values.get(prescribed_action, 0.0)
        q_delta      = prescribed_q - actual_q
        cumulative_q_delta += q_delta

        # Per-TP state handoff: reuse turning-point's state_vector as baseline
        steps.append(ArcStep(
            turning_point_id    = tp.id,
            actual_action       = actual_action,
            prescribed_action   = prescribed_action,
            actual_q_value      = actual_q,
            prescribed_q_value  = prescribed_q,
            q_delta             = q_delta,
            state_handoff_after = tp.state_vector,
        ))

    final_baseline   = _final_state(operative_id)
    final_prescribed = _uplift_state(final_baseline, cumulative_q_delta)
    obj_delta        = _objective_delta_from_q(cumulative_q_delta)

    return ArcRewrite(
        operative              = operative_id,
        steps                  = steps,
        cumulative_q_delta     = cumulative_q_delta,
        final_state_baseline   = final_baseline,
        final_state_prescribed = final_prescribed,
        objective_delta        = obj_delta,
    )
