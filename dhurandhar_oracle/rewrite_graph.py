"""
rewrite_graph.py — LangGraph for rewrite-arc (Mode 3).

Topology:
  START → arc_rewrite_node → narrator_node → END

The arc_rewrite_node internally invokes the existing oracle_graph once
per turning point, so this graph is intentionally thin.
"""
from __future__ import annotations

from langgraph.graph import END, StateGraph

from dhurandhar_oracle.agents.arc_rewrite_node import arc_rewrite_node
from dhurandhar_oracle.agents.narrator_node import narrator_node
from dhurandhar_oracle.state import DhurandharState


def _route(state: DhurandharState) -> str:
    return "end" if state.get("errors") else "narrator"


def build_rewrite_graph() -> StateGraph:
    graph = StateGraph(DhurandharState)
    graph.add_node("arc_rewrite", arc_rewrite_node)
    graph.add_node("narrator",    narrator_node)

    graph.set_entry_point("arc_rewrite")
    graph.add_conditional_edges("arc_rewrite", _route,
                                {"narrator": "narrator", "end": END})
    graph.add_edge("narrator", END)
    return graph.compile()


rewrite_graph = build_rewrite_graph()
