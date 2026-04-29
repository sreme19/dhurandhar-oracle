# Oracle briefing — `hamza` / `ltf-raid-cover-crisis`

> SP Chaudhry Aslam's Lyari Task Force launches a wave of raids across PAC-linked businesses, including the juice shop area where Hamza operates as a waiter. LTF officers begin pulling in 'new faces' for interrogation. Mohammed Aalam's cover is under pressure. Hamza, now mid-embedded in Dakait's trust network, must navigate an LTF interrogation without triggering either Aslam's suspicion (who could unmask him as an Indian agent) or Dakait's paranoia (who would suspect Hamza turned informant if he was released too easily from LTF custody).

## POMDP — Optimal Policy

- **Optimal action:** `use_handler_aalam_to_signal_delhi_abort`
- V(b): `-44.291`
- P(mission success): `40.0%`
- P(cover intact): `77.5%`

| Action | Q(b, a) |
|---|---|
| `use_handler_aalam_to_signal_delhi_abort` ← OPTIMAL | -44.291 |
| `warn_dakait_network_earn_trust` | -45.248 |
| `submit_to_ltf_interrogation_maintain_cover` | -45.315 |
| `attempt_covert_contact_with_sp_aslam` | -45.448 |
| `flee_before_raid_reaches_area` | -47.333 |

## Critical Path (CPM/PERT)

- Path: `build_trust_dakait` → `gather_political_intel`
- Total: **90 d**  →  Optimal: **81 d**  (save 9 d)
- Bottleneck: `gather_political_intel`
- Parallelisable: `build_trust_dakait` ‖ `ltf_survival_protocol`, `aalam_cover_preserve` ‖ `ltf_survival_protocol`

## Value of Information

- Total entropy: **1.88 bits**
- Top target: `Dakait's current suspicion level toward Hamza following LTF crisis`

| Rank | Target | VoI (bits) | Effort | Recommendation |
|---|---|---|---|---|
| 1 | Dakait's current suspicion level toward Hamza following LTF crisis | 1.70 | 5.0 | Low priority — defer; access difficulty (5.0) outweighs VoI (1.70 bits) |
| 2 | Identity of LTF informant inside Dakait's PAC network | 1.22 | 6.0 | Low priority — defer; access difficulty (6.0) outweighs VoI (1.22 bits) |
| 3 | Whether SP Aslam can be approached for covert cooperation or is a pure adversary | 1.32 | 7.5 | Low priority — defer; access difficulty (7.5) outweighs VoI (1.32 bits) |

## Stackelberg Equilibrium

- Handler commits to: `use_handler_aalam_to_signal_delhi_abort`
- Operative best response: `use_handler_aalam_to_signal_delhi_abort`
- Adversary counter: `rehman_dakait: attempt_covert_contact_with_sp_aslam`
- Indian payoff: `0.574`
- Commitment value vs Nash: `+0.114`

## Shapley Values — Asset Coalition

| Actor | φ | Defection incentive |
|---|---|---|
| mohammed_aalam | 0.850 | 0.000 |
| ajay_sanyal | 0.800 | 0.000 |

## Monte Carlo Simulation

- Rollouts per arm: 2000
- Actual (use_handler_aalam_to_signal_delhi_abort): P(success)=**100.0%**  [99.8%–100.0%]
- Optimal (use_handler_aalam_to_signal_delhi_abort): P(success)=**100.0%**  [99.8%–100.0%]
- Δ = **+0.0%** if optimal path taken
- Key causal lever: `use_handler_aalam_to_signal_delhi_abort → mission_abort  (p=0.85)`

## Threat Scores (SNA)

| Actor | Score | Betweenness | Eigenvector | High-threat |
|---|---|---|---|---|
| rehman_dakait | 4.250 | 0.000 | 0.000 | no |
| sp_choudhary_aslam | 3.750 | 0.000 | 0.000 | no |

## Warnings

- state_node: using char.state_by_act['film1_act2'] over TP state_vector
- adversary_node: no high_threat_actors set — using all adversaries with capability >= 7.0 (['sp_choudhary_aslam', 'rehman_dakait'])
- adversary_node: multi-adversary Stackelberg over ['sp_choudhary_aslam', 'rehman_dakait']
- narrator_node: ANTHROPIC_API_KEY not set — using template fallback
