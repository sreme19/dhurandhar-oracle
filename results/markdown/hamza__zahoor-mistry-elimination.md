# Oracle briefing — `hamza` / `zahoor-mistry-elimination`

> March 2022. Zahoor Mistry — one of the five IC-814 hijackers who walked free in 1999 — has lived under the alias 'Zahid Akhund' in Karachi for 22 years, running a furniture shop. Hamza and Rizwan have located him. The operation: a drive-by elimination on a Karachi street. The turning point is not whether to act — Mistry is a confirmed target — but how: a clean kill that leaves no fingerprints pointing to Indian intelligence, versus a 'capture and extract' that could yield intelligence on remaining IC-814 network but risks triggering ISI counter-response. The film frames the elimination as the first public-facing proof that India's new doctrine is real.

## POMDP — Optimal Policy

- **Optimal action:** `execute_with_intelligence_collection_hybrid`
- V(b): `-49.806`
- P(mission success): `44.5%`
- P(cover intact): `87.5%`

| Action | Q(b, a) |
|---|---|
| `execute_with_intelligence_collection_hybrid` ← OPTIMAL | -49.806 |
| `execute_clean_drive_by_no_fingerprints` | -49.962 |
| `abandon_target_focus_on_iqbal_track` | -49.962 |
| `delay_for_additional_surveillance` | -50.162 |
| `capture_mistry_extract_for_interrogation` | -52.091 |

## Critical Path (CPM/PERT)

- Path: `mistry_routine_map` → `execute_elimination` → `post_op_cover_maintain`
- Total: **32 d**  →  Optimal: **25 d**  (save 8 d)
- Bottleneck: `post_op_cover_maintain`
- Parallelisable: `mistry_routine_map` ‖ `exfil_route_plan`

## Value of Information

- Total entropy: **1.65 bits**
- Top target: `How aggressively ISI responds to Mistry killing — proportional to whether India is suspected`

| Rank | Target | VoI (bits) | Effort | Recommendation |
|---|---|---|---|---|
| 1 | How aggressively ISI responds to Mistry killing — proportional to whether India is suspected | 1.40 | 6.0 | Low priority — defer; access difficulty (6.0) outweighs VoI (1.40 bits) |
| 2 | Other IC-814 hijackers still alive and their current locations | 1.07 | 7.0 | Low priority — defer; access difficulty (7.0) outweighs VoI (1.07 bits) |

## Stackelberg Equilibrium

- Handler commits to: `execute_with_intelligence_collection_hybrid`
- Operative best response: `execute_with_intelligence_collection_hybrid`
- Adversary counter: `abandon_target_focus_on_iqbal_track`
- Indian payoff: `0.715`
- Commitment value vs Nash: `+0.172`

## Shapley Values — Asset Coalition

| Actor | φ | Defection incentive |
|---|---|---|
| ajay_sanyal | 0.900 | 0.000 |
| rizwan_shah | 0.850 | 0.000 |

## Monte Carlo Simulation

- Rollouts per arm: 2000
- Actual (execute_with_intelligence_collection_hybrid): P(success)=**100.0%**  [99.8%–100.0%]
- Optimal (execute_with_intelligence_collection_hybrid): P(success)=**100.0%**  [99.8%–100.0%]
- Δ = **+0.0%** if optimal path taken
- Key causal lever: `execute_with_intelligence_collection_hybrid → mistry_eliminated_clean  (p=0.75)`

## Threat Scores (SNA)

| Actor | Score | Betweenness | Eigenvector | High-threat |
|---|---|---|---|---|
| major_iqbal | 4.500 | 0.000 | 0.000 | no |

## Warnings

- adversary_node: no high_threat_actors set — using all adversaries with capability >= 7.0 (['major_iqbal'])
- narrator_node: ANTHROPIC_API_KEY not set — using template fallback
