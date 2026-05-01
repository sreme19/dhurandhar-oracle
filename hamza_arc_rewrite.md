WARNING: narrator_node: ANTHROPIC_API_KEY not set — using template fallback
Arc rewrite: hamza
                        Per-turning-point counterfactual                        
┏━━━━━━━━━━━━━┳━━━━━━━━━━━━━━┳━━━━━━━━━━━━━┳━━━━━━━━━━━┳━━━━━━━━━━━━━━┳━━━━━━━━┓
┃ Turning     ┃              ┃             ┃           ┃              ┃        ┃
┃ point       ┃ Actual       ┃ Prescribed  ┃ Q(actual) ┃ Q(prescribe… ┃ ΔQ     ┃
┡━━━━━━━━━━━━━╇━━━━━━━━━━━━━━╇━━━━━━━━━━━━━╇━━━━━━━━━━━╇━━━━━━━━━━━━━━╇━━━━━━━━┩
│ aalam-hand… │ conduct_sol… │ request_de… │ 3.010     │ 3.560        │ +0.550 │
│ jas-raw-re… │ accept_recr… │ refuse_rec… │ -31.895   │ -31.420      │ +0.475 │
│ torkham-en… │ request_exf… │ conduct_pa… │ -51.333   │ -49.266      │ +2.067 │
│ dakait-fir… │ deepen_crim… │ accelerate… │ -54.277   │ -54.233      │ +0.044 │
│ ltf-raid-c… │ flee_before… │ use_handle… │ -54.088   │ -51.485      │ +2.603 │
│ marriage-p… │ propose_mar… │ withdraw_f… │ 3.981     │ 4.435        │ +0.454 │
│ yalina-rom… │ use_yalina_… │ avoid_yali… │ 3.848     │ 4.442        │ +0.594 │
│ 26-11-cele… │ confront_da… │ photograph… │ -51.305   │ -46.169      │ +5.136 │
│ dakait-amb… │ exfiltrate_… │ abort_ambu… │ -55.841   │ -53.661      │ +2.180 │
│ naya-bhara… │ refuse_mand… │ accept_man… │ -6.766    │ -1.954       │ +4.812 │
│ yalina-ide… │ confess_and… │ confess_to… │ -162.336  │ -160.249     │ +2.087 │
│ zahoor-mis… │ capture_mis… │ execute_wi… │ -52.091   │ -49.806      │ +2.285 │
│ isi-captur… │ offer_limit… │ negotiate_… │ 5.333     │ 5.929        │ +0.596 │
│ major-iqba… │ strike_comp… │ attempt_li… │ -154.781  │ -152.296     │ +2.485 │
│ major-iqba… │ rpg_tanker_… │ abort_iqba… │ -152.681  │ -152.296     │ +0.385 │
│ pathankot-… │ observe_onl… │ accept_nex… │ 3.444     │ 3.941        │ +0.497 │
│ sanyal-isi… │ deploy_shah… │ escalate_d… │ 7.983     │ 8.379        │ +0.396 │
│ mystery-ki… │ break_conta… │ feed_isi_f… │ 4.888     │ 5.882        │ +0.994 │
└─────────────┴──────────────┴─────────────┴───────────┴──────────────┴────────┘
  Cumulative ΔQ: +28.640
  Final state — baseline:   {'cover_integrity': 5.5, 'trust_capital': 7.8, 
'intelligence_depth': 7.5, 'network_strength': 4.0, 'exposure_risk': 7.5}
  Final state — prescribed: {'cover_integrity': 6.5, 'trust_capital': 8.6, 
'intelligence_depth': 9.5, 'network_strength': 4.8, 'exposure_risk': 6.3}
  5d career objective Δ: yield=+3.00  impact=+2.10  cost=-1.20  network=+1.50  
attribution=-0.90
╭───────────────────── Arc Rewrite — Counterfactual Brief ─────────────────────╮
│ ## Arc rewrite: hamza                                                        │
│                                                                              │
│ ### Per-turning-point counterfactual                                         │
│ - aalam-handler-contact: actual=conduct_solo_surveillance_unsanctioned       │
│ prescribed=request_delhi_reduce_pressure  ΔQ=+0.550                          │
│ - jas-raw-recruitment: actual=accept_recruitment_full_erasure                │
│ prescribed=refuse_recruitment_face_execution  ΔQ=+0.475                      │
│ - torkham-entry-cover-setup: actual=request_exfil_abort_mission              │
│ prescribed=conduct_passive_surveillance_only  ΔQ=+2.067                      │
│ - dakait-first-meeting: actual=deepen_criminal_cover                         │
│ prescribed=accelerate_dakait_trust  ΔQ=+0.044                                │
│ - ltf-raid-cover-crisis: actual=flee_before_raid_reaches_area                │
│ prescribed=use_handler_aalam_to_signal_delhi_abort  ΔQ=+2.603                │
│ - marriage-proposal-gambit: actual=propose_marriage_full_commitment          │
│ prescribed=withdraw_from_yalina_maintain_distance  ΔQ=+0.454                 │
│ - yalina-romance-risk:                                                       │
│ actual=use_yalina_contact_for_jamali_intel_then_disengage                    │
│ prescribed=avoid_yalina_protect_cover  ΔQ=+0.594                             │
│ - 26-11-celebration-revelation: actual=confront_dakait_blow_cover            │
│ prescribed=photograph_evidence_maintain_cover_continue  ΔQ=+5.136            │
│ - dakait-ambush-coordination:                                                │
│ actual=exfiltrate_first_let_aslam_act_independently                          │
│ prescribed=abort_ambush_protect_yalina  ΔQ=+2.180                            │
│ - naya-bharat-mandate: actual=refuse_mandate_permanent_exfil                 │
│ prescribed=accept_mandate_limited_scope_ficn_only  ΔQ=+4.812                 │
│ - yalina-identity-exposure: actual=confess_and_begin_joint_exfil_plan        │
│ prescribed=confess_to_yalina_appeal_to_love_and_zayan  ΔQ=+2.087             │
│ - zahoor-mistry-elimination: actual=capture_mistry_extract_for_interrogation │
│ prescribed=execute_with_intelligence_collection_hybrid  ΔQ=+2.285            │
│ - isi-capture-torture: actual=offer_limited_outdated_intelligence            │
│ prescribed=negotiate_prisoner_exchange_reveal_sanyal_channel  ΔQ=+0.596      │
│ - major-iqbal-madrassa-siege: actual=strike_compound_eliminate_all           │
│ prescribed=attempt_live_capture_iqbal_priority  ΔQ=+2.485                    │
│ - major-iqbal-tanker-final: actual=rpg_tanker_remote_deny_escape             │
│ prescribed=abort_iqbal_survives_mission_incomplete  ΔQ=+0.385                │
│ - pathankot-homecoming-choice: actual=observe_only_do_not_reveal_identity    │
│ prescribed=accept_next_mission_remain_operative  ΔQ=+0.497                   │
│ - sanyal-isi-blackmail: actual=deploy_shahnawaz_recordings_demand_release    │
│ prescribed=escalate_diplomatically_official_india_pak_channel  ΔQ=+0.396     │
│ - mystery-killings-pakistan-covert-campaign:                                 │
│ actual=break_contact_exfiltrate_iran_corridor                                │
│ prescribed=feed_isi_false_profile_extend_operational_window  ΔQ=+0.994       │
│                                                                              │
│ Cumulative ΔQ: +28.640                                                       │
│                                                                              │
│ ### 5d career objective delta                                                │
│ - mission_yield Δ      = +3.00                                               │
│ - strategic_impact Δ   = +2.10                                               │
│ - personal_cost Δ      = -1.20  (negative = better)                          │
│ - network_durability Δ = +1.50                                               │
│ - attribution_risk Δ   = -0.90  (negative = better)                          │
╰──────────────────────────────────────────────────────────────────────────────╯
