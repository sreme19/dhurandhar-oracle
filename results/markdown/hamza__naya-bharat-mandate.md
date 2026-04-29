# Oracle briefing — `hamza` / `naya-bharat-mandate`

> 2015. Post-2014 election, India's NSA Ajay Sanyal calls Hamza out of his Karachi semi-retirement. The new government's 'Naya Bharat' (New India) doctrine has replaced strategic restraint with a mandate for proactive accountability. Sanyal offers Hamza an expanded mandate: target the 26/11 planners — Major Iqbal, Azam Cheema, Sajid Mir — and simultaneously dismantle the financial infrastructure (FICN/Khanani network, Punjab narco-Khalistan pipeline). Unlike Film 1's institutional-bureaucratic operation, Hamza now has near-autonomous authority. The turning point: does Hamza accept the mandate that is both personal revenge and national mission, knowing the costs of Film 1's years-long sacrifice?

## POMDP — Optimal Policy

- **Optimal action:** `accept_mandate_full_autonomous_authority`
- V(b): `-9.859`
- P(mission success): `46.1%`
- P(cover intact): `91.0%`

| Action | Q(b, a) |
|---|---|
| `accept_mandate_request_institutional_backup` | -9.804 |
| `accept_mandate_limited_scope_ficn_only` | -9.804 |
| `accept_mandate_full_autonomous_authority` ← OPTIMAL | -9.859 |
| `negotiate_terms_family_protection_first` | -12.173 |
| `refuse_mandate_permanent_exfil` | -13.875 |

## Critical Path (CPM/PERT)

- Path: `rizwan_integration` → `reactivate_karachi_network` → `major_iqbal_locate`
- Total: **293 d**  →  Optimal: **176 d**  (save 117 d)
- Bottleneck: `major_iqbal_locate`
- Parallelisable: `target_prioritisation` ‖ `rizwan_integration`, `zahoor_mistry_locate` ‖ `khanani_network_mapping`, `major_iqbal_locate` ‖ `khanani_network_mapping`

## Value of Information

- Total entropy: **1.46 bits**
- Top target: `Zahoor Mistry's current alias and address in Karachi`

| Rank | Target | VoI (bits) | Effort | Recommendation |
|---|---|---|---|---|
| 1 | Zahoor Mistry's current alias and address in Karachi | 1.10 | 6.0 | Low priority — defer; access difficulty (6.0) outweighs VoI (1.10 bits) |
| 2 | Current Khanani-Kalia FICN distribution routes into India | 1.29 | 8.0 | Low priority — defer; access difficulty (8.0) outweighs VoI (1.29 bits) |
| 3 | Major Iqbal's current operational base and security posture | 1.43 | 9.0 | Low priority — defer; access difficulty (9.0) outweighs VoI (1.43 bits) |
| 4 | Happy PHD's narco-Khalistan pipeline: drug routes and arms smuggling into Punjab | 1.20 | 8.5 | Low priority — defer; access difficulty (8.5) outweighs VoI (1.20 bits) |

## Stackelberg Equilibrium

- Handler commits to: `refuse_mandate_permanent_exfil`
- Operative best response: `refuse_mandate_permanent_exfil`
- Adversary counter: `major_iqbal: accept_mandate_limited_scope_ficn_only`
- Indian payoff: `0.734`
- Commitment value vs Nash: `+0.159`

## Shapley Values — Asset Coalition

| Actor | φ | Defection incentive |
|---|---|---|
| ajay_sanyal | 0.900 | 0.000 |
| yalina_jamali | 0.900 | 0.000 |

## Monte Carlo Simulation

- Rollouts per arm: 2000
- Actual (accept_mandate_full_autonomous_authority): P(success)=**100.0%**  [99.8%–100.0%]
- Optimal (accept_mandate_full_autonomous_authority): P(success)=**100.0%**  [99.8%–100.0%]
- Δ = **+0.0%** if optimal path taken
- Key causal lever: `accept_mandate_full_autonomous_authority → film2_operation_begins  (p=0.95)`

## Threat Scores (SNA)

| Actor | Score | Betweenness | Eigenvector | High-threat |
|---|---|---|---|---|
| major_iqbal | 4.500 | 0.000 | 0.000 | no |
| khanani_javed | 3.750 | 0.000 | 0.000 | no |

## Warnings

- adversary_node: no high_threat_actors set — using all adversaries with capability >= 7.0 (['major_iqbal', 'khanani_javed'])
- adversary_node: multi-adversary Stackelberg over ['major_iqbal', 'khanani_javed']
- narrator_node: ANTHROPIC_API_KEY not set — using template fallback
