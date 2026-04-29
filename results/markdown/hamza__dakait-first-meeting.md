# Oracle briefing — `hamza` / `dakait-first-meeting`

> Hamza secures his first direct meeting with Rehman Dakait. He must choose how to position himself — as a useful criminal asset, a political broker, or an intelligence source — without triggering Dakait's suspicion.

## POMDP — Optimal Policy

- **Optimal action:** `accelerate_dakait_trust`
- V(b): `-54.233`
- P(mission success): `42.7%`
- P(cover intact): `87.5%`

| Action | Q(b, a) |
|---|---|
| `accelerate_dakait_trust` ← OPTIMAL | -54.233 |
| `request_handler_backup` | -54.233 |
| `deepen_criminal_cover` | -54.277 |
| `offer_political_intelligence` | -54.674 |
| `trigger_early_exfil` | -55.521 |

## Critical Path (CPM/PERT)

- Path: `establish_cover` → `infiltrate_gang_periphery` → `build_trust_dakait` → `expose_political_link` → `safe_exfil`
- Total: **123 d**  →  Optimal: **84 d**  (save 38 d)
- Bottleneck: `safe_exfil`
- Parallelisable: `establish_cover` ‖ `contact_handler_network`, `build_trust_dakait` ‖ `gather_political_intel`

## Value of Information

- Total entropy: **1.65 bits**
- Top target: `Mohammed Aalam's true allegiance`

| Rank | Target | VoI (bits) | Effort | Recommendation |
|---|---|---|---|---|
| 1 | Mohammed Aalam's true allegiance | 1.24 | 3.5 | Low priority — defer; access difficulty (3.5) outweighs VoI (1.24 bits) |
| 2 | Dakait's arms cache location | 1.07 | 5.0 | Low priority — defer; access difficulty (5.0) outweighs VoI (1.07 bits) |
| 3 | Jamali's political patronage network | 1.32 | 6.5 | Low priority — defer; access difficulty (6.5) outweighs VoI (1.32 bits) |
| 4 | Jamali's offshore terror financing accounts | 1.48 | 8.0 | Low priority — defer; access difficulty (8.0) outweighs VoI (1.48 bits) |

## Stackelberg Equilibrium

- Handler commits to: `accelerate_dakait_trust`
- Operative best response: `accelerate_dakait_trust`
- Adversary counter: `trigger_early_exfil`
- Indian payoff: `0.715`
- Commitment value vs Nash: `+0.172`

## Shapley Values — Asset Coalition

| Actor | φ | Defection incentive |
|---|---|---|
| ajay_sanyal | 0.950 | 0.000 |
| mohammed_aalam | 0.900 | -0.000 |

## Monte Carlo Simulation

- Rollouts per arm: 2000
- Actual (accelerate_dakait_trust): P(success)=**77.0%**  [75.0%–78.7%]
- Optimal (accelerate_dakait_trust): P(success)=**79.2%**  [77.4%–81.0%]
- Δ = **+2.3%** if optimal path taken
- Key causal lever: `accelerate_dakait_trust → dakait_trust_rises  (p=0.80)`

## Threat Scores (SNA)

| Actor | Score | Betweenness | Eigenvector | High-threat |
|---|---|---|---|---|
| rehman_dakait | 4.250 | 0.000 | 0.000 | no |
| sp_choudhary_aslam | 3.250 | 0.000 | 0.000 | no |

## Warnings

- state_node: using char.state_by_act['film1_act2'] over TP state_vector
- adversary_node: no high_threat_actors set — using all adversaries with capability >= 7.0 (['rehman_dakait'])
- narrator_node: ANTHROPIC_API_KEY not set — using template fallback
