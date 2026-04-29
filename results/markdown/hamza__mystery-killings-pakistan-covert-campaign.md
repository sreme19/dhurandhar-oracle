# Oracle briefing — `hamza` / `mystery-killings-pakistan-covert-campaign`

> 2022-2024. A pattern emerges across Pakistan's major cities: India's most-wanted terrorists are dying. March 2022: Zahoor Mistry (IC-814 hijacker, the man who inspired Film 1) shot dead at his Crescent Furniture store in Karachi — 22 years after the hijacking. 2023: Sajid Mir (26/11 handler, the ghost who was declared dead by Pakistan) reportedly poisoned in custody. May 2023: Paramjit Singh Panjwar (Khalistan Commando Force chief, Pakistan-based) shot dead in Lahore. 2023-2024: Multiple Hizbul and JeM commanders die in car bombs, shootings, 'unknown assailants'. The Guardian reports 'up to 20 assassinations since 2020, Indian government ordered.' Pakistan's intelligence officials brief The Guardian; Islamabad lodges formal diplomatic protests. Hamza — Jaskirat Singh Rangi, living under a third cover identity, operational in Karachi — is the covert instrument. The turning point: Pakistan's ISI has identified the pattern and has a partial profile of the operator. Does Hamza complete the final target on his list — or break contact and exfiltrate before ISI closes the net?

## POMDP — Optimal Policy

- **Optimal action:** `feed_isi_false_profile_extend_operational_window`
- V(b): `5.882`
- P(mission success): `50.0%`
- P(cover intact): `100.0%`

| Action | Q(b, a) |
|---|---|
| `feed_isi_false_profile_extend_operational_window` ← OPTIMAL | 5.882 |
| `complete_final_target_before_isi_closes_net` | 5.488 |
| `assess_final_target_security_posture_post_pattern_identified` | 5.488 |
| `identify_degree_of_isi_partial_profile_accuracy` | 5.288 |
| `break_contact_exfiltrate_iran_corridor` | 4.888 |

## Critical Path (CPM/PERT)

- Path: `final_target_security_assess` → `final_operation_execute`
- Total: **11 d**  →  Optimal: **6 d**  (save 4 d)
- Bottleneck: `final_operation_execute`
- Parallelisable: `isi_profile_accuracy_assess` ‖ `final_target_security_assess`, `exfil_route_prepare` ‖ `isi_profile_accuracy_assess`

## Value of Information

- Total entropy: **1.74 bits**
- Top target: `Current location and security posture of the final target — ISI protection tightened post-pattern-identification`

| Rank | Target | VoI (bits) | Effort | Recommendation |
|---|---|---|---|---|
| 1 | Current location and security posture of the final target — ISI protection tightened post-pattern-identification | 1.70 | 9.5 | Low priority — defer; access difficulty (9.5) outweighs VoI (1.70 bits) |
| 2 | How complete is ISI's partial profile of the operator — current cover identity, location, cell structure | 1.72 | 10.0 | Low priority — defer; access difficulty (10.0) outweighs VoI (1.72 bits) |

## Stackelberg Equilibrium

- Handler commits to: `feed_isi_false_profile_extend_operational_window`
- Operative best response: `feed_isi_false_profile_extend_operational_window`
- Adversary counter: `assess_final_target_security_posture_post_pattern_identified`
- Indian payoff: `0.715`
- Commitment value vs Nash: `+0.172`

## Shapley Values — Asset Coalition

| Actor | φ | Defection incentive |
|---|---|---|
| ajay_sanyal | 0.880 | 0.000 |

## Monte Carlo Simulation

- Rollouts per arm: 2000
- Actual (feed_isi_false_profile_extend_operational_window): P(success)=**100.0%**  [99.8%–100.0%]
- Optimal (feed_isi_false_profile_extend_operational_window): P(success)=**100.0%**  [99.8%–100.0%]
- Δ = **+0.0%** if optimal path taken
- Key causal lever: `feed_isi_false_profile_extend_operational_window → isi_false_profile_buys_time_final_op_possible  (p=0.60)`

## Threat Scores (SNA)

| Actor | Score | Betweenness | Eigenvector | High-threat |
|---|---|---|---|---|
| isi_counterintelligence_hunt_operator | 4.750 | 0.000 | 0.000 | no |

## Warnings

- adversary_node: no high_threat_actors set — using all adversaries with capability >= 7.0 (['isi_counterintelligence_hunt_operator'])
- narrator_node: ANTHROPIC_API_KEY not set — using template fallback
