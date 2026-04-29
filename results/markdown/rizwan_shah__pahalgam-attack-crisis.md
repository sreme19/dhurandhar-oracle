# Oracle briefing — `rizwan_shah` / `pahalgam-attack-crisis`

> April 22, 2025. The Resistance Front (TRF) — an LeT proxy created in 2019 to provide FATF deniability — kills 26 tourists in the Baisaran Valley meadow near Pahalgam. 25 tourists (mostly Hindu) and one local Muslim pony operator are shot with M4 carbines and AK-47s. It is the deadliest civilian attack in India since 26/11. TRF initially claims responsibility twice, then retracts. ISI-TRF coordination is confirmed through signals intelligence. Rizwan Shah, now running operations from a position of deep knowledge of the ISI-LeT structure, must determine: was this an ISI-sanctioned escalation or a TRF operational overreach? The answer determines the appropriate scale and nature of India's response.

## POMDP — Optimal Policy

- **Optimal action:** `confirm_isi_sanction_level_inform_delhi_scale`
- V(b): `5.882`
- P(mission success): `50.0%`
- P(cover intact): `100.0%`

| Action | Q(b, a) |
|---|---|
| `confirm_isi_sanction_level_inform_delhi_scale` ← OPTIMAL | 5.882 |
| `identify_trf_cell_commander_locate_for_elimination` | 5.288 |
| `trace_weapons_supply_chain_m4_carbines_origin` | 5.288 |
| `provide_intelligence_for_diplomatic_dossier` | 5.288 |
| `assess_follow_on_attack_probability` | 4.888 |

## Critical Path (CPM/PERT)

- Path: `weapons_trace`
- Total: **32 d**  →  Optimal: **19 d**  (save 13 d)
- Bottleneck: `weapons_trace`
- Parallelisable: `isi_sanction_confirm` ‖ `trf_cell_locate`, `isi_sanction_confirm` ‖ `weapons_trace`

## Value of Information

- Total entropy: **1.51 bits**
- Top target: `Identity and location of TRF operational commander who planned Pahalgam attack`

| Rank | Target | VoI (bits) | Effort | Recommendation |
|---|---|---|---|---|
| 1 | Identity and location of TRF operational commander who planned Pahalgam attack | 1.36 | 8.0 | Low priority — defer; access difficulty (8.0) outweighs VoI (1.36 bits) |
| 2 | Was Pahalgam ordered by ISI DG Munir personally or TRF semi-autonomous operation? | 1.48 | 9.0 | Low priority — defer; access difficulty (9.0) outweighs VoI (1.48 bits) |
| 3 | Origin of M4 carbines used in attack — ISI-TRF arms pipeline route | 1.21 | 7.5 | Low priority — defer; access difficulty (7.5) outweighs VoI (1.21 bits) |

## Stackelberg Equilibrium

- Handler commits to: `confirm_isi_sanction_level_inform_delhi_scale`
- Operative best response: `confirm_isi_sanction_level_inform_delhi_scale`
- Adversary counter: `isi_general_asim_munir: provide_intelligence_for_diplomatic_dossier`
- Indian payoff: `0.773`
- Commitment value vs Nash: `+0.242`

## Shapley Values — Asset Coalition

| Actor | φ | Defection incentive |
|---|---|---|
| ajay_sanyal | 0.920 | 0.000 |

## Monte Carlo Simulation

- Rollouts per arm: 2000
- Actual (confirm_isi_sanction_level_inform_delhi_scale): P(success)=**100.0%**  [99.8%–100.0%]
- Optimal (confirm_isi_sanction_level_inform_delhi_scale): P(success)=**100.0%**  [99.8%–100.0%]
- Δ = **+0.0%** if optimal path taken
- Key causal lever: `confirm_isi_sanction_level_inform_delhi_scale → india_response_calibrated_correctly  (p=0.85)`

## Threat Scores (SNA)

| Actor | Score | Betweenness | Eigenvector | High-threat |
|---|---|---|---|---|
| isi_general_asim_munir | 4.750 | 0.000 | 0.000 | no |
| trf_isi_coordination | 4.000 | 0.000 | 0.000 | no |

## Warnings

- state_node: using char.state_by_act['film3_act2'] over TP state_vector
- adversary_node: no high_threat_actors set — using all adversaries with capability >= 7.0 (['trf_isi_coordination', 'isi_general_asim_munir'])
- adversary_node: multi-adversary Stackelberg over ['trf_isi_coordination', 'isi_general_asim_munir']
- narrator_node: ANTHROPIC_API_KEY not set — using template fallback
