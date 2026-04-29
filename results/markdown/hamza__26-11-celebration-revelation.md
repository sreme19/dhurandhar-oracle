# Oracle briefing — `hamza` / `26-11-celebration-revelation`

> November 26, 2008. While Mumbai burns 1,200 km away, Hamza witnesses Rehman Dakait celebrating the 26/11 attacks with ISI handler Major Iqbal inside Dakait's Lyari compound. Hamza had previously passed intelligence to Aalam about the ISI-Lyari-LeT network — intelligence that could have warned of the attack. Now he watches the men he has spent years infiltrating toast an atrocity he could have prevented. This is the moral crisis of Film 1: Hamza has the mission's primary target (Dakait-ISI link) confirmed, the intelligence failure exposed, and the primary adversary (Major Iqbal) identified in person — but acting now would blow everything. He must maintain his cover through his own grief and rage.

## POMDP — Optimal Policy

- **Optimal action:** `maintain_cover_report_iqbal_identification`
- V(b): `-50.146`
- P(mission success): `42.9%`
- P(cover intact): `84.0%`

| Action | Q(b, a) |
|---|---|
| `maintain_cover_report_iqbal_identification` ← OPTIMAL | -50.146 |
| `photograph_evidence_maintain_cover_continue` | -50.302 |
| `attempt_immediate_abort_signal` | -50.922 |
| `signal_delhi_evidence_request_extraction` | -52.545 |
| `confront_dakait_blow_cover` | -55.082 |

## Critical Path (CPM/PERT)

- Path: `iqbal_identity_confirm` → `expose_political_link_documentary` → `exfil_evidence_package`
- Total: **51 d**  →  Optimal: **51 d**  (save 0 d)
- Bottleneck: `exfil_evidence_package`

## Value of Information

- Total entropy: **1.71 bits**
- Top target: `Visual/photographic confirmation of Major Iqbal's identity`

| Rank | Target | VoI (bits) | Effort | Recommendation |
|---|---|---|---|---|
| 1 | Visual/photographic confirmation of Major Iqbal's identity | 1.68 | 0.5 | High priority — gather immediately via: maintain_cover_report_iqbal_identification, photograph_evidence_maintain_cover_continue |
| 2 | Documentary evidence of Dakait-Iqbal operational meeting (26/11 nexus) | 1.63 | 4.0 | Low priority — defer; access difficulty (4.0) outweighs VoI (1.63 bits) |
| 3 | Intelligence on Major Iqbal's next planned operation (post-26/11) | 1.54 | 9.0 | Low priority — defer; access difficulty (9.0) outweighs VoI (1.54 bits) |

## Stackelberg Equilibrium

- Handler commits to: `maintain_cover_report_iqbal_identification`
- Operative best response: `maintain_cover_report_iqbal_identification`
- Adversary counter: `major_iqbal: photograph_evidence_maintain_cover_continue`
- Indian payoff: `0.754`
- Commitment value vs Nash: `+0.207`

## Shapley Values — Asset Coalition

| Actor | φ | Defection incentive |
|---|---|---|
| mohammed_aalam | 0.850 | 0.000 |
| ajay_sanyal | 0.800 | 0.000 |

## Monte Carlo Simulation

- Rollouts per arm: 2000
- Actual (maintain_cover_report_iqbal_identification): P(success)=**100.0%**  [99.8%–100.0%]
- Optimal (maintain_cover_report_iqbal_identification): P(success)=**100.0%**  [99.8%–100.0%]
- Δ = **+0.0%** if optimal path taken
- Key causal lever: `maintain_cover_report_iqbal_identification → iqbal_identity_product_delivered  (p=0.90)`

## Threat Scores (SNA)

| Actor | Score | Betweenness | Eigenvector | High-threat |
|---|---|---|---|---|
| major_iqbal | 4.500 | 0.000 | 0.000 | no |
| rehman_dakait | 4.250 | 0.000 | 0.000 | no |

## Warnings

- state_node: using char.state_by_act['film1_act3'] over TP state_vector
- adversary_node: no high_threat_actors set — using all adversaries with capability >= 7.0 (['major_iqbal', 'rehman_dakait'])
- adversary_node: multi-adversary Stackelberg over ['major_iqbal', 'rehman_dakait']
- narrator_node: ANTHROPIC_API_KEY not set — using template fallback
