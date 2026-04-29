# Oracle briefing — `hamza` / `yalina-romance-risk`

> Hamza meets Yalina Jamali — daughter of PPP politician Jameel Jamali — through the Lyari social circuit. She is educated, politically aware, and drawn to Hamza's quiet intensity. He is drawn to her genuinely. The turning point: Hamza must decide whether to pursue the relationship (which could provide strategic access to the Jamali political network — a key mission target) or maintain emotional distance to protect both her and his cover. Pursuing her is both the most tactically useful and the most personally dangerous choice.

## POMDP — Optimal Policy

- **Optimal action:** `avoid_yalina_protect_cover`
- V(b): `4.442`
- P(mission success): `48.6%`
- P(cover intact): `96.5%`

| Action | Q(b, a) |
|---|---|
| `avoid_yalina_protect_cover` ← OPTIMAL | 4.442 |
| `pursue_yalina_strategically_emotional_distance` | 4.048 |
| `pursue_yalina_authentically_accept_risk` | 3.988 |
| `use_yalina_contact_for_jamali_intel_then_disengage` | 3.848 |
| `report_yalina_contact_to_aalam_request_guidance` | 3.848 |

## Critical Path (CPM/PERT)

- Path: `build_trust_dakait` → `isi_link_documentary` → `safe_exfil`
- Total: **204 d**  →  Optimal: **156 d**  (save 47 d)
- Bottleneck: `safe_exfil`
- Parallelisable: `build_trust_dakait` ‖ `jamali_political_access`

## Value of Information

- Total entropy: **1.75 bits**
- Top target: `How much Yalina knows of her father's criminal/ISI connections`

| Rank | Target | VoI (bits) | Effort | Recommendation |
|---|---|---|---|---|
| 1 | How much Yalina knows of her father's criminal/ISI connections | 1.05 | 4.0 | Low priority — defer; access difficulty (4.0) outweighs VoI (1.05 bits) |
| 2 | Jameel Jamali's offshore accounts receiving ISI/FICN transfers | 1.54 | 7.5 | Low priority — defer; access difficulty (7.5) outweighs VoI (1.54 bits) |
| 3 | Which ISI officer Jamali liaises with (Major Iqbal connection) | 1.49 | 8.0 | Low priority — defer; access difficulty (8.0) outweighs VoI (1.49 bits) |

## Stackelberg Equilibrium

- Handler commits to: `avoid_yalina_protect_cover`
- Operative best response: `avoid_yalina_protect_cover`
- Adversary counter: `report_yalina_contact_to_aalam_request_guidance`
- Indian payoff: `0.715`
- Commitment value vs Nash: `+0.172`

## Shapley Values — Asset Coalition

| Actor | φ | Defection incentive |
|---|---|---|
| mohammed_aalam | 0.880 | 0.000 |
| ajay_sanyal | 0.800 | 0.000 |
| jameel_jamali | 0.700 | 0.000 |

## Monte Carlo Simulation

- Rollouts per arm: 2000
- Actual (avoid_yalina_protect_cover): P(success)=**100.0%**  [99.8%–100.0%]
- Optimal (avoid_yalina_protect_cover): P(success)=**100.0%**  [99.8%–100.0%]
- Δ = **+0.0%** if optimal path taken
- Key causal lever: `avoid_yalina_protect_cover → cover_integrity_maintained  (p=0.88)`

## Threat Scores (SNA)

| Actor | Score | Betweenness | Eigenvector | High-threat |
|---|---|---|---|---|
| rehman_dakait | 4.250 | 0.000 | 0.000 | no |
| jameel_jamali | 2.500 | 0.000 | 0.000 | no |

## Warnings

- state_node: using char.state_by_act['film1_act2'] over TP state_vector
- adversary_node: no high_threat_actors set — using all adversaries with capability >= 7.0 (['rehman_dakait'])
- narrator_node: ANTHROPIC_API_KEY not set — using template fallback
