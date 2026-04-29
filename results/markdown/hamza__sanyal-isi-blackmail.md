# Oracle briefing — `hamza` / `sanyal-isi-blackmail`

> Ajay Sanyal deploys the operation's insurance: compromising videos of ISI Director General Shahnawaz leaking Pakistan intelligence to Israeli Mossad. The material was held as a long-game leverage asset throughout the Film 2 operation. Sanyal confronts Shahnawaz through a back-channel: release Hamza, frame Uzair Baloch as the scapegoat for Major Iqbal's death, and the Shahnawaz-Israel recordings stay buried. This is the resolution mechanism — not kinetic, not diplomatic, but raw intelligence leverage. The turning point: does Sanyal use the material (and give away a long-term asset), and what are the terms?

## POMDP — Optimal Policy

- **Optimal action:** `escalate_diplomatically_official_india_pak_channel`
- V(b): `8.379`
- P(mission success): `51.7%`
- P(cover intact): `100.0%`

| Action | Q(b, a) |
|---|---|
| `escalate_diplomatically_official_india_pak_channel` ← OPTIMAL | 8.379 |
| `deploy_shahnawaz_recordings_demand_release` | 7.983 |
| `negotiate_prisoner_exchange_other_terms` | 7.983 |
| `attempt_rescue_operation_rizwan_led` | 7.983 |
| `abandon_hamza_maintain_deniability` | 7.983 |

## Critical Path (CPM/PERT)

- Path: `shahnawaz_confrontation` → `hamza_extraction`
- Total: **8 d**  →  Optimal: **6 d**  (save 2 d)
- Bottleneck: `hamza_extraction`
- Parallelisable: `shahnawaz_confrontation` ‖ `uzair_scapegoat_package`

## Value of Information

- Total entropy: **1.49 bits**
- Top target: `Full content and credibility of Shahnawaz-Israel recordings as leverage material`

| Rank | Target | VoI (bits) | Effort | Recommendation |
|---|---|---|---|---|
| 1 | Full content and credibility of Shahnawaz-Israel recordings as leverage material | 1.48 | 0.5 | High priority — gather immediately via: deploy_shahnawaz_recordings_demand_release |
| 2 | Whether ISI's response to losing Iqbal will be de-escalation or retaliatory escalation | 1.27 | 8.0 | Low priority — defer; access difficulty (8.0) outweighs VoI (1.27 bits) |

## Stackelberg Equilibrium

- Handler commits to: `escalate_diplomatically_official_india_pak_channel`
- Operative best response: `escalate_diplomatically_official_india_pak_channel`
- Adversary counter: `abandon_hamza_maintain_deniability`
- Indian payoff: `0.715`
- Commitment value vs Nash: `+0.172`

## Shapley Values — Asset Coalition

| Actor | φ | Defection incentive |
|---|---|---|
| hamza | 0.980 | 0.000 |

## Monte Carlo Simulation

- Rollouts per arm: 2000
- Actual (escalate_diplomatically_official_india_pak_channel): P(success)=**100.0%**  [99.8%–100.0%]
- Optimal (escalate_diplomatically_official_india_pak_channel): P(success)=**100.0%**  [99.8%–100.0%]
- Δ = **+0.0%** if optimal path taken
- Key causal lever: `escalate_diplomatically_official_india_pak_channel → diplomatic_crisis  (p=0.90)`

## Threat Scores (SNA)

| Actor | Score | Betweenness | Eigenvector | High-threat |
|---|---|---|---|---|
| isi_director_general_shahnawaz | 4.500 | 0.000 | -0.000 | no |

## Warnings

- adversary_node: no high_threat_actors set — using all adversaries with capability >= 7.0 (['isi_director_general_shahnawaz'])
- narrator_node: ANTHROPIC_API_KEY not set — using template fallback
