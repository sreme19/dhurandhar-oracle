# Oracle briefing — `rizwan_shah` / `surgical-strikes-execution`

> Night of September 28-29, 2016. Indian Para SF — Ghatak platoons of 6 Bihar and 10 Dogra regiments, trained on the terrain — cross the Line of Control and destroy 7 JeM/LeT infiltration launchpads across 4 sectors in PoK. 35-50 militants killed (Indian estimates; Pakistan denies any strikes occurred). DGMO Lt Gen Ranbir Singh makes a public announcement the next morning — the first time India officially acknowledged a cross-LOC operation since 1971. Rizwan Shah, whose ground intelligence formed the targeting package, must now manage the aftermath: ISI is conducting a sweep to identify how India knew exact launchpad locations. His cover is at maximum risk in the 72 hours post-strike.

## POMDP — Optimal Policy

- **Optimal action:** `go_dark_cease_all_communication_72_hours`
- V(b): `-27.350`
- P(mission success): `47.5%`
- P(cover intact): `95.0%`

| Action | Q(b, a) |
|---|---|
| `go_dark_cease_all_communication_72_hours` ← OPTIMAL | -27.350 |
| `exfiltrate_immediately_cover_burned` | -27.580 |
| `feed_isi_false_intelligence_source_misdirection` | -27.690 |
| `maintain_cover_by_expressing_outrage_at_strikes` | -27.980 |
| `continue_operations_assess_strike_effectiveness` | -28.385 |

## Critical Path (CPM/PERT)

- Path: `isi_sweep_survive` → `isi_retaliation_assess_surgical`
- Total: **24 d**  →  Optimal: **14 d**  (save 10 d)
- Bottleneck: `isi_retaliation_assess_surgical`
- Parallelisable: `isi_sweep_survive` ‖ `battle_damage_assess_surgical`, `reposition_cover_narrative` ‖ `isi_sweep_survive`

## Value of Information

- Total entropy: **1.65 bits**
- Top target: `Whether ISI has authorised a retaliatory attack inside India to restore deterrence after the strikes`

| Rank | Target | VoI (bits) | Effort | Recommendation |
|---|---|---|---|---|
| 1 | Whether ISI has authorised a retaliatory attack inside India to restore deterrence after the strikes | 1.57 | 9.0 | Low priority — defer; access difficulty (9.0) outweighs VoI (1.57 bits) |
| 2 | Which ISI counterintelligence team is conducting the post-strike source hunt — and do they have Rizwan's name | 1.63 | 9.5 | Low priority — defer; access difficulty (9.5) outweighs VoI (1.63 bits) |
| 3 | New launchpad locations ISI is establishing post-strike under improved OPSEC | 1.40 | 8.5 | Low priority — defer; access difficulty (8.5) outweighs VoI (1.40 bits) |

## Stackelberg Equilibrium

- Handler commits to: `exfiltrate_immediately_cover_burned`
- Operative best response: `exfiltrate_immediately_cover_burned`
- Adversary counter: `continue_operations_assess_strike_effectiveness`
- Indian payoff: `0.715`
- Commitment value vs Nash: `+0.172`

## Shapley Values — Asset Coalition

| Actor | φ | Defection incentive |
|---|---|---|
| ajay_sanyal | 0.920 | 0.000 |

## Monte Carlo Simulation

- Rollouts per arm: 2000
- Actual (go_dark_cease_all_communication_72_hours): P(success)=**100.0%**  [99.8%–100.0%]
- Optimal (go_dark_cease_all_communication_72_hours): P(success)=**100.0%**  [99.8%–100.0%]
- Δ = **+0.0%** if optimal path taken
- Key causal lever: `go_dark_cease_all_communication_72_hours → cover_survives_isi_sweep  (p=0.80)`

## Threat Scores (SNA)

| Actor | Score | Betweenness | Eigenvector | High-threat |
|---|---|---|---|---|
| isi_counterintelligence_post_strike | 4.500 | 0.000 | 0.000 | no |

## Warnings

- state_node: using char.state_by_act['film3_act2'] over TP state_vector
- adversary_node: no high_threat_actors set — using all adversaries with capability >= 7.0 (['isi_counterintelligence_post_strike'])
- narrator_node: ANTHROPIC_API_KEY not set — using template fallback
