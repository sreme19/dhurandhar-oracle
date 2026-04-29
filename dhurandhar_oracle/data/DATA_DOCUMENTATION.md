# Data Documentation

Last updated: 2026-04-29T14:42:37.137092Z

This document describes all JSON data assets under `dhurandhar_oracle/data` and the conventions used to maintain them.

## Data Governance Rules

- Append-only enrichment: do not delete narrative fields when adding references.
- Preserve original authored content in turning points/outcomes; add metadata fields instead.
- Use `source_refs` for evidence links and `grounding_log` / `source_ref_additions` for audit trail.
- Use `schema_version` and `updated_at` to track data evolution.

## Top-Level Files

- `encyclopedia_index.json`

## `turning_points` (37 files)

Core decision snapshots used by the oracle pipeline. Each file captures operative state, actions, DAG, tasks, adversaries, alliances, and intelligence targets.

- `turning_points/26-11-celebration-revelation.json`
- `turning_points/aalam-handler-contact.json`
- `turning_points/article-370-abrogation.json`
- `turning_points/balakot-airstrike-abhinandan.json`
- `turning_points/burhan-wani-killing-radicalisation.json`
- `turning_points/cds-rawat-crash-institutional-setback.json`
- `turning_points/dakait-ambush-coordination.json`
- `turning_points/dakait-first-meeting.json`
- `turning_points/doklam-china-second-front.json`
- `turning_points/galwan-china-kinetic-clash.json`
- `turning_points/imran-khan-collapse-pakistan-instability.json`
- `turning_points/isi-capture-torture.json`
- `turning_points/jas-raw-recruitment.json`
- `turning_points/khanani-ficn-network-strike.json`
- `turning_points/ltf-raid-cover-crisis.json`
- `turning_points/major-iqbal-madrassa-siege.json`
- `turning_points/major-iqbal-tanker-final.json`
- `turning_points/marriage-proposal-gambit.json`
- `turning_points/mystery-killings-pakistan-covert-campaign.json`
- `turning_points/naya-bharat-mandate.json`
- `turning_points/nijjar-killing-india-canada-crisis.json`
- `turning_points/operation-sindoor-strike.json`
- `turning_points/pahalgam-attack-crisis.json`
- `turning_points/pathankot-homecoming-choice.json`
- `turning_points/pulwama-balakot-decision.json`
- `turning_points/reasi-pilgrim-bus-attack.json`
- `turning_points/rizwan-partnership-activation.json`
- `turning_points/sajid-mir-prison-poisoning.json`
- `turning_points/sanyal-isi-blackmail.json`
- `turning_points/surgical-strikes-execution.json`
- `turning_points/tahawwur-rana-extradition.json`
- `turning_points/taliban-kabul-fall-recalibration.json`
- `turning_points/torkham-entry-cover-setup.json`
- `turning_points/uri-attack-surgical-decision.json`
- `turning_points/yalina-identity-exposure.json`
- `turning_points/yalina-romance-risk.json`
- `turning_points/zahoor-mistry-elimination.json`

## `outcomes` (30 files)

Outcome records for each turning point, used for actual-vs-optimal analysis and traceability.

- `outcomes/26-11-celebration-revelation.json`
- `outcomes/aalam-handler-contact.json`
- `outcomes/article-370-abrogation.json`
- `outcomes/balakot-airstrike-abhinandan.json`
- `outcomes/burhan-wani-killing-radicalisation.json`
- `outcomes/dakait-ambush-coordination.json`
- `outcomes/dakait-first-meeting.json`
- `outcomes/doklam-china-second-front.json`
- `outcomes/isi-capture-torture.json`
- `outcomes/jas-raw-recruitment.json`
- `outcomes/khanani-ficn-network-strike.json`
- `outcomes/ltf-raid-cover-crisis.json`
- `outcomes/major-iqbal-madrassa-siege.json`
- `outcomes/major-iqbal-tanker-final.json`
- `outcomes/marriage-proposal-gambit.json`
- `outcomes/naya-bharat-mandate.json`
- `outcomes/operation-sindoor-strike.json`
- `outcomes/pahalgam-attack-crisis.json`
- `outcomes/pathankot-homecoming-choice.json`
- `outcomes/pulwama-balakot-decision.json`
- `outcomes/rizwan-partnership-activation.json`
- `outcomes/sajid-mir-prison-poisoning.json`
- `outcomes/sanyal-isi-blackmail.json`
- `outcomes/surgical-strikes-execution.json`
- `outcomes/tahawwur-rana-extradition.json`
- `outcomes/torkham-entry-cover-setup.json`
- `outcomes/uri-attack-surgical-decision.json`
- `outcomes/yalina-identity-exposure.json`
- `outcomes/yalina-romance-risk.json`
- `outcomes/zahoor-mistry-elimination.json`

## `characters` (17 files)

Indian-side and supporting character profiles used by loaders and side-gating logic.

- `characters/ajay_sanyal.json`
- `characters/amarjit_singh_brar.json`
- `characters/aquib_ali_zarwari.json`
- `characters/devavrat_kapoor.json`
- `characters/dgp_prashant_kumar.json`
- `characters/fictional_punjab_cast.json`
- `characters/hamza.json`
- `characters/ks_bhullar.json`
- `characters/mohammed_aalam.json`
- `characters/naieem_baloch.json`
- `characters/nawab_shafiq.json`
- `characters/rizwan_shah.json`
- `characters/shabnam.json`
- `characters/sp_choudhary_aslam.json`
- `characters/sushant_bansal.json`
- `characters/ulfat.json`
- `characters/yalina_jamali.json`

## `adversaries` (23 files)

Adversary profiles and threat actor metadata used in game-theoretic and network components.

- `adversaries/abdul_bhuttovi.json`
- `adversaries/ajmal_kasab.json`
- `adversaries/arshad_pappu.json`
- `adversaries/azam_cheema.json`
- `adversaries/baba_ladla.json`
- `adversaries/babu_dakait.json`
- `adversaries/bade_sahab.json`
- `adversaries/david_headley.json`
- `adversaries/dawood_ibrahim.json`
- `adversaries/general_shamshad_hassan.json`
- `adversaries/happy_phd.json`
- `adversaries/ibrahim_athar.json`
- `adversaries/jameel_jamali.json`
- `adversaries/khanani_altaf.json`
- `adversaries/khanani_javed.json`
- `adversaries/major_iqbal.json`
- `adversaries/rehman_dakait.json`
- `adversaries/sajid_mir.json`
- `adversaries/shakeel_commando.json`
- `adversaries/shirani_ahmad_baloch.json`
- `adversaries/uzair_baloch.json`
- `adversaries/yasir_arafat_film.json`
- `adversaries/zahoor_mistry.json`

## `context` (4 files)

Narrative/political/historical context packs used for enrichment and scenario framing.

- `context/ficn_network.json`
- `context/ib_vs_raw_friction.json`
- `context/narco_jihad_doctrine.json`
- `context/punjab_khalistan_arc.json`

## `missions` (1 files)

Mission-level orchestration records (phase structure, triggers, and network mapping).

- `missions/operation-lyari.json`

## `timeline` (1 files)

Chronological datasets used for sequencing and temporal grounding.

- `timeline/master_timeline.json`

## `enrichment` (8 files)

Append-only source-ref seeds, gap reports, and external grounding metadata.

- `enrichment/source_refs_gap_report.json`
- `enrichment/source_refs_gap_report_batch2.json`
- `enrichment/source_refs_gap_report_batch3.json`
- `enrichment/source_refs_gap_report_batch4.json`
- `enrichment/source_refs_seed.json`
- `enrichment/source_refs_seed_batch2.json`
- `enrichment/source_refs_seed_batch3.json`
- `enrichment/source_refs_seed_batch4.json`

## Field-Level Expectations

- `turning_points/*`: `id`, `operative`, `film`, `act`, `description`, `state_vector`, `available_actions`, `mission_tasks`, `causal_dag`, `adversaries`, `alliance_snapshot`, `intelligence_targets`, `belief_state`.
- `outcomes/*`: `turning_point_id`, `actual_action`, `immediate_effects`, `terminal_state`, `days_elapsed`, plus enrichment fields (`losses`, `intel_gained`, `cover_change`, `confidence`, `source_refs`, `schema_version`).
- `enrichment/*`: seed files and batch gap reports; these are generated artifacts used to append references into turning points without destructive edits.

