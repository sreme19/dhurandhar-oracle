# Oracle briefing — `hamza` / `major-iqbal-madrassa-siege`

> Hamza has located Major Iqbal's operational compound — a madrassa network in Karachi used as a Mujahideen staging ground and ISI safe house. Rizwan Shah coordinates a strike on the compound (BUF — disguised Pakistan Rangers — are the cover force). Hamza must decide how to approach the final confrontation: lead the assault directly and risk capture, direct from a remote position, or attempt a negotiated extraction of Major Iqbal (live capture for intelligence) versus simple elimination. This is the decisive kinetic engagement of Film 2.

## POMDP — Optimal Policy

- **Optimal action:** `attempt_live_capture_iqbal_priority`
- V(b): `-152.296`
- P(mission success): `0.0%`
- P(cover intact): `0.0%`

| Action | Q(b, a) |
|---|---|
| `attempt_live_capture_iqbal_priority` ← OPTIMAL | -152.296 |
| `lead_assault_direct_command` | -152.681 |
| `direct_from_remote_position_rizwan_leads` | -152.681 |
| `abort_negotiate_diplomatic_channel` | -152.681 |
| `strike_compound_eliminate_all` | -154.781 |

## Critical Path (CPM/PERT)

- Path: `compound_layout_final` → `execute_compound_assault` → `iqbal_neutralised`
- Total: **5 d**  →  Optimal: **3 d**  (save 2 d)
- Bottleneck: `iqbal_neutralised`
- Parallelisable: `compound_layout_final` ‖ `buf_coordinate`

## Value of Information

- Total entropy: **1.65 bits**
- Top target: `Major Iqbal's pre-planned escape routes from compound`

| Rank | Target | VoI (bits) | Effort | Recommendation |
|---|---|---|---|---|
| 1 | Major Iqbal's pre-planned escape routes from compound | 1.57 | 7.0 | Low priority — defer; access difficulty (7.0) outweighs VoI (1.57 bits) |
| 2 | How quickly ISI can reinforce the compound after assault begins | 1.45 | 7.5 | Low priority — defer; access difficulty (7.5) outweighs VoI (1.45 bits) |

## Stackelberg Equilibrium

- Handler commits to: `attempt_live_capture_iqbal_priority`
- Operative best response: `attempt_live_capture_iqbal_priority`
- Adversary counter: `abort_negotiate_diplomatic_channel`
- Indian payoff: `0.715`
- Commitment value vs Nash: `+0.172`

## Shapley Values — Asset Coalition

| Actor | φ | Defection incentive |
|---|---|---|
| rizwan_shah | 0.950 | 0.000 |
| ajay_sanyal | 0.900 | -0.000 |

## Monte Carlo Simulation

- Rollouts per arm: 2000
- Actual (attempt_live_capture_iqbal_priority): P(success)=**100.0%**  [99.8%–100.0%]
- Optimal (attempt_live_capture_iqbal_priority): P(success)=**100.0%**  [99.8%–100.0%]
- Δ = **+0.0%** if optimal path taken
- Key causal lever: `attempt_live_capture_iqbal_priority → isi_identifies_hamza_post_assault  (p=0.70)`

## Threat Scores (SNA)

| Actor | Score | Betweenness | Eigenvector | High-threat |
|---|---|---|---|---|
| major_iqbal | 4.500 | 0.000 | 0.000 | no |

## Warnings

- adversary_node: no high_threat_actors set — using all adversaries with capability >= 7.0 (['major_iqbal'])
- narrator_node: ANTHROPIC_API_KEY not set — using template fallback
