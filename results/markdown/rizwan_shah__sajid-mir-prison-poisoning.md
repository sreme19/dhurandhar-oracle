# Oracle briefing — `rizwan_shah` / `sajid-mir-prison-poisoning`

> December 2023. Sajid Mir — convicted in May 2023 to 15 years for terror financing, the first real conviction of a 26/11 handler — is found poisoned in Central Jail, Dera Ghazi Khan. He is airlifted on ventilator support. The poisoning is unclaimed. Rizwan Shah's mission: determine whether the poisoning is an ISI internal operation (silencing a witness who may have begun cooperating with Indian intelligence via back-channels), a Dhurandhar operation (eliminating a target before Mir could cut a deal), or a factional LeT killing. The answer determines how to respond and whether Mir's intelligence value is now accessible.

## POMDP — Optimal Policy

- **Optimal action:** `confirm_mir_dead_pivot_to_next_target`
- V(b): `5.929`
- P(mission success): `50.0%`
- P(cover intact): `100.0%`

| Action | Q(b, a) |
|---|---|
| `confirm_mir_dead_pivot_to_next_target` ← OPTIMAL | 5.929 |
| `investigate_isi_internal_order_confirm_or_deny` | 5.533 |
| `attempt_prison_contact_mir_before_death` | 5.533 |
| `exploit_isi_internal_conflict_revealed_by_poisoning` | 5.533 |
| `pass_intelligence_to_india_advocate_diplomatic_protest` | 5.333 |

## Critical Path (CPM/PERT)

- Path: `poisoning_attribution` → `isi_internal_fracture_map`
- Total: **90 d**  →  Optimal: **83 d**  (save 8 d)
- Bottleneck: `isi_internal_fracture_map`
- Parallelisable: `poisoning_attribution` ‖ `mir_survival_assessment`

## Value of Information

- Total entropy: **1.76 bits**
- Top target: `Which remaining 26/11 figures ISI may target to suppress evidence (Hafiz Saeed? Sajid Mir's co-conspirators?)`

| Rank | Target | VoI (bits) | Effort | Recommendation |
|---|---|---|---|---|
| 1 | Which remaining 26/11 figures ISI may target to suppress evidence (Hafiz Saeed? Sajid Mir's co-conspirators?) | 1.50 | 8.0 | Low priority — defer; access difficulty (8.0) outweighs VoI (1.50 bits) |
| 2 | Identity of faction that ordered Sajid Mir's poisoning | 1.55 | 8.5 | Low priority — defer; access difficulty (8.5) outweighs VoI (1.55 bits) |
| 3 | What Mir may have told Pakistani investigators or international monitors about ISI 26/11 involvement | 1.62 | 9.0 | Low priority — defer; access difficulty (9.0) outweighs VoI (1.62 bits) |

## Stackelberg Equilibrium

- Handler commits to: `confirm_mir_dead_pivot_to_next_target`
- Operative best response: `confirm_mir_dead_pivot_to_next_target`
- Adversary counter: `exploit_isi_internal_conflict_revealed_by_poisoning`
- Indian payoff: `0.715`
- Commitment value vs Nash: `+0.172`

## Shapley Values — Asset Coalition

| Actor | φ | Defection incentive |
|---|---|---|
| ajay_sanyal | 0.900 | -0.000 |
| sushant_bansal | 0.800 | 0.000 |

## Monte Carlo Simulation

- Rollouts per arm: 2000
- Actual (confirm_mir_dead_pivot_to_next_target): P(success)=**100.0%**  [99.8%–100.0%]
- Optimal (confirm_mir_dead_pivot_to_next_target): P(success)=**100.0%**  [99.8%–100.0%]
- Δ = **+0.0%** if optimal path taken
- Key causal lever: `confirm_mir_dead_pivot_to_next_target → mir_dead_intelligence_lost  (p=0.90)`

## Threat Scores (SNA)

| Actor | Score | Betweenness | Eigenvector | High-threat |
|---|---|---|---|---|
| isi_internal_cleanup_faction | 4.250 | 0.000 | 0.000 | no |

## Warnings

- state_node: using char.state_by_act['film3_act1'] over TP state_vector
- adversary_node: no high_threat_actors set — using all adversaries with capability >= 7.0 (['isi_internal_cleanup_faction'])
- narrator_node: ANTHROPIC_API_KEY not set — using template fallback
