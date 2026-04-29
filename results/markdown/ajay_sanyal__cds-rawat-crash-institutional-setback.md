# Oracle briefing — `ajay_sanyal` / `cds-rawat-crash-institutional-setback`

> December 8, 2021. An IAF Mi-17V5 helicopter carrying Chief of Defence Staff General Bipin Rawat, his wife Madhulika Rawat, and 11 other personnel crashes near Coonoor, Tamil Nadu in mountainous terrain. 13 of 14 on board are killed; one DSC soldier survives with severe burns. The IAF court of inquiry later concludes: pilot error — controlled flight into terrain due to loss of spatial orientation in cloud conditions. India's first CDS — the architect of jointness of the three services, a key figure in Doklam and Galwan response planning — is dead. NSA Ajay Sanyal must manage: (1) ISI's inevitable attempt to exploit the institutional vacuum; (2) the loss of a critical military voice at a moment of active China-India standoff and ongoing J&K operations; (3) the political sensitivity of having India's most senior military officer die in what is officially an accident.

## POMDP — Optimal Policy

- **Optimal action:** `accelerate_cds_replacement_prevent_morale_gap`
- V(b): `5.953`
- P(mission success): `50.0%`
- P(cover intact): `100.0%`

| Action | Q(b, a) |
|---|---|
| `accelerate_cds_replacement_prevent_morale_gap` ← OPTIMAL | 5.953 |
| `counter_isi_sabotage_narrative_information_operations` | 5.555 |
| `assess_isi_exploitation_of_institutional_vacuum` | 5.555 |
| `maintain_lac_negotiation_continuity_without_cds` | 5.555 |
| `assess_enemy_exploitation_window_3_month_cds_vacancy` | 5.555 |

## Critical Path (CPM/PERT)

- Path: `lac_continuity`
- Total: **37 d**  →  Optimal: **22 d**  (save 15 d)
- Bottleneck: `lac_continuity`
- Parallelisable: `isi_exploitation_window_monitor` ‖ `sabotage_narrative_counter`, `isi_exploitation_window_monitor` ‖ `lac_continuity`, `cds_replacement_brief` ‖ `lac_continuity`

## Value of Information

- Total entropy: **1.92 bits**
- Top target: `ISI information operations coordination behind Rawat sabotage narrative — specific actors, platforms, messaging`

| Rank | Target | VoI (bits) | Effort | Recommendation |
|---|---|---|---|---|
| 1 | ISI information operations coordination behind Rawat sabotage narrative — specific actors, platforms, messaging | 1.49 | 6.5 | Low priority — defer; access difficulty (6.5) outweighs VoI (1.49 bits) |
| 2 | Any ISI-JeM attack planning specifically timed to the CDS vacancy window (December 2021 – March 2022) | 1.76 | 8.0 | Low priority — defer; access difficulty (8.0) outweighs VoI (1.76 bits) |
| 3 | PLA's specific negotiating positions at corps commander talks post-Rawat — evidence of exploitation of CDS vacuum | 1.63 | 8.5 | Low priority — defer; access difficulty (8.5) outweighs VoI (1.63 bits) |

## Stackelberg Equilibrium

- Handler commits to: `accelerate_cds_replacement_prevent_morale_gap`
- Operative best response: `accelerate_cds_replacement_prevent_morale_gap`
- Adversary counter: `pla_lac_negotiation_post_rawat: maintain_lac_negotiation_continuity_without_cds`
- Indian payoff: `0.763`
- Commitment value vs Nash: `+0.212`

## Shapley Values — Asset Coalition

| Actor | φ | Defection incentive |
|---|---|---|
| narendra_modi | 0.980 | 0.000 |

## Monte Carlo Simulation

- Rollouts per arm: 2000
- Actual (accelerate_cds_replacement_prevent_morale_gap): P(success)=**100.0%**  [99.8%–100.0%]
- Optimal (accelerate_cds_replacement_prevent_morale_gap): P(success)=**100.0%**  [99.8%–100.0%]
- Δ = **+0.0%** if optimal path taken
- Key causal lever: `accelerate_cds_replacement_prevent_morale_gap → institutional_continuity_maintained  (p=0.85)`

## Threat Scores (SNA)

| Actor | Score | Betweenness | Eigenvector | High-threat |
|---|---|---|---|---|
| pla_lac_negotiation_post_rawat | 4.500 | 0.000 | 0.000 | no |
| isi_information_operations_rawat | 3.750 | 0.000 | 0.000 | no |

## Warnings

- state_node: using char.state_by_act['film4_act1'] over TP state_vector
- adversary_node: no high_threat_actors set — using all adversaries with capability >= 7.0 (['isi_information_operations_rawat', 'pla_lac_negotiation_post_rawat'])
- adversary_node: multi-adversary Stackelberg over ['isi_information_operations_rawat', 'pla_lac_negotiation_post_rawat']
- narrator_node: ANTHROPIC_API_KEY not set — using template fallback
