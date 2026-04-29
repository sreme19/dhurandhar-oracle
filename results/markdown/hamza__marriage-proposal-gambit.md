# Oracle briefing — `hamza` / `marriage-proposal-gambit`

> Hamza proposes marriage to Yalina by formally approaching her father Jameel Jamali. The proposal is simultaneously a genuine declaration (Hamza has genuinely fallen for Yalina) and a calculated cover-deepening move — marrying into the Jamali family would grant him authority in Lyari's political-criminal network, make him nearly impossible to suspect as an Indian agent, and open direct access to the Jamali-ISI financial channel. The decision to go through with the proposal is the most ethically complex moment of Film 1.

## POMDP — Optimal Policy

- **Optimal action:** `withdraw_from_yalina_maintain_distance`
- V(b): `4.435`
- P(mission success): `48.0%`
- P(cover intact): `95.0%`

| Action | Q(b, a) |
|---|---|
| `withdraw_from_yalina_maintain_distance` ← OPTIMAL | 4.435 |
| `propose_informally_delay_formal_engagement` | 4.040 |
| `use_proposal_as_access_then_abandon` | 4.040 |
| `request_delhi_guidance_on_personal_entanglement` | 3.995 |
| `propose_marriage_full_commitment` | 3.981 |

## Critical Path (CPM/PERT)

- Path: `jamali_political_access` → `isi_money_trail` → `major_iqbal_identification`
- Total: **253 d**  →  Optimal: **228 d**  (save 25 d)
- Bottleneck: `major_iqbal_identification`
- Parallelisable: `jamali_political_access` ‖ `build_trust_dakait_via_family_standing`

## Value of Information

- Total entropy: **1.86 bits**
- Top target: `Extent of Yalina's knowledge of father's ISI-criminal connections`

| Rank | Target | VoI (bits) | Effort | Recommendation |
|---|---|---|---|---|
| 1 | Extent of Yalina's knowledge of father's ISI-criminal connections | 1.02 | 3.5 | Low priority — defer; access difficulty (3.5) outweighs VoI (1.02 bits) |
| 2 | Documentary evidence of Jamali receiving ISI funds via Major Iqbal cut-out | 1.71 | 8.0 | Low priority — defer; access difficulty (8.0) outweighs VoI (1.71 bits) |
| 3 | Confirm true identity and chain of command of 'Major Iqbal' ISI handler | 1.76 | 9.0 | Low priority — defer; access difficulty (9.0) outweighs VoI (1.76 bits) |

## Stackelberg Equilibrium

- Handler commits to: `withdraw_from_yalina_maintain_distance`
- Operative best response: `withdraw_from_yalina_maintain_distance`
- Adversary counter: `use_proposal_as_access_then_abandon`
- Indian payoff: `0.715`
- Commitment value vs Nash: `+0.172`

## Shapley Values — Asset Coalition

| Actor | φ | Defection incentive |
|---|---|---|
| mohammed_aalam | 0.880 | -0.000 |
| ajay_sanyal | 0.800 | 0.000 |

## Monte Carlo Simulation

- Rollouts per arm: 2000
- Actual (withdraw_from_yalina_maintain_distance): P(success)=**100.0%**  [99.8%–100.0%]
- Optimal (withdraw_from_yalina_maintain_distance): P(success)=**100.0%**  [99.8%–100.0%]
- Δ = **+0.0%** if optimal path taken
- Key causal lever: `withdraw_from_yalina_maintain_distance → cover_depth_maximum  (p=0.20)`

## Threat Scores (SNA)

| Actor | Score | Betweenness | Eigenvector | High-threat |
|---|---|---|---|---|
| major_iqbal | 4.500 | 0.000 | 0.000 | no |
| jameel_jamali | 2.600 | 0.033 | 0.000 | no |

## Warnings

- state_node: using char.state_by_act['film1_act2'] over TP state_vector
- adversary_node: no high_threat_actors set — using all adversaries with capability >= 7.0 (['major_iqbal'])
- narrator_node: ANTHROPIC_API_KEY not set — using template fallback
