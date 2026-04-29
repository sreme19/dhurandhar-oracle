# Oracle briefing — `rizwan_shah` / `tahawwur-rana-extradition`

> April 10, 2025. Tahawwur Rana — Pakistani-American 26/11 co-conspirator, colleague of David Headley — arrives in India after the US Supreme Court rejects his final extradition appeal. He is the first significant 26/11 figure extradited to face Indian justice. NIA takes custody. Rana worked with Headley to plan 26/11 and was convicted in the US on other charges. His potential testimony could expose ISI's chain of command in 26/11 planning. Rizwan's role: provide intelligence on which ISI officers and LeT figures Rana has contact knowledge of, to maximise the intelligence yield from NIA's interrogation. The risk: ISI will attempt to either discredit Rana's testimony or eliminate any witnesses he might name while he is in Indian custody.

## POMDP — Optimal Policy

- **Optimal action:** `monitor_isi_countermeasures_against_rana_testimony`
- V(b): `1.953`
- P(mission success): `50.0%`
- P(cover intact): `100.0%`

| Action | Q(b, a) |
|---|---|
| `monitor_isi_countermeasures_against_rana_testimony` ← OPTIMAL | 1.953 |
| `map_rana_network_for_remaining_26_11_figures` | 1.755 |
| `coordinate_rana_testimony_with_headley_us_records` | 1.705 |
| `provide_nia_intelligence_briefing_on_rana_knowledge` | 1.555 |
| `identify_isi_figures_rana_can_name_preemptively` | 1.555 |

## Critical Path (CPM/PERT)

- Path: `rana_knowledge_map` → `26_11_remaining_chain`
- Total: **40 d**  →  Optimal: **32 d**  (save 8 d)
- Bottleneck: `26_11_remaining_chain`
- Parallelisable: `rana_knowledge_map` ‖ `isi_countermeasures_monitor`

## Value of Information

- Total entropy: **1.68 bits**
- Top target: `Names of ISI officers Rana has personal knowledge of beyond Major Iqbal`

| Rank | Target | VoI (bits) | Effort | Recommendation |
|---|---|---|---|---|
| 1 | Names of ISI officers Rana has personal knowledge of beyond Major Iqbal | 1.59 | 7.0 | Low priority — defer; access difficulty (7.0) outweighs VoI (1.59 bits) |
| 2 | Which ISI officers are activated to suppress Rana's testimony — reveals who feels most exposed | 1.47 | 8.5 | Low priority — defer; access difficulty (8.5) outweighs VoI (1.47 bits) |

## Stackelberg Equilibrium

- Handler commits to: `monitor_isi_countermeasures_against_rana_testimony`
- Operative best response: `monitor_isi_countermeasures_against_rana_testimony`
- Adversary counter: `coordinate_rana_testimony_with_headley_us_records`
- Indian payoff: `0.715`
- Commitment value vs Nash: `+0.172`

## Shapley Values — Asset Coalition

| Actor | φ | Defection incentive |
|---|---|---|
| ajay_sanyal | 0.920 | -0.000 |
| us_trump_administration | 0.700 | 0.000 |

## Monte Carlo Simulation

- Rollouts per arm: 2000
- Actual (monitor_isi_countermeasures_against_rana_testimony): P(success)=**100.0%**  [99.8%–100.0%]
- Optimal (monitor_isi_countermeasures_against_rana_testimony): P(success)=**100.0%**  [99.8%–100.0%]
- Δ = **+0.0%** if optimal path taken
- Key causal lever: `monitor_isi_countermeasures_against_rana_testimony → isi_countermeasures_mapped  (p=0.85)`

## Threat Scores (SNA)

| Actor | Score | Betweenness | Eigenvector | High-threat |
|---|---|---|---|---|
| isi_legal_suppression | 4.000 | 0.000 | 0.000 | no |

## Warnings

- state_node: using char.state_by_act['film3_act2'] over TP state_vector
- adversary_node: no high_threat_actors set — using all adversaries with capability >= 7.0 (['isi_legal_suppression'])
- narrator_node: ANTHROPIC_API_KEY not set — using template fallback
