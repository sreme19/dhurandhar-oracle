"""
graph.py — LangGraph StateGraph definition.

Topology:
                         ┌──► intel_network_node ──┐
START ─► state_node ─────┤                          ├──► belief_node
                         └──► coalition_node ───────┘
                                                          │
                                                          ▼
                                                       voi_node
                                                          │
                                                          ▼
                                                    adversary_node (Stackelberg)
                                                          │
                                                          ▼
                                                    strategy_node (POMDP)
                                                          │
                                                          ▼
                                                    critical_path_node (CPM)
                                                          │
                                                          ▼
                                                    simulator_node (Monte Carlo)
                                                          │
                                            ┌─────────────┘
                                            ▼
                                     route_after_simulator
                                      ├── "narrator" ──► narrator_node ──► END
                                      └── "end"       ──────────────────► END

Fan-out: state_node → [intel_network_node, coalition_node]  (parallel)
Fan-in:  both write to DhurandharState → belief_node reads both outputs

LangGraph handles the parallel fan-out via two edges from state_node.
The shared `errors` and `warnings` keys use Annotated[list, operator.add]
reducers so concurrent writes are safely merged.
"""
from __future__ import annotations

from langgraph.graph import StateGraph, END

from dhurandhar_oracle.state import DhurandharState, route_after_simulator
from dhurandhar_oracle.agents.state_node          import state_node
from dhurandhar_oracle.agents.intel_network_node  import intel_network_node
from dhurandhar_oracle.agents.coalition_node      import coalition_node
from dhurandhar_oracle.agents.belief_node         import belief_node
from dhurandhar_oracle.agents.voi_node            import voi_node
from dhurandhar_oracle.agents.adversary_node      import adversary_node
from dhurandhar_oracle.agents.strategy_node       import strategy_node
from dhurandhar_oracle.agents.critical_path_node  import critical_path_node
from dhurandhar_oracle.agents.simulator_node      import simulator_node
from dhurandhar_oracle.agents.narrator_node       import narrator_node


def build_graph() -> StateGraph:
    """Construct and compile the LangGraph pipeline."""
    graph = StateGraph(DhurandharState)

    # ── Node registration ─────────────────────────────────────────────────────
    graph.add_node("state",         state_node)
    graph.add_node("intel_network", intel_network_node)
    graph.add_node("coalition",     coalition_node)
    graph.add_node("belief",        belief_node)
    graph.add_node("voi",           voi_node)
    graph.add_node("adversary",     adversary_node)
    graph.add_node("strategy",      strategy_node)
    graph.add_node("critical_path", critical_path_node)
    graph.add_node("simulator",     simulator_node)
    graph.add_node("narrator",      narrator_node)

    # ── Entry point ───────────────────────────────────────────────────────────
    graph.set_entry_point("state")

    # ── Parallel fan-out from state → intel_network + coalition ──────────────
    graph.add_edge("state",         "intel_network")
    graph.add_edge("state",         "coalition")

    # ── Fan-in to belief ──────────────────────────────────────────────────────
    graph.add_edge("intel_network", "belief")
    graph.add_edge("coalition",     "belief")

    # ── Linear pipeline: belief → voi → adversary → strategy → cpm → sim ─────
    graph.add_edge("belief",        "voi")
    graph.add_edge("voi",           "adversary")
    graph.add_edge("adversary",     "strategy")
    graph.add_edge("strategy",      "critical_path")
    graph.add_edge("critical_path", "simulator")

    # ── Conditional edge: simulator → narrator | end ──────────────────────────
    graph.add_conditional_edges(
        "simulator",
        route_after_simulator,
        {"narrator": "narrator", "end": END},
    )
    graph.add_edge("narrator", END)

    return graph.compile()


# Singleton — imported by cli.py
oracle_graph = build_graph()
