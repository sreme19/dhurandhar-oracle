# Oracle briefing — `ajay_sanyal` / `galwan-china-kinetic-clash`

> Night of June 15-16, 2020. Following weeks of India-China military disengagement talks in eastern Ladakh (Pangong Tso, Galwan Valley, Hot Springs — 5 friction points), Indian Army's 16 Bihar Regiment CO Colonel Santosh Babu leads a patrol to verify Chinese withdrawal per the June 6 de-escalation agreement. The Chinese have not withdrawn — they have built new structures. What follows is a hand-to-hand combat at 14,000 feet in sub-zero temperatures: rocks, iron rods wrapped in barbed wire, nail-studded clubs. 20 Indian soldiers killed including Colonel Santosh Babu — the highest Indian military death toll in a China clash since 1967. Chinese casualties: officially 4 (China's first admission of any LOC casualties since 1979); credible estimates suggest 35-45. NSA Ajay Sanyal must now manage India's strategic response: the China threat is no longer a Doklam-style standoff — it is kinetic, lethal, and has breached a half-century of relative restraint.

## POMDP — Optimal Policy

- **Optimal action:** `design_economic_military_response_package`
- V(b): `8.511`
- P(mission success): `52.5%`
- P(cover intact): `100.0%`

| Action | Q(b, a) |
|---|---|
| `design_economic_military_response_package` ← OPTIMAL | 8.511 |
| `assess_pla_intent_galwan_strategic_vs_tactical` | 8.118 |
| `map_china_pakistan_two_front_coordination` | 8.118 |
| `identify_pla_galwan_authorisation_chain` | 7.918 |
| `assess_nuclear_dimension_china_confrontation` | 7.518 |

## Critical Path (CPM/PERT)

- Path: `pla_intent_assess` → `economic_response_design`
- Total: **41 d**  →  Optimal: **24 d**  (save 16 d)
- Bottleneck: `economic_response_design`
- Parallelisable: `pla_intent_assess` ‖ `china_pakistan_coordination_galwan`, `pla_intent_assess` ‖ `pla_casualty_real_count`

## Value of Information

- Total entropy: **1.76 bits**
- Top target: `Real PLA casualty count from Galwan — intelligence leverage for future negotiations and domestic narrative management`

| Rank | Target | VoI (bits) | Effort | Recommendation |
|---|---|---|---|---|
| 1 | Real PLA casualty count from Galwan — intelligence leverage for future negotiations and domestic narrative management | 1.50 | 8.5 | Low priority — defer; access difficulty (8.5) outweighs VoI (1.50 bits) |
| 2 | Whether Galwan action was authorised at Politburo Standing Committee level — determines sustained vs. accidental escalation | 1.73 | 10.0 | Low priority — defer; access difficulty (10.0) outweighs VoI (1.73 bits) |
| 3 | Evidence of PLA-ISI coordination on simultaneous two-front pressure during India's COVID distraction | 1.59 | 9.5 | Low priority — defer; access difficulty (9.5) outweighs VoI (1.59 bits) |

## Stackelberg Equilibrium

- Handler commits to: `design_economic_military_response_package`
- Operative best response: `design_economic_military_response_package`
- Adversary counter: `pla_western_theatre_command_galwan: assess_nuclear_dimension_china_confrontation`
- Indian payoff: `0.629`
- Commitment value vs Nash: `+0.187`

## Shapley Values — Asset Coalition

| Actor | φ | Defection incentive |
|---|---|---|
| narendra_modi | 0.980 | 0.000 |
| pakistan | 0.880 | 0.000 |

## Monte Carlo Simulation

- Rollouts per arm: 2000
- Actual (design_economic_military_response_package): P(success)=**100.0%**  [99.8%–100.0%]
- Optimal (design_economic_military_response_package): P(success)=**100.0%**  [99.8%–100.0%]
- Δ = **+0.0%** if optimal path taken
- Key causal lever: `design_economic_military_response_package → india_economic_response_imposed  (p=0.90)`

## Threat Scores (SNA)

| Actor | Score | Betweenness | Eigenvector | High-threat |
|---|---|---|---|---|
| pla_western_theatre_command_galwan | 5.000 | 0.000 | 0.000 | no |
| isi_two_front_galwan_exploitation | 4.250 | 0.000 | 0.000 | no |

## Warnings

- state_node: using char.state_by_act['film4_act1'] over TP state_vector
- adversary_node: no high_threat_actors set — using all adversaries with capability >= 7.0 (['pla_western_theatre_command_galwan', 'isi_two_front_galwan_exploitation'])
- adversary_node: multi-adversary Stackelberg over ['pla_western_theatre_command_galwan', 'isi_two_front_galwan_exploitation']
- narrator_node: ANTHROPIC_API_KEY not set — using template fallback
