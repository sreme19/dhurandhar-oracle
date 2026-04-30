"""
forward_graph.py — LangGraph for project-forward (Mode 2).

Topology:
  START → forward_state_node → realworld_context_node → forward_projection_node
        → narrator_node → END

The narrator_node is reused from the turning-point pipeline; it auto-detects
which mode it's in by checking which result keys are populated in state.
"""
from __future__ import annotations

from langgraph.graph import END, StateGraph

from dhurandhar_oracle.agents.forward_projection_node import forward_projection_node
from dhurandhar_oracle.agents.forward_state_node import forward_state_node
from dhurandhar_oracle.agents.narrator_node import narrator_node
from dhurandhar_oracle.agents.realworld_context_node import realworld_context_node
from dhurandhar_oracle.state import DhurandharState


def _route_after_projection(state: DhurandharState) -> str:
    if state.get("errors"):
        return "end"
    return "narrator"


def build_forward_graph() -> StateGraph:
    graph = StateGraph(DhurandharState)
    graph.add_node("forward_state",      forward_state_node)
    graph.add_node("realworld_context",  realworld_context_node)
    graph.add_node("forward_projection", forward_projection_node)
    graph.add_node("narrator",           narrator_node)

    graph.set_entry_point("forward_state")
    graph.add_edge("forward_state",      "realworld_context")
    graph.add_edge("realworld_context",  "forward_projection")
    graph.add_conditional_edges(
        "forward_projection",
        _route_after_projection,
        {"narrator": "narrator", "end": END},
    )
    graph.add_edge("narrator", END)
    return graph.compile()


forward_graph = build_forward_graph()
