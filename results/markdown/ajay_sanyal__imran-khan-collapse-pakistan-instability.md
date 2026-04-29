# Oracle briefing — `ajay_sanyal` / `imran-khan-collapse-pakistan-instability`

> April 10, 2022 – May 9, 2023. Pakistan's civilian-military compact collapses in real time. PM Imran Khan is ousted via no-confidence vote (April 10, 2022) after the military establishment — specifically Army Chief General Qamar Javed Bajwa — withdraws support. Imran's 'conspiracy' narrative (blaming the US and Bajwa) splits Pakistan's political establishment and the public. Thirteen months later, on May 9, 2023, Imran Khan is arrested on corruption charges. His supporters storm military installations including the Lahore Corps Commander's residence — an unprecedented attack on military property by civilian supporters. The military cracks down. Pakistan's political system is in a death spiral: the military rules but cannot govern; civilian governments cannot survive; the economy is collapsing (IMF bailout crisis). NSA Ajay Sanyal must assess: does Pakistani internal collapse create a strategic opportunity for India, or does it create an unstable nuclear-armed adversary more dangerous than a coherent one?

## POMDP — Optimal Policy

- **Optimal action:** `identify_imran_isi_military_split_intelligence_implications`
- V(b): `1.976`
- P(mission success): `50.0%`
- P(cover intact): `100.0%`

| Action | Q(b, a) |
|---|---|
| `identify_imran_isi_military_split_intelligence_implications` ← OPTIMAL | 1.976 |
| `assess_isi_operational_continuity_through_political_chaos` | 1.778 |
| `evaluate_pakistan_nuclear_command_stability` | 1.778 |
| `map_munir_doctrine_compared_to_bajwa` | 1.778 |
| `assess_domestic_distraction_kashmir_escalation_risk` | 1.778 |

## Critical Path (CPM/PERT)

- Path: `munir_doctrine_map` → `domestic_distraction_escalation_assess`
- Total: **97 d**  →  Optimal: **58 d**  (save 39 d)
- Bottleneck: `domestic_distraction_escalation_assess`
- Parallelisable: `isi_operational_continuity_assess` ‖ `nuclear_command_stability`, `isi_operational_continuity_assess` ‖ `munir_doctrine_map`

## Value of Information

- Total entropy: **1.59 bits**
- Top target: `Whether General Munir has authorised ISI to plan a Kashmir escalation to restore military legitimacy domestically`

| Rank | Target | VoI (bits) | Effort | Recommendation |
|---|---|---|---|---|
| 1 | Whether General Munir has authorised ISI to plan a Kashmir escalation to restore military legitimacy domestically | 1.54 | 9.0 | Low priority — defer; access difficulty (9.0) outweighs VoI (1.54 bits) |
| 2 | Current NCA composition and loyalty chain under Munir — who controls nuclear release authority during political chaos | 1.51 | 10.0 | Low priority — defer; access difficulty (10.0) outweighs VoI (1.51 bits) |
| 3 | Whether Imran Khan possesses operational intelligence from his PM tenure that ISI considers a security threat — leverage for his detention | 1.27 | 8.5 | Low priority — defer; access difficulty (8.5) outweighs VoI (1.27 bits) |

## Stackelberg Equilibrium

- Handler commits to: `identify_imran_isi_military_split_intelligence_implications`
- Operative best response: `identify_imran_isi_military_split_intelligence_implications`
- Adversary counter: `general_asim_munir_coas: evaluate_pakistan_nuclear_command_stability`
- Indian payoff: `0.671`
- Commitment value vs Nash: `+0.087`

## Shapley Values — Asset Coalition

| Actor | φ | Defection incentive |
|---|---|---|
| narendra_modi | 0.980 | 0.000 |
| china | 0.880 | 0.000 |

## Monte Carlo Simulation

- Rollouts per arm: 2000
- Actual (identify_imran_isi_military_split_intelligence_implications): P(success)=**100.0%**  [99.8%–100.0%]
- Optimal (identify_imran_isi_military_split_intelligence_implications): P(success)=**100.0%**  [99.8%–100.0%]
- Δ = **+0.0%** if optimal path taken

## Threat Scores (SNA)

| Actor | Score | Betweenness | Eigenvector | High-threat |
|---|---|---|---|---|
| general_asim_munir_coas | 4.750 | 0.000 | 0.000 | no |
| imran_khan_isi_split | 3.500 | 0.000 | 0.000 | no |

## Warnings

- state_node: using char.state_by_act['film4_act2'] over TP state_vector
- adversary_node: no high_threat_actors set — using all adversaries with capability >= 7.0 (['general_asim_munir_coas', 'imran_khan_isi_split'])
- adversary_node: multi-adversary Stackelberg over ['general_asim_munir_coas', 'imran_khan_isi_split']
- narrator_node: ANTHROPIC_API_KEY not set — using template fallback
