"""
dhurandhar-oracle — LangGraph DhurandharState and routing helpers.

DhurandharState is the single shared TypedDict that all nodes read/write.
Each node returns only the keys it updates.

Routing functions are consumed by graph.py conditional edges.

`errors` and `warnings` use Annotated[list, operator.add] so that the
parallel fan-out branches (intel_network_node + coalition_node) can both
append to them without triggering LangGraph's concurrent-write guard.
"""
from __future__ import annotations

import operator
from typing import Annotated, Optional, TypedDict

from dhurandhar_oracle.schemas import (
    AdversaryModel,
    AllianceEdge,
    BeliefGap,
    CausalDAG,
    CentralityScores,
    CriticalPathResult,
    HMMResult,
    IntelligenceTarget,
    MissionTask,
    OperativeState,
    POOMDPResult,
    ShapleyResult,
    SimulationOutput,
    StackelbergResult,
    ThreatScore,
    VoIResult,
)


class DhurandharState(TypedDict, total=False):
    # ── Inputs ────────────────────────────────────────────────────────────────
    operative:       str            # e.g. "hamza"
    turning_point:   str            # e.g. "dakait-first-meeting"
    action_override: Optional[str]  # CLI --action flag; None means find optimal

    # ── state_node ────────────────────────────────────────────────────────────
    state_vector:              OperativeState
    available_actions:         list[str]
    causal_dag:                CausalDAG
    adversaries:               list[AdversaryModel]
    alliance_snapshot:         list[AllianceEdge]
    mission_tasks:             list[MissionTask]
    intelligence_targets:      list[IntelligenceTarget]
    initial_belief_state:      dict[str, float]   # world_state → prob (from JSON)
    turning_point_description: str               # TP description text → narrator context
    real_world_correlation:    Optional[dict]    # grounded event data → narrator context

    # ── intel_network_node (parallel with coalition_node) ─────────────────────
    intel_graph_data:    dict              # serialised NetworkX adjacency
    centrality:          CentralityScores
    threat_scores:       list[ThreatScore]
    high_threat_actors:  list[str]

    # ── coalition_node (parallel with intel_network_node) ─────────────────────
    shapley: ShapleyResult

    # ── belief_node ───────────────────────────────────────────────────────────
    hmm_results:  list[HMMResult]
    belief_gaps:  list[BeliefGap]

    # ── voi_node ──────────────────────────────────────────────────────────────
    voi_result: VoIResult

    # ── adversary_node (Stackelberg) ──────────────────────────────────────────
    stackelberg: StackelbergResult

    # ── strategy_node (POMDP) ────────────────────────────────────────────────
    pomdp: POOMDPResult

    # ── critical_path_node ────────────────────────────────────────────────────
    critical_path: CriticalPathResult

    # ── simulator_node ────────────────────────────────────────────────────────
    simulation_actual:  Optional[SimulationOutput]
    simulation_optimal: Optional[SimulationOutput]

    # ── narrator_node ─────────────────────────────────────────────────────────
    narrative: str

    # ── Pipeline bookkeeping — Annotated so parallel branches can both write ──
    errors:   Annotated[list[str], operator.add]
    warnings: Annotated[list[str], operator.add]


# ── Routing helpers ────────────────────────────────────────────────────────────

def route_after_belief(state: DhurandharState) -> str:
    """Always run VoI after belief gaps are computed."""
    return "voi"


def route_after_voi(state: DhurandharState) -> str:
    """Always run adversary (Stackelberg) after VoI."""
    return "adversary"


def route_strategy(state: DhurandharState) -> str:
    """Always POMDP — Stackelberg result feeds belief-state update."""
    return "strategy_pomdp"


def route_after_simulator(state: DhurandharState) -> str:
    """Skip narrator on fatal errors or missing API key."""
    if state.get("errors"):
        return "end"
    return "narrator"
