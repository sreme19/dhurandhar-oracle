# Oracle briefing — `rizwan_shah` / `burhan-wani-killing-radicalisation`

> July 8, 2016. Hizbul Mujahideen commander Burhan Wani — 22 years old, the social-media face of the new Kashmiri insurgency — is killed in an encounter in Kokernag, Tral. His death triggers the worst Kashmir unrest since 2010: 90+ civilian deaths, 15,000+ pellet gun injuries over 7 months, 100+ youths joining militancy within weeks. Intelligence gathering in Kashmir suffers a 'temporary blow' as sources dry up amid community backlash. Rizwan Shah, monitoring the radicalisation pipeline from his position embedded in the ISI-linked Kashmiri network, must assess: is this a spontaneous grief surge or is ISI exploiting Wani's martyrdom to systematically recruit a new generation of militants before the political window closes?

## POMDP — Optimal Policy

- **Optimal action:** `identify_radicalized_youth_cohort_leaders`
- V(b): `1.953`
- P(mission success): `50.0%`
- P(cover intact): `100.0%`

| Action | Q(b, a) |
|---|---|
| `identify_radicalized_youth_cohort_leaders` ← OPTIMAL | 1.953 |
| `assess_isi_exploitation_of_wani_narrative` | 1.755 |
| `map_new_militant_recruitment_pipeline` | 1.755 |
| `monitor_hurriyat_isi_coordination_post_wani` | 1.555 |
| `provide_intelligence_on_pellet_gun_propaganda_operations` | 1.555 |

## Critical Path (CPM/PERT)

- Path: `isi_exploitation_assess` → `source_network_rebuild`
- Total: **110 d**  →  Optimal: **95 d**  (save 16 d)
- Bottleneck: `source_network_rebuild`
- Parallelisable: `isi_exploitation_assess` ‖ `recruitment_pipeline_map`

## Value of Information

- Total entropy: **1.37 bits**
- Top target: `Extent and coordination of ISI media operations weaponising pellet gun imagery internationally`

| Rank | Target | VoI (bits) | Effort | Recommendation |
|---|---|---|---|---|
| 1 | Extent and coordination of ISI media operations weaponising pellet gun imagery internationally | 1.03 | 6.0 | Low priority — defer; access difficulty (6.0) outweighs VoI (1.03 bits) |
| 2 | Confirmation that ISI is directing — not merely exploiting — post-Wani recruitment surge through specific operational channels | 1.30 | 8.0 | Low priority — defer; access difficulty (8.0) outweighs VoI (1.30 bits) |
| 3 | Identities of radicalised youth cell leaders who will form next-generation militant orgs (proto-TRF, 2019-onward) | 1.23 | 9.0 | Low priority — defer; access difficulty (9.0) outweighs VoI (1.23 bits) |

## Stackelberg Equilibrium

- Handler commits to: `identify_radicalized_youth_cohort_leaders`
- Operative best response: `identify_radicalized_youth_cohort_leaders`
- Adversary counter: `provide_intelligence_on_pellet_gun_propaganda_operations`
- Indian payoff: `0.715`
- Commitment value vs Nash: `+0.172`

## Shapley Values — Asset Coalition

| Actor | φ | Defection incentive |
|---|---|---|
| ajay_sanyal | 0.880 | 0.000 |
| hurriyat_conference | 0.750 | 0.000 |

## Monte Carlo Simulation

- Rollouts per arm: 2000
- Actual (identify_radicalized_youth_cohort_leaders): P(success)=**100.0%**  [99.8%–100.0%]
- Optimal (identify_radicalized_youth_cohort_leaders): P(success)=**100.0%**  [99.8%–100.0%]
- Δ = **+0.0%** if optimal path taken
- Key causal lever: `identify_radicalized_youth_cohort_leaders → trf_precursor_cells_formed_undetected  (p=0.60)`

## Threat Scores (SNA)

| Actor | Score | Betweenness | Eigenvector | High-threat |
|---|---|---|---|---|
| isi_kashmir_desk_wani_exploitation | 4.250 | 0.000 | 0.000 | no |
| hurriyat_conference_post_wani | 3.250 | 0.000 | 0.000 | no |

## Warnings

- state_node: using char.state_by_act['film3_act1'] over TP state_vector
- adversary_node: no high_threat_actors set — using all adversaries with capability >= 7.0 (['isi_kashmir_desk_wani_exploitation'])
- narrator_node: ANTHROPIC_API_KEY not set — using template fallback
