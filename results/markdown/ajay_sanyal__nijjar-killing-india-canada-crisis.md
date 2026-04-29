# Oracle briefing — `ajay_sanyal` / `nijjar-killing-india-canada-crisis`

> June 18, 2023. Hardeep Singh Nijjar — president of the Guru Nanak Sikh Gurdwara in Surrey, British Columbia, Canadian citizen, designated 'individual terrorist' by India in 2020 for leading Sikhs for Justice's Khalistan Referendum campaign — is shot dead in the gurdwara parking lot by masked gunmen in a coordinated ambush. Three Canadian citizens of South Asian origin are later arrested. On September 18, 2023, Canadian PM Justin Trudeau tells Parliament there are 'credible allegations' of Indian government involvement. India expels 41 Canadian diplomats; Canada expels 6 Indian officials. The Five Eyes intelligence alliance is activated against India. NSA Ajay Sanyal must manage the most significant diplomatic-intelligence crisis India has faced with a Western democracy — while the operation itself remains officially unacknowledged.

## POMDP — Optimal Policy

- **Optimal action:** `assess_gchq_signals_intelligence_india_operations_depth`
- V(b): `1.905`
- P(mission success): `50.0%`
- P(cover intact): `100.0%`

| Action | Q(b, a) |
|---|---|
| `assess_gchq_signals_intelligence_india_operations_depth` ← OPTIMAL | 1.905 |
| `calculate_canada_diplomatic_cost_benefit_analysis` | 1.710 |
| `manage_five_eyes_intelligence_exposure_diplomatic_damage` | 1.510 |
| `identify_remaining_isi_khalistan_network_canada_us` | 1.510 |
| `expose_nijjar_isi_funding_links_counter_narrative` | 1.110 |

## Critical Path (CPM/PERT)

- Path: `nijjar_isi_link_expose` → `remaining_isi_khalistan_map`
- Total: **97 d**  →  Optimal: **58 d**  (save 39 d)
- Bottleneck: `remaining_isi_khalistan_map`
- Parallelisable: `five_eyes_exposure_manage` ‖ `nijjar_isi_link_expose`, `five_eyes_exposure_manage` ‖ `canada_diplomatic_cost_assess`

## Value of Information

- Total entropy: **1.77 bits**
- Top target: `ISI handler chain and remaining funded nodes in Khalistan diaspora network — Canada, UK, US, Australia targets`

| Rank | Target | VoI (bits) | Effort | Recommendation |
|---|---|---|---|---|
| 1 | ISI handler chain and remaining funded nodes in Khalistan diaspora network — Canada, UK, US, Australia targets | 1.59 | 8.5 | Low priority — defer; access difficulty (8.5) outweighs VoI (1.59 bits) |
| 2 | What specific intelligence Canada shared with Five Eyes partners about Indian covert operations beyond Nijjar | 1.68 | 9.5 | Low priority — defer; access difficulty (9.5) outweighs VoI (1.68 bits) |
| 3 | Depth and scope of GCHQ signals intelligence collection on Indian covert operations globally — what other operations are now exposed | 1.71 | 10.0 | Low priority — defer; access difficulty (10.0) outweighs VoI (1.71 bits) |

## Stackelberg Equilibrium

- Handler commits to: `assess_gchq_signals_intelligence_india_operations_depth`
- Operative best response: `assess_gchq_signals_intelligence_india_operations_depth`
- Adversary counter: `isi_khalistan_operation_canada: calculate_canada_diplomatic_cost_benefit_analysis`
- Indian payoff: `0.738`
- Commitment value vs Nash: `+0.144`

## Shapley Values — Asset Coalition

| Actor | φ | Defection incentive |
|---|---|---|
| narendra_modi | 0.980 | 0.000 |
| five_eyes_alliance | 0.950 | 0.000 |
| khalistan_diaspora_network | 0.700 | 0.000 |

## Monte Carlo Simulation

- Rollouts per arm: 2000
- Actual (assess_gchq_signals_intelligence_india_operations_depth): P(success)=**100.0%**  [99.8%–100.0%]
- Optimal (assess_gchq_signals_intelligence_india_operations_depth): P(success)=**100.0%**  [99.8%–100.0%]
- Δ = **+0.0%** if optimal path taken

## Threat Scores (SNA)

| Actor | Score | Betweenness | Eigenvector | High-threat |
|---|---|---|---|---|
| isi_khalistan_operation_canada | 3.750 | 0.000 | 0.000 | no |
| canadian_government_trudeau | 3.500 | 0.000 | 0.000 | no |

## Warnings

- state_node: using char.state_by_act['film4_act2'] over TP state_vector
- adversary_node: no high_threat_actors set — using all adversaries with capability >= 7.0 (['isi_khalistan_operation_canada', 'canadian_government_trudeau'])
- adversary_node: multi-adversary Stackelberg over ['isi_khalistan_operation_canada', 'canadian_government_trudeau']
- narrator_node: ANTHROPIC_API_KEY not set — using template fallback
