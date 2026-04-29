# Oracle briefing — `rizwan_shah` / `pulwama-balakot-decision`

> February 14, 2019, 1535 hours. Adil Ahmad Dar, a 20-year-old local Kashmiri recruited by JeM, drives a Maruti Eeco packed with 300-350kg of IED into bus 49 of a 78-vehicle CRPF convoy on NH-44 near Lethapora, Pulwama. 40 CRPF personnel killed — the deadliest attack on security forces since 26/11. JeM claims responsibility within hours. The IP address used to upload Adil Ahmad Dar's martyrdom video traces to a location near Rawalpindi — Pakistan's army cantonment city. PM Modi chairs CCS within hours. The political mandate for retaliation is immediate and total. Rizwan Shah, monitoring ISI-JeM networks, holds critical intelligence about the Balakot training camp used to plan the attack — the same camp NSA Sanyal wants to strike. The decision: deliver the intelligence package now and enable a strike, or hold it as leverage for a deeper JeM network operation?

## POMDP — Optimal Policy

- **Optimal action:** `confirm_isi_sanction_level_on_pulwama`
- V(b): `5.882`
- P(mission success): `50.0%`
- P(cover intact): `100.0%`

| Action | Q(b, a) |
|---|---|
| `confirm_isi_sanction_level_on_pulwama` ← OPTIMAL | 5.882 |
| `deliver_broader_jem_network_map_for_deeper_operation` | 5.488 |
| `identify_jem_handlers_who_managed_dar_recruitment` | 5.288 |
| `deliver_balakot_targeting_intelligence_enable_air_strike` | 4.888 |
| `assess_isi_retaliation_threshold_if_india_strikes` | 4.888 |

## Critical Path (CPM/PERT)

- Path: `dar_handler_identify`
- Total: **23 d**  →  Optimal: **14 d**  (save 9 d)
- Bottleneck: `dar_handler_identify`
- Parallelisable: `balakot_targeting_package` ‖ `isi_retaliation_threshold`, `isi_pulwama_sanction_confirm` ‖ `balakot_targeting_package`, `dar_handler_identify` ‖ `balakot_targeting_package`, `dar_handler_identify` ‖ `isi_retaliation_threshold`

## Value of Information

- Total entropy: **1.24 bits**
- Top target: `Current occupancy, command presence, and physical layout of Markaz Subhan Allah (Balakot) for IAF precision targeting`

| Rank | Target | VoI (bits) | Effort | Recommendation |
|---|---|---|---|---|
| 1 | Current occupancy, command presence, and physical layout of Markaz Subhan Allah (Balakot) for IAF precision targeting | 1.23 | 8.5 | Low priority — defer; access difficulty (8.5) outweighs VoI (1.23 bits) |
| 2 | ISI/JeM handler who recruited Adil Ahmad Dar — leads to broader recruitment pipeline disruption | 1.06 | 8.0 | Low priority — defer; access difficulty (8.0) outweighs VoI (1.06 bits) |
| 3 | PAF's planned retaliation if India strikes Balakot in Pakistan proper — F-16 sortie plan, targets designated | 1.21 | 9.5 | Low priority — defer; access difficulty (9.5) outweighs VoI (1.21 bits) |

## Stackelberg Equilibrium

- Handler commits to: `confirm_isi_sanction_level_on_pulwama`
- Operative best response: `confirm_isi_sanction_level_on_pulwama`
- Adversary counter: `isi_ghq_post_pulwama: identify_jem_handlers_who_managed_dar_recruitment`
- Indian payoff: `0.707`
- Commitment value vs Nash: `+0.229`

## Shapley Values — Asset Coalition

| Actor | φ | Defection incentive |
|---|---|---|
| ajay_sanyal | 0.920 | 0.000 |
| jem_masood_azhar | 0.850 | 0.000 |

## Monte Carlo Simulation

- Rollouts per arm: 2000
- Actual (confirm_isi_sanction_level_on_pulwama): P(success)=**100.0%**  [99.8%–100.0%]
- Optimal (confirm_isi_sanction_level_on_pulwama): P(success)=**100.0%**  [99.8%–100.0%]
- Δ = **+0.0%** if optimal path taken
- Key causal lever: `confirm_isi_sanction_level_on_pulwama → diplomatic_dossier_strengthened  (p=0.88)`

## Threat Scores (SNA)

| Actor | Score | Betweenness | Eigenvector | High-threat |
|---|---|---|---|---|
| isi_ghq_post_pulwama | 4.750 | 0.000 | 0.000 | no |
| jem_masood_azhar_command | 4.250 | 0.000 | 0.000 | no |

## Warnings

- state_node: using char.state_by_act['film3_act2'] over TP state_vector
- adversary_node: no high_threat_actors set — using all adversaries with capability >= 7.0 (['isi_ghq_post_pulwama', 'jem_masood_azhar_command'])
- adversary_node: multi-adversary Stackelberg over ['isi_ghq_post_pulwama', 'jem_masood_azhar_command']
- narrator_node: ANTHROPIC_API_KEY not set — using template fallback
