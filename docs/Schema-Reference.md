# Schema Reference

This page documents every Pydantic data model in `dhurandhar-oracle` and the JSON data file formats on disk. All models live in `schemas.py`. The shared pipeline state is in `state.py`. For field-level usage within the pipeline see [Multi-Agent System](Multi-Agent-System).

---

## Core Field-State Models

### `OperativeState`

The 5-dimensional state vector describing an operative's field situation at a specific moment. All values are floats in [0, 10].

| Field | Direction | Description |
|---|---|---|
| `cover_integrity` | Higher = better | How intact the operative's false identity is |
| `trust_capital` | Higher = better | Trust built with the target criminal/political network |
| `intelligence_depth` | Higher = better | Quality and quantity of intel gathered so far |
| `network_strength` | Higher = better | Quality of handler/asset support network |
| `exposure_risk` | **Lower = better** | How close the operative is to being discovered |

Used by: `state_node` (loaded from TP JSON), `strategy_node` (POMDP input), `coalition_node`, `simulator_node`, `arc_chain` (state handoff).

---

### `CausalEdge`

A directed edge in the causal model of an operation.

| Field | Type | Description |
|---|---|---|
| `cause` | `str` | Source node ID |
| `effect` | `str` | Target node ID |
| `strength` | `float` [0,1] | ≈ P(effect \| cause) |
| `known_confounders` | `list[str]` | Confounding variables (for transparency) |
| `identified` | `bool` | Whether do-calculus identification holds |
| `confidence` | `float` [0,1] | Confidence in the strength estimate |
| `strength_low` / `strength_high` | `Optional[float]` | Credible interval on strength |
| `estimation_method` | `Optional[str]` | How edge strength was estimated |
| `source_refs` | `list[str]` | Traceability references |

### `CausalDAG`

Container for the causal model at a turning point.

| Field | Type | Description |
|---|---|---|
| `nodes` | `list[str]` | All node IDs (actions + outcomes + intermediates) |
| `edges` | `list[CausalEdge]` | Directed edges |

Helper methods: `successors(node)`, `predecessors(node)`, `get_edge(cause, effect)`

---

### `AllianceEdge`

A directed edge in the alliance/network snapshot.

| Field | Type | Description |
|---|---|---|
| `source` | `str` | Actor ID |
| `target` | `str` | Actor ID |
| `strength` | `float` [0,1] | Alliance strength |
| `betrayal_history` | `int` | Count of prior betrayals |
| `in_coalition` | `bool` | Currently part of Indian-side coalition |
| `trigger_condition` | `Optional[str]` | Condition under which this alliance activates |

---

## Adversary Models

### `ProspectParams`

Kahneman-Tversky Prospect Theory parameters for an adversary's decision-making.

| Field | Default | Description |
|---|---|---|
| `lam` | 2.25 | Loss aversion λ (losses hurt ~2× more than equivalent gains) |
| `gamma` | 0.65 | Probability weighting γ |
| `alpha` | 0.88 | Gain curvature α |
| `beta` | 0.88 | Loss curvature β |
| `ref` | 0.0 | Reference point (status quo) |

### `AdversaryModel`

Intelligence profile for a single adversary actor.

| Field | Type | Description |
|---|---|---|
| `actor` | `str` | Actor ID (must match `data/adversaries/` or character ID) |
| `objective` | `str` | Primary operational objective |
| `capability` | `float` [0,10] | Threat capability score |
| `trigger_threshold` | `float` [0,10] | Capability level at which actor escalates |
| `information_set` | `list[str]` | What this actor knows about the operative |
| `observable_actions` | `list[str]` | Actions the operative has seen this actor take (HMM observation sequence) |
| `hidden_states` | `list[str]` | HMM hidden state space for this actor |
| `prospect_params` | `ProspectParams` | Behavioural finance parameters |

---

## CPM / PERT Models

### `MissionTask`

A task node in the mission PERT network.

| Field | Type | Description |
|---|---|---|
| `id` | `str` | Unique task identifier |
| `name` | `str` | Human-readable task name |
| `optimistic_days` | `int` (≥1) | PERT best-case duration |
| `most_likely_days` | `int` (≥1) | PERT most-likely duration |
| `pessimistic_days` | `int` (≥1) | PERT worst-case duration |
| `dependencies` | `list[str]` | IDs of predecessor tasks (must complete before this starts) |
| `parallelizable_with` | `list[str]` | IDs of tasks with no dependency relationship |
| `requires_cover` | `bool` | Whether intact cover is a prerequisite |
| `risk_to_cover` | `float` [0,1] | P(cover degradation) if task is rushed |

Computed properties:
- `pert_expected` → `(O + 4M + P) / 6`
- `pert_variance` → `((P − O) / 6)²`

---

## Intelligence Target Model

### `IntelligenceTarget`

An intelligence collection opportunity, used as VoI input.

| Field | Type | Description |
|---|---|---|
| `id` | `str` | Unique target identifier |
| `name` | `str` | Human-readable target name |
| `current_entropy` | `float` (≥0) | Current uncertainty about this target in bits |
| `mission_relevance` | `float` [0,1] | How much this target affects mission success |
| `access_difficulty` | `float` [0,10] | Effort/risk required to gather this intel |
| `access_actions` | `list[str]` | Actions that would yield this intel |
| `confidence` | `float` [0,1] | Confidence in the target scoring inputs |
| `source_refs` | `list[str]` | Traceability references |

---

## Turning Point Model

### `TurningPoint`

The fundamental query unit — one per key scene/decision across both films.

| Field | Type | Description |
|---|---|---|
| `id` | `str` | Unique identifier (e.g. `dakait-first-meeting`) |
| `operative` | `str` | Character ID of the Indian-side protagonist |
| `film` | `int` [1–4] | Film number |
| `act` | `int` [1–3] | Act within the film |
| `description` | `str` | Scene description text |
| `state_vector` | `OperativeState` | Operative's 5-dim state at this point |
| `available_actions` | `list[str]` | Discrete choices available |
| `mission_tasks` | `list[MissionTask]` | CPM/PERT task graph for this turning point |
| `causal_dag` | `CausalDAG` | Causal model for this turning point |
| `adversaries` | `list[AdversaryModel]` | Relevant adversary profiles |
| `alliance_snapshot` | `list[AllianceEdge]` | Network state at this turning point |
| `intelligence_targets` | `list[IntelligenceTarget]` | Available intel collection opportunities |
| `belief_state` | `dict[str, float]` | Initial POMDP belief: world_state_id → probability |
| `real_world_correlation` | `Optional[dict]` | Grounded real-world event data passed to narrator |
| `next_turning_point` | `Optional[str]` | ID of chronologically next TP (belief propagation) |
| `terminal_belief` | `Optional[dict[str, float]]` | Belief at end of TP, seeds next TP |
| `source_refs` | `list[str]` | Documentary / research references |
| `schema_version` | `str` | Data schema version (current: `"1.1.0"`) |

---

## Algorithm Output Schemas

### `POOMDPResult` — POMDP strategy output

| Field | Type | Description |
|---|---|---|
| `belief_state` | `dict[str, float]` | Updated belief after Stackelberg evidence |
| `optimal_action` | `str` | argmax action |
| `belief_state_value` | `float` | V(b) expected value at current belief |
| `policy` | `dict[str, str]` | `belief_hash → optimal_action` for nearby beliefs |
| `cover_integrity_prob` | `float` [0,1] | P(cover intact) under optimal action |
| `mission_success_prob` | `float` [0,1] | P(mission success) under optimal action |
| `action_values` | `dict[str, float]` | Q(b, a) for every available action |

### `StackelbergResult` — adversary equilibrium output

| Field | Type | Description |
|---|---|---|
| `leader_action` | `str` | Handler's committed strategy |
| `operative_best_response` | `str` | Operative's optimal response |
| `follower_best_response` | `str` | Adversary's optimal counter |
| `equilibrium_payoff_indian` | `float` | Indian side equilibrium payoff |
| `equilibrium_payoff_adversary` | `float` | Adversary equilibrium payoff |
| `commitment_value` | `float` | V(Stackelberg) − V(Nash) |

### `CriticalPathResult` — CPM/PERT output

| Field | Type | Description |
|---|---|---|
| `critical_path` | `list[str]` | Task IDs on critical path in order |
| `total_duration_days` | `float` | PERT expected total (sequential) |
| `optimal_duration_days` | `float` | Duration with parallelisation |
| `days_saved` | `float` | Difference |
| `bottleneck_task` | `str` | Highest-impact task on critical path |
| `slack_tasks` | `list[tuple[str, float]]` | (task_id, slack_days) |
| `parallelisation_opportunities` | `list[tuple[str, str]]` | (task_a, task_b) concurrent pairs |

### `VoIEntry` / `VoIResult` — Value of Information output

`VoIEntry` (one per target):

| Field | Type | Description |
|---|---|---|
| `intelligence_target` | `str` | Target ID |
| `voi_bits` | `float` (≥0) | Expected entropy reduction in bits |
| `priority_rank` | `int` | 1 = highest priority |
| `effort_required` | `float` | From `IntelligenceTarget.access_difficulty` |
| `recommendation` | `str` | Human-readable recommendation |

`VoIResult`:

| Field | Type | Description |
|---|---|---|
| `rankings` | `list[VoIEntry]` | All targets ranked |
| `top_target` | `str` | Highest VoI target ID |
| `total_entropy_bits` | `float` | H(current belief state) |

### `CentralityScores` / `ThreatScore` — SNA outputs

`CentralityScores`:

| Field | Type | Description |
|---|---|---|
| `betweenness` | `dict[str, float]` | Betweenness centrality per actor |
| `eigenvector` | `dict[str, float]` | Eigenvector centrality per actor |
| `clustering` | `dict[str, float]` | Clustering coefficient per actor |
| `communities` | `list[list[str]]` | Louvain community partition |

`ThreatScore` (one per actor):

| Field | Type | Description |
|---|---|---|
| `actor` | `str` | Actor ID |
| `score` | `float` | Composite: 0.5×capability + 0.3×betweenness + 0.2×eigenvector |
| `betweenness` | `float` | Raw betweenness |
| `eigenvector` | `float` | Raw eigenvector |
| `is_high` | `bool` | Above high-threat threshold |

### `ShapleyResult` — coalition attribution output

| Field | Type | Description |
|---|---|---|
| `values` | `dict[str, float]` | Shapley value φᵢ per actor |
| `defection_incentives` | `dict[str, float]` | Normalised solo value (gain from leaving coalition) |

### `HMMResult` / `BeliefGap` — mole detection outputs

`HMMResult` (one per actor):

| Field | Type | Description |
|---|---|---|
| `actor` | `str` | Actor ID |
| `hidden_states` | `list[str]` | State space for this actor |
| `most_likely_state` | `str` | Viterbi endpoint |
| `state_probs` | `dict[str, float]` | Posterior marginals from Forward-Backward |
| `viterbi_path` | `list[str]` | Full most-likely state sequence |

`BeliefGap` (one per actor):

| Field | Type | Description |
|---|---|---|
| `actor` | `str` | Actor ID |
| `operative_believed` | `str` | What the operative's current belief says |
| `hmm_inferred` | `str` | What HMM infers from observable history |
| `gap` | `float` | Dissimilarity score [0, 1] |

### `SimulationOutput` — Monte Carlo output

| Field | Type | Description |
|---|---|---|
| `action` | `str` | Action evaluated |
| `p_mission_success` | `float` [0,1] | P(mission success) |
| `p_cover_blown` | `float` [0,1] | P(cover blown) |
| `ci_low` / `ci_high` | `float` | 95% Wilson CI bounds |
| `n_rollouts` | `int` | Number of MC samples |
| `mode_outcome` | `str` | Modal terminal outcome label |
| `key_lever` | `Optional[str]` | Highest-impact causal edge (`cause→effect`) |

---

## Character and Career-Arc Models

### `CharacterProfile`

Master character record. `side` gates oracle access.

| Field | Type | Description |
|---|---|---|
| `id` | `str` | Character identifier (used in CLI commands) |
| `name` | `str` | Full name (may include cover identity) |
| `nationality` | `str` | |
| `side` | `"indian" \| "pakistani" \| "unknown"` | **Gates oracle access — only `"indian"` can be queried** |
| `role` | `str` | e.g. `"RAW undercover operative"`, `"NSA handler"` |
| `films` | `list[int]` | Film numbers the character appears in |
| `cover_identity` | `Optional[str]` | False name used in the field (Indian operatives only) |
| `real_life_inspiration` | `Optional[str]` | Documentary reference |
| `state_by_act` | `dict[str, OperativeState]` | `"film1_act2"` → operative state at that act |
| `observable_history` | `list[ObservableActionEntry]` | Per-film/act action log for HMM |
| `adversary_model` | `Optional[AdversaryModel]` | If this character also appears as an adversary |
| `is_real_public_figure` | `bool` | Forward projections flagged `[SPECULATIVE]` if True |
| `archetype` | `"fictional_operative" \| "public_figure" \| "support_actor"` | Tiers `suggest` CLI output |
| `long_horizon_objective_weights` | `Optional[LongHorizonWeights]` | Per-operative career-arc objective weights |

**Validation:** `cover_identity` is only allowed when `side == "indian"`. Weights must sum to 1.0.

### `LongHorizonObjective`

5-dimensional career-arc objective vector. All values [0, 10].

| Field | Direction | Description |
|---|---|---|
| `mission_yield` | Higher = better | Cumulative actionable intelligence / operational success |
| `strategic_impact` | Higher = better | Geopolitical / doctrinal impact of the operative's career |
| `personal_cost` | **Lower = better** | Psychological, identity, life-risk toll |
| `network_durability` | Higher = better | Handler/asset network durability across the career |
| `attribution_risk` | **Lower = better** | Risk of operation being attributed to India |

### `LongHorizonWeights`

Per-operative weights that collapse `LongHorizonObjective` to a scalar. Must sum to 1.0.

| Field | Default | Description |
|---|---|---|
| `mission_yield` | 0.30 | Weight magnitude for mission yield |
| `strategic_impact` | 0.25 | Weight magnitude for strategic impact |
| `personal_cost` | 0.15 | Weight magnitude for personal cost (penalised in solver) |
| `network_durability` | 0.15 | Weight magnitude for network durability |
| `attribution_risk` | 0.15 | Weight magnitude for attribution risk (penalised in solver) |

### `MacroAction`

A career-level decision the operative can make in response to a real-world event (Mode 2).

| Field | Type | Description |
|---|---|---|
| `id` | `str` | Action identifier |
| `label` | `str` | Short human-readable label |
| `description` | `str` | Full description |
| `objective_delta` | `ObjectiveDelta` | Expected per-step signed change to 5d objective |
| `transition_probs` | `dict[CareerTerminalStatus, float]` | Probability of each career status after this action (must sum to 1.0) |
| `requires_status` | `list[CareerTerminalStatus]` | Action only available when status is in this list |

### `MacroArc`

The post-D2 forward career arc for one operative. Loaded from `data/post_d2_arc/<operative>.json`.

| Field | Type | Description |
|---|---|---|
| `operative` | `str` | Operative ID |
| `arc_start` | `str` | ISO date — usually post-D2 canon end |
| `description` | `str` | Narrative description of the arc |
| `actions` | `list[MacroAction]` | All available macro-actions |
| `events` | `list[MacroEvent]` | Chronological real-world events to respond to |
| `initial_status` | `CareerTerminalStatus` | Starting career status (default: `"active"`) |
| `initial_objective` | `LongHorizonObjective` | Starting 5d objective values |
| `is_speculative_real_figure` | `bool` | If True, narrative prepends `[SPECULATIVE]` |

### `ForwardProjection` — Mode 2 output

| Field | Type | Description |
|---|---|---|
| `operative` | `str` | Operative ID |
| `arc_start` / `horizon_until` | `str` | ISO date range |
| `is_speculative_real_figure` | `bool` | Speculative flag |
| `predicted` | `CareerTrajectory` | Conservative canonical extrapolation |
| `prescribed` | `CareerTrajectory` | Oracle-optimal MDP policy |
| `scalar_score_delta` | `float` | prescribed.scalar_score − predicted.scalar_score |
| `objective_delta` | `ObjectiveDelta` | 5d difference between trajectories |
| `key_divergence_event` | `Optional[str]` | First event where trajectories diverge |

### `ArcRewrite` — Mode 3 output

| Field | Type | Description |
|---|---|---|
| `operative` | `str` | Operative ID |
| `steps` | `list[ArcStep]` | Per-TP: actual/prescribed actions, Q-values, delta, state handoff |
| `cumulative_q_delta` | `float` | Σ Q(prescribed) − Q(actual) across all TPs |
| `final_state_baseline` | `OperativeState` | Canon end state |
| `final_state_prescribed` | `OperativeState` | Counterfactual end state (heuristic uplift) |
| `objective_delta` | `ObjectiveDelta` | 5d career-level improvement estimate |

---

## JSON Data File Formats

### Character file — `data/characters/<id>.json`

Validated against `CharacterProfile`. Minimum required fields:

```json
{
  "id": "hamza",
  "name": "Hamza Ali Mazari / Jaskirat Singh Rangi",
  "nationality": "Indian",
  "side": "indian",
  "role": "RAW undercover operative",
  "films": [1, 2],
  "cover_identity": "Hamza Ali Mazari",
  "state_by_act": {
    "film1_act1": {
      "cover_integrity": 9.0,
      "trust_capital": 2.0,
      "intelligence_depth": 1.0,
      "network_strength": 7.0,
      "exposure_risk": 1.5
    }
  },
  "archetype": "fictional_operative",
  "schema_version": "1.1.0"
}
```

### Turning point file — `data/turning_points/<id>.json`

Validated against `TurningPoint`. Contains the full computational payload:

```json
{
  "id": "dakait-first-meeting",
  "operative": "hamza",
  "film": 1,
  "act": 1,
  "description": "...",
  "state_vector": { "cover_integrity": 8.5, ... },
  "available_actions": ["build_trust_slow", "extract_intel_now", "abort_mission"],
  "mission_tasks": [
    {
      "id": "gain_entry",
      "name": "Gain entry to inner circle",
      "optimistic_days": 7,
      "most_likely_days": 14,
      "pessimistic_days": 30,
      "dependencies": [],
      "parallelizable_with": ["gather_street_intel"],
      "requires_cover": true,
      "risk_to_cover": 0.1
    }
  ],
  "causal_dag": {
    "nodes": ["build_trust_slow", "cover_intact", "intel_extracted", ...],
    "edges": [
      { "cause": "build_trust_slow", "effect": "cover_intact", "strength": 0.85, ... }
    ]
  },
  "adversaries": [ { "actor": "rehman_dakait", "capability": 8.5, ... } ],
  "alliance_snapshot": [ { "source": "hamza", "target": "mohammed_aalam", "strength": 0.9, ... } ],
  "intelligence_targets": [
    { "id": "dakait_real_name", "current_entropy": 3.2, "mission_relevance": 0.9, "access_difficulty": 6.0, ... }
  ],
  "belief_state": { "cover_intact_low_suspicion": 0.7, "cover_intact_high_suspicion": 0.2, ... },
  "schema_version": "1.1.0"
}
```

### Outcome file — `data/outcomes/<turning_point_id>.json`

Validated against `OutcomeEntry`. Records what actually happened:

```json
{
  "turning_point_id": "dakait-first-meeting",
  "actual_action": "build_trust_slow",
  "immediate_effects": ["Gained Dakait's trust", "Delayed intel extraction"],
  "terminal_state": "in_progress",
  "days_elapsed": 21,
  "cover_change": 0.5,
  "confidence": 0.8,
  "schema_version": "1.1.0"
}
```

### MacroArc file — `data/post_d2_arc/<operative>.json`

Validated against `MacroArc`. Required for Mode 2 (Forward Projection):

```json
{
  "operative": "hamza",
  "arc_start": "2025-04-01",
  "description": "Post-Dhurandhar-2 career arc — real-world events 2025-2026",
  "initial_status": "active",
  "initial_objective": { "mission_yield": 7.5, "strategic_impact": 6.0, ... },
  "actions": [
    {
      "id": "pivot_offshore",
      "label": "Pivot to overseas operations",
      "objective_delta": { "mission_yield": 1.5, "personal_cost": 2.0, ... },
      "transition_probs": { "active": 0.90, "killed": 0.04, "blown": 0.03, "extracted": 0.02, "retired": 0.01 },
      "requires_status": ["active"]
    }
  ],
  "events": [
    {
      "id": "pahalgam-2025",
      "date": "2025-04-22",
      "label": "Pahalgam attack",
      "context_ref": "pahalgam-2025",
      "available_actions": ["pivot_offshore", "deep_strike_response"]
    }
  ]
}
```

---

## Adding New Operatives and Turning Points

### Adding a new Indian-side operative

1. Create `data/characters/<operative_id>.json` with `"side": "indian"`.
2. Populate `state_by_act` with at least one entry (format: `"film1_act1"`, `"film2_act3"`, etc.).
3. Set `archetype` to `"fictional_operative"` (queryable) or `"public_figure"` (flagged speculative in forward mode).
4. Run `dhurandhar-oracle list-characters` to verify the operative appears.

### Adding a new turning point

1. Create `data/turning_points/<id>.json` validated against `TurningPoint`.
2. Ensure `operative` matches an existing `"indian"`-side character ID.
3. Populate `causal_dag` with at least one action node and one outcome node connected by an edge.
4. Populate `belief_state` with a valid probability distribution (values sum to 1.0).
5. Create the corresponding `data/outcomes/<id>.json` with `actual_action` set to one of `available_actions`.
6. Run `dhurandhar-oracle audit-data` to check coverage and flag any missing outcomes or low-confidence edges.

### Adding a macro-arc for Mode 2

1. Create `data/post_d2_arc/<operative_id>.json` validated against `MacroArc`.
2. Ensure all `available_actions` in events reference valid `MacroAction.id` values.
3. Validate that each `MacroAction.transition_probs` sums to 1.0 (Pydantic will raise on load if not).
4. Run `dhurandhar-oracle suggest --mode forward` to confirm the operative appears in the ready list.
