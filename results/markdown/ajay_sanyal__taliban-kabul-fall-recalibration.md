# Oracle briefing — `ajay_sanyal` / `taliban-kabul-fall-recalibration`

> August 15, 2021. Kabul falls to the Taliban in hours, not the weeks the CIA had predicted. President Ashraf Ghani flees. The US-trained 300,000-man Afghan National Army collapses without a fight. India had invested $3 billion in Afghanistan — Salma Dam, Kandahar consulates, Parliament building, roads — all now under Taliban control. India had 4 consulates in Afghanistan, all closed in panic. NSA Ajay Sanyal must perform an immediate strategic recalibration: Pakistan's 'strategic depth' in Afghanistan is now realised, but its costs are also visible — the TTP (Tehrik-i-Taliban Pakistan) will be emboldened, Pakistan's western border will bleed. The key intelligence question: will the Taliban honour the Pakistan-ISI relationship that gave it sanctuary for 20 years, or will the Pashtunwali code and TTP pressures turn Afghanistan into Pakistan's own strategic nightmare?

## POMDP — Optimal Policy

- **Optimal action:** `assess_taliban_isi_relationship_post_kabul`
- V(b): `5.953`
- P(mission success): `50.0%`
- P(cover intact): `100.0%`

| Action | Q(b, a) |
|---|---|
| `assess_taliban_isi_relationship_post_kabul` ← OPTIMAL | 5.953 |
| `evaluate_ttp_escalation_threat_to_pakistan_stability` | 5.555 |
| `design_quiet_engagement_channel_taliban` | 5.555 |
| `assess_isi_use_of_afghan_territory_for_india_operations` | 5.555 |
| `map_us_equipment_windfall_taliban_capabilities` | 5.555 |

## Critical Path (CPM/PERT)

- Path: `taliban_isi_relationship_assess` → `afghan_territory_india_ops_assess`
- Total: **160 d**  →  Optimal: **96 d**  (save 64 d)
- Bottleneck: `afghan_territory_india_ops_assess`
- Parallelisable: `taliban_isi_relationship_assess` ‖ `ttp_escalation_map`, `us_equipment_taliban_capability` ‖ `taliban_isi_relationship_assess`

## Value of Information

- Total entropy: **1.51 bits**
- Top target: `TTP attack trajectory — when does TTP destabilisation of Pakistan create a strategic opening for India to apply pressure`

| Rank | Target | VoI (bits) | Effort | Recommendation |
|---|---|---|---|---|
| 1 | TTP attack trajectory — when does TTP destabilisation of Pakistan create a strategic opening for India to apply pressure | 1.33 | 7.0 | Low priority — defer; access difficulty (7.0) outweighs VoI (1.33 bits) |
| 2 | Degree of Taliban openness to quiet Indian engagement — trade, technical assistance, Salma Dam — without formal recognition | 1.21 | 8.0 | Low priority — defer; access difficulty (8.0) outweighs VoI (1.21 bits) |
| 3 | Whether Taliban is providing ISI operational space for anti-India activities in Afghan territory post-Kabul | 1.44 | 9.5 | Low priority — defer; access difficulty (9.5) outweighs VoI (1.44 bits) |

## Stackelberg Equilibrium

- Handler commits to: `assess_taliban_isi_relationship_post_kabul`
- Operative best response: `assess_taliban_isi_relationship_post_kabul`
- Adversary counter: `isi_post_kabul_strategic_management: map_us_equipment_windfall_taliban_capabilities`
- Indian payoff: `0.531`
- Commitment value vs Nash: `+0.118`

## Shapley Values — Asset Coalition

| Actor | φ | Defection incentive |
|---|---|---|
| narendra_modi | 0.980 | 0.000 |

## Monte Carlo Simulation

- Rollouts per arm: 2000
- Actual (assess_taliban_isi_relationship_post_kabul): P(success)=**100.0%**  [99.8%–100.0%]
- Optimal (assess_taliban_isi_relationship_post_kabul): P(success)=**100.0%**  [99.8%–100.0%]
- Δ = **+0.0%** if optimal path taken
- Key causal lever: `assess_taliban_isi_relationship_post_kabul → taliban_independent_isi_relationship_deteriorates  (p=0.60)`

## Threat Scores (SNA)

| Actor | Score | Betweenness | Eigenvector | High-threat |
|---|---|---|---|---|
| isi_post_kabul_strategic_management | 4.250 | 0.000 | 0.000 | no |
| afghan_taliban_command | 4.000 | 0.000 | 0.000 | no |

## Warnings

- state_node: using char.state_by_act['film4_act1'] over TP state_vector
- adversary_node: no high_threat_actors set — using all adversaries with capability >= 7.0 (['isi_post_kabul_strategic_management', 'afghan_taliban_command'])
- adversary_node: multi-adversary Stackelberg over ['isi_post_kabul_strategic_management', 'afghan_taliban_command']
- narrator_node: ANTHROPIC_API_KEY not set — using template fallback
