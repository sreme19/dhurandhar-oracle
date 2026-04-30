"""
forward_projection_node — runs the career_mdp solver on the loaded macro
arc and produces a ForwardProjection (predicted vs prescribed trajectories).

Inputs:
  state.macro_arc            — MacroArc (loaded by state_node_forward)
  state.horizon_until        — ISO date; events past this date are pruned
  state.forced_event_action  — optional override for one event

Output:
  state.forward_projection   — ForwardProjection
"""
from __future__ import annotations

from dhurandhar_oracle.io.loader import load_character
from dhurandhar_oracle.optimisation.career_mdp import (
    _apply_delta,
    _make_policy_predicted,
    _make_policy_prescribed,
    _rollout,
    project,
    scalar_score,
    solve,
)
from dhurandhar_oracle.schemas import (
    CareerStep,
    CareerTrajectory,
    ForwardProjection,
    LongHorizonWeights,
    MacroArc,
    ObjectiveDelta,
)
from dhurandhar_oracle.state import DhurandharState


def forward_projection_node(state: DhurandharState) -> dict:
    arc: MacroArc = state.get("macro_arc")
    horizon_until = state.get("horizon_until")
    forced = state.get("forced_event_action")
    operative_id = state.get("operative")

    if arc is None:
        return {"errors": [f"forward_projection_node: macro_arc missing for {operative_id}"]}

    # Per-operative weights override default
    weights: LongHorizonWeights = LongHorizonWeights()
    try:
        char = load_character(operative_id)
        if char.long_horizon_objective_weights is not None:
            weights = char.long_horizon_objective_weights
    except FileNotFoundError:
        pass

    # Prune events past the horizon
    if horizon_until:
        pruned_events = [e for e in arc.events if e.date <= horizon_until]
        arc = arc.model_copy(update={"events": pruned_events})

    if not arc.events:
        return {"errors": ["forward_projection_node: no events within horizon"]}

    predicted, prescribed = project(arc, weights, n_rollouts=1500, seed=0)

    # Apply forced override on the prescribed trajectory if requested
    if forced:
        prescribed = _apply_forced_override(arc, weights, forced, seed=0)

    # Compute deltas
    score_delta = prescribed.scalar_score - predicted.scalar_score
    obj_delta = ObjectiveDelta(
        mission_yield      = prescribed.final_objective.mission_yield      - predicted.final_objective.mission_yield,
        strategic_impact   = prescribed.final_objective.strategic_impact   - predicted.final_objective.strategic_impact,
        personal_cost      = prescribed.final_objective.personal_cost      - predicted.final_objective.personal_cost,
        network_durability = prescribed.final_objective.network_durability - predicted.final_objective.network_durability,
        attribution_risk   = prescribed.final_objective.attribution_risk   - predicted.final_objective.attribution_risk,
    )

    # First event where prescribed action differs from predicted action
    key_div = None
    for p_step, q_step in zip(predicted.steps, prescribed.steps):
        if p_step.chosen_action != q_step.chosen_action:
            key_div = p_step.event_id
            break

    projection = ForwardProjection(
        operative                    = operative_id,
        arc_start                    = arc.arc_start,
        horizon_until                = horizon_until or arc.events[-1].date,
        is_speculative_real_figure   = arc.is_speculative_real_figure,
        predicted                    = predicted,
        prescribed                   = prescribed,
        scalar_score_delta           = score_delta,
        objective_delta              = obj_delta,
        key_divergence_event         = key_div,
    )
    return {"forward_projection": projection}


def _apply_forced_override(arc: MacroArc, weights: LongHorizonWeights,
                           forced: dict, seed: int) -> CareerTrajectory:
    """Re-roll the prescribed trajectory with a single event's action forced."""
    import random
    forced_event = forced.get("event_id")
    forced_action = forced.get("action_id")
    solved = solve(arc, weights)
    base_policy = _make_policy_prescribed(solved)

    def policy_with_override(idx, status, event):
        if event.id == forced_event:
            return forced_action
        return base_policy(idx, status, event)

    rng = random.Random(seed)
    steps, status, obj = _rollout(arc, policy_with_override, weights, rng)
    return CareerTrajectory(
        label           = "prescribed",
        steps           = steps,
        final_status    = status,
        final_objective = obj,
        scalar_score    = scalar_score(obj, weights),
        n_rollouts      = 1,
    )
