"""
arc_rewrite_node — runs the chained per-turning-point counterfactual
analysis via optimisation.arc_chain.rewrite_arc.

Inputs:
  state.operative          — Indian-side operative ID
  state.forced_tp_action   — optional {"turning_point_id": .., "action_id": ..}

Outputs:
  state.arc_rewrite        — ArcRewrite
"""
from __future__ import annotations

from dhurandhar_oracle.io.loader import load_character
from dhurandhar_oracle.optimisation.arc_chain import rewrite_arc
from dhurandhar_oracle.state import DhurandharState


def arc_rewrite_node(state: DhurandharState) -> dict:
    operative_id = state.get("operative")
    if not operative_id:
        return {"errors": ["arc_rewrite_node: operative not provided"]}

    try:
        char = load_character(operative_id)
    except FileNotFoundError as exc:
        return {"errors": [f"character not found: {exc}"]}

    if char.side != "indian":
        return {"errors": [
            f"arc_rewrite_node: operative '{operative_id}' is side='{char.side}'. "
            "Only Indian-side operatives can be queried."
        ]}

    forced = state.get("forced_tp_action")
    rewrite = rewrite_arc(operative_id, forced_tp_action=forced)
    return {"arc_rewrite": rewrite}
