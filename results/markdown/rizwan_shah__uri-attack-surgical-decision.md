# Oracle briefing — `rizwan_shah` / `uri-attack-surgical-decision`

> September 18, 2016. Four JeM fedayeen storm the 12 Infantry Brigade HQ at Uri, J&K, at 0530 hours. The camp houses double the normal complement due to a battalion changeover — 19 Indian Army soldiers killed (initially 18, one more dies later), the deadliest attack on security forces in Kashmir in decades. The fedayeen wore Indian Army uniforms, used GPS devices, and carried Pakistani-origin food rations — a forensic link to JeM and ISI. NSA Ajay Sanyal convenes a crisis session; PM Modi gives a 10-day window for a military response option. Rizwan Shah, embedded near ISI-JeM planning circles, has partial intelligence on the launchpad locations used — but acting on it now risks blowing his cover. The turning point: does he reveal his intelligence to enable the surgical strike option, accepting the end of his current placement, or hold and continue building towards a longer operation?

## POMDP — Optimal Policy

- **Optimal action:** `hold_intelligence_protect_cover_continue_long_op`
- V(b): `4.805`
- P(mission success): `53.5%`
- P(cover intact): `100.0%`

| Action | Q(b, a) |
|---|---|
| `hold_intelligence_protect_cover_continue_long_op` ← OPTIMAL | 4.805 |
| `map_isi_escalation_intent_post_uri` | 4.611 |
| `reveal_launchpad_intelligence_enable_surgical_option` | 4.411 |
| `provide_partial_intelligence_via_dead_drop_no_cover_risk` | 4.411 |
| `assess_jem_followon_attack_timeline` | 4.011 |

## Critical Path (CPM/PERT)

- Path: `launchpad_intelligence_package` → `cover_exfil_plan`
- Total: **14 d**  →  Optimal: **9 d**  (save 6 d)
- Bottleneck: `cover_exfil_plan`
- Parallelisable: `launchpad_intelligence_package` ‖ `isi_escalation_assess`, `followon_attack_intercept` ‖ `isi_escalation_assess`

## Value of Information

- Total entropy: **1.54 bits**
- Top target: `Confirmed GPS coordinates and occupancy of 7 JeM/LeT infiltration launchpads in PoK — actionable for surgical targeting`

| Rank | Target | VoI (bits) | Effort | Recommendation |
|---|---|---|---|---|
| 1 | Confirmed GPS coordinates and occupancy of 7 JeM/LeT infiltration launchpads in PoK — actionable for surgical targeting | 1.53 | 8.5 | Low priority — defer; access difficulty (8.5) outweighs VoI (1.53 bits) |
| 2 | Whether ISI-JeM has a follow-on attack planned within the 10-day political response window | 1.42 | 8.0 | Low priority — defer; access difficulty (8.0) outweighs VoI (1.42 bits) |
| 3 | Whether ISI will retaliate conventionally if India conducts surgical strikes across LOC | 1.39 | 9.5 | Low priority — defer; access difficulty (9.5) outweighs VoI (1.39 bits) |

## Stackelberg Equilibrium

- Handler commits to: `hold_intelligence_protect_cover_continue_long_op`
- Operative best response: `hold_intelligence_protect_cover_continue_long_op`
- Adversary counter: `isi_strategic_command: assess_jem_followon_attack_timeline`
- Indian payoff: `0.533`
- Commitment value vs Nash: `+0.087`

## Shapley Values — Asset Coalition

| Actor | φ | Defection incentive |
|---|---|---|
| ajay_sanyal | 0.900 | 0.000 |
| jem | 0.880 | 0.000 |

## Monte Carlo Simulation

- Rollouts per arm: 2000
- Actual (hold_intelligence_protect_cover_continue_long_op): P(success)=**100.0%**  [99.8%–100.0%]
- Optimal (hold_intelligence_protect_cover_continue_long_op): P(success)=**100.0%**  [99.8%–100.0%]
- Δ = **+0.0%** if optimal path taken
- Key causal lever: `hold_intelligence_protect_cover_continue_long_op → long_operation_yields_deeper_intelligence  (p=0.75)`

## Threat Scores (SNA)

| Actor | Score | Betweenness | Eigenvector | High-threat |
|---|---|---|---|---|
| isi_strategic_command | 4.750 | 0.000 | 0.000 | no |
| jem_isi_planning_cell | 4.250 | 0.000 | 0.000 | no |

## Warnings

- state_node: using char.state_by_act['film3_act1'] over TP state_vector
- adversary_node: no high_threat_actors set — using all adversaries with capability >= 7.0 (['jem_isi_planning_cell', 'isi_strategic_command'])
- adversary_node: multi-adversary Stackelberg over ['jem_isi_planning_cell', 'isi_strategic_command']
- narrator_node: ANTHROPIC_API_KEY not set — using template fallback
