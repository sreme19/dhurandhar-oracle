# Technical Reference

This page is the authoritative technical specification for every algorithm in `dhurandhar-oracle`. For a beginner-friendly introduction see [Models Guide](Models-Guide). For data schemas see [Schema Reference](Schema-Reference).

---

## Algorithm Dependency Chain

Algorithms do not run independently — each feeds the next. The chain below shows the **data dependencies** across the turning-point pipeline:

```
┌──────────────────────┐     ┌─────────────────┐
│  SNA (NetworkX)      │     │  Shapley Values  │
│  → centrality,       │     │  → shapley,      │
│    threat_scores,    │     │    defection_     │
│    high_threat_actors│     │    incentives     │
└──────────┬───────────┘     └────────┬─────────┘
           │                          │
           └──────────┬───────────────┘
                      ▼
            ┌─────────────────────┐
            │  HMM                │
            │  → hmm_results,     │  needs: high_threat_actors + shapley.defection_incentives
            │    belief_gaps      │
            └──────────┬──────────┘
                       ▼
            ┌─────────────────────┐
            │  VoI                │  needs: belief_state (loaded at state_node)
            │  → voi_result       │
            └──────────┬──────────┘
                       ▼
            ┌─────────────────────┐
            │  Stackelberg        │  needs: belief_gaps (from HMM)
            │  → stackelberg      │
            └──────────┬──────────┘
                       ▼
            ┌─────────────────────┐
            │  POMDP (PBVI)       │  needs: stackelberg (feeds belief update)
            │  → pomdp            │
            └──────────┬──────────┘
                       ▼
            ┌─────────────────────┐
            │  CPM / PERT         │  independent of POMDP; needs mission_tasks
            │  → critical_path    │
            └──────────┬──────────┘
                       ▼
            ┌─────────────────────┐
            │  Monte Carlo        │  needs: pomdp.optimal_action + causal_dag
            │  → simulation_*     │
            └─────────────────────┘
```

SNA and Shapley run **in parallel** (LangGraph fan-out). All subsequent nodes are sequential.

---

## 1. POMDP — Point-Based Value Iteration (PBVI)

**Question answered:** What is the optimal next action when the operative does not know the full world state?

**Source:** `optimisation/pomdp.py`, consumed by `agents/strategy_node.py`

**Why POMDP, not MDP:** Intelligence operations are the canonical POMDP domain. The operative cannot observe full world state — is the handler compromised? Does Dakait suspect Hamza? POMDP planning operates over a *belief state* (a probability distribution over possible world states) and produces policies that account for this uncertainty. The predecessor project (got-oracle) used a fully-observable MDP; this is the central algorithmic step up. PBVI is chosen over exact POMDP solvers because it is tractable for moderate state spaces and suits the discrete action/observation model of intelligence ops.

### Inputs

| Field | Type | Source | Description |
|---|---|---|---|
| `initial_belief_state` | `dict[str, float]` | `state_node` (from TP JSON) | World state → probability. Must sum to 1.0 |
| `available_actions` | `list[str]` | `state_node` | Discrete action set for this turning point |
| `causal_dag` | `CausalDAG` | `state_node` | Nodes + directed edges with `strength` (≈ P(effect\|cause)) |
| `adversaries` | `list[AdversaryModel]` | `state_node` | Capability, objective, hidden states per adversary |
| `state_vector` | `OperativeState` | `state_node` | 5-dim field-state vector at this turning point |
| `stackelberg` | `StackelbergResult` | `adversary_node` | Leader commitment feeds the belief update |

### Outputs — `POOMDPResult`

| Field | Type | Description |
|---|---|---|
| `belief_state` | `dict[str, float]` | Updated belief distribution after Stackelberg evidence |
| `optimal_action` | `str` | argmax action under current belief |
| `belief_state_value` | `float` | V(b) — expected value at current belief |
| `policy` | `dict[str, str]` | `belief_hash → optimal_action` for nearby beliefs |
| `cover_integrity_prob` | `float` [0,1] | P(cover_intact) under optimal action |
| `mission_success_prob` | `float` [0,1] | P(mission_success) under optimal action |
| `action_values` | `dict[str, float]` | Q(b, a) for every available action |

### Mathematical Formulation

A POMDP is defined by the tuple ⟨S, A, O, T, Z, R, b₀⟩:

- **S** — finite set of world states (e.g., `cover_intact_low_suspicion`, `cover_blown_handler_compromised`)
- **A** — finite action set (`available_actions`)
- **O** — observation set (`trust_signal`, `intelligence_return`, `handler_report`, etc.)
- **T(s, a, s')** = P(s' | s, a) — transition probabilities derived from `causal_dag` edge strengths
- **Z(o | s', a)** = P(o | s', a) — observation probabilities (currently proportional partition approximation)
- **R(s, a)** — reward function encoding mission objectives
- **b₀** — initial belief state from turning-point JSON

**Belief update:** After taking action a and observing o:

```
b'(s') = η · Z(o|s',a) · Σ_s T(s,a,s') · b(s)
```

where η is a normalisation constant.

**Value function** over belief space is represented as a set of α-vectors (hyperplanes). Each α-vector defines a linear value function over beliefs:

```
V(b) = max_α  α · b
```

**PBVI backup operator** adds one new α-vector per belief point per iteration:

```
α̂_a(s) = R(s,a) + γ · Σ_{s'} T(s,a,s') · max_{α'} Σ_o Z(o|s',a) · (α' · b_o)
```

The algorithm iterates until value improvement falls below a convergence threshold (default ε = 1e-4) or a maximum iteration count is reached.

**Q-value for action a at belief b:**

```
Q(b, a) = Σ_s b(s) · α̂_a(s)
```

The optimal action is `argmax_a Q(b, a)`.

---

## 2. Stackelberg Equilibrium

**Question answered:** Given that RAW handler commits to a strategy first, how will the adversary respond — and does that commitment give India an advantage?

**Source:** `optimisation/stackelberg.py`, consumed by `agents/adversary_node.py`

**Why Stackelberg, not Nash/CFR:** got-oracle used CFR (Counterfactual Regret Minimisation) for symmetric simultaneous games. In Dhurandhar, the RAW handler *commits* to orders before the operative acts, and the operative acts before the adversary can fully respond. This sequential leader-follower structure is a Stackelberg game. Stackelberg equilibrium captures the value of *commitment* — the handler's credible pre-commitment changes the operative's optimal response and, through it, the adversary's counter. Nash equilibrium would miss this asymmetry.

### Inputs

| Field | Type | Source | Description |
|---|---|---|---|
| `available_actions` | `list[str]` | `state_node` | Action set shared with POMDP |
| `adversaries` | `list[AdversaryModel]` | `state_node` | Adversary capabilities, objectives, Prospect Theory params |
| `state_vector` | `OperativeState` | `state_node` | Current operative field state |
| `belief_gaps` | `list[BeliefGap]` | `belief_node` | HMM-inferred loyalty gaps feed adversary information set |

### Outputs — `StackelbergResult`

| Field | Type | Description |
|---|---|---|
| `leader_action` | `str` | Handler's committed strategy |
| `operative_best_response` | `str` | Operative's optimal response given leader commitment |
| `follower_best_response` | `str` | Adversary's optimal counter |
| `equilibrium_payoff_indian` | `float` | Indian side payoff at equilibrium |
| `equilibrium_payoff_adversary` | `float` | Adversary payoff at equilibrium |
| `commitment_value` | `float` | V(Stackelberg) − V(Nash): marginal gain from pre-commitment |

### Mathematical Formulation

Three players in sequential order:

1. **Leader (RAW handler)** — commits to strategy σ_L
2. **Middle player (operative)** — observes σ_L, best-responds with σ_M(σ_L)
3. **Follower (adversary)** — observes σ_M, best-responds with σ_F(σ_M)

Solved by **backward induction**:

**Step 1 — Follower's best response:**

```
σ*_F(σ_M) = argmax_{σ_F} u_F(σ_M, σ_F)
```

**Step 2 — Middle player's best response given leader commitment:**

```
σ*_M(σ_L) = argmax_{σ_M} u_M(σ_L, σ_M, σ*_F(σ_M))
```

**Step 3 — Leader's optimal commitment:**

```
σ*_L = argmax_{σ_L} u_L(σ_L, σ*_M(σ_L), σ*_F(σ*_M(σ_L)))
```

**Commitment value** measures the benefit of sequential play:

```
commitment_value = V_Stackelberg(σ*_L) − V_Nash
```

Adversary payoffs are modulated by **Prospect Theory** parameters (`ProspectParams`) — the adversary evaluates gains and losses asymmetrically (loss aversion λ = 2.25 by default).

---

## 3. Hidden Markov Model (HMM) — Mole Detection

**Question answered:** Based on observable actions, what is the hidden loyalty state of each actor — and is there a significant gap between what the operative believes and what HMM infers?

**Source:** `optimisation/hmm.py`, consumed by `agents/belief_node.py`

**Why HMM:** Loyalty is a hidden (latent) variable; only actions are observable. HMM is the standard framework for inferring a latent state sequence from a discrete observation sequence. The Viterbi algorithm gives the most likely state path; Forward-Backward gives per-timestep posteriors; Baum-Welch re-estimates parameters from data.

### Inputs

| Field | Type | Source | Description |
|---|---|---|---|
| `adversaries` | `list[AdversaryModel]` | `state_node` | `observable_actions` and `hidden_states` per actor |
| `high_threat_actors` | `list[str]` | `intel_network_node` | Actors warranting HMM scrutiny |
| `shapley` | `ShapleyResult` | `coalition_node` | `defection_incentives` inform prior transition probs |

### Outputs

**`HMMResult` per actor:**

| Field | Type | Description |
|---|---|---|
| `actor` | `str` | Actor ID |
| `hidden_states` | `list[str]` | State space: `loyal`, `wavering`, `compromised`, `turned` |
| `most_likely_state` | `str` | Viterbi endpoint |
| `state_probs` | `dict[str, float]` | Posterior marginals from Forward-Backward |
| `viterbi_path` | `list[str]` | Full most-likely state sequence over observable history |

**`BeliefGap` per actor:**

| Field | Type | Description |
|---|---|---|
| `actor` | `str` | Actor ID |
| `operative_believed` | `str` | What the operative's current belief says |
| `hmm_inferred` | `str` | What the HMM infers from observable history |
| `gap` | `float` | Dissimilarity score [0, 1] |

**Mole alert threshold:** `defection_incentive > 0.5 AND gap > 0.6`

### Mathematical Formulation

**States:** Q = {loyal, wavering, compromised, turned}

**Observations:** O = {observable_actions listed in AdversaryModel}

**Parameters:** λ = (A, B, π)
- A[i,j] = P(state_j at t+1 | state_i at t) — transition matrix
- B[i,k] = P(obs_k | state_i) — emission matrix
- π[i] = P(state_i at t=0) — initial distribution

**Viterbi algorithm** (most likely path):

```
δ_t(i) = max_{q_1…q_{t-1}} P(q_1…q_{t-1}, q_t=i, o_1…o_t | λ)
δ_t(j) = max_i [δ_{t-1}(i) · A[i,j]] · B[j, o_t]
```

**Forward-Backward** (posterior marginals):

```
γ_t(i) = P(q_t=i | O, λ) = α_t(i) · β_t(i) / P(O|λ)
```

**Baum-Welch** (EM parameter re-estimation) updates A, B, π from the observation sequence when sufficient data is available.

---

## 4. Shapley Values — Coalition Attribution

**Question answered:** What is each Indian-side asset's fair contribution to the coalition, and who has an incentive to defect?

**Source:** `optimisation/shapley.py`, consumed by `agents/coalition_node.py`

**Why Shapley:** Shapley values are the unique fair attribution in cooperative game theory — they satisfy efficiency, symmetry, linearity, and the dummy player axioms. Identifying defection incentives (the gain an asset gets from leaving the coalition) is critical for operational security.

### Inputs

| Field | Type | Source | Description |
|---|---|---|---|
| `alliance_snapshot` | `list[AllianceEdge]` | `state_node` | Strength and betrayal history per alliance edge |
| `state_vector` | `OperativeState` | `state_node` | Operative field state affects coalition value |

### Outputs — `ShapleyResult`

| Field | Type | Description |
|---|---|---|
| `values` | `dict[str, float]` | Shapley value φᵢ per actor |
| `defection_incentives` | `dict[str, float]` | Gain actor i gets from leaving the coalition |

### Mathematical Formulation

For N players, the Shapley value for player i is:

```
φᵢ = Σ_{S ⊆ N\{i}}  [|S|! · (|N|−|S|−1)! / |N|!] · [v(S∪{i}) − v(S)]
```

where v(S) is the value function for coalition S (derived from alliance_snapshot strengths and operative state).

**Computational modes:**
- **Exact** — O(N · 2^N), used when N ≤ 8
- **Monte Carlo approximation** — O(n_samples · N), used when N > 8; samples random permutations and averages marginal contributions

**Defection incentive** for actor i:

```
defection_incentive(i) = v({i}) / v(N)   [normalised solo value]
```

High defection incentive (> 0.5) combined with HMM gap > 0.6 triggers a mole alert.

---

## 5. Value of Information (VoI)

**Question answered:** Which intelligence target should the operative gather first, given limited time and risk budget?

**Source:** `optimisation/voi.py`, consumed by `agents/voi_node.py`

**Why VoI:** POMDP chooses the optimal *action*; VoI answers the complementary question about *information gathering*. VoI measures the expected entropy reduction from each intelligence target — high-VoI targets reduce uncertainty the most per unit effort/risk and should be prioritised.

### Inputs

| Field | Type | Source | Description |
|---|---|---|---|
| `intelligence_targets` | `list[IntelligenceTarget]` | `state_node` | Per-target: `current_entropy`, `mission_relevance`, `access_difficulty` |
| `initial_belief_state` | `dict[str, float]` | `state_node` | Current belief distribution over world states |

### Outputs — `VoIResult`

| Field | Type | Description |
|---|---|---|
| `rankings` | `list[VoIEntry]` | Priority-ordered targets |
| `top_target` | `str` | Highest VoI target ID |
| `total_entropy_bits` | `float` | H(current belief state) in bits |

Each `VoIEntry`:

| Field | Type | Description |
|---|---|---|
| `intelligence_target` | `str` | Target ID |
| `voi_bits` | `float` | Expected entropy reduction in bits |
| `priority_rank` | `int` | 1 = highest |
| `effort_required` | `float` | From `IntelligenceTarget.access_difficulty` |
| `recommendation` | `str` | Human-readable action recommendation |

### Mathematical Formulation

**Current belief entropy:**

```
H(b) = −Σ_s b(s) · log₂(b(s))     [bits]
```

**Exact VoI** for target X:

```
VoI(X) = H(b) − E[H(b | observe X)]
       = H(b) − Σ_o P(o|b) · H(b_o)
```

**Current approximation** (pending full Z(o|s',a) observation model):

```
VoI(X) ≈ H(b) · mission_relevance(X)
```

**Effort-adjusted priority score:**

```
score(X) = VoI(X) / access_difficulty(X)
```

Targets are ranked by this score descending.

> **Note:** The approximation is flagged as a TODO in the source — it will be replaced with the proper POMDP observation model once the full Z(o|s',a) matrix is available per turning point.

---

## 6. Social Network Analysis (SNA)

**Question answered:** Who are the power brokers in the Karachi criminal-political network, and which actors are the highest threat?

**Source:** `optimisation/network.py`, consumed by `agents/intel_network_node.py`

### Inputs

| Field | Type | Source | Description |
|---|---|---|---|
| `adversaries` | `list[AdversaryModel]` | `state_node` | Actors and capability scores |
| `alliance_snapshot` | `list[AllianceEdge]` | `state_node` | Network edges with `strength` and `in_coalition` |

### Outputs

**`CentralityScores`:**

| Field | Type | Description |
|---|---|---|
| `betweenness` | `dict[str, float]` | Betweenness centrality per actor |
| `eigenvector` | `dict[str, float]` | Eigenvector centrality per actor |
| `clustering` | `dict[str, float]` | Local clustering coefficient |
| `communities` | `list[list[str]]` | Louvain community partition |

**`ThreatScore` per actor:**

| Field | Type | Description |
|---|---|---|
| `actor` | `str` | Actor ID |
| `score` | `float` | Composite threat score |
| `betweenness` | `float` | Raw betweenness centrality |
| `eigenvector` | `float` | Raw eigenvector centrality |
| `is_high` | `bool` | True if score above high-threat threshold |

### Mathematical Formulation

**Betweenness centrality** (fraction of shortest paths through node v):

```
C_B(v) = Σ_{s≠v≠t} σ(s,t|v) / σ(s,t)
```

**Eigenvector centrality** (importance proportional to neighbours' importance):

```
A · x = λ_max · x     →     x_i = (1/λ_max) Σ_j A_{ij} x_j
```

**Composite threat score:**

```
threat(v) = 0.5 · capability(v) + 0.3 · C_B(v) + 0.2 · eigenvector(v)
```

**Community detection:** Louvain algorithm maximising modularity Q:

```
Q = (1/2m) Σ_{ij} [A_{ij} − k_i·k_j/(2m)] · δ(c_i, c_j)
```

Implementation uses **NetworkX** for graph construction and centrality computation.

---

## 7. Critical Path Method (CPM) + PERT

**Question answered:** What is the minimum mission duration, which tasks are on the critical path, and how much time could be saved through parallelisation?

**Source:** `optimisation/cpm.py`, consumed by `agents/critical_path_node.py`

**Why CPM/PERT:** The "what could have been done faster" question is literally a project scheduling problem. Mission tasks form a dependency graph with uncertain durations. CPM finds the binding constraint; PERT three-point estimation quantifies duration uncertainty.

### Inputs

| Field | Type | Source | Description |
|---|---|---|---|
| `mission_tasks` | `list[MissionTask]` | `state_node` | Task graph with PERT estimates and dependency list |

Each `MissionTask`:

| Field | Type | Description |
|---|---|---|
| `optimistic_days` | `int` | PERT optimistic estimate (O) |
| `most_likely_days` | `int` | PERT most-likely estimate (M) |
| `pessimistic_days` | `int` | PERT pessimistic estimate (P) |
| `dependencies` | `list[str]` | IDs of predecessor tasks |
| `parallelizable_with` | `list[str]` | IDs of tasks with no dependency relationship |
| `requires_cover` | `bool` | Whether intact cover is a prerequisite |
| `risk_to_cover` | `float` [0,1] | Probability this task degrades cover if rushed |

### Outputs — `CriticalPathResult`

| Field | Type | Description |
|---|---|---|
| `critical_path` | `list[str]` | Task IDs on the critical path in order |
| `total_duration_days` | `float` | PERT expected duration (sequential plan) |
| `optimal_duration_days` | `float` | Duration if all parallelisation opportunities exploited |
| `days_saved` | `float` | `total_duration_days − optimal_duration_days` |
| `bottleneck_task` | `str` | Task with highest impact on total duration |
| `slack_tasks` | `list[tuple[str, float]]` | (task_id, slack_days) for non-critical tasks |
| `parallelisation_opportunities` | `list[tuple[str, str]]` | (task_a, task_b) pairs that can run concurrently |

### Mathematical Formulation

**PERT expected duration** per task:

```
E[d] = (O + 4M + P) / 6
```

**PERT variance** per task:

```
Var[d] = ((P − O) / 6)²
```

**Forward pass** (earliest start/finish times):

```
ES(v) = max_{u ∈ predecessors(v)} EF(u)
EF(v) = ES(v) + E[d_v]
```

**Backward pass** (latest start/finish times, from project end):

```
LF(v) = min_{w ∈ successors(v)} LS(w)
LS(v) = LF(v) − E[d_v]
```

**Total float (slack):**

```
slack(v) = LS(v) − ES(v)   [= LF(v) − EF(v)]
```

Tasks with `slack = 0` form the **critical path**. The bottleneck task is the critical-path task with the highest `E[d]`.

---

## 8. Monte Carlo Simulation

**Question answered:** What is the probability of mission success and cover integrity under the actual action taken versus the POMDP-optimal action?

**Source:** `agents/simulator_node.py`

### Inputs

| Field | Type | Source | Description |
|---|---|---|---|
| `causal_dag` | `CausalDAG` | `state_node` | Nodes + directed edges with strength and confidence |
| `state_vector` | `OperativeState` | `state_node` | Current field state |
| `pomdp` | `POOMDPResult` | `strategy_node` | `optimal_action` for the comparison rollout |
| `action_override` | `Optional[str]` | CLI `--action` flag | If set, used as the "actual" action |

### Outputs — two `SimulationOutput` objects

`simulation_actual` (outcome action) and `simulation_optimal` (POMDP-prescribed action):

| Field | Type | Description |
|---|---|---|
| `action` | `str` | Action this simulation evaluated |
| `p_mission_success` | `float` [0,1] | Fraction of rollouts reaching success |
| `p_cover_blown` | `float` [0,1] | Fraction where cover_integrity falls below threshold |
| `ci_low` / `ci_high` | `float` | 95% Wilson confidence interval bounds |
| `n_rollouts` | `int` | Number of Monte Carlo samples |
| `mode_outcome` | `str` | Modal terminal outcome label |
| `key_lever` | `Optional[str]` | Highest-impact causal edge (format: `cause→effect`) |

### Mathematical Formulation

**Rollout:** Vectorised Bernoulli sampling through the `CausalDAG`. At each edge (cause → effect) with strength p, the effect node activates with probability p if the cause is active:

```
effect_active ~ Bernoulli(strength · cause_active)
```

This propagates from the action node through the DAG to outcome nodes.

**Mission success condition:** Outcome nodes associated with mission objectives all active.

**Cover blown condition:** `cover_integrity` component of operative state falls below a threshold (typically 2.0 out of 10).

**Wilson confidence interval** for a proportion p̂ over n rollouts:

```
CI = (p̂ + z²/2n ± z·√(p̂(1−p̂)/n + z²/4n²)) / (1 + z²/n)
```

where z = 1.96 for 95% coverage.

**Key lever identification:** The causal edge whose removal (strength → 0) causes the largest drop in `p_mission_success` under the optimal action.

---

## 9. Career MDP — Finite-Horizon Backward Induction (Mode 2: Forward Projection)

**Question answered:** What is the optimal sequence of career-level decisions across real 2025–2026 events, and how does it compare to a canonical conservative extrapolation?

**Source:** `optimisation/career_mdp.py`, consumed by `agents/forward_projection_node.py`

**Why finite-horizon MDP, not POMDP:** The single-turning-point POMDP is appropriate for field-level uncertainty. For a multi-year career arc, the right abstraction is coarser — macro-actions (career postures) chosen in response to macro-events. The state space is small (5 absorbing status values × event index) and dynamics are well-modelled by `MacroAction.transition_probs`. Scaling PBVI to a decade of decisions is computationally infeasible and conceptually mismatched.

### Inputs

| Field | Type | Source | Description |
|---|---|---|---|
| `macro_arc` | `MacroArc` | `forward_state_node` | Events, macro-actions, initial objective and status |
| `weights` | `LongHorizonWeights` | `CharacterProfile` | Per-operative weights for 5d objective collapse |

### Outputs — `(predicted, prescribed)` `CareerTrajectory` pair

Each `CareerTrajectory`:

| Field | Type | Description |
|---|---|---|
| `label` | `"predicted"` or `"prescribed"` | Trajectory type |
| `steps` | `list[CareerStep]` | Per-event: chosen action, status, objective (with MC CI bands) |
| `final_status` | `CareerTerminalStatus` | `active \| killed \| blown \| extracted \| retired` |
| `final_objective` | `LongHorizonObjective` | 5d objective at horizon |
| `scalar_score` | `float` | Cumulative weighted reward (MDP convention, not clipped) |
| `n_rollouts` | `int` | MC rollouts used for CI bands |

### Mathematical Formulation

**State:** (event_index i, career_status s) where s ∈ {active, killed, blown, extracted, retired}

**Reward function** (scalar collapse of 5d objective delta):

```
r(a) = w_yield · Δmission_yield
     + w_impact · Δstrategic_impact
     − w_cost · Δpersonal_cost
     + w_network · Δnetwork_durability
     − w_attr · Δattribution_risk
```

Sign convention: `personal_cost` and `attribution_risk` are penalised (lower is better); the other three are rewarded. Weights are from `LongHorizonWeights` (default sum = 1.0, validated).

**Backward induction** (over N events in chronological order):

```
V(N, s) = 0   for all s                          [terminal]
V(i, s) = max_{a ∈ A(i,s)}  r(a) + Σ_{s'} P(s'|a) · V(i+1, s')
```

where A(i, s) = legal macro-actions at event i given status s (`MacroAction.requires_status`).

**Two trajectories** from the same solved arc:
- **Predicted:** greedy on a conservative default policy (prefer `maintain_lyari_cover` → `mentor_rizwan_in_field` → first legal action) — represents the operative's canonical extrapolation without oracle guidance.
- **Prescribed:** greedy on the optimal MDP policy from backward induction.

**Monte Carlo CI bands:** 1500 rollouts per trajectory, sampling status transitions from `MacroAction.transition_probs`. Per-step CI uses the 5th/95th percentile across rollouts.

---

## 10. Arc Chain — Rewrite-Arc Analysis (Mode 3: Counterfactual Rewrite)

**Question answered:** At every turning point across films 1+2, what was the suboptimal choice, what should have been done, and what is the cumulative Q-delta?

**Source:** `optimisation/arc_chain.py`, consumed by `agents/arc_rewrite_node.py`

### Mechanism

For each turning point in chronological order (film, act, id):

1. Invoke the full `oracle_graph` (POMDP + all supporting algorithms)
2. Read `pomdp.action_values` to obtain Q(b, a) for every action
3. Read the `outcome` JSON to find the actually-taken action
4. Compute per-TP Q-delta: `q_delta_i = Q(b, prescribed) − Q(b, actual)`
5. Accumulate: `cumulative_q_delta = Σ q_delta_i`

### State Uplift Heuristic

The prescribed final `OperativeState` is derived from the baseline (last `state_by_act` entry) plus a Q-delta-weighted uplift:

```
scale = clip(cumulative_q_delta × 0.3, min=−2.0, max=+2.0)

cover_integrity    += 0.5 × scale
trust_capital      += 0.4 × scale
intelligence_depth += 1.0 × scale
network_strength   += 0.4 × scale
exposure_risk      −= 0.6 × scale     [lower is better]
```

### 5d Objective Delta Heuristic

```
s = clip(cumulative_q_delta × 0.25, min=−3.0, max=+3.0)

mission_yield      = +1.0 × s
strategic_impact   = +0.7 × s
personal_cost      = −0.4 × s     [reduction is good]
network_durability = +0.5 × s
attribution_risk   = −0.3 × s     [reduction is good]
```

### Outputs — `ArcRewrite`

| Field | Type | Description |
|---|---|---|
| `steps` | `list[ArcStep]` | Per-TP: actual action, prescribed action, Q-values, delta, state handoff |
| `cumulative_q_delta` | `float` | Total Q-value gain if all prescribed actions had been taken |
| `final_state_baseline` | `OperativeState` | Actual end state from canon |
| `final_state_prescribed` | `OperativeState` | Counterfactual end state |
| `objective_delta` | `ObjectiveDelta` | 5d career-level improvement estimate |

**Self-consistency guarantee:** Both actual and prescribed Q-values come from the same solver invocation. The comparison is internally consistent — we are not mixing ground truths from different oracles.

---

## Algorithm Summary Table

| Algorithm | Mode | Node | Complexity | Key Output |
|---|---|---|---|---|
| PBVI / POMDP | Turning-point | `strategy_node` | O(|S|²·|A|·|O|·iterations) | `optimal_action`, `action_values` |
| Stackelberg | Turning-point | `adversary_node` | O(\|A\|³) backward induction | `leader_action`, `commitment_value` |
| HMM (Viterbi+FB) | Turning-point | `belief_node` | O(|Q|²·T) per actor | `belief_gaps`, mole alerts |
| Shapley values | Turning-point | `coalition_node` | Exact O(N·2^N), MC O(n·N) | `values`, `defection_incentives` |
| VoI (entropy) | Turning-point | `voi_node` | O(|targets|) | `voi_result` ranked priorities |
| SNA (NetworkX) | Turning-point | `intel_network_node` | O(V·E) centrality | `centrality`, `threat_scores` |
| CPM + PERT | Turning-point | `critical_path_node` | O(V+E) topo sort | `critical_path`, `days_saved` |
| Monte Carlo | Turning-point | `simulator_node` | O(n_rollouts·\|edges\|) | `p_mission_success` delta |
| Career MDP | Forward (Mode 2) | `forward_projection_node` | O(N·\|A\|·\|S\|) | `predicted`/`prescribed` trajectories |
| Arc Chain | Rewrite (Mode 3) | `arc_rewrite_node` | O(n_TPs × oracle_graph) | `cumulative_q_delta`, `ArcRewrite` |
