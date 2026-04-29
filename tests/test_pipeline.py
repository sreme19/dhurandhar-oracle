"""
Integration tests for the full LangGraph pipeline.

Tests run against the sample turning point (dakait-first-meeting) with
the hamza character. They do NOT require an ANTHROPIC_API_KEY — the
narrator falls back to the Rich template.

TODO (implement in P2 after grounding and data validation):
  - test_full_pipeline_hamza_dakait
  - test_indian_gate_rejects_dakait_as_operative
  - test_unknown_operative_returns_error
  - test_unknown_turning_point_returns_error
  - test_action_override_propagates
  - test_parallel_nodes_both_write
  - test_no_narrative_flag
"""
import pytest

from dhurandhar_oracle.graph import oracle_graph


# ── Gate tests ─────────────────────────────────────────────────────────────────

def test_indian_gate_rejects_pakistani_character(tmp_path, monkeypatch):
    """
    If a character JSON with side='pakistani' is queried,
    state_node should return an error and the pipeline should abort.
    """
    # Write a minimal Pakistani character JSON
    char_dir = tmp_path / "characters"
    char_dir.mkdir(parents=True)
    import json
    (char_dir / "rehman_dakait.json").write_text(json.dumps({
        "id": "rehman_dakait",
        "name": "Rehman Dakait",
        "nationality": "Pakistani",
        "side": "pakistani",
        "role": "Criminal boss",
        "films": [1],
        "state_by_act": {},
    }))

    # Monkeypatch DATA_DIR to point to tmp_path
    import dhurandhar_oracle.io.loader as loader
    monkeypatch.setattr(loader, "_DATA_DIR", tmp_path)

    result = oracle_graph.invoke({
        "operative": "rehman_dakait",
        "turning_point": "dakait-first-meeting",
        "errors": [], "warnings": [],
    })

    assert result.get("errors"), "Expected errors for Pakistani character"
    assert any("indian" in e.lower() or "side" in e.lower() for e in result["errors"])


def test_unknown_operative_returns_error():
    """Querying a non-existent operative should return an error."""
    result = oracle_graph.invoke({
        "operative": "does_not_exist",
        "turning_point": "dakait-first-meeting",
        "errors": [], "warnings": [],
    })
    assert result.get("errors")


def test_unknown_turning_point_returns_error():
    """Querying a non-existent turning point should return an error."""
    result = oracle_graph.invoke({
        "operative": "hamza",
        "turning_point": "does_not_exist",
        "errors": [], "warnings": [],
    })
    assert result.get("errors")


# ── Full pipeline tests (skip until P2) ───────────────────────────────────────

@pytest.mark.skip(reason="Full pipeline test — enable after POMDP PBVI is implemented (P2)")
def test_full_pipeline_hamza_dakait():
    """Full pipeline with sample data — all output keys should be populated."""
    result = oracle_graph.invoke({
        "operative": "hamza",
        "turning_point": "dakait-first-meeting",
        "errors": [], "warnings": [],
    })
    assert not result.get("errors"), f"Pipeline errors: {result.get('errors')}"
    assert result.get("pomdp")         is not None, "POMDP result missing"
    assert result.get("critical_path") is not None, "CPM result missing"
    assert result.get("voi_result")    is not None, "VoI result missing"
    assert result.get("stackelberg")   is not None, "Stackelberg result missing"
    assert result.get("shapley")       is not None, "Shapley result missing"
    assert result.get("narrative")     is not None, "Narrative missing"


@pytest.mark.skip(reason="Full pipeline test — enable after POMDP PBVI is implemented (P2)")
def test_action_override_propagates():
    """--action flag should appear in simulation_actual.action."""
    result = oracle_graph.invoke({
        "operative": "hamza",
        "turning_point": "dakait-first-meeting",
        "action_override": "trigger_early_exfil",
        "errors": [], "warnings": [],
    })
    assert not result.get("errors")
    sim = result.get("simulation_actual")
    assert sim is not None
    assert sim.action == "trigger_early_exfil"


@pytest.mark.skip(reason="Full pipeline test — enable after POMDP PBVI is implemented (P2)")
def test_parallel_nodes_both_write():
    """intel_network_node and coalition_node both run; outputs should be present."""
    result = oracle_graph.invoke({
        "operative": "hamza",
        "turning_point": "dakait-first-meeting",
        "errors": [], "warnings": [],
    })
    assert result.get("threat_scores")  is not None
    assert result.get("shapley")        is not None
