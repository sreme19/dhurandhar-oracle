# dhurandhar-oracle — Steering Document

## Mission

Build a multi-agent AI system for Indian intelligence operatives in the Dhurandhar universe.
Given a character and a turning point in their mission, the oracle computes:

1. The **optimal next action** (POMDP policy over belief state)
2. **What could have been done faster** (CPM/PERT critical path analysis)
3. **Which intelligence to gather next** (Value of Information ranking)
4. **How adversaries will respond** (Stackelberg equilibrium — leader-follower)
5. **Who is hiding something** (HMM belief gap — mole detection)
6. **Who is the most valuable asset** (Shapley values over handler/asset coalition)
7. **Mission success probability** (Monte Carlo simulation)

## Hard Constraints

- **Indian-side characters only.** The oracle refuses queries for Pakistani adversaries
  (Rehman Dakait, Jameel Jamali, etc.). Those characters exist only as adversary models.
  Check `character.side == "indian"` before running the pipeline.
- The `side` field is validated at CLI entry and at `state_node` load time.

## Architecture Decisions

### Why POMDP, not MDP?
got-oracle used MDP (fully observable state). Intelligence operations are the canonical
POMDP domain — the operative never knows the full world state. Is the handler compromised?
Does Dakait suspect Hamza? POMDP planning operates over a *belief state* (a probability
distribution over possible world states), producing policies that account for uncertainty
in what the operative knows. This is the central algorithmic step up from got-oracle.

We use Point-Based Value Iteration (PBVI) — tractable for moderate state spaces and
well-suited to the discrete action/observation model of intelligence ops.

### Why Stackelberg, not CFR?
got-oracle used CFR (Counterfactual Regret Minimisation) for symmetric Nash equilibrium —
all adversaries act simultaneously without knowing each other's plans.

In Dhurandhar, the RAW handler *commits* to a strategy (orders) before the operative
acts, and the operative acts before the target can respond. This is a sequential
leader-follower (Stackelberg) game, not a symmetric simultaneous game. Stackelberg
equilibrium captures the value of *commitment* — the handler's ability to credibly
pre-commit to a strategy changes the operative's optimal response.

### Why Critical Path Method (CPM) + PERT?
The "what could Hamza have done faster" question is literally a project scheduling problem.
We model the mission as a task network (DAG) with estimated durations (optimistic,
most-likely, pessimistic — PERT three-point estimation). CPM identifies:
- The **critical path** — tasks that directly determine total mission duration
- **Slack** — how much each non-critical task can slip without delaying the mission
- **Parallelisation opportunities** — tasks that have no dependency on each other

### Why Value of Information (VoI)?
"What should Rizwan do next?" is partly answered by POMDP, but the
*information-gathering* sub-question is answered by VoI. VoI measures how many bits
of entropy each intelligence target would reduce from the mission's current belief state.
High-VoI targets should be prioritised; low-VoI targets can wait.
VoI = H(belief_state) - E[H(belief_state | observe target)]

### Reused from got-oracle
- **HMM** (Viterbi + Baum-Welch): mole detection — infer hidden loyalty states from
  observable actions. Same algorithm, new domain.
- **Shapley values**: asset contribution — who is most valuable to the handler network?
  Same algorithm, new domain.
- **SNA / NetworkX**: Karachi criminal-political power network, same as GoT alliance graph.
- **Monte Carlo**: mission success + cover integrity simulation, same as survival rollouts.
- **LangGraph**: same StateGraph topology — parallel fan-out, typed state, checkpointing.

## Data Model

### Turning Point
The fundamental query unit. One per key scene/decision across both films.
Fields: `operative`, `film` (1|2), `act` (1|2|3), `state_vector`, `available_actions`,
`mission_tasks` (for CPM), `causal_dag`, `adversaries`, `alliance_snapshot`,
`intelligence_targets` (for VoI), `belief_state` (initial POMDP distribution).

### Character Profile
`side: Literal["indian", "pakistani", "unknown"]` gates access.
Includes `cover_identity` for operatives running under false names.
Includes `real_life_inspiration` for documentary accuracy.

### OperativeState (5-dimensional, replaces PlayerState)
| Dimension | Meaning |
|---|---|
| `cover_integrity` | How intact is the operative's false identity |
| `trust_capital` | Trust built with target criminal/political network |
| `intelligence_depth` | Quality and quantity of intel gathered so far |
| `network_strength` | Quality of handler/asset support network |
| `exposure_risk` | How close the operative is to being discovered |

## Project Series Context

| Project | New techniques introduced |
|---|---|
| ipl-oracle | MILP, MDP, Monte Carlo, Bayesian networks, LangChain |
| got-oracle | CFR, HMM, Prospect Theory, Shapley values, SNA, LangGraph |
| **dhurandhar-oracle** | **POMDP (PBVI), CPM/PERT, Value of Information, Stackelberg** |

## Open Data Questions (grounding — resolve before implementation)

<!-- TODO: confirm with user after watching both films -->
1. Is "Rizwan Shah" the correct name for the film-2 operative, and what is his role?
2. Is Hamza's Karachi cover identity a local criminal, or does he have a different alias?
3. Is Mohammed Aalam (the handler) revealed to be compromised by end of film 1?
4. Does Ajay Sanyal survive both films, or is he a turning-point casualty?
5. What is the chronological span of the mission in film 1? (weeks / months / years)
6. Does film 2 continue directly from film 1's post-credits, or is there a time jump?
7. Is "Dhurandhar" the code name for Hamza, or the name of the overall RAW operation?
8. Is SP Choudhary Aslam (Sanjay Dutt) an obstacle, an ally, or a double-agent?
9. What is the specific intelligence objective — disrupt Dakait–Jamali connection, or something broader?
10. Are there any Indian-side characters in film 2 not present in film 1?
