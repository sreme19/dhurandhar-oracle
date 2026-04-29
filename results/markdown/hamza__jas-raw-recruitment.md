# Oracle briefing — `hamza` / `jas-raw-recruitment`

> Jaskirat Singh Rangi — a death-row convict who killed 12 men in revenge for his family's destruction — is abducted from a prison transfer vehicle by Ajay Sanyal. Sanyal offers him a choice: die on the gallows as a murderer, or be reborn as 'Hamza Ali Mazari' and serve India in Pakistan. Jaskirat must decide whether to accept total identity erasure in exchange for a mission that may take decades. His answer shapes everything that follows.

## POMDP — Optimal Policy

- **Optimal action:** `refuse_recruitment_face_execution`
- V(b): `-31.420`
- P(mission success): `47.8%`
- P(cover intact): `100.0%`

| Action | Q(b, a) |
|---|---|
| `refuse_recruitment_face_execution` ← OPTIMAL | -31.420 |
| `negotiate_conditions_partial_identity` | -31.795 |
| `demand_family_protection_first` | -31.795 |
| `accept_recruitment_full_erasure` | -31.895 |
| `accept_and_plan_defection` | -31.895 |

## Critical Path (CPM/PERT)

- Path: `urdu_cultural_immersion`
- Total: **191 d**  →  Optimal: **114 d**  (save 76 d)
- Bottleneck: `urdu_cultural_immersion`
- Parallelisable: `identity_construction` ‖ `urdu_cultural_immersion`, `identity_construction` ‖ `karachi_geography_briefing`, `urdu_cultural_immersion` ‖ `karachi_geography_briefing`

## Value of Information

- Total entropy: **0.88 bits**
- Top target: `Lyari criminal network hierarchy and ISI linkages`

| Rank | Target | VoI (bits) | Effort | Recommendation |
|---|---|---|---|---|
| 1 | Lyari criminal network hierarchy and ISI linkages | 0.84 | 9.0 | Low priority — defer; access difficulty (9.0) outweighs VoI (0.84 bits) |
| 2 | JeM/LeT terror financing pipeline through Karachi criminal networks | 0.80 | 9.5 | Low priority — defer; access difficulty (9.5) outweighs VoI (0.80 bits) |

## Stackelberg Equilibrium

- Handler commits to: `refuse_recruitment_face_execution`
- Operative best response: `refuse_recruitment_face_execution`
- Adversary counter: `demand_family_protection_first`
- Indian payoff: `0.715`
- Commitment value vs Nash: `+0.172`

## Monte Carlo Simulation

- Rollouts per arm: 2000
- Actual (refuse_recruitment_face_execution): P(success)=**100.0%**  [99.8%–100.0%]
- Optimal (refuse_recruitment_face_execution): P(success)=**100.0%**  [99.8%–100.0%]
- Δ = **+0.0%** if optimal path taken
- Key causal lever: `refuse_recruitment_face_execution → operative_executed  (p=0.98)`

## Threat Scores (SNA)

| Actor | Score | Betweenness | Eigenvector | High-threat |
|---|---|---|---|---|
| institutional_inertia_ib_raw | 3.500 | 0.000 | 0.000 | no |

## Warnings

- state_node: using char.state_by_act['film1_act1'] over TP state_vector
- coalition_node: no in-coalition edges — returning empty Shapley
- adversary_node: no high_threat_actors set — using all adversaries with capability >= 7.0 (['institutional_inertia_ib_raw'])
- narrator_node: ANTHROPIC_API_KEY not set — using template fallback
