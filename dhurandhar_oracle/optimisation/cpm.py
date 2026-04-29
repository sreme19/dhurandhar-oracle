"""
cpm.py — Critical Path Method + PERT three-point estimation.

NEW to this project series.

CPM algorithm:
  1. Build a task DAG (directed acyclic graph) from MissionTask.dependencies
  2. Forward pass: compute Earliest Start (ES) and Earliest Finish (EF)
       ES(start_node) = 0
       ES(n) = max(EF(predecessor) for predecessor in predecessors(n))
       EF(n) = ES(n) + duration(n)
  3. Backward pass: compute Latest Start (LS) and Latest Finish (LF)
       LF(end_node) = EF(end_node)
       LF(n) = min(LS(successor) for successor in successors(n))
       LS(n) = LF(n) - duration(n)
  4. Slack(n) = LS(n) - ES(n)
  5. Critical path = nodes where Slack = 0, in topological order

PERT three-point estimate:
  E(duration) = (O + 4M + P) / 6  where O=optimistic, M=most_likely, P=pessimistic
  σ²(duration) = ((P - O) / 6)²

Total project σ² = sum of σ² over critical path tasks.
95% confidence interval for total duration: E ± 1.96 × sqrt(Σ σ²)
"""
from __future__ import annotations

import networkx as nx

from dhurandhar_oracle.schemas import MissionTask


def build_task_graph(tasks: list[MissionTask]) -> nx.DiGraph:
    """Build a directed task graph from MissionTask dependency lists."""
    G = nx.DiGraph()
    task_map = {t.id: t for t in tasks}

    for t in tasks:
        G.add_node(t.id, task=t, duration=t.pert_expected)

    for t in tasks:
        for dep_id in t.dependencies:
            if dep_id in task_map:
                G.add_edge(dep_id, t.id)
            # else: unknown dependency — warn at caller

    return G


def forward_pass(
    G: nx.DiGraph,
    tasks: list[MissionTask],
) -> tuple[dict[str, float], dict[str, float]]:
    """
    Compute Earliest Start (ES) and Earliest Finish (EF) for each task.
    Returns: (es_map, ef_map) keyed by task.id
    """
    # TODO: implement forward pass
    #   Walk in topological order
    #   ES(n) = max(EF(pred)) for each predecessor, 0 if no predecessors
    #   EF(n) = ES(n) + pert_expected
    es: dict[str, float] = {}
    ef: dict[str, float] = {}

    for node in nx.topological_sort(G):
        task: MissionTask = G.nodes[node]["task"]
        if not list(G.predecessors(node)):
            es[node] = 0.0
        else:
            es[node] = max(ef[pred] for pred in G.predecessors(node))
        ef[node] = es[node] + task.pert_expected

    return es, ef


def backward_pass(
    G: nx.DiGraph,
    tasks: list[MissionTask],
    max_ef: float,
) -> tuple[dict[str, float], dict[str, float]]:
    """
    Compute Latest Start (LS) and Latest Finish (LF) for each task.
    Returns: (ls_map, lf_map) keyed by task.id
    """
    # TODO: implement backward pass
    ls: dict[str, float] = {}
    lf: dict[str, float] = {}

    for node in reversed(list(nx.topological_sort(G))):
        task: MissionTask = G.nodes[node]["task"]
        if not list(G.successors(node)):
            lf[node] = max_ef
        else:
            lf[node] = min(ls[succ] for succ in G.successors(node))
        ls[node] = lf[node] - task.pert_expected

    return ls, lf


def compute_critical_path(G: nx.DiGraph, critical_ids: list[str]) -> list[str]:
    """Return critical path task IDs in topological order."""
    critical_set = set(critical_ids)
    return [n for n in nx.topological_sort(G) if n in critical_set]


def find_parallelisation_opportunities(
    G: nx.DiGraph,
    tasks: list[MissionTask],
) -> list[tuple[str, str]]:
    """
    Find pairs of tasks with no dependency between them (directly or transitively)
    that also appear in each other's parallelizable_with list.
    These are safe to run in parallel — the operative or handler can assign
    different assets to them simultaneously.
    """
    # TODO: implement full transitive closure check
    #   For now: use explicit parallelizable_with annotations
    opportunities: list[tuple[str, str]] = []
    seen: set[frozenset] = set()

    tc = nx.transitive_closure(G)

    for t in tasks:
        for other_id in t.parallelizable_with:
            key = frozenset({t.id, other_id})
            if key not in seen:
                # Verify no dependency exists in either direction
                if not tc.has_edge(t.id, other_id) and not tc.has_edge(other_id, t.id):
                    opportunities.append((t.id, other_id))
                seen.add(key)

    return opportunities
