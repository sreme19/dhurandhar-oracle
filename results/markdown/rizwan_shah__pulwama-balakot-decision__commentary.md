# Oracle briefing — `rizwan_shah` / `pulwama-balakot-decision`

> **Scenario.** February 14, 2019, 1535 hrs. Adil Ahmad Dar drives a 300–350 kg
> IED into CRPF bus 49 on NH-44 near Lethapora, Pulwama — 40 personnel KIA.
> Within hours, the martyrdom-video upload trace points to a Rawalpindi IP and
> the CCS convenes. Rizwan Shah is sitting on Balakot training-camp targeting
> intelligence. The choice space: deliver the targeting package now and enable
> a strike, hold the intelligence to run a deeper JeM-network operation, or
> first lock down the ISI-sanction-level question that determines escalation
> ladder height.

---

## 1. POMDP — Optimal Policy

**Optimal action: `confirm_isi_sanction_level_on_pulwama`** with V(b) = **5.882**.

| Action | Q(b, a) | Δ vs optimal |
|---|---|---|
| `confirm_isi_sanction_level_on_pulwama` ← OPTIMAL | **5.882** | — |
| `deliver_broader_jem_network_map_for_deeper_operation` | 5.488 | −0.394 |
| `identify_jem_handlers_who_managed_dar_recruitment` | 5.288 | −0.594 |
| `deliver_balakot_targeting_intelligence_enable_air_strike` | 4.888 | −0.994 |
| `assess_isi_retaliation_threshold_if_india_strikes` | 4.888 | −0.994 |

**Belief state b at decision time:**

| World state s | b(s) |
|---|---|
| `paf_will_retaliate_if_india_strikes_balakot` | 0.700 |
| `isi_will_accept_balakot_strike_as_punishment_no_conventional_war` | 0.200 |
| `isi_intends_nuclear_signalling_as_deterrent_if_struck` | 0.070 |
| `pakistan_will_seek_immediate_ceasefire_post_strike` | 0.030 |

P(mission success) = **50.0%** | P(cover intact) = **100.0%**

### Mathematical reading

PBVI (Pineau et al., 2003) approximates the piecewise-linear-convex value
function V(b) over the |S|-dim belief simplex by maintaining a finite set of
α-vectors Γ. For belief b,

```
V(b) = max_α∈Γ  ⟨α, b⟩
π(b) = argmax_a  max_{α∈Γ_a}  ⟨α, b⟩
```

The Bellman backup at each iteration is

```
α_{a,o}(s) = Σ_{s'} T(s'|s,a) · Z(o|s',a) · α*(s')
α_a(s)     = R(s,a) + γ · Σ_o  max_α  Σ_{s'} α_{a,o}(s')
```

with γ = 0.95.

**Why `confirm_isi_sanction_level_on_pulwama` wins.** The action-value gap
between the optimal action and the runner-up is
**Q* − Q⁽²⁾ = 5.882 − 5.488 = 0.394**. In present-value terms that is
≈ 0.394 / (1 − 0.95) = 7.88 reward units of long-horizon advantage.

The belief is *heavily skewed* (0.700) toward the PAF-retaliation state — i.e.
striking immediately is expected to provoke conventional response. Three of
the five actions (deliver targeting, assess threshold, identify handlers) all
operate *downstream* of the sanction-level question. Confirming sanction
level is an **information-gathering action that expands future feasibility**:
once you know whether ISI as an institution authored Pulwama (vs. a JeM
freelance), the optimal escalation ladder collapses to either (a) full Balakot
strike with diplomatic backing or (b) constrained covert response. This is a
classic POMDP "wait for observation before committing" pattern — visible in
the −0.99 Q-gap to the strike-enabling actions, which the model penalises
because they collapse belief mass into the high-cost
`isi_intends_nuclear_signalling…` branch (b = 0.07) without first ruling it
out.

P(mission success) = 0.5 reflects the ambiguity: the belief is concentrated on
states that *do not* contain a positive `mission_success` token, so the
state-decoder applies the mid-tier success weight (cover_intact × adv × phase)
≈ 0.5 across the dominant mass. P(cover intact) = 1.0 because no belief mass
sits on a `cover_*` failure state — Rizwan's identity has *zero* exposure
risk at this turning point; he is operating from inside RAW, not under cover.

---

## 2. Stackelberg Equilibrium

| Field | Value |
|---|---|
| Handler commits to | `confirm_isi_sanction_level_on_pulwama` |
| Operative best response | `confirm_isi_sanction_level_on_pulwama` |
| Adversary follower (ISI GHQ) | `identify_jem_handlers_who_managed_dar_recruitment` |
| Indian payoff | **0.707** |
| Adversary payoff | 0.293 |
| Commitment value vs Nash | **+0.229** |

### Mathematical reading

In the Stackelberg game the handler (RAW/IB leadership) plays first. The
solver does backward induction:

```
a*_L = argmax_{a_L}  U_L( a_L,  BR_F(a_L) )
```

where BR_F is the follower (adversary) best-response correspondence under
prospect-weighted utility (λ = 2.25, γ = 0.65, α = β = 0.88).

**Commitment value** is the handler's payoff gap between the Stackelberg
equilibrium and the simultaneous-move Nash equilibrium:

```
V_commit = U_L(Stackelberg) − U_L(Nash) = 0.229
```

A positive commitment value of **+0.229 on a [0,1] payoff scale** is large —
it says ~23 % of the handler's achievable utility comes purely from the
ability to *publicly pre-commit* to a sanction-confirmation track before the
adversary chooses. Operationally this maps to NSA Sanyal making the
"intelligence-first, strike-second" doctrine known (e.g., the Modi-Doval CCS
posture that Balakot will only be authorised once the dossier is airtight) —
ISI then optimally pivots its own operations to handler-identification
counter-intelligence rather than racing to harden Balakot.

The **0.707 / 0.293** payoff split is non-zero-sum because both sides assign
positive utility to information clarity (different signs on different states),
which is why the equilibrium isn't (1, 0).

---

## 3. Critical Path (CPM / PERT)

| Field | Value |
|---|---|
| Total expected duration | **22.7 d** |
| Optimal (with parallelisation) | **13.6 d** |
| Saving | **9.1 d** (40 %) |
| Bottleneck | `dar_handler_identify` |
| Critical path | `dar_handler_identify` |

| Slack task | Slack (d) |
|---|---|
| `balakot_targeting_package` | 15.5 |
| `isi_retaliation_threshold` | 13.2 |
| `isi_pulwama_sanction_confirm` | 10.0 |

**Parallelisable pairs:** `balakot_targeting_package ‖ isi_retaliation_threshold`,
`isi_pulwama_sanction_confirm ‖ balakot_targeting_package`,
`dar_handler_identify ‖ balakot_targeting_package`,
`dar_handler_identify ‖ isi_retaliation_threshold`.

### Mathematical reading

PERT three-point estimate per task:

```
E[T_i] = (O_i + 4 M_i + P_i) / 6
σ²_i  = ((P_i − O_i) / 6)²
```

CPM forward pass: ES(n) = max_{p∈preds} EF(p), EF(n) = ES(n) + E[T_n].
Backward pass: LF(n) = min_{s∈succs} LS(s), LS(n) = LF(n) − E[T_n].
Slack(n) = LS(n) − ES(n). Critical path = {n : Slack(n) = 0}.

The fact that `dar_handler_identify` is the *only* zero-slack task means the
mission's logical chain has exactly one constraint and four near-independent
sidequests. **The 9.1-day saving (40 % wall-clock reduction)** comes entirely
from running `balakot_targeting_package` and `isi_retaliation_threshold`
concurrently with handler identification. The slack on
`isi_pulwama_sanction_confirm` (10 d) is the operational reason it can be
the POMDP-optimal information action without delaying the strike envelope —
it has high informational value but no schedule cost.

---

## 4. Value of Information

Total marginal entropy across intelligence targets: **1.245 bits** (top
target: Balakot Markaz Subhan Allah occupancy).

| Rank | Target | VoI (bits) | Effort | Recommendation |
|---|---|---|---|---|
| 1 | Markaz Subhan Allah occupancy / layout (IAF targeting) | 1.232 | 8.5 | Defer — effort outweighs VoI |
| 2 | ISI/JeM handler who recruited Adil Ahmad Dar | 1.058 | 8.0 | Defer |
| 3 | PAF retaliation plan (F-16 sortie plan, designated targets) | 1.208 | 9.5 | Defer |

### Mathematical reading

VoI is the expected entropy reduction on a target T given an observation o:

```
VoI(T) = H(T) − E_o [ H(T | o) ]   (in bits)
```

A 1.232-bit reduction over a target with prior entropy near 2 bits means the
Balakot intel cuts uncertainty by roughly **57 %** — that is the single most
valuable observation in the set. However, the cost-adjusted recommendation
flips because all three top targets have effort ≥ 8.0 on a [0, 10] scale, and
the oracle's heuristic compares VoI in bits against effort/10:
`net_value = VoI − effort × cost_per_unit_effort`. With effort 8.5 and
VoI 1.232 bits, the net is sub-zero on the project-level cost basis. This
is why the recommendation is "monitor channels, defer aggressive collection"
— the POMDP's choice (`confirm_isi_sanction_level…`) is itself a **lower-effort
information acquisition** that resolves a different slice of belief uncertainty.

---

## 5. Monte Carlo Simulation

| Arm | P(success) | 95% CI | P(cover blown) |
|---|---|---|---|
| Actual = `confirm_isi_sanction_level_on_pulwama` | **100.0 %** | [99.8 %, 100 %] | 0.0 % |
| Optimal = `confirm_isi_sanction_level_on_pulwama` | **100.0 %** | [99.8 %, 100 %] | 0.0 % |

Δ (optimal − actual) = **+0.0 %**. Key causal lever:
`confirm_isi_sanction_level_on_pulwama → diplomatic_dossier_strengthened` with
edge strength p = 0.88.

### Mathematical reading

Each rollout walks the causal DAG forward from the action node, sampling each
edge as a Bernoulli with parameter `edge.strength`. Across n = 2000 rollouts
the success rate is estimated; the CI uses the Wilson score interval

```
center = (p̂ + z²/2n) / (1 + z²/n)
margin = z · √( p̂(1−p̂)/n + z²/(4n²) )  / (1 + z²/n)
```

with z = 1.96 for 95% confidence.

The **near-degenerate CI [99.81 %, 100 %]** says the causal DAG from this
action terminates almost deterministically in mission_success — there are no
high-strength edges leading to `cover_blown` or `mission_fail` reachable
from `confirm_isi_sanction_level…`. The dominant edge strength of 0.88 to
`diplomatic_dossier_strengthened` is what carries the rollouts.

> **Caveat.** Δ = 0 because the simulator currently uses the POMDP-optimal
> action as both the *actual* and *optimal* arm (see `simulator_node.py`
> line 53 — historical-action loading from `outcomes/*.json` is still a TODO).
> To see a non-trivial counterfactual delta, re-run with
> `--action deliver_balakot_targeting_intelligence_enable_air_strike` and
> compare.

---

## 6. HMM Belief Gaps — Mole Detection

No belief gaps detected at this turning point. Rizwan's institutional setting
(RAW HQ analyst, not field cover) means there is no operative-vs-handler
loyalty ambiguity to score. The HMM Viterbi pass is therefore vacuous here.

---

## 7. Shapley Values — Asset Coalition

| Actor | φ (contribution) | Defection incentive | Risk |
|---|---|---|---|
| `ajay_sanyal` | **0.920** | 0.000 | LOW |
| `jem_masood_azhar` | 0.850 | 0.000 | LOW |

### Mathematical reading

Shapley value:

```
φ_i(v) = Σ_{S ⊆ N\{i}}  |S|! · (n − |S| − 1)! / n! · [ v(S ∪ {i}) − v(S) ]
```

Both actors clear φ ≈ 0.85–0.92 on a 0–1 scale: each is **near-essential** to
the coalition value function v(S). Sanyal's slight edge (0.92 vs 0.85) reflects
his role as the strategic decision-aggregator — without him, the
intelligence-to-action chain breaks, while JeM/Masood is the *target-side*
node whose presence fixes the adversary identification. Defection incentive
= 0.0 means neither agent gets positive utility from leaving the coalition;
the alliance is structurally stable.

---

## 8. Threat Scores (SNA)

| Actor | Composite | Betweenness | Eigenvector | High-threat |
|---|---|---|---|---|
| `isi_ghq_post_pulwama` | 4.75 | 0.0 | 0.0 | no |
| `jem_masood_azhar_command` | 4.25 | 0.0 | 0.0 | no |

### Mathematical reading

Composite threat = capability-weighted aggregate over the alliance graph.
Both actors are *not* high-threat-flagged here because the alliance graph at
this turning point is sparse (zero-betweenness, zero-eigenvector centrality)
— ISI/JeM are modelled as **end-nodes**, not bridges between distinct
networks, so no actor sits on a structural choke-point. The capability
component dominates the score (ISI ≈ 9.5/10, JeM ≈ 8.5/10), and the threshold
for `is_high` requires either capability ≥ 7 *and* non-zero centrality, or
composite ≥ 5. Neither hits the bar despite raw capability being high.

---

## Bottom-line model recommendation

> **Do not deliver Balakot targeting yet.** The POMDP says wait; the
> Stackelberg analysis says publicly committing to "intelligence-first" gives
> a +0.23 (≈ 23 %) utility advantage; CPM confirms confirming sanction level
> consumes 10 days of slack and *does not* delay the strike window; Monte
> Carlo says the action's causal chain is near-deterministic on
> diplomatic-dossier success. Every algorithm points the same way:
> **`confirm_isi_sanction_level_on_pulwama`** before any kinetic option is
> exercised.

---

_Generated by `dhurandhar-oracle run rizwan_shah pulwama-balakot-decision`._
_Pipeline: state → intel_network ‖ coalition → belief → voi → adversary
(Stackelberg) → strategy (POMDP/PBVI) → critical_path (CPM/PERT) →
simulator (Monte Carlo) → narrator._
