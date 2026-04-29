# Oracle briefing — `rizwan_shah` / `balakot-airstrike-abhinandan`

> February 26-28, 2019. Operation Bandar: 20 IAF Mirage 2000 fighters strike Markaz Subhan Allah, Balakot, Khyber Pakhtunkhwa at 0330 hours, dropping 1,000kg SPICE-2000 bombs. First Indian air strike on Pakistani territory since 1971. The next morning, PAF retaliates — F-16s enter J&K airspace. In the dogfight, Wing Commander Abhinandan Varthaman's MiG-21 Bison shoots down a PAF F-16 (India's claim) before his aircraft is hit by a AMRAAM missile. He ejects over PoK, is captured by Pakistani villagers, handed to the Pakistani Army. The world watches as a nuclear-armed standoff hangs on 60 hours of diplomatic pressure. Rizwan Shah, blown from his Pakistan position post-strike, is now running exit intelligence operations — and must assess: will Pakistan return Abhinandan as a 'peace gesture' (ceasefire signal) or hold him to extract concessions?

## POMDP — Optimal Policy

- **Optimal action:** `provide_nuclear_threshold_signalling_intelligence`
- V(b): `1.905`
- P(mission success): `50.0%`
- P(cover intact): `100.0%`

| Action | Q(b, a) |
|---|---|
| `provide_nuclear_threshold_signalling_intelligence` ← OPTIMAL | 1.905 |
| `assess_pakistan_intent_abhinandan_return_or_leverage` | 1.710 |
| `assess_us_saudi_back_channel_effectiveness` | 1.710 |
| `monitor_paf_next_sortie_planning_continued_escalation` | 1.510 |
| `exfiltrate_through_iran_corridor_cover_blown` | 1.110 |

## Critical Path (CPM/PERT)

- Path: `rizwan_exfiltration_balakot`
- Total: **6 d**  →  Optimal: **4 d**  (save 2 d)
- Bottleneck: `rizwan_exfiltration_balakot`
- Parallelisable: `abhinandan_return_assess` ‖ `nuclear_signalling_monitor_balakot`, `abhinandan_return_assess` ‖ `paf_escalation_assess`, `paf_escalation_assess` ‖ `nuclear_signalling_monitor_balakot`, `rizwan_exfiltration_balakot` ‖ `abhinandan_return_assess`

## Value of Information

- Total entropy: **1.24 bits**
- Top target: `Whether Pakistan's GHQ has decided to release Abhinandan unconditionally or is seeking concessions`

| Rank | Target | VoI (bits) | Effort | Recommendation |
|---|---|---|---|---|
| 1 | Whether Pakistan's GHQ has decided to release Abhinandan unconditionally or is seeking concessions | 1.23 | 7.0 | Low priority — defer; access difficulty (7.0) outweighs VoI (1.23 bits) |
| 2 | Whether PAF has authorised follow-on sorties and the intended target set if India retaliates further | 1.22 | 9.0 | Low priority — defer; access difficulty (9.0) outweighs VoI (1.22 bits) |
| 3 | Whether Pakistan's National Command Authority has activated any nuclear readiness protocols | 1.23 | 10.0 | Low priority — defer; access difficulty (10.0) outweighs VoI (1.23 bits) |

## Stackelberg Equilibrium

- Handler commits to: `provide_nuclear_threshold_signalling_intelligence`
- Operative best response: `provide_nuclear_threshold_signalling_intelligence`
- Adversary counter: `us_trump_administration_mediator: monitor_paf_next_sortie_planning_continued_escalation`
- Indian payoff: `0.597`
- Commitment value vs Nash: `+0.079`

## Shapley Values — Asset Coalition

| Actor | φ | Defection incentive |
|---|---|---|
| ajay_sanyal | 0.920 | 0.000 |

## Monte Carlo Simulation

- Rollouts per arm: 2000
- Actual (provide_nuclear_threshold_signalling_intelligence): P(success)=**100.0%**  [99.8%–100.0%]
- Optimal (provide_nuclear_threshold_signalling_intelligence): P(success)=**100.0%**  [99.8%–100.0%]
- Δ = **+0.0%** if optimal path taken
- Key causal lever: `provide_nuclear_threshold_signalling_intelligence → nuclear_threshold_signalling_confirmed  (p=0.20)`

## Threat Scores (SNA)

| Actor | Score | Betweenness | Eigenvector | High-threat |
|---|---|---|---|---|
| us_trump_administration_mediator | 4.750 | 0.000 | 0.000 | no |
| ghq_imran_govt_split | 4.500 | 0.000 | 0.000 | no |

## Warnings

- state_node: using char.state_by_act['film3_act3'] over TP state_vector
- adversary_node: no high_threat_actors set — using all adversaries with capability >= 7.0 (['ghq_imran_govt_split', 'us_trump_administration_mediator'])
- adversary_node: multi-adversary Stackelberg over ['ghq_imran_govt_split', 'us_trump_administration_mediator']
- narrator_node: ANTHROPIC_API_KEY not set — using template fallback
