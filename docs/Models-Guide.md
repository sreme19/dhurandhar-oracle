# Models Guide (Beginner Friendly)

This page explains the core models used in `dhurandhar-oracle` in plain language.

If you are new to these concepts, start with the **What it answers** line for each model.

## Big Picture

At each turning point, the oracle asks:

1. What action should the operative take now?
2. What information is worth collecting first?
3. How might adversaries react?
4. Where did time get wasted?
5. How likely is success under different choices?

No single model can answer all of this. The system combines several models, each for a specific question.

## 1) POMDP (PBVI)

**What it answers:** "What is the best next action when I do not know the full state of the world?"

- **Why needed:** In intelligence work, the operative never has perfect visibility (who is loyal, who is suspicious, who is compromised).
- **Core idea:** Maintain a **belief state** (probability distribution over possible world states), then choose action with highest expected long-term value.
- **In this project:** `strategy_node` uses POMDP planning to rank actions and select an optimal one.
- **Input examples:** Current belief state, available actions, causal dynamics, adversary context.
- **Output examples:** Optimal action, action values, mission success probability, cover integrity probability.

## 2) Value of Information (VoI)

**What it answers:** "Which intelligence target should I gather first?"

- **Why needed:** Collection resources are limited. Not all intel is equally useful.
- **Core idea:** Prefer targets that reduce uncertainty the most per unit effort/risk.
- **In this project:** `voi_node` ranks intelligence targets by expected entropy reduction.
- **Input examples:** Belief state + target metadata (relevance, difficulty).
- **Output examples:** Priority list of intel targets and recommendations.

## 3) Stackelberg Game

**What it answers:** "If we commit to strategy X, how will the adversary respond?"

- **Why needed:** In many operations, one side commits first, others respond sequentially.
- **Core idea:** Leader commits, follower best-responds; evaluate equilibrium payoff.
- **In this project:** `adversary_node` models handler/operative/adversary interaction.
- **Output examples:** Predicted adversary counter, best response, commitment value.

## 4) CPM/PERT (Critical Path)

**What it answers:** "What could have been done faster?"

- **Why needed:** Operations can fail due to delay, not only bad tactical choice.
- **Core idea:** Build task dependency graph, compute critical path, slack, and parallelization opportunities.
- **In this project:** `critical_path_node` identifies bottlenecks and days potentially saved.
- **Output examples:** Critical path, bottleneck tasks, estimated time savings.

## 5) HMM (Hidden Markov Model)

**What it answers:** "Is someone's hidden loyalty state changing?"

- **Why needed:** True intent is hidden; we observe signals, not ground truth.
- **Core idea:** Infer hidden states from observed sequences.
- **In this project:** `belief_node` compares inferred hidden state vs operative belief to flag suspicious gaps.
- **Output examples:** Most-likely hidden state, belief gap alerts, possible mole risk.

## 6) Shapley Values

**What it answers:** "Which asset/ally contributes most to coalition value?"

- **Why needed:** Team operations need fair contribution attribution and defection risk awareness.
- **Core idea:** Compute each actor's average marginal contribution across coalition permutations.
- **In this project:** `coalition_node` scores assets and estimates defection incentives.
- **Output examples:** Contribution ranking and coalition stability signals.

## 7) Monte Carlo Simulation

**What it answers:** "How likely is mission success under actual vs optimal decisions?"

- **Why needed:** Deterministic answers hide uncertainty.
- **Core idea:** Run many stochastic rollouts through causal pathways; estimate outcome distributions.
- **In this project:** `simulator_node` compares actual action vs optimal action scenarios.
- **Output examples:** Success probabilities with confidence intervals and delta improvement.

## How These Models Work Together

- **State loading** sets the scenario.
- **Network + coalition analysis** enrich actor-level context.
- **Belief and VoI** decide uncertainty-reduction priorities.
- **Stackelberg + POMDP** select strategic action under adversarial uncertainty.
- **CPM/PERT** checks execution speed and bottlenecks.
- **Monte Carlo** stress-tests outcome uncertainty.
- **Narrator** explains results in readable war-room format.

## Common Misunderstandings

- **"One model gives the final truth."**  
  Not here. Outputs are synthesized across models.

- **"High confidence means real-world certainty."**  
  Confidence reflects available data quality, assumptions, and scenario encoding.

- **"Contextual sources prove fictional events."**  
  Contextual sources provide plausibility anchors, not direct proof of plot-specific events.

