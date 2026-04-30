"""End-to-end smoke test of the forward-projection pipeline on Hamza."""
from __future__ import annotations


def test_forward_graph_runs_for_hamza():
    from dhurandhar_oracle.forward_graph import forward_graph

    result = forward_graph.invoke({
        "operative":      "hamza",
        "mode":           "forward",
        "horizon_until":  "2026-04-30",
        "errors":   [],
        "warnings": [],
    })
    assert not result.get("errors"), result.get("errors")
    fp = result.get("forward_projection")
    assert fp is not None
    assert fp.operative == "hamza"
    assert len(fp.predicted.steps) == len(fp.prescribed.steps)
    assert fp.scalar_score_delta >= 0


def test_forward_rejects_pakistani_side(tmp_path, monkeypatch):
    """Sanity: the side-gating still applies in forward mode."""
    from dhurandhar_oracle.forward_graph import forward_graph

    # No Pakistani character in the data is queryable; pick an "unknown"-side
    # ID that exists.
    from dhurandhar_oracle.io.loader import list_characters
    others = [c for c in list_characters() if c.side != "indian"]
    if not others:
        return  # nothing to test
    bad_id = others[0].id
    result = forward_graph.invoke({
        "operative":      bad_id,
        "mode":           "forward",
        "horizon_until":  "2026-04-30",
        "errors":   [],
        "warnings": [],
    })
    assert result.get("errors"), "expected forward_state_node to reject non-Indian operative"


def test_forward_horizon_prunes_events():
    from dhurandhar_oracle.forward_graph import forward_graph

    early = forward_graph.invoke({
        "operative":      "hamza",
        "mode":           "forward",
        "horizon_until":  "2026-01-31",
        "errors":   [],
        "warnings": [],
    })
    full = forward_graph.invoke({
        "operative":      "hamza",
        "mode":           "forward",
        "horizon_until":  "2026-04-30",
        "errors":   [],
        "warnings": [],
    })
    assert len(early["forward_projection"].prescribed.steps) < len(full["forward_projection"].prescribed.steps)
