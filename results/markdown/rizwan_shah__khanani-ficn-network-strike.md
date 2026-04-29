# Oracle briefing — `rizwan_shah` / `khanani-ficn-network-strike`

> 2016. Rizwan Shah, coordinating with Hamza, has mapped the Khanani-Kalia International (KKI) fake Indian currency note (FICN) distribution network. Javed Khanani (Altaf's brother, operating after Altaf's 2015 US arrest) is the primary target. The operation is timed to coordinate with a Delhi decision on currency demonetisation — rendering the FICN stockpile worthless as a coordinated intelligence strike. Rizwan must decide how to execute the financial network takedown: whether to physically eliminate Khanani (kinetic), disrupt the network through financial intelligence passed to FATF, or time the operation with the demonetisation announcement for maximum impact.

## POMDP — Optimal Policy

- **Optimal action:** `pass_kki_network_map_to_fatf_via_delhi`
- V(b): `-54.323`
- P(mission success): `41.6%`
- P(cover intact): `81.0%`

| Action | Q(b, a) |
|---|---|
| `disrupt_distribution_routes_without_elimination` | -54.280 |
| `pass_kki_network_map_to_fatf_via_delhi` ← OPTIMAL | -54.323 |
| `delay_operation_gather_complete_network_map` | -54.480 |
| `capture_khanani_extract_d_company_isi_links` | -56.225 |
| `eliminate_khanani_javed_kinetic_timed_to_demonetisation` | -56.625 |

## Critical Path (CPM/PERT)

- Path: `ficn_distribution_route_map` → `punjab_pipeline_intel_package`
- Total: **65 d**  →  Optimal: **47 d**  (save 18 d)
- Bottleneck: `punjab_pipeline_intel_package`
- Parallelisable: `khanani_javed_surveillance` ‖ `ficn_distribution_route_map`, `punjab_pipeline_intel_package` ‖ `execute_khanani_strike`

## Value of Information

- Total entropy: **1.82 bits**
- Top target: `Complete KKI network: all routes, cut-outs, and ISI officer contacts`

| Rank | Target | VoI (bits) | Effort | Recommendation |
|---|---|---|---|---|
| 1 | Complete KKI network: all routes, cut-outs, and ISI officer contacts | 1.68 | 3.0 | Medium priority — schedule after cover deepening |
| 2 | Happy PHD's complete Punjab narco-Khalistan supply chain | 1.42 | 7.5 | Low priority — defer; access difficulty (7.5) outweighs VoI (1.42 bits) |
| 3 | Dawood Ibrahim D-Company officers receiving ISI FICN protection | 1.46 | 8.5 | Low priority — defer; access difficulty (8.5) outweighs VoI (1.46 bits) |

## Stackelberg Equilibrium

- Handler commits to: `capture_khanani_extract_d_company_isi_links`
- Operative best response: `capture_khanani_extract_d_company_isi_links`
- Adversary counter: `major_iqbal: delay_operation_gather_complete_network_map`
- Indian payoff: `0.734`
- Commitment value vs Nash: `+0.159`

## Shapley Values — Asset Coalition

| Actor | φ | Defection incentive |
|---|---|---|
| rizwan_shah | 0.920 | 0.000 |
| ajay_sanyal | 0.900 | 0.000 |

## Monte Carlo Simulation

- Rollouts per arm: 2000
- Actual (pass_kki_network_map_to_fatf_via_delhi): P(success)=**100.0%**  [99.8%–100.0%]
- Optimal (pass_kki_network_map_to_fatf_via_delhi): P(success)=**100.0%**  [99.8%–100.0%]
- Δ = **+0.0%** if optimal path taken
- Key causal lever: `pass_kki_network_map_to_fatf_via_delhi → fatf_grey_list_evidence_strengthened  (p=0.88)`

## Threat Scores (SNA)

| Actor | Score | Betweenness | Eigenvector | High-threat |
|---|---|---|---|---|
| major_iqbal | 4.500 | 0.000 | 0.000 | no |
| khanani_javed | 3.750 | 0.000 | 0.000 | no |

## Warnings

- state_node: using char.state_by_act['film2_act2'] over TP state_vector
- adversary_node: no high_threat_actors set — using all adversaries with capability >= 7.0 (['khanani_javed', 'major_iqbal'])
- adversary_node: multi-adversary Stackelberg over ['khanani_javed', 'major_iqbal']
- narrator_node: ANTHROPIC_API_KEY not set — using template fallback
