# Oracle briefing — `hamza` / `pathankot-homecoming-choice`

> Jaskirat Singh Rangi — no longer Hamza, or not yet — returns to his hometown of Pathankot after extraction. He stands outside his family home. His mother, sister, and nephews are visible inside. They believe Jaskirat is dead — executed long ago. He could walk in and end the story as Jaskirat. Or he could walk away and continue as whatever he has become. The film offers no resolution — the door remains open, literally and figuratively. This is the final turning point of the Dhurandhar duology: not a tactical decision but an existential one. What is left of Jaskirat Singh Rangi after 20+ years of being Hamza Ali Mazari?

## POMDP — Optimal Policy

- **Optimal action:** `accept_next_mission_remain_operative`
- V(b): `3.941`
- P(mission success): `50.0%`
- P(cover intact): `100.0%`

| Action | Q(b, a) |
|---|---|
| `accept_next_mission_remain_operative` ← OPTIMAL | 3.941 |
| `enter_family_home_reveal_jaskirat_alive` | 3.644 |
| `negotiate_permanent_civilian_identity_in_india` | 3.644 |
| `return_to_pakistan_yalina_and_zayan` | 3.644 |
| `observe_only_do_not_reveal_identity` | 3.444 |

## Critical Path (CPM/PERT)

- Path: `family_decision`
- Total: **187 d**  →  Optimal: **150 d**  (save 36 d)
- Bottleneck: `family_decision`
- Parallelisable: `pakistan_family_fate` ‖ `family_decision`

## Value of Information

- Total entropy: **1.53 bits**
- Top target: `Confirmation that Yalina and Zayan are safe post-operation in Karachi`

| Rank | Target | VoI (bits) | Effort | Recommendation |
|---|---|---|---|---|
| 1 | Confirmation that Yalina and Zayan are safe post-operation in Karachi | 1.23 | 7.0 | Low priority — defer; access difficulty (7.0) outweighs VoI (1.23 bits) |
| 2 | Whether Sanyal has a Film 3 mission ready — the post-credits implication | 0.77 | 5.0 | Low priority — defer; access difficulty (5.0) outweighs VoI (0.77 bits) |

## Stackelberg Equilibrium

- Handler commits to: `accept_next_mission_remain_operative`
- Operative best response: `accept_next_mission_remain_operative`
- Adversary counter: `return_to_pakistan_yalina_and_zayan`
- Indian payoff: `0.715`
- Commitment value vs Nash: `+0.172`

## Shapley Values — Asset Coalition

| Actor | φ | Defection incentive |
|---|---|---|
| ajay_sanyal | 0.900 | 0.000 |

## Monte Carlo Simulation

- Rollouts per arm: 2000
- Actual (accept_next_mission_remain_operative): P(success)=**100.0%**  [99.8%–100.0%]
- Optimal (accept_next_mission_remain_operative): P(success)=**100.0%**  [99.8%–100.0%]
- Δ = **+0.0%** if optimal path taken
- Key causal lever: `accept_next_mission_remain_operative → operative_continues  (p=0.95)`

## Threat Scores (SNA)

| Actor | Score | Betweenness | Eigenvector | High-threat |
|---|---|---|---|---|
| institutional_raw_ib | 4.000 | 0.000 | 0.000 | no |

## Warnings

- adversary_node: no high_threat_actors set — using all adversaries with capability >= 7.0 (['institutional_raw_ib'])
- narrator_node: ANTHROPIC_API_KEY not set — using template fallback
