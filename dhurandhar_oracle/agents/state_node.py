"""
state_node — Load turning point + validate Indian-side operative.

Responsibilities:
  1. Load the turning point JSON from data/turning_points/<id>.json
  2. Load the character profile from data/characters/<operative>.json
  3. GATE: raise ValueError if character.side != "indian"
  4. Populate DhurandharState with:
       state_vector, available_actions, causal_dag, adversaries,
       alliance_snapshot, mission_tasks, intelligence_targets, initial_belief_state

Input  keys: operative, turning_point
Output keys: state_vector, available_actions, causal_dag, adversaries,
             alliance_snapshot, mission_tasks, intelligence_targets,
             initial_belief_state, errors, warnings
"""
from __future__ import annotations

from dhurandhar_oracle.io.loader import load_character, load_turning_point
from dhurandhar_oracle.state import DhurandharState


def state_node(state: DhurandharState) -> dict:
    """Load state and enforce Indian-side gate."""
    operative    = state["operative"]
    turning_pt   = state["turning_point"]
    errors: list[str]   = []
    warnings: list[str] = []

    # ── Load character profile ────────────────────────────────────────────────
    try:
        char = load_character(operative)
    except FileNotFoundError:
        return {"errors": [f"Character not found: {operative}"]}

    # ── Indian-side gate ──────────────────────────────────────────────────────
    if char.side != "indian":
        return {
            "errors": [
                f"'{operative}' is side='{char.side}'. "
                "dhurandhar-oracle only runs for Indian-side characters."
            ]
        }

    # ── Load turning point ────────────────────────────────────────────────────
    try:
        tp = load_turning_point(turning_pt)
    except FileNotFoundError:
        return {"errors": [f"Turning point not found: {turning_pt}"]}

    if tp.operative != operative:
        warnings.append(
            f"Turning point '{turning_pt}' is authored for '{tp.operative}', "
            f"but queried as '{operative}'. Proceeding with caution."
        )

    # ── Merge char.state_by_act into tp.state_vector if a matching act key exists ──
    act_key = f"film{tp.film}_act{tp.act}"
    char_state = char.state_by_act.get(act_key)
    effective_state = char_state if char_state is not None else tp.state_vector
    if char_state is not None:
        warnings.append(
            f"state_node: using char.state_by_act['{act_key}'] over TP state_vector"
        )

    # ── Propagate terminal_belief from previous TP if this TP has no prior context ──
    initial_belief = tp.belief_state
    if not initial_belief:
        warnings.append("state_node: empty belief_state — using uniform prior over 3 states")
        initial_belief = {f"state_{i}": 1.0 / 3 for i in range(3)}

    return {
        "state_vector":              effective_state,
        "available_actions":         tp.available_actions,
        "causal_dag":                tp.causal_dag,
        "adversaries":               tp.adversaries,
        "alliance_snapshot":         tp.alliance_snapshot,
        "mission_tasks":             tp.mission_tasks,
        "intelligence_targets":      tp.intelligence_targets,
        "initial_belief_state":      initial_belief,
        "turning_point_description": tp.description,
        "real_world_correlation":    tp.real_world_correlation,
        "errors":                    errors,
        "warnings":                  warnings,
    }
