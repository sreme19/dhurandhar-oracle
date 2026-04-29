# Oracle briefing — `rizwan_shah` / `rizwan-partnership-activation`

> Ajay Sanyal introduces Rizwan Shah as Hamza's operational partner for Film 2. Rizwan is a trained RAW officer who has been embedded in the Karachi criminal underworld independently — not a deep-cover operative like Hamza, but an elite intelligence officer with direct field experience. The turning point: how does Hamza (13 years undercover, autonomous, emotionally scarred) integrate a new partner who represents the institutional apparatus he has operated outside? The partnership's dynamic — trust level, division of targets, information sharing — will determine the operation's architecture.

## POMDP — Optimal Policy

- **Optimal action:** `assign_rizwan_ficn_track_hamza_retains_iqbal_track`
- V(b): `4.448`
- P(mission success): `48.4%`
- P(cover intact): `96.0%`

| Action | Q(b, a) |
|---|---|
| `assign_rizwan_ficn_track_hamza_retains_iqbal_track` ← OPTIMAL | 4.448 |
| `integrate_rizwan_full_partnership_equal_access` | 4.053 |
| `integrate_rizwan_limited_access_compartmentalised` | 4.053 |
| `request_sanyal_solo_operation_no_rizwan` | 4.008 |
| `test_rizwan_loyalty_before_full_integration` | 3.993 |

## Critical Path (CPM/PERT)

- Path: `rizwan_cover_audit` → `target_assignment` → `khanani_initial_penetration`
- Total: **110 d**  →  Optimal: **66 d**  (save 44 d)
- Bottleneck: `khanani_initial_penetration`
- Parallelisable: `rizwan_comms_establish` ‖ `rizwan_cover_audit`, `zahoor_mistry_operation` ‖ `khanani_initial_penetration`

## Value of Information

- Total entropy: **1.63 bits**
- Top target: `Security audit of Rizwan Shah's existing Karachi cover`

| Rank | Target | VoI (bits) | Effort | Recommendation |
|---|---|---|---|---|
| 1 | Security audit of Rizwan Shah's existing Karachi cover | 1.47 | 3.0 | Low priority — defer; access difficulty (3.0) outweighs VoI (1.47 bits) |
| 2 | Current ISI counter-intelligence sweeps targeting Indian agents in Karachi | 1.44 | 7.5 | Low priority — defer; access difficulty (7.5) outweighs VoI (1.44 bits) |
| 3 | Javed Khanani's operational base and daily routine | 1.31 | 7.0 | Low priority — defer; access difficulty (7.0) outweighs VoI (1.31 bits) |

## Stackelberg Equilibrium

- Handler commits to: `assign_rizwan_ficn_track_hamza_retains_iqbal_track`
- Operative best response: `assign_rizwan_ficn_track_hamza_retains_iqbal_track`
- Adversary counter: `test_rizwan_loyalty_before_full_integration`
- Indian payoff: `0.715`
- Commitment value vs Nash: `+0.172`

## Shapley Values — Asset Coalition

| Actor | φ | Defection incentive |
|---|---|---|
| ajay_sanyal | 1.780 | 0.000 |
| sushant_bansal | 0.750 | 0.000 |
| rizwan_shah | 0.650 | 0.000 |

## Monte Carlo Simulation

- Rollouts per arm: 2000
- Actual (assign_rizwan_ficn_track_hamza_retains_iqbal_track): P(success)=**100.0%**  [99.8%–100.0%]
- Optimal (assign_rizwan_ficn_track_hamza_retains_iqbal_track): P(success)=**100.0%**  [99.8%–100.0%]
- Δ = **+0.0%** if optimal path taken
- Key causal lever: `assign_rizwan_ficn_track_hamza_retains_iqbal_track → dual_track_operation_efficient  (p=0.85)`

## Threat Scores (SNA)

| Actor | Score | Betweenness | Eigenvector | High-threat |
|---|---|---|---|---|
| major_iqbal | 4.500 | 0.000 | 0.000 | no |

## Warnings

- state_node: using char.state_by_act['film2_act1'] over TP state_vector
- adversary_node: no high_threat_actors set — using all adversaries with capability >= 7.0 (['major_iqbal'])
- narrator_node: ANTHROPIC_API_KEY not set — using template fallback
