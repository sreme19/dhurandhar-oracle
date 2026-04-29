# Oracle briefing — `hamza` / `yalina-identity-exposure`

> Yalina discovers Hamza's true identity: Jaskirat Singh Rangi, an Indian RAW operative. The trigger is ambiguous — years of small inconsistencies, a document she finds, or a moment during the ISI-Iqbal escalation when Hamza's reactions don't fit the man she married. Their son Zayan is in the household. Yalina holds the key to Hamza's survival (she could expose him to ISI/Pakistan authorities) or his mission (she could protect him). Her choice — and Hamza's response when confronted — is the film's central emotional turning point. The decision calculus is not tactical but moral: what does Hamza owe the woman he has genuinely loved under false pretenses for over a decade?

## POMDP — Optimal Policy

- **Optimal action:** `confess_to_yalina_appeal_to_love_and_zayan`
- V(b): `-160.249`
- P(mission success): `0.0%`
- P(cover intact): `0.0%`

| Action | Q(b, a) |
|---|---|
| `deny_and_maintain_cover_gaslight` | -160.236 |
| `preemptively_neutralise_yalina_as_threat` | -160.236 |
| `confess_to_yalina_appeal_to_love_and_zayan` ← OPTIMAL | -160.249 |
| `confess_and_begin_joint_exfil_plan` | -162.336 |
| `request_sanyal_emergency_extraction` | -162.336 |

## Critical Path (CPM/PERT)

- Path: `yalina_management` → `major_iqbal_operation_continue`
- Total: **36 d**  →  Optimal: **33 d**  (save 2 d)
- Bottleneck: `major_iqbal_operation_continue`
- Parallelisable: `yalina_management` ‖ `zayan_protection`

## Value of Information

- Total entropy: **1.60 bits**
- Top target: `Whether Yalina will protect or expose Hamza — read from her psychological state`

| Rank | Target | VoI (bits) | Effort | Recommendation |
|---|---|---|---|---|
| 1 | Whether Yalina will protect or expose Hamza — read from her psychological state | 1.58 | 5.5 | Low priority — defer; access difficulty (5.5) outweighs VoI (1.59 bits) |
| 2 | Whether ASP Omar Haider will escalate to ISI or handle at local police level | 1.44 | 6.0 | Low priority — defer; access difficulty (6.0) outweighs VoI (1.44 bits) |

## Shapley Values — Asset Coalition

| Actor | φ | Defection incentive |
|---|---|---|
| rizwan_shah | 0.920 | 0.000 |
| ajay_sanyal | 0.900 | 0.000 |

## Monte Carlo Simulation

- Rollouts per arm: 2000
- Actual (confess_to_yalina_appeal_to_love_and_zayan): P(success)=**100.0%**  [99.8%–100.0%]
- Optimal (confess_to_yalina_appeal_to_love_and_zayan): P(success)=**100.0%**  [99.8%–100.0%]
- Δ = **+0.0%** if optimal path taken
- Key causal lever: `confess_to_yalina_appeal_to_love_and_zayan → zayan_safety_secured  (p=0.75)`

## Threat Scores (SNA)

| Actor | Score | Betweenness | Eigenvector | High-threat |
|---|---|---|---|---|
| yalina_jamali | 3.596 | 0.083 | 0.423 | no |
| asp_omar_haider | 2.963 | 0.000 | 0.107 | no |

## Warnings

- adversary_node: no active adversaries — skipping Stackelberg
- narrator_node: ANTHROPIC_API_KEY not set — using template fallback
