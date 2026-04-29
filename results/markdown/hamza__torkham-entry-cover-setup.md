# Oracle briefing — `hamza` / `torkham-entry-cover-setup`

> Hamza Ali Mazari crosses from Afghanistan into Pakistan via the Torkham border crossing. He carries documents establishing him as a Baloch from Quetta with criminal connections. In Lyari, he takes work as a waiter at Mohammed Aalam's juice shop — his cover employer and field handler. He must establish himself as a credible, low-level Lyari resident without triggering the neighbourhood's intense communal surveillance, while beginning to map the gang structure from the ground up.

## POMDP — Optimal Policy

- **Optimal action:** `conduct_passive_surveillance_only`
- V(b): `-49.266`
- P(mission success): `47.4%`
- P(cover intact): `94.0%`

| Action | Q(b, a) |
|---|---|
| `conduct_passive_surveillance_only` ← OPTIMAL | -49.266 |
| `establish_lyari_street_presence_slow` | -49.422 |
| `bribe_local_informants_for_quick_intel` | -49.622 |
| `accelerate_gang_contact_via_aalam` | -50.001 |
| `request_exfil_abort_mission` | -51.333 |

## Critical Path (CPM/PERT)

- Path: `passive_surveillance` → `peripheral_gang_contact`
- Total: **114 d**  →  Optimal: **68 d**  (save 45 d)
- Bottleneck: `peripheral_gang_contact`
- Parallelisable: `establish_cover` ‖ `passive_surveillance`, `police_landscape_map` ‖ `establish_cover`, `police_landscape_map` ‖ `passive_surveillance`

## Value of Information

- Total entropy: **1.31 bits**
- Top target: `Whether Mohammed Aalam's juice shop cover is secure (LTF not suspicious)`

| Rank | Target | VoI (bits) | Effort | Recommendation |
|---|---|---|---|---|
| 1 | Whether Mohammed Aalam's juice shop cover is secure (LTF not suspicious) | 1.05 | 2.5 | Low priority — defer; access difficulty (2.5) outweighs VoI (1.05 bits) |
| 2 | Lyari Task Force patrol patterns and informant density | 0.72 | 3.0 | Low priority — defer; access difficulty (3.0) outweighs VoI (0.72 bits) |
| 3 | People's Aman Committee (PAC) leadership hierarchy under Rehman Dakait | 1.15 | 7.0 | Low priority — defer; access difficulty (7.0) outweighs VoI (1.15 bits) |

## Stackelberg Equilibrium

- Handler commits to: `conduct_passive_surveillance_only`
- Operative best response: `conduct_passive_surveillance_only`
- Adversary counter: `request_exfil_abort_mission`
- Indian payoff: `0.715`
- Commitment value vs Nash: `+0.172`

## Shapley Values — Asset Coalition

| Actor | φ | Defection incentive |
|---|---|---|
| mohammed_aalam | 0.750 | 0.000 |
| ajay_sanyal | 0.700 | 0.000 |

## Monte Carlo Simulation

- Rollouts per arm: 2000
- Actual (conduct_passive_surveillance_only): P(success)=**100.0%**  [99.8%–100.0%]
- Optimal (conduct_passive_surveillance_only): P(success)=**100.0%**  [99.8%–100.0%]
- Δ = **+0.0%** if optimal path taken
- Key causal lever: `conduct_passive_surveillance_only → community_acceptance_achieved  (p=0.75)`

## Threat Scores (SNA)

| Actor | Score | Betweenness | Eigenvector | High-threat |
|---|---|---|---|---|
| sp_choudhary_aslam | 3.500 | 0.000 | 0.000 | no |
| lyari_community_surveillance | 2.750 | 0.000 | 0.000 | no |

## Warnings

- state_node: using char.state_by_act['film1_act1'] over TP state_vector
- adversary_node: no high_threat_actors set — using all adversaries with capability >= 7.0 (['sp_choudhary_aslam'])
- narrator_node: ANTHROPIC_API_KEY not set — using template fallback
