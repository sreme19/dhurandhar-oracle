# Oracle briefing — `rizwan_shah` / `doklam-china-second-front`

> June 18 – August 28, 2017. China's PLA begins constructing a road across the Doklam plateau — Bhutanese territory at the India-China-Bhutan tri-junction — toward the Jampheri Ridge, which overlooks India's Siliguri Corridor (the 27km 'Chicken's Neck' connecting Northeast India to the mainland). Indian Army intervenes on Bhutan's behalf per the 1949 India-Bhutan treaty, blocking the road construction. A 73-day military standoff ensues — Indian and Chinese troops in eyeball-to-eyeball positions at 14,000 feet. For Rizwan Shah, embedded in Pakistan-focused ISI networks, this represents a doctrinal shift: India now faces a coordinated two-front pressure — ISI-Pakistan in the west, PLA-China in the east. The critical intelligence question: is Doklam ISI-coordinated with China, or an independent Chinese move that ISI will exploit?

## POMDP — Optimal Policy

- **Optimal action:** `identify_jem_escalation_plans_during_doklam_window`
- V(b): `1.953`
- P(mission success): `50.0%`
- P(cover intact): `100.0%`

| Action | Q(b, a) |
|---|---|
| `identify_jem_escalation_plans_during_doklam_window` ← OPTIMAL | 1.953 |
| `assess_china_isi_coordination_doklam_timing` | 1.755 |
| `map_isi_exploitation_of_doklam_two_front_pressure` | 1.755 |
| `monitor_cpec_intelligence_sharing_pakistan_china` | 1.555 |
| `provide_intelligence_on_chinese_pla_doctrine_signals` | 1.555 |

## Critical Path (CPM/PERT)

- Path: `china_isi_coordination_confirm` → `cpec_intelligence_sharing_map`
- Total: **97 d**  →  Optimal: **82 d**  (save 16 d)
- Bottleneck: `cpec_intelligence_sharing_map`
- Parallelisable: `china_isi_coordination_confirm` ‖ `isi_kashmir_escalation_doklam_window`

## Value of Information

- Total entropy: **1.58 bits**
- Top target: `Specific JeM/LeT attack plan targeting the Doklam distraction window — any planned strikes in J&K or mainland India`

| Rank | Target | VoI (bits) | Effort | Recommendation |
|---|---|---|---|---|
| 1 | Specific JeM/LeT attack plan targeting the Doklam distraction window — any planned strikes in J&K or mainland India | 1.42 | 7.5 | Low priority — defer; access difficulty (7.5) outweighs VoI (1.42 bits) |
| 2 | ISI-PLA communication confirming whether Doklam timing was coordinated with Pakistan's post-Uri recovery phase | 1.45 | 9.5 | Low priority — defer; access difficulty (9.5) outweighs VoI (1.45 bits) |

## Stackelberg Equilibrium

- Handler commits to: `identify_jem_escalation_plans_during_doklam_window`
- Operative best response: `identify_jem_escalation_plans_during_doklam_window`
- Adversary counter: `pla_western_theatre_command: map_isi_exploitation_of_doklam_two_front_pressure`
- Indian payoff: `0.676`
- Commitment value vs Nash: `+0.173`

## Shapley Values — Asset Coalition

| Actor | φ | Defection incentive |
|---|---|---|
| bhutan | 0.900 | 0.000 |
| ajay_sanyal | 0.880 | 0.000 |
| pakistan | 0.820 | 0.000 |

## Monte Carlo Simulation

- Rollouts per arm: 2000
- Actual (identify_jem_escalation_plans_during_doklam_window): P(success)=**100.0%**  [99.8%–100.0%]
- Optimal (identify_jem_escalation_plans_during_doklam_window): P(success)=**100.0%**  [99.8%–100.0%]
- Δ = **+0.0%** if optimal path taken
- Key causal lever: `identify_jem_escalation_plans_during_doklam_window → kashmir_attack_during_doklam_standoff  (p=0.65)`

## Threat Scores (SNA)

| Actor | Score | Betweenness | Eigenvector | High-threat |
|---|---|---|---|---|
| pla_western_theatre_command | 4.750 | 0.000 | 0.000 | no |
| isi_two_front_exploitation | 4.250 | 0.000 | 0.000 | no |

## Warnings

- state_node: using char.state_by_act['film3_act2'] over TP state_vector
- adversary_node: no high_threat_actors set — using all adversaries with capability >= 7.0 (['pla_western_theatre_command', 'isi_two_front_exploitation'])
- adversary_node: multi-adversary Stackelberg over ['pla_western_theatre_command', 'isi_two_front_exploitation']
- narrator_node: ANTHROPIC_API_KEY not set — using template fallback
