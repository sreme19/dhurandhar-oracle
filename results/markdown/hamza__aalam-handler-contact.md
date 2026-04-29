# Oracle briefing — `hamza` / `aalam-handler-contact`

> Hamza has spent three months as a juice shop waiter, building his Lyari identity. Mohammed Aalam (the juice shop owner and RAW-embedded field handler) now activates the first formal intelligence-passing protocol. This turning point captures the moment Hamza must decide how aggressively to push for gang access — Aalam is urging patience while Sanyal's handlers in Delhi are pressing for actionable product. The tension between tradecraft caution and operational urgency is the central decision.

## POMDP — Optimal Policy

- **Optimal action:** `request_delhi_reduce_pressure`
- V(b): `3.560`
- P(mission success): `49.4%`
- P(cover intact): `98.5%`

| Action | Q(b, a) |
|---|---|
| `request_delhi_reduce_pressure` ← OPTIMAL | 3.560 |
| `push_for_faster_gang_access_risk_cover` | 3.210 |
| `establish_parallel_contact_outside_aalam` | 3.210 |
| `accept_aalam_pace_build_slowly` | 3.150 |
| `conduct_solo_surveillance_unsanctioned` | 3.010 |

## Critical Path (CPM/PERT)

- Path: `peripheral_gang_contact` → `dakait_profile_build` → `isi_link_preliminary`
- Total: **341 d**  →  Optimal: **318 d**  (save 23 d)
- Bottleneck: `isi_link_preliminary`
- Parallelisable: `peripheral_gang_contact` ‖ `police_landscape_map`

## Value of Information

- Total entropy: **1.24 bits**
- Top target: `Whether Aalam's cover as juice shop owner is secure`

| Rank | Target | VoI (bits) | Effort | Recommendation |
|---|---|---|---|---|
| 1 | Whether Aalam's cover as juice shop owner is secure | 1.12 | 2.0 | Medium priority — schedule after cover deepening |
| 2 | Rehman Dakait's daily schedule and approach routes | 1.06 | 6.5 | Low priority — defer; access difficulty (6.5) outweighs VoI (1.06 bits) |
| 3 | PAC internal faction dynamics (who is loyal vs. using Dakait) | 0.87 | 7.0 | Low priority — defer; access difficulty (7.0) outweighs VoI (0.87 bits) |

## Stackelberg Equilibrium

- Handler commits to: `request_delhi_reduce_pressure`
- Operative best response: `request_delhi_reduce_pressure`
- Adversary counter: `conduct_solo_surveillance_unsanctioned`
- Indian payoff: `0.715`
- Commitment value vs Nash: `+0.172`

## Shapley Values — Asset Coalition

| Actor | φ | Defection incentive |
|---|---|---|
| mohammed_aalam | 0.850 | -0.000 |
| ajay_sanyal | 0.750 | 0.000 |

## Monte Carlo Simulation

- Rollouts per arm: 2000
- Actual (request_delhi_reduce_pressure): P(success)=**100.0%**  [99.8%–100.0%]
- Optimal (request_delhi_reduce_pressure): P(success)=**100.0%**  [99.8%–100.0%]
- Δ = **+0.0%** if optimal path taken
- Key causal lever: `request_delhi_reduce_pressure → cover_stable  (p=0.70)`

## Threat Scores (SNA)

| Actor | Score | Betweenness | Eigenvector | High-threat |
|---|---|---|---|---|
| sp_choudhary_aslam | 3.500 | 0.000 | 0.000 | no |

## Warnings

- state_node: using char.state_by_act['film1_act1'] over TP state_vector
- adversary_node: no high_threat_actors set — using all adversaries with capability >= 7.0 (['sp_choudhary_aslam'])
- narrator_node: ANTHROPIC_API_KEY not set — using template fallback
