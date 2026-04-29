# Oracle briefing — `hamza` / `isi-capture-torture`

> ISI captures Hamza following Major Iqbal's death. He is held in an ISI facility and subjected to enhanced interrogation. ISI knows he is an Indian operative — the question is what he will give them: other RAW assets in Pakistan, the full architecture of the Film 1-2 operations, information about Rizwan Shah. The turning point: how does Hamza resist? And what does he sacrifice to protect the network? The session is also a character arc endpoint — this is what 13 years of deep cover costs in its most concrete form.

## POMDP — Optimal Policy

- **Optimal action:** `resist_completely_reveal_nothing`
- V(b): `5.929`
- P(mission success): `50.0%`
- P(cover intact): `100.0%`

| Action | Q(b, a) |
|---|---|
| `resist_completely_reveal_nothing` ← OPTIMAL | 5.929 |
| `negotiate_prisoner_exchange_reveal_sanyal_channel` | 5.533 |
| `emergency_signal_rizwan_rescue_attempt` | 5.533 |
| `offer_limited_outdated_intelligence` | 5.333 |
| `feign_cooperation_provide_false_intel` | 5.333 |

## Critical Path (CPM/PERT)

- Path: `survive_long_enough_for_sanyal_action`
- Total: **20 d**  →  Optimal: **12 d**  (save 8 d)
- Bottleneck: `survive_long_enough_for_sanyal_action`
- Parallelisable: `protect_rizwan_identity` ‖ `protect_delhi_network`, `survive_long_enough_for_sanyal_action` ‖ `protect_rizwan_identity`, `survive_long_enough_for_sanyal_action` ‖ `protect_delhi_network`

## Value of Information

- Total entropy: **1.77 bits**
- Top target: `Leverage material on ISI DG Shahnawaz (Israel leak videos) — Sanyal holds this`

| Rank | Target | VoI (bits) | Effort | Recommendation |
|---|---|---|---|---|
| 1 | Leverage material on ISI DG Shahnawaz (Israel leak videos) — Sanyal holds this | 1.75 | 0.5 | High priority — gather immediately via: negotiate_prisoner_exchange_reveal_sanyal_channel |
| 2 | What ISI already knows about Hamza's operations — calibrate resistance strategy | 1.59 | 6.0 | Low priority — defer; access difficulty (6.0) outweighs VoI (1.59 bits) |

## Stackelberg Equilibrium

- Handler commits to: `resist_completely_reveal_nothing`
- Operative best response: `resist_completely_reveal_nothing`
- Adversary counter: `isi_director_general_shahnawaz: feign_cooperation_provide_false_intel`
- Indian payoff: `0.690`
- Commitment value vs Nash: `+0.163`

## Shapley Values — Asset Coalition

| Actor | φ | Defection incentive |
|---|---|---|
| hamza | 1.900 | 0.000 |

## Monte Carlo Simulation

- Rollouts per arm: 2000
- Actual (resist_completely_reveal_nothing): P(success)=**100.0%**  [99.8%–100.0%]
- Optimal (resist_completely_reveal_nothing): P(success)=**100.0%**  [99.8%–100.0%]
- Δ = **+0.0%** if optimal path taken
- Key causal lever: `resist_completely_reveal_nothing → rizwan_identity_protected  (p=0.85)`

## Threat Scores (SNA)

| Actor | Score | Betweenness | Eigenvector | High-threat |
|---|---|---|---|---|
| isi_director_general_shahnawaz | 4.500 | 0.000 | 0.000 | no |
| isi_interrogation_team | 4.000 | 0.000 | 0.000 | no |

## Warnings

- adversary_node: no high_threat_actors set — using all adversaries with capability >= 7.0 (['isi_interrogation_team', 'isi_director_general_shahnawaz'])
- adversary_node: multi-adversary Stackelberg over ['isi_interrogation_team', 'isi_director_general_shahnawaz']
- narrator_node: ANTHROPIC_API_KEY not set — using template fallback
