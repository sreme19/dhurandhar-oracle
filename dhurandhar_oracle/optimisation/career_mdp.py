"""
career_mdp.py — finite-horizon MDP solver for the post-D2 career arc.

State = (event_index, terminal_status). Action = a MacroAction.id legal at
the event AND the current status. Reward = scalar projection of the action's
ObjectiveDelta through the operative's LongHorizonWeights, with a fixed sign
convention that flips personal_cost and attribution_risk (lower is better).

The solver runs backward induction over events in chronological order. Each
non-terminal status has a value V[i, status]; the policy at each (event,
status) is the action argmax of expected reward + discounted next-state value.

Two trajectories are produced from the same arc:
  - predicted:  greedy on a "default-conservative" prior (Hamza maintains
                cover etc.) — represents the canonical extrapolation.
  - prescribed: greedy on the optimal MDP policy — represents the oracle's
                recommendation.

Monte Carlo rollouts on the prescribed policy provide CI bands on the final
objective (used by the narrator for uncertainty calibration).
"""
from __future__ import annotations

import random
from dataclasses import dataclass
from typing import Optional

from dhurandhar_oracle.schemas import (
    CareerStep,
    CareerTerminalStatus,
    CareerTrajectory,
    LongHorizonObjective,
    LongHorizonWeights,
    MacroAction,
    MacroArc,
    MacroEvent,
    ObjectiveDelta,
)

_TERMINAL_STATUSES: tuple[CareerTerminalStatus, ...] = ("killed", "blown", "extracted", "retired")
_DEFAULT_WEIGHTS = LongHorizonWeights()  # uses class defaults; sums to 1.0


def scalar_score(obj: LongHorizonObjective, weights: LongHorizonWeights) -> float:
    """
    Collapse a 5d objective into a scalar.
    Sign convention: mission_yield, strategic_impact, network_durability are
    rewarded; personal_cost and attribution_risk are penalised.
    """
    return (
        weights.mission_yield      * obj.mission_yield
        + weights.strategic_impact * obj.strategic_impact
        - weights.personal_cost    * obj.personal_cost
        + weights.network_durability * obj.network_durability
        - weights.attribution_risk * obj.attribution_risk
    )


def _clip(v: float) -> float:
    return max(0.0, min(10.0, v))


def _apply_delta(obj: LongHorizonObjective, delta: ObjectiveDelta) -> LongHorizonObjective:
    return LongHorizonObjective(
        mission_yield      = _clip(obj.mission_yield      + delta.mission_yield),
        strategic_impact   = _clip(obj.strategic_impact   + delta.strategic_impact),
        personal_cost      = _clip(obj.personal_cost      + delta.personal_cost),
        network_durability = _clip(obj.network_durability + delta.network_durability),
        attribution_risk   = _clip(obj.attribution_risk   + delta.attribution_risk),
    )


def _scalar_delta(delta: ObjectiveDelta, weights: LongHorizonWeights) -> float:
    """Scalar contribution of a single-step delta under sign convention."""
    return (
        weights.mission_yield      * delta.mission_yield
        + weights.strategic_impact * delta.strategic_impact
        - weights.personal_cost    * delta.personal_cost
        + weights.network_durability * delta.network_durability
        - weights.attribution_risk * delta.attribution_risk
    )


@dataclass(frozen=True)
class _Solved:
    """Internal solver output: optimal value table + policy."""
    # value[(event_idx, status)] -> expected scalar return-to-go
    value:  dict
    # policy[(event_idx, status)] -> action_id (only for "active" generally)
    policy: dict


def _legal_actions(event: MacroEvent, status: CareerTerminalStatus,
                   actions_by_id: dict[str, MacroAction]) -> list[MacroAction]:
    out: list[MacroAction] = []
    for aid in event.available_actions:
        a = actions_by_id.get(aid)
        if a is None:
            continue
        if status in a.requires_status:
            out.append(a)
    return out


def _expected_next_value(action: MacroAction, next_idx: int,
                         value: dict, n_events: int) -> float:
    """Σ p(s' | a) · V(next_idx, s'). Terminal status absorbs (no further reward)."""
    if next_idx >= n_events:
        return 0.0
    total = 0.0
    for s_next, p in action.transition_probs.items():
        total += p * value.get((next_idx, s_next), 0.0)
    return total


def solve(arc: MacroArc, weights: Optional[LongHorizonWeights] = None) -> _Solved:
    """Backward-induction value iteration over the finite event horizon."""
    w = weights or _DEFAULT_WEIGHTS
    actions_by_id = {a.id: a for a in arc.actions}
    events_sorted = sorted(arc.events, key=lambda e: e.date)
    n = len(events_sorted)

    value:  dict = {}
    policy: dict = {}

    # Terminal absorbing values: 0 (we measure only future reward)
    for idx in range(n + 1):
        for st in _TERMINAL_STATUSES:
            value[(idx, st)] = 0.0

    # Backward pass over event indices n-1 .. 0
    for idx in reversed(range(n)):
        event = events_sorted[idx]
        # Active status: choose best action
        actions = _legal_actions(event, "active", actions_by_id)
        if not actions:
            value[(idx, "active")] = 0.0
            policy[(idx, "active")] = None
            continue
        best_a, best_q = None, float("-inf")
        for a in actions:
            r = _scalar_delta(a.objective_delta, w)
            v_next = _expected_next_value(a, idx + 1, value, n)
            q = r + v_next
            if q > best_q:
                best_q, best_a = q, a.id
        value[(idx, "active")]  = best_q
        policy[(idx, "active")] = best_a

        # Terminal statuses keep absorbing-value 0; doctrine_consolidation
        # etc. is permitted only if the event explicitly lists it (rare).
        for st in _TERMINAL_STATUSES:
            ts_actions = _legal_actions(event, st, actions_by_id)
            if not ts_actions:
                value[(idx, st)]  = value.get((idx, st), 0.0)
                policy[(idx, st)] = None
                continue
            best_a, best_q = None, float("-inf")
            for a in ts_actions:
                r = _scalar_delta(a.objective_delta, w)
                v_next = _expected_next_value(a, idx + 1, value, n)
                q = r + v_next
                if q > best_q:
                    best_q, best_a = q, a.id
            value[(idx, st)]  = best_q
            policy[(idx, st)] = best_a

    return _Solved(value=value, policy=policy)


def _sample_status(action: MacroAction, rng: random.Random) -> CareerTerminalStatus:
    """Sample resulting status from action.transition_probs."""
    r = rng.random()
    cum = 0.0
    for st, p in action.transition_probs.items():
        cum += p
        if r <= cum:
            return st
    # numerical fallback
    return "active"


def _rollout(arc: MacroArc, policy_fn, weights: LongHorizonWeights,
             rng: random.Random) -> tuple[list[CareerStep], CareerTerminalStatus, LongHorizonObjective]:
    """Simulate one trajectory under a policy fn (event_idx, status, event) -> action_id."""
    actions_by_id = {a.id: a for a in arc.actions}
    events_sorted = sorted(arc.events, key=lambda e: e.date)
    obj    = arc.initial_objective.model_copy()
    status: CareerTerminalStatus = arc.initial_status
    steps: list[CareerStep] = []

    for idx, event in enumerate(events_sorted):
        if status != "active":
            # Most absorbing statuses end the trajectory; doctrine_consolidation
            # etc. handles its own follow-on (still considered terminal here).
            break
        action_id = policy_fn(idx, status, event)
        if action_id is None:
            break
        action = actions_by_id[action_id]
        obj    = _apply_delta(obj, action.objective_delta)
        status = _sample_status(action, rng)
        steps.append(CareerStep(
            event_id        = event.id,
            event_date      = event.date,
            event_label     = event.label,
            chosen_action   = action.id,
            action_label    = action.label,
            status_after    = status,
            objective_after = obj,
        ))
    return steps, status, obj


def _make_policy_prescribed(solved: _Solved):
    def fn(idx, status, event):
        return solved.policy.get((idx, status))
    return fn


def _make_policy_predicted(arc: MacroArc):
    """
    Conservative default ('predicted' = canonical extrapolation):
      - prefer 'maintain_lyari_cover' if available,
      - else 'mentor_rizwan_in_field',
      - else first available action.
    Captures the assumption that, absent oracle guidance, the operative
    continues current posture.
    """
    actions_by_id = {a.id: a for a in arc.actions}
    preference = ["maintain_lyari_cover", "mentor_rizwan_in_field",
                  "doctrine_consolidation"]

    def fn(idx, status, event):
        legal = [aid for aid in event.available_actions
                 if aid in actions_by_id
                 and status in actions_by_id[aid].requires_status]
        if not legal:
            return None
        for p in preference:
            if p in legal:
                return p
        return legal[0]
    return fn


def _aggregate_objective_bands(rollouts: list[LongHorizonObjective]) -> tuple[
    LongHorizonObjective, LongHorizonObjective, LongHorizonObjective
]:
    """Mean, lower-quartile, upper-quartile over MC rollouts."""
    if not rollouts:
        zero = LongHorizonObjective(mission_yield=0, strategic_impact=0,
                                    personal_cost=0, network_durability=0,
                                    attribution_risk=0)
        return zero, zero, zero
    fields = ["mission_yield", "strategic_impact", "personal_cost",
              "network_durability", "attribution_risk"]
    n = len(rollouts)
    mean_kw, lo_kw, hi_kw = {}, {}, {}
    for f in fields:
        vals = sorted(getattr(r, f) for r in rollouts)
        mean_kw[f] = sum(vals) / n
        lo_kw[f]   = vals[int(0.05 * (n - 1))]
        hi_kw[f]   = vals[int(0.95 * (n - 1))]
    return (LongHorizonObjective(**mean_kw),
            LongHorizonObjective(**lo_kw),
            LongHorizonObjective(**hi_kw))


def project(arc: MacroArc, weights: Optional[LongHorizonWeights] = None,
            n_rollouts: int = 1500, seed: int = 0
            ) -> tuple[CareerTrajectory, CareerTrajectory]:
    """
    Solve the arc and return (predicted, prescribed) CareerTrajectory pair.
    Each trajectory's CareerSteps include MC CI bands per step.
    """
    w = weights or _DEFAULT_WEIGHTS
    solved = solve(arc, w)
    predicted_policy  = _make_policy_predicted(arc)
    prescribed_policy = _make_policy_prescribed(solved)

    actions_by_id = {a.id: a for a in arc.actions}

    def _trajectory(label, policy_fn) -> CareerTrajectory:
        rng = random.Random(seed)
        # 1) Deterministic mean trajectory: take expected status-after for each step
        #    (we actually run one fresh rng-seeded rollout for the spine, then
        #    augment per-step bands from MC).
        spine_rng = random.Random(seed)
        spine_steps, spine_status, spine_obj = _rollout(arc, policy_fn, w, spine_rng)
        # Cumulative scalar reward = Σ scalar_delta over each chosen action.
        # This is the MDP's reward function — independent of [0,10] clipping
        # on the rendered objective vector — so it is the meaningful headline.
        cumulative_reward = sum(
            _scalar_delta(actions_by_id[s.chosen_action].objective_delta, w)
            for s in spine_steps
        )

        # 2) MC rollouts for per-step CI on objective_after.
        per_step_rollouts: list[list[LongHorizonObjective]] = [[] for _ in spine_steps]
        final_objs: list[LongHorizonObjective] = []
        for k in range(n_rollouts):
            r = random.Random(seed * 1000003 + k)
            steps_k, _status_k, obj_k = _rollout(arc, policy_fn, w, r)
            final_objs.append(obj_k)
            for i, s in enumerate(steps_k):
                if i < len(per_step_rollouts):
                    per_step_rollouts[i].append(s.objective_after)

        # Attach CI bands to spine steps
        annotated: list[CareerStep] = []
        for i, s in enumerate(spine_steps):
            mean_o, lo, hi = _aggregate_objective_bands(per_step_rollouts[i])
            annotated.append(CareerStep(
                event_id        = s.event_id,
                event_date      = s.event_date,
                event_label     = s.event_label,
                chosen_action   = s.chosen_action,
                action_label    = s.action_label,
                status_after    = s.status_after,
                objective_after = mean_o,
                objective_lower = lo,
                objective_upper = hi,
            ))
        # Render: spine result is what an executed policy looks like.
        # Headline scalar score = cumulative per-step reward (MDP convention),
        # not a function of the [0,10]-clipped final objective.
        return CareerTrajectory(
            label           = label,
            steps           = annotated,
            final_status    = spine_status,
            final_objective = spine_obj,
            scalar_score    = cumulative_reward,
            n_rollouts      = n_rollouts,
        )

    predicted  = _trajectory("predicted",  predicted_policy)
    prescribed = _trajectory("prescribed", prescribed_policy)
    return predicted, prescribed
