"""
forward_state_node — loads the macro-arc for an Indian-side operative.

Mirrors the pattern of state_node (turning-point loader) but for the
post-D2 forward mode. Enforces:
  - operative.side == "indian" (hard constraint)
  - macro-arc file exists for this operative
  - if operative is a real public figure, set the speculative flag
"""
from __future__ import annotations

from dhurandhar_oracle.io.loader import load_character, load_macro_arc
from dhurandhar_oracle.state import DhurandharState


def forward_state_node(state: DhurandharState) -> dict:
    operative_id = state.get("operative")
    if not operative_id:
        return {"errors": ["forward_state_node: operative not provided"]}

    try:
        char = load_character(operative_id)
    except FileNotFoundError as exc:
        return {"errors": [f"character not found: {exc}"]}

    if char.side != "indian":
        return {"errors": [
            f"forward_state_node: operative '{operative_id}' is side='{char.side}'. "
            "Only Indian-side operatives can be queried."
        ]}

    try:
        arc = load_macro_arc(operative_id)
    except FileNotFoundError:
        return {"errors": [
            f"forward_state_node: no post-D2 macro-arc authored for '{operative_id}'. "
            f"Add data/post_d2_arc/{operative_id}.json to enable project-forward."
        ]}

    if char.is_real_public_figure and not arc.is_speculative_real_figure:
        arc = arc.model_copy(update={"is_speculative_real_figure": True})

    return {"macro_arc": arc, "warnings": []}
