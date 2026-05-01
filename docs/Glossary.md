# Glossary

Domain terms, algorithm shorthand, and intelligence-operations concepts used throughout the documentation and codebase.

---

## A

**Action override (`--action`)**
CLI flag that forces the oracle to evaluate a specific action instead of finding the POMDP-optimal one. Used for counterfactual analysis: "what would have happened if Hamza had done X instead?"

**Alliance edge (`AllianceEdge`)**
A directed relationship between two actors in the network snapshot. Carries `strength` [0,1] and `betrayal_history`. Used by both SNA (centrality) and Shapley (coalition value).

**Arc chain**
The Mode 3 (rewrite-arc) algorithm. Chains the full turning-point oracle across every turning point in an operative's arc, comparing actual Q-values to prescribed Q-values and accumulating a cumulative Q-delta. See [Technical Reference § Arc Chain](Technical-Reference).

**Arc rewrite**
Mode 3 of the oracle. Answers: "What should the operative have done differently across films 1 and 2, and what is the cumulative gain?" Produces an `ArcRewrite` output. CLI command: `rewrite-arc`.

**Attribution risk**
One of the five career-arc objective dimensions (`LongHorizonObjective`). Measures the risk that an operation or operative is publicly attributed to India. Lower is better. Penalised in the scalar score formula.

---

## B

**Backward induction**
The solution method for Stackelberg games and the finite-horizon career MDP. Starts from the terminal state and computes optimal values backwards to the initial state. Guarantees subgame-perfect equilibrium in Stackelberg; optimal policy in the career MDP.

**Belief gap (`BeliefGap`)**
The discrepancy between what the operative *believes* about an actor's loyalty state and what the HMM *infers* from observable actions. A high gap (> 0.6) combined with a high defection incentive (> 0.5) triggers a mole alert.

**Belief state**
A probability distribution over possible world states. The central concept in POMDP planning. Represented as `dict[str, float]` where keys are world state IDs and values sum to 1.0. The operative never observes world state directly — they reason over the belief state.

**Belief state value V(b)**
The expected long-term reward at the current belief state under the optimal POMDP policy. Reported as `pomdp.belief_state_value`. Higher is better.

**PBVI (Point-Based Value Iteration)**
The POMDP solver used in `dhurandhar-oracle`. An approximate algorithm that maintains a set of α-vectors (hyperplanes over belief space) and backs up value at a fixed set of belief points per iteration. More tractable than exact POMDP solvers for moderate state spaces. See [Technical Reference § POMDP](Technical-Reference).

---

## C

**Causal DAG (`CausalDAG`)**
A directed acyclic graph where nodes are events/outcomes and edges carry conditional probability strengths. Used by the POMDP (transition model) and Monte Carlo (rollout propagation). Not to be confused with the alliance network.

**Career MDP**
The finite-horizon Markov Decision Process used in Mode 2 (Forward Projection). State = (event_index, career_status). Actions = macro-actions. Solved by backward induction. Distinct from the turning-point POMDP because the state is fully observable at the career level.

**Career status (`CareerTerminalStatus`)**
The operative's career-level status: `active | killed | blown | extracted | retired`. Once non-active, the status is absorbing in the career MDP (no further reward accrues unless a special action with `requires_status` permits it).

**Centrality**
Graph-theoretic measures of node importance. `dhurandhar-oracle` computes three: betweenness (fraction of shortest paths through a node), eigenvector (importance proportional to neighbours' importance), and clustering coefficient (local triangle density). Combined with capability to produce threat scores.

**Commitment value**
`StackelbergResult.commitment_value` = V(Stackelberg) − V(Nash). The marginal gain to India from the handler's ability to credibly pre-commit to a strategy. A positive value means sequential leadership is strategically advantageous at this turning point.

**Community detection**
Grouping of network actors into densely-connected clusters. Uses the Louvain algorithm (maximises modularity Q). Informs which factions the operative can target or exploit.

**Cover integrity**
Dimension 1 of `OperativeState`. How intact the operative's false identity is. Scale [0, 10]; higher is better. Falling near 0 means imminent exposure. Many mission tasks have `requires_cover=True` — they cannot proceed safely if cover is compromised.

**Cover identity**
The false name and persona an Indian-side operative uses in the field. Stored as `CharacterProfile.cover_identity`. Example: Hamza Ali Mazari is the cover identity of Jaskirat Singh Rangi.

**CPM (Critical Path Method)**
A project scheduling algorithm that identifies the sequence of tasks (the critical path) that directly determines total mission duration. Tasks on the critical path have zero slack — any delay directly delays the mission. See [Technical Reference § CPM/PERT](Technical-Reference).

---

## D

**Defection incentive**
`ShapleyResult.defection_incentives[actor]` — the normalised value an asset would receive by leaving the Indian-side coalition and acting alone. High defection incentive (> 0.5) signals a potential loyalty risk.

**DhurandharState**
The single shared `TypedDict` that all LangGraph nodes read from and write to. The complete key contract is in [Multi-Agent System](Multi-Agent-System). Parallel nodes use `Annotated[list, operator.add]` reducers for `errors` and `warnings`.

---

## E

**Emission probability**
In the HMM, B[i,k] = P(observation k | hidden state i). Describes how likely each observable action is given a particular loyalty state. Estimated from `AdversaryModel.observable_actions`.

**Exposure risk**
Dimension 5 of `OperativeState`. How close the operative is to being discovered. Scale [0, 10]; **lower is better**. The only OperativeState dimension where the direction is reversed.

---

## F

**Fan-in**
LangGraph topology term. A node that waits for multiple upstream nodes to complete before executing. In `oracle_graph`, `belief_node` is the fan-in after the parallel `intel_network_node` / `coalition_node` branches.

**Fan-out**
LangGraph topology term. A node with multiple outgoing edges that triggers downstream nodes in parallel. In `oracle_graph`, `state_node` fans out to `intel_network_node` and `coalition_node` simultaneously.

**Film numbering**
- Film 1: Dhurandhar 1 (Karachi/Lyari arc, 26/11 intelligence gathering)
- Film 2: Dhurandhar 2 (Punjab narco-jihad arc, Rizwan Shah introduction)
- Films 3–4: Future continuations (planned)

**Forward projection**
Mode 2 of the oracle. Projects an Indian-side operative's career through real 2025–2026 events and compares a conservative extrapolation (predicted) against the oracle-optimal policy (prescribed). CLI command: `project-forward`.

---

## G

**Graph (LangGraph StateGraph)**
A compiled execution plan that routes a shared state object through agent nodes. `dhurandhar-oracle` has three: `oracle_graph` (turning-point), `forward_graph` (forward), `rewrite_graph` (rewrite). See [Multi-Agent System](Multi-Agent-System).

---

## H

**Handler**
The RAW officer managing the operative from the Indian side. In the Stackelberg model, the handler is the *leader* — commits to a strategy first.

**Hidden Markov Model (HMM)**
A probabilistic model where the system transitions through hidden (unobservable) states emitting observable outputs. Used to infer an actor's hidden loyalty state sequence from their observable action history. See [Technical Reference § HMM](Technical-Reference).

**HMM hidden states**
The loyalty states the HMM infers: `loyal | wavering | compromised | turned`. "Turned" means the actor has flipped to the adversary side.

---

## I

**Indian-side gate**
The access control that prevents Pakistani-side characters from being queried as oracle protagonists. Enforced at `state_node`, `forward_state_node`, and `arc_rewrite_node`. There is no bypass flag. Pakistani characters exist only as `AdversaryModel` objects inside algorithm inputs.

**Intelligence depth**
Dimension 3 of `OperativeState`. Quality and quantity of intelligence gathered so far. Higher is better.

**Intelligence target (`IntelligenceTarget`)**
A piece of information the operative could gather. Has `current_entropy` (uncertainty), `mission_relevance`, `access_difficulty`, and `access_actions`. Used by VoI to rank collection priorities.

---

## L

**LangGraph**
The orchestration framework used to define and execute the multi-agent pipeline. Each node is a Python function over `DhurandharState`. LangGraph handles parallel fan-out, conditional routing, and state merging.

**Leader (Stackelberg)**
The first mover in a Stackelberg game. In `dhurandhar-oracle`, the RAW handler commits to a strategy before the operative and adversary respond. This commitment is the source of `commitment_value`.

**Long-horizon objective (`LongHorizonObjective`)**
The 5-dimensional career-arc objective vector: `mission_yield`, `strategic_impact`, `personal_cost`, `network_durability`, `attribution_risk`. Distinct from the per-turning-point `OperativeState`. Used exclusively in Modes 2 and 3.

**Loss aversion (λ)**
Kahneman-Tversky Prospect Theory parameter in `ProspectParams`. Default λ = 2.25, meaning losses weigh approximately 2.25× more than equivalent gains in the adversary's decision function.

**Louvain algorithm**
Community detection algorithm maximising graph modularity. Used by SNA to partition the Karachi criminal-political network into factions.

---

## M

**Macro-action (`MacroAction`)**
A coarse career-level decision the operative can make in response to a real-world event (Mode 2). Examples: `pivot_offshore`, `deep_strike_response`, `mentor_rizwan_in_field`. Each has an `objective_delta` and `transition_probs`.

**Macro-arc (`MacroArc`)**
The post-D2 career arc data for one operative. Contains the list of real-world events and available macro-actions. Loaded from `data/post_d2_arc/<operative>.json`. Required for Mode 2.

**Mole alert**
Triggered when `defection_incentive > 0.5` AND `belief_gap > 0.6` for an actor. Indicates the operative should treat this asset as potentially compromised.

**Mission yield**
Dimension 1 of `LongHorizonObjective`. Cumulative actionable intelligence and operational success across the operative's career. Higher is better.

**Monte Carlo simulation**
Mode 1 algorithm. Runs vectorised Bernoulli rollouts through the `CausalDAG` to estimate `p_mission_success` and `p_cover_blown` under the actual and optimal actions, with Wilson confidence intervals. See [Technical Reference § Monte Carlo](Technical-Reference).

---

## N

**Narrator node**
The final node in all three pipelines. Calls the Claude API (`claude-sonnet-4-6` by default) to synthesise all quantitative outputs into a structured war-room briefing. Falls back to a Rich template if `ANTHROPIC_API_KEY` is not set.

**Network durability**
Dimension 4 of `LongHorizonObjective`. How well the handler/asset network survives across the operative's career. Higher is better.

---

## O

**Objective delta (`ObjectiveDelta`)**
A signed 5-dimensional change vector applied to a `LongHorizonObjective`. Can be negative (reduces personal_cost or attribution_risk, which is beneficial). No [0,10] bounds — values can be any float.

**Operative**
An Indian-side intelligence officer who can be queried by the oracle. Must have `side="indian"` in their `CharacterProfile`. See [Schema Reference § CharacterProfile](Schema-Reference).

**OperativeState**
See **Field-state vector** above and [Schema Reference § OperativeState](Schema-Reference).

**oracle_graph**
The compiled LangGraph StateGraph for Mode 1 (turning-point). The only graph that involves POMDP, Stackelberg, HMM, Shapley, VoI, SNA, CPM, and Monte Carlo nodes.

---

## P

**PBVI**
See **Point-Based Value Iteration** above.

**PERT (Program Evaluation and Review Technique)**
Three-point duration estimation for mission tasks: `(O + 4M + P) / 6`. Provides expected duration and variance from optimistic (O), most-likely (M), and pessimistic (P) estimates. Used with CPM.

**POMDP (Partially Observable Markov Decision Process)**
The decision-theoretic framework for planning under state uncertainty. The operative has a *belief state* (probability distribution over world states) rather than direct world-state observation. The oracle's central algorithm for turning-point mode. Solved via PBVI.

**Policy**
A mapping from belief states (or belief hashes) to optimal actions. The POMDP solver produces a policy valid for beliefs near the current one, stored as `pomdp.policy`.

**Prescribed trajectory**
In Mode 2 (forward), the oracle-optimal career trajectory produced by backward induction on the career MDP. Contrasted with the **predicted trajectory** (conservative canonical extrapolation).

**Predicted trajectory**
In Mode 2 (forward), the conservative default trajectory assuming the operative continues their current posture (prefers `maintain_lyari_cover` → `mentor_rizwan_in_field` → first legal action).

**Prospect Theory**
Behavioural economics model (Kahneman-Tversky) for how adversaries evaluate gains and losses asymmetrically. Parameters in `ProspectParams`. Used to modulate adversary payoffs in the Stackelberg model.

---

## Q

**Q-value Q(b, a)**
The expected long-term reward of taking action a at belief state b, under the optimal POMDP policy thereafter. Reported in `pomdp.action_values`. The optimal action is `argmax_a Q(b, a)`.

**Q-delta**
In Mode 3 (arc rewrite), the difference `Q(b, prescribed) − Q(b, actual)` at a single turning point. Accumulated across all turning points to produce `arc_rewrite.cumulative_q_delta`.

---

## R

**RAW (Research and Analysis Wing)**
India's external intelligence agency. The handler chain in `dhurandhar-oracle` runs through RAW/IB officers.

**Real-world correlation**
`TurningPoint.real_world_correlation` — a dictionary of grounded real-world event data attached to a turning point for documentary accuracy. Passed to `narrator_node` for Claude briefing context.

**Reducer (LangGraph)**
A function applied when multiple nodes write to the same state key concurrently. `dhurandhar-oracle` uses `Annotated[list, operator.add]` for `errors` and `warnings`, safely merging concurrent list appends from the parallel `intel_network_node` / `coalition_node` branches.

---

## S

**Scalar score**
The single-number summary of a career trajectory in Mode 2. Computed as the cumulative per-step weighted reward: `Σ weights · objective_delta` across all chosen macro-actions. Uses the MDP's reward function directly (not the [0,10]-clipped rendered objective), so it is the meaningful optimality headline.

**Shapley value (φᵢ)**
The fair contribution of asset i to the Indian-side coalition value, averaging marginal contributions over all possible coalition orderings. See [Technical Reference § Shapley](Technical-Reference).

**Side gate**
See **Indian-side gate**.

**Slack (CPM)**
`LS(task) − ES(task)` — how many days a task can slip without delaying the mission. Tasks with zero slack are on the critical path. Tasks with positive slack can be deprioritised.

**SNA (Social Network Analysis)**
The analysis of the Karachi criminal-political network using graph-theoretic centrality measures. Identifies power brokers (high betweenness), influential nodes (high eigenvector), and community structure (Louvain). See [Technical Reference § SNA](Technical-Reference).

**Speculative flag**
If `CharacterProfile.is_speculative_real_figure=True`, Mode 2 forward projections and narratives are prefixed with `[SPECULATIVE — projection of a real public figure]`.

**Stackelberg equilibrium**
A subgame-perfect Nash equilibrium in a sequential (leader-follower) game. The handler commits first, operative responds, adversary counter-responds. Solved by backward induction. See [Technical Reference § Stackelberg](Technical-Reference).

**State vector**
See `OperativeState` — the 5-dimensional turning-point field state. Not to be confused with `LongHorizonObjective` (career-level state) or `initial_belief_state` (POMDP belief).

---

## T

**Threat score**
Composite measure per actor: `0.5 × capability + 0.3 × betweenness + 0.2 × eigenvector`. Actors above the high-threat threshold are passed to `belief_node` for HMM analysis.

**Transition probability**
In the career MDP: `MacroAction.transition_probs[status]` — the probability of transitioning to each `CareerTerminalStatus` after taking this action. Must sum to 1.0.

**Trust capital**
Dimension 2 of `OperativeState`. Trust built with the target criminal/political network. Higher is better. Depleting trust capital forces the operative into riskier or lower-value actions.

**Turning point**
The fundamental query unit — a key decision moment in an operative's arc, anchored to a specific film and act. Contains the full computational payload (state vector, causal DAG, adversaries, mission tasks, belief state). See [Schema Reference § TurningPoint](Schema-Reference).

---

## V

**Value function V(b)**
In POMDP: the expected long-term reward starting from belief state b under the optimal policy. Represented as `max_α (α · b)` over a set of α-vectors. See [Technical Reference § POMDP](Technical-Reference).

**Value of Information (VoI)**
The expected reduction in uncertainty (measured in bits of entropy) from gathering a specific piece of intelligence. High VoI targets should be collected first. See [Technical Reference § VoI](Technical-Reference).

**Viterbi algorithm**
Dynamic programming algorithm that finds the most likely hidden state sequence in an HMM given an observation sequence. Used in `belief_node` to determine the most likely loyalty trajectory for each high-threat actor.

---

## W

**Wilson confidence interval**
The confidence interval used by `simulator_node` for Monte Carlo proportions. More accurate than the normal approximation for small n or extreme probabilities. Formula: `(p̂ + z²/2n ± z·√(p̂(1−p̂)/n + z²/4n²)) / (1 + z²/n)`.

**World state**
A discrete label for the operative's unobservable situation (e.g., `cover_intact_low_suspicion`, `cover_blown_handler_compromised`). The POMDP maintains a probability distribution over world states as the belief state.
