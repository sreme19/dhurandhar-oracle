"""End-to-end smoke test of the rewrite-arc pipeline on Hamza."""
from __future__ import annotations

import pytest


@pytest.mark.slow
def test_rewrite_graph_runs_for_hamza():
    """Full rewrite of Hamza's arc — runs the per-TP POMDP loop. ~minute-scale."""
    from dhurandhar_oracle.rewrite_graph import rewrite_graph

    result = rewrite_graph.invoke({
        "operative":  "hamza",
        "mode":       "rewrite",
        "errors":   [],
        "warnings": [],
    })
    assert not result.get("errors"), result.get("errors")
    ar = result.get("arc_rewrite")
    assert ar is not None
    assert ar.operative == "hamza"
    assert len(ar.steps) > 0
    # Cumulative Q-delta should be non-negative — prescribed >= actual at every TP.
    assert ar.cumulative_q_delta >= 0


def test_rewrite_rejects_pakistani_side():
    from dhurandhar_oracle.io.loader import list_characters
    from dhurandhar_oracle.rewrite_graph import rewrite_graph

    others = [c for c in list_characters() if c.side != "indian"]
    if not others:
        return
    result = rewrite_graph.invoke({
        "operative":  others[0].id,
        "mode":       "rewrite",
        "errors":   [],
        "warnings": [],
    })
    assert result.get("errors")
