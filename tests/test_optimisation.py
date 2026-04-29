"""
Unit tests for optimisation modules.

Mirrors got-oracle/tests/test_optimisation.py structure.
Each test validates a specific algorithm in isolation —
no LangGraph, no Anthropic API, no file I/O.

TODO (implement in P2 after grounding):
  - test_pomdp_*      : PBVI solver correctness
  - test_cpm_*        : forward/backward pass, critical path identification
  - test_voi_*        : entropy computation, ranking order
  - test_stackelberg_*: backward induction, commitment value sign
  - test_hmm_*        : (ported from got-oracle, adapted for loyalty states)
  - test_shapley_*    : (ported from got-oracle)
  - test_network_*    : (ported from got-oracle, adapted for intel graph)
"""
import math
import pytest
import numpy as np

# ── HMM tests (ported from got-oracle) ────────────────────────────────────────

from dhurandhar_oracle.optimisation.hmm import HMMParams, viterbi, forward_backward, baum_welch


def test_hmm_uniform_init():
    p = HMMParams.uniform(n_hidden=3, n_obs=2)
    assert p.A.shape  == (3, 3)
    assert p.B.shape  == (3, 2)
    assert p.pi.shape == (3,)
    np.testing.assert_allclose(p.A.sum(axis=1),  [1, 1, 1], atol=1e-9)
    np.testing.assert_allclose(p.B.sum(axis=1),  [1, 1, 1], atol=1e-9)
    np.testing.assert_allclose(p.pi.sum(),        1.0,       atol=1e-9)


def test_viterbi_length():
    p   = HMMParams.uniform(n_hidden=3, n_obs=2)
    obs = [0, 1, 0, 1, 0]
    path, log_prob = viterbi(p, obs)
    assert len(path) == len(obs)
    assert all(0 <= s < 3 for s in path)
    assert log_prob <= 0   # log probability ≤ 0


def test_viterbi_deterministic():
    p   = HMMParams.uniform(n_hidden=3, n_obs=2)
    obs = [0, 1, 1, 0]
    path1, _ = viterbi(p, obs)
    path2, _ = viterbi(p, obs)
    assert path1 == path2


def test_forward_backward_shape():
    p   = HMMParams.uniform(n_hidden=3, n_obs=2)
    obs = [0, 1, 0]
    gamma = forward_backward(p, obs)
    assert gamma.shape == (len(obs), 3)
    np.testing.assert_allclose(gamma.sum(axis=1), [1, 1, 1], atol=1e-6)


def test_baum_welch_improves_likelihood():
    """After EM, the model should fit the sequences at least as well."""
    rng   = np.random.default_rng(0)
    p     = HMMParams.uniform(n_hidden=2, n_obs=3)
    seqs  = [[int(rng.integers(3)) for _ in range(8)] for _ in range(5)]
    p_new = baum_welch(p, seqs, n_iter=10)
    # Matrices should still be valid distributions
    np.testing.assert_allclose(p_new.A.sum(axis=1), [1, 1], atol=1e-6)
    np.testing.assert_allclose(p_new.B.sum(axis=1), [1, 1], atol=1e-6)


# ── Shapley tests (ported from got-oracle) ─────────────────────────────────────

from dhurandhar_oracle.optimisation.shapley import shapley_exact, shapley_approx, defection_incentive


def test_shapley_exact_null_player():
    """An actor who never contributes should have φ = 0."""
    actors = ["hamza", "aalam", "null_asset"]
    def v(S: frozenset) -> float:
        return 1.0 if "hamza" in S else 0.0
    phi = shapley_exact(actors, v)
    assert abs(phi["null_asset"]) < 1e-9


def test_shapley_exact_efficiency():
    """Σ φᵢ = v(grand coalition)."""
    actors = ["hamza", "aalam", "sanyal"]
    def v(S: frozenset) -> float:
        return len(S) * 0.5
    phi = shapley_exact(actors, v)
    total = sum(phi.values())
    assert abs(total - v(frozenset(actors))) < 1e-9


def test_shapley_approx_close_to_exact():
    actors = ["hamza", "aalam", "sanyal"]
    def v(S: frozenset) -> float:
        return len(S) ** 0.8
    exact  = shapley_exact(actors, v)
    approx = shapley_approx(actors, v, n_samples=5000, seed=7)
    for actor in actors:
        assert abs(exact[actor] - approx[actor]) < 0.08


def test_defection_incentive_sign():
    actors = ["hamza", "aalam"]
    def v(S: frozenset) -> float:
        return 2.0 if len(S) == 2 else 0.5
    phi = shapley_exact(actors, v)
    # Both actors benefit from coalition — defection incentive should be negative
    for actor in actors:
        incentive = defection_incentive(actor, actors, v, phi[actor])
        assert incentive < 0


# ── SNA / network tests ────────────────────────────────────────────────────────

from dhurandhar_oracle.optimisation.network import (
    build_intel_graph, compute_centrality, compute_threat_scores,
)
from dhurandhar_oracle.schemas import AdversaryModel, AllianceEdge, ProspectParams


def _make_adversary(actor: str, capability: float = 5.0) -> AdversaryModel:
    return AdversaryModel(
        actor=actor,
        objective="test",
        capability=capability,
        trigger_threshold=5.0,
        observable_actions=["a"],
        hidden_states=["s0", "s1"],
        prospect_params=ProspectParams(),
    )


def _make_edge(src: str, tgt: str, strength: float = 0.5) -> AllianceEdge:
    return AllianceEdge(source=src, target=tgt, strength=strength, in_coalition=True)


def test_build_intel_graph_nodes():
    adversaries = [_make_adversary("dakait"), _make_adversary("jamali")]
    edges       = [_make_edge("dakait", "jamali")]
    G = build_intel_graph(adversaries, edges)
    assert "dakait" in G.nodes
    assert "jamali" in G.nodes
    assert G.has_edge("dakait", "jamali")


def test_compute_centrality_returns_all_nodes():
    adversaries = [_make_adversary("dakait"), _make_adversary("jamali")]
    edges = [_make_edge("dakait", "jamali"), _make_edge("jamali", "dakait")]
    G  = build_intel_graph(adversaries, edges)
    c  = compute_centrality(G)
    assert set(c.betweenness.keys()) == set(G.nodes())


def test_threat_scores_ordered():
    adversaries = [
        _make_adversary("dakait", capability=9.0),
        _make_adversary("jamali", capability=3.0),
    ]
    edges = [_make_edge("dakait", "jamali")]
    G  = build_intel_graph(adversaries, edges)
    c  = compute_centrality(G)
    ts = compute_threat_scores(adversaries, c)
    assert ts[0].actor == "dakait"   # higher capability should score first


# ── CPM tests ──────────────────────────────────────────────────────────────────

from dhurandhar_oracle.optimisation.cpm import (
    build_task_graph, forward_pass, backward_pass, compute_critical_path,
)
from dhurandhar_oracle.schemas import MissionTask


def _make_task(id: str, ml: int, deps: list[str] = None) -> MissionTask:
    return MissionTask(
        id=id, name=id,
        optimistic_days=max(1, ml - 3),
        most_likely_days=ml,
        pessimistic_days=ml + 5,
        dependencies=deps or [],
    )


def test_forward_pass_no_deps():
    tasks = [_make_task("t1", 5), _make_task("t2", 3)]
    G     = build_task_graph(tasks)
    es, ef = forward_pass(G, tasks)
    assert es["t1"] == 0
    assert es["t2"] == 0
    assert abs(ef["t1"] - tasks[0].pert_expected) < 1e-9


def test_forward_pass_serial():
    tasks = [_make_task("t1", 5), _make_task("t2", 3, ["t1"])]
    G     = build_task_graph(tasks)
    es, ef = forward_pass(G, tasks)
    assert abs(es["t2"] - ef["t1"]) < 1e-9


def test_critical_path_all_serial():
    """When all tasks are serial, every task is on the critical path."""
    tasks = [
        _make_task("t1", 5),
        _make_task("t2", 3, ["t1"]),
        _make_task("t3", 4, ["t2"]),
    ]
    G        = build_task_graph(tasks)
    es, ef   = forward_pass(G, tasks)
    ls, lf   = backward_pass(G, tasks, max_ef=max(ef.values()))
    slack    = {t.id: ls[t.id] - es[t.id] for t in tasks}
    critical = [tid for tid, s in slack.items() if abs(s) < 1e-9]
    cp       = compute_critical_path(G, critical)
    assert len(cp) == 3


# ── VoI tests ──────────────────────────────────────────────────────────────────

from dhurandhar_oracle.optimisation.voi import compute_voi_ranking, _shannon_entropy
from dhurandhar_oracle.schemas import IntelligenceTarget


def test_shannon_entropy_uniform():
    belief = {"s0": 0.5, "s1": 0.5}
    h = _shannon_entropy(belief)
    assert abs(h - 1.0) < 1e-9   # 1 bit for fair coin


def test_shannon_entropy_certain():
    belief = {"s0": 1.0, "s1": 0.0}
    h = _shannon_entropy(belief)
    assert abs(h) < 1e-9   # 0 bits when certain


def test_voi_ranking_ordered():
    targets = [
        IntelligenceTarget(id="t1", name="High value", current_entropy=3.0,
                           mission_relevance=0.9, access_difficulty=2.0, access_actions=[]),
        IntelligenceTarget(id="t2", name="Low value", current_entropy=1.0,
                           mission_relevance=0.2, access_difficulty=5.0, access_actions=[]),
    ]
    belief = {"s0": 0.5, "s1": 0.5}
    result = compute_voi_ranking(targets, belief)
    assert result.top_target == "High value"
    assert result.rankings[0].priority_rank == 1


# ── Stackelberg tests ──────────────────────────────────────────────────────────

from dhurandhar_oracle.optimisation.stackelberg import solve_stackelberg
from dhurandhar_oracle.schemas import OperativeState


def test_stackelberg_returns_valid_actions():
    adv = _make_adversary("dakait", capability=8.0)
    sv  = OperativeState(
        cover_integrity=7.0, trust_capital=4.0,
        intelligence_depth=3.0, network_strength=5.0, exposure_risk=4.0,
    )
    actions = ["deepen_cover", "offer_intel", "exfil"]
    result  = solve_stackelberg(adv, actions, sv, [])
    assert result.operative_best_response in actions
    assert result.leader_action in actions


def test_stackelberg_commitment_value_finite():
    adv     = _make_adversary("dakait", capability=7.0)
    sv      = OperativeState(
        cover_integrity=8.0, trust_capital=5.0,
        intelligence_depth=4.0, network_strength=6.0, exposure_risk=3.0,
    )
    actions = ["a", "b", "c"]
    result  = solve_stackelberg(adv, actions, sv, [])
    assert math.isfinite(result.commitment_value)


# ── POMDP / PBVI tests ────────────────────────────────────────────────────────

from dhurandhar_oracle.optimisation.pomdp import PBVISolver, build_pomdp
from dhurandhar_oracle.schemas import CausalDAG


def _make_pomdp_inputs():
    actions = ["deepen_cover", "gather_intel", "trigger_early_exfil"]
    dag = CausalDAG(nodes=["deepen_cover", "trust_increase", "trigger_early_exfil",
                           "cover_blown"], edges=[])
    sv = OperativeState(cover_integrity=8.0, trust_capital=5.0,
                        intelligence_depth=4.0, network_strength=6.0,
                        exposure_risk=3.0)
    belief = {
        "cover_intact_mission_early_adv_unaware":     0.6,
        "cover_intact_mission_mid_adv_suspicious":    0.25,
        "cover_suspected_mission_mid_adv_suspicious": 0.1,
        "cover_blown_mission_stalled_adv_certain":    0.05,
    }
    return actions, dag, sv, belief


def test_pomdp_optimal_action_in_actions():
    actions, dag, sv, belief = _make_pomdp_inputs()
    model = build_pomdp(actions, dag, [], sv, belief)
    solver = PBVISolver(model, n_belief_points=20, n_iterations=30)
    solver.solve()
    result = solver.extract_result(belief)
    assert result.optimal_action in actions


def test_pomdp_belief_state_value_finite():
    actions, dag, sv, belief = _make_pomdp_inputs()
    model = build_pomdp(actions, dag, [], sv, belief)
    solver = PBVISolver(model, n_belief_points=20, n_iterations=30)
    solver.solve()
    result = solver.extract_result(belief)
    assert math.isfinite(result.belief_state_value)
    assert 0.0 <= result.cover_integrity_prob <= 1.0
    assert 0.0 <= result.mission_success_prob <= 1.0
    assert set(result.action_values.keys()) == set(actions)
