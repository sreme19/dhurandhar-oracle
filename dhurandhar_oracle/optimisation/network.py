"""
network.py — Social Network Analysis for the Karachi criminal-political power network.

Adapted from got-oracle/got_oracle/optimisation/network.py.
Same SNA algorithm, new domain: nodes are criminal bosses, political patrons,
police officers, and intelligence assets instead of GoT houses.

Key difference: edges carry `trust_level` (0-1) and an `is_indian` flag.
The power graph spans *both* sides — the operative maps the full network
to identify brokers (high betweenness = key intermediaries to flip).

Public API:
  build_intel_graph(adversaries, alliance_snapshot)  → nx.DiGraph
  compute_centrality(G)                              → CentralityScores
  compute_threat_scores(adversaries, centrality)     → list[ThreatScore]
"""
from __future__ import annotations

import networkx as nx

from dhurandhar_oracle.schemas import (
    AdversaryModel, AllianceEdge, CentralityScores, ThreatScore,
)

_THREAT_CAPABILITY_W  = 0.50
_THREAT_BETWEENNESS_W = 0.30
_THREAT_EIGENVECTOR_W = 0.20


def build_intel_graph(
    adversaries: list[AdversaryModel],
    alliance_snapshot: list[AllianceEdge],
) -> nx.DiGraph:
    """
    Build directed power graph from alliance_snapshot.
    Nodes: all actors in edges + all adversaries
    Edge attributes: strength, betrayal_history, in_coalition
    """
    G = nx.DiGraph()

    # Add adversary nodes
    adversary_ids = {a.actor for a in adversaries}
    for adv in adversaries:
        G.add_node(adv.actor, capability=adv.capability, is_adversary=True)

    # Add alliance edges
    for edge in alliance_snapshot:
        G.add_node(edge.source, **{"is_adversary": edge.source in adversary_ids})
        G.add_node(edge.target, **{"is_adversary": edge.target in adversary_ids})
        G.add_edge(
            edge.source, edge.target,
            weight=edge.strength,
            betrayal_history=edge.betrayal_history,
            in_coalition=edge.in_coalition,
        )

    return G


def compute_centrality(G: nx.DiGraph) -> CentralityScores:
    """Compute betweenness, eigenvector centrality, and community detection."""
    if G.number_of_nodes() == 0:
        return CentralityScores(betweenness={}, eigenvector={}, clustering={}, communities=[])

    # Betweenness centrality (uses edge weights)
    betweenness = nx.betweenness_centrality(G, weight="weight", normalized=True)

    # Eigenvector centrality (requires undirected or connected graph)
    try:
        G_undirected = G.to_undirected()
        eigenvector  = nx.eigenvector_centrality_numpy(G_undirected, weight="weight")
    except Exception:
        eigenvector = {n: 0.0 for n in G.nodes()}

    # Clustering coefficient
    clustering = nx.clustering(G.to_undirected(), weight="weight")

    # Community detection (greedy modularity on undirected graph)
    try:
        from networkx.algorithms.community import greedy_modularity_communities
        communities_raw = greedy_modularity_communities(G.to_undirected(), weight="weight")
        communities = [sorted(c) for c in communities_raw]
    except Exception:
        communities = [sorted(G.nodes())]

    return CentralityScores(
        betweenness=betweenness,
        eigenvector=eigenvector,
        clustering=clustering,
        communities=communities,
    )


def compute_threat_scores(
    adversaries: list[AdversaryModel],
    centrality: CentralityScores,
) -> list[ThreatScore]:
    """
    Score each adversary as a threat:
      score = 0.5 × capability + 0.3 × betweenness + 0.2 × eigenvector
    (scaled to 0–10)
    """
    scores: list[ThreatScore] = []

    for adv in adversaries:
        b = centrality.betweenness.get(adv.actor, 0.0)
        e = centrality.eigenvector.get(adv.actor, 0.0)
        raw_score = (
            _THREAT_CAPABILITY_W  * adv.capability
            + _THREAT_BETWEENNESS_W * b * 10   # betweenness 0–1 → 0–10
            + _THREAT_EIGENVECTOR_W * e * 10
        )
        scores.append(ThreatScore(
            actor=adv.actor,
            score=round(raw_score, 3),
            betweenness=round(b, 4),
            eigenvector=round(e, 4),
            is_high=raw_score >= 6.0,
        ))

    scores.sort(key=lambda ts: -ts.score)
    return scores
