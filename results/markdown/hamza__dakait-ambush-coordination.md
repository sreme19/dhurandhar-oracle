# Oracle briefing — `hamza` / `dakait-ambush-coordination`

> Following 26/11, Hamza has extracted the Dakait-Jamali-ISI evidence. Mission objective achieved. Hamza now engineers Rehman Dakait's elimination by coordinating secretly with SP Chaudhry Aslam's LTF. He must lure Dakait into a jungle ambush while maintaining his loyal-lieutenant performance inside the PAC network. This is the most operationally delicate moment: one slip in front of Dakait, and the extraction dies with Hamza. One misfire in coordinating with Aslam, and Hamza is either shot by LTF or exposed as an Indian agent by Aslam using him as a bargaining chip with ISI.

## POMDP — Optimal Policy

- **Optimal action:** `abort_ambush_protect_yalina`
- V(b): `-46.169`
- P(mission success): `42.9%`
- P(cover intact): `84.0%`

| Action | Q(b, a) |
|---|---|
| `abort_ambush_protect_yalina` ← OPTIMAL | -46.169 |
| `lure_dakait_to_ambush_coordinate_with_aslam` | -46.727 |
| `provide_intel_to_aslam_without_direct_involvement` | -47.078 |
| `attempt_to_turn_dakait_as_informant_instead` | -47.520 |
| `exfiltrate_first_let_aslam_act_independently` | -48.767 |

## Critical Path (CPM/PERT)

- Path: `lure_dakait` → `post_dakait_cover_maintain` → `safe_exfil`
- Total: **15 d**  →  Optimal: **10 d**  (save 5 d)
- Bottleneck: `safe_exfil`
- Parallelisable: `lure_dakait` ‖ `coordinate_aslam_ltf`, `evidence_package_exfil` ‖ `lure_dakait`, `evidence_package_exfil` ‖ `coordinate_aslam_ltf`

## Value of Information

- Total entropy: **1.71 bits**
- Top target: `Dakait's route on the day of the planned ambush`

| Rank | Target | VoI (bits) | Effort | Recommendation |
|---|---|---|---|---|
| 1 | Dakait's route on the day of the planned ambush | 1.63 | 2.0 | Medium priority — schedule after cover deepening |
| 2 | Who in PAC would suspect Hamza's role in Dakait's death (Uzair Baloch threat level) | 1.29 | 5.0 | Low priority — defer; access difficulty (5.0) outweighs VoI (1.29 bits) |
| 3 | Confirmation that SP Aslam will execute ambush without exposing Hamza as Indian agent | 1.54 | 6.0 | Low priority — defer; access difficulty (6.0) outweighs VoI (1.54 bits) |

## Stackelberg Equilibrium

- Handler commits to: `abort_ambush_protect_yalina`
- Operative best response: `abort_ambush_protect_yalina`
- Adversary counter: `rehman_dakait: attempt_to_turn_dakait_as_informant_instead`
- Indian payoff: `0.574`
- Commitment value vs Nash: `+0.114`

## Shapley Values — Asset Coalition

| Actor | φ | Defection incentive |
|---|---|---|
| hamza | 0.900 | 0.000 |
| mohammed_aalam | 0.880 | -0.000 |
| ajay_sanyal | 0.850 | 0.000 |
| yalina_jamali | 0.850 | 0.000 |

## Monte Carlo Simulation

- Rollouts per arm: 2000
- Actual (abort_ambush_protect_yalina): P(success)=**100.0%**  [99.8%–100.0%]
- Optimal (abort_ambush_protect_yalina): P(success)=**100.0%**  [99.8%–100.0%]
- Δ = **+0.0%** if optimal path taken
- Key causal lever: `abort_ambush_protect_yalina → yalina_protected  (p=0.90)`

## Threat Scores (SNA)

| Actor | Score | Betweenness | Eigenvector | High-threat |
|---|---|---|---|---|
| rehman_dakait | 4.947 | 0.000 | 0.349 | no |
| sp_choudhary_aslam | 4.176 | 0.000 | 0.213 | no |

## Warnings

- state_node: using char.state_by_act['film1_act3'] over TP state_vector
- adversary_node: no high_threat_actors set — using all adversaries with capability >= 7.0 (['rehman_dakait', 'sp_choudhary_aslam'])
- adversary_node: multi-adversary Stackelberg over ['rehman_dakait', 'sp_choudhary_aslam']
- narrator_node: ANTHROPIC_API_KEY not set — using template fallback
