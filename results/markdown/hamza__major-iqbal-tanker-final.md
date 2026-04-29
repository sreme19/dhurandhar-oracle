# Oracle briefing — `hamza` / `major-iqbal-tanker-final`

> The final confrontation. Major Iqbal has retreated to a Karachi shipping yard after the madrassa compound assault. Hamza pursues alone — Rizwan is compromised elsewhere. The shipping yard contains a kerosene tanker. Iqbal and Hamza engage in a final duel. Hamza destroys Iqbal's transport vehicle with an RPG. The confrontation ends in a tanker explosion that kills Major Iqbal. The mission's primary objective — eliminating the 26/11 ISI architect — is completed. But Hamza is exposed, wounded, and about to be captured by ISI forces responding to the explosion.

## POMDP — Optimal Policy

- **Optimal action:** `pursue_iqbal_to_shipping_yard_engage_direct`
- V(b): `-152.296`
- P(mission success): `0.0%`
- P(cover intact): `0.0%`

| Action | Q(b, a) |
|---|---|
| `pursue_iqbal_to_shipping_yard_engage_direct` ← OPTIMAL | -152.296 |
| `rpg_tanker_remote_deny_escape` | -152.681 |
| `abort_iqbal_survives_mission_incomplete` | -152.681 |
| `call_for_rizwan_backup_delay` | -152.731 |
| `capture_iqbal_alive_extract` | -154.781 |

## Critical Path (CPM/PERT)

- Path: `iqbal_cornered` → `final_engagement` → `post_engagement_survival`
- Total: **5 d**  →  Optimal: **5 d**  (save 0 d)
- Bottleneck: `post_engagement_survival`

## Value of Information

- Total entropy: **1.68 bits**
- Top target: `Who inherits Iqbal's ISI operational role — successor identification`

| Rank | Target | VoI (bits) | Effort | Recommendation |
|---|---|---|---|---|
| 1 | Who inherits Iqbal's ISI operational role — successor identification | 1.42 | 9.5 | Low priority — defer; access difficulty (9.5) outweighs VoI (1.42 bits) |

## Stackelberg Equilibrium

- Handler commits to: `pursue_iqbal_to_shipping_yard_engage_direct`
- Operative best response: `pursue_iqbal_to_shipping_yard_engage_direct`
- Adversary counter: `major_iqbal: abort_iqbal_survives_mission_incomplete`
- Indian payoff: `0.501`
- Commitment value vs Nash: `+0.076`

## Shapley Values — Asset Coalition

| Actor | φ | Defection incentive |
|---|---|---|
| ajay_sanyal | 0.900 | 0.000 |

## Monte Carlo Simulation

- Rollouts per arm: 2000
- Actual (pursue_iqbal_to_shipping_yard_engage_direct): P(success)=**100.0%**  [99.8%–100.0%]
- Optimal (pursue_iqbal_to_shipping_yard_engage_direct): P(success)=**100.0%**  [99.8%–100.0%]
- Δ = **+0.0%** if optimal path taken
- Key causal lever: `pursue_iqbal_to_shipping_yard_engage_direct → iqbal_killed_mission_complete  (p=0.75)`

## Threat Scores (SNA)

| Actor | Score | Betweenness | Eigenvector | High-threat |
|---|---|---|---|---|
| major_iqbal | 4.500 | 0.000 | 0.000 | no |
| isi_rapid_response | 4.250 | 0.000 | 0.000 | no |

## Warnings

- adversary_node: no high_threat_actors set — using all adversaries with capability >= 7.0 (['major_iqbal', 'isi_rapid_response'])
- adversary_node: multi-adversary Stackelberg over ['major_iqbal', 'isi_rapid_response']
- narrator_node: ANTHROPIC_API_KEY not set — using template fallback
