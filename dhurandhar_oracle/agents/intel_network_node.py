"""
intel_network_node — Build Karachi criminal-political power network.

Runs IN PARALLEL with coalition_node (LangGraph fan-out from state_node).

Responsibilities:
  1. Build a directed NetworkX graph from alliance_snapshot edges
  2. Compute betweenness centrality, eigenvector centrality, clustering
  3. Detect communities (Louvain / greedy modularity)
  4. Score each adversary: threat_score = 0.5*capability + 0.3*betweenness + 0.2*eigenvector
  5. Mark actors above threshold as high_threat_actors

Input  keys: adversaries, alliance_snapshot
Output keys: intel_graph_data, centrality, threat_scores, high_threat_actors, errors, warnings

New vs got-oracle: same SNA algorithm, but edges now carry
  `trust_level` (instead of `strength`) and nodes carry
  `is_indian` flag for separating the two sides of the network.
"""
from __future__ import annotations

from dhurandhar_oracle.optimisation.network import (
    build_intel_graph,
    compute_centrality,
    compute_threat_scores,
)
from dhurandhar_oracle.state import DhurandharState

_HIGH_THREAT_THRESHOLD = 6.0


def intel_network_node(state: DhurandharState) -> dict:
    """Build power network and compute threat scores."""
    errors:   list[str] = []
    warnings: list[str] = []

    adversaries      = state.get("adversaries", [])
    alliance_snapshot = state.get("alliance_snapshot", [])

    if not adversaries:
        warnings.append("intel_network_node: no adversaries — skipping SNA")
        return {"errors": errors, "warnings": warnings}

    # ── Build graph ───────────────────────────────────────────────────────────
    G = build_intel_graph(adversaries, alliance_snapshot)
    centrality = compute_centrality(G)
    threat_scores = compute_threat_scores(adversaries, centrality)

    high_threat = [ts.actor for ts in threat_scores if ts.score >= _HIGH_THREAT_THRESHOLD]

    # Serialise for state (NetworkX graph is not JSON-serialisable)
    graph_data = {
        "nodes": list(G.nodes(data=True)),
        "edges": list(G.edges(data=True)),
    }

    return {
        "intel_graph_data":  graph_data,
        "centrality":        centrality,
        "threat_scores":     threat_scores,
        "high_threat_actors": high_threat,
        "errors":            errors,
        "warnings":          warnings,
    }
