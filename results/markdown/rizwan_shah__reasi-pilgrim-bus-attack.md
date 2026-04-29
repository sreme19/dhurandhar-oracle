# Oracle briefing — `rizwan_shah` / `reasi-pilgrim-bus-attack`

> June 9, 2024, 1800 hours. A passenger bus carrying Hindu pilgrims from the Shiv Khori cave temple toward Katra is ambushed by two terrorists who open fire from elevated positions in Pouni tehsil, Reasi district, Jammu division. The driver loses control; the bus falls into a gorge. 9 pilgrims killed, 33 injured (many from the fall, not direct gunfire). The attackers, carrying M4 carbines and AK-47s with Pakistani markings, flee into the forest. Security forces pursue but fail to neutralise them immediately. The attack is significant on two levels: (1) it targets Hindu pilgrims in Jammu division — not the Kashmir Valley — expanding the operational footprint; (2) it occurs in Modi 3.0's first week (Modi sworn in June 9, 2024), a deliberate signal. Rizwan Shah, re-positioned post-Balakot in a rebuilt cover, has intelligence on the infiltration route used — but the terrain and timing have already yielded. The turning point: can he provide retroactive intelligence that identifies the handler chain and prevents the follow-on?

## POMDP — Optimal Policy

- **Optimal action:** `map_infiltration_route_pir_panjal_active_corridor`
- V(b): `5.882`
- P(mission success): `50.0%`
- P(cover intact): `100.0%`

| Action | Q(b, a) |
|---|---|
| `map_infiltration_route_pir_panjal_active_corridor` ← OPTIMAL | 5.882 |
| `trace_m4_pipeline_reasi_to_isi_source` | 5.288 |
| `identify_trf_jem_joint_cell_handler_reasi` | 5.288 |
| `assess_follow_on_attack_planning_jammu_pivot` | 4.888 |
| `provide_intelligence_for_captured_attacker_interrogation` | 4.888 |

## Critical Path (CPM/PERT)

- Path: `trf_jem_handler_identify` → `followon_jammu_attack_assess`
- Total: **48 d**  →  Optimal: **29 d**  (save 19 d)
- Bottleneck: `followon_jammu_attack_assess`
- Parallelisable: `m4_pipeline_trace_reasi` ‖ `trf_jem_handler_identify`, `m4_pipeline_trace_reasi` ‖ `pir_panjal_route_map`

## Value of Information

- Total entropy: **1.51 bits**
- Top target: `ISI procurement source for M4 carbines — Gulf intermediary, route into Pakistan, distribution to TRF-JeM (same pipeline used in Pahalgam 2025)`

| Rank | Target | VoI (bits) | Effort | Recommendation |
|---|---|---|---|---|
| 1 | ISI procurement source for M4 carbines — Gulf intermediary, route into Pakistan, distribution to TRF-JeM (same pipeline used in Pahalgam 2025) | 1.44 | 8.0 | Low priority — defer; access difficulty (8.0) outweighs VoI (1.44 bits) |
| 2 | How many other cells used the Pir Panjal corridor in 2023-2024 — current active infiltrators in Jammu division | 1.36 | 8.0 | Low priority — defer; access difficulty (8.0) outweighs VoI (1.36 bits) |
| 3 | ISI-TRF-JeM three-actor handler chain for Reasi attack — ISI authorising officer, TRF coordinator, JeM operative manager | 1.39 | 8.5 | Low priority — defer; access difficulty (8.5) outweighs VoI (1.39 bits) |

## Stackelberg Equilibrium

- Handler commits to: `map_infiltration_route_pir_panjal_active_corridor`
- Operative best response: `map_infiltration_route_pir_panjal_active_corridor`
- Adversary counter: `provide_intelligence_for_captured_attacker_interrogation`
- Indian payoff: `0.715`
- Commitment value vs Nash: `+0.172`

## Shapley Values — Asset Coalition

| Actor | φ | Defection incentive |
|---|---|---|
| ajay_sanyal | 0.900 | 0.000 |
| trf | 0.880 | 0.000 |
| jem | 0.800 | 0.000 |

## Monte Carlo Simulation

- Rollouts per arm: 2000
- Actual (map_infiltration_route_pir_panjal_active_corridor): P(success)=**100.0%**  [99.8%–100.0%]
- Optimal (map_infiltration_route_pir_panjal_active_corridor): P(success)=**100.0%**  [99.8%–100.0%]
- Δ = **+0.0%** if optimal path taken
- Key causal lever: `map_infiltration_route_pir_panjal_active_corridor → pir_panjal_route_closed_follow_on_prevented  (p=0.65)`

## Threat Scores (SNA)

| Actor | Score | Betweenness | Eigenvector | High-threat |
|---|---|---|---|---|
| isi_trf_jem_jammu_pivot_cell | 4.000 | 0.000 | 0.000 | no |

## Warnings

- adversary_node: no high_threat_actors set — using all adversaries with capability >= 7.0 (['isi_trf_jem_jammu_pivot_cell'])
- narrator_node: ANTHROPIC_API_KEY not set — using template fallback
