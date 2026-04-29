"""
belief_node — HMM mole detection.  Infer hidden loyalty states.

Runs AFTER the parallel fan-in of intel_network_node + coalition_node.

Responsibilities:
  1. For each high-threat adversary, run Viterbi over their observable
     action sequence to infer the most likely hidden state sequence
  2. Compare the operative's naive belief (from turning_point JSON) against
     the HMM-inferred state → produce BeliefGap for each adversary
  3. Flag assets with defection_incentive > 0.5 AND belief_gap > 0.6
     as suspected moles (cross-check with Shapley coalition_node output)

Input  keys: adversaries, high_threat_actors, shapley
Output keys: hmm_results, belief_gaps, errors, warnings

Key difference from got-oracle:
  Hidden states here reflect *loyalty* (loyal | wavering | compromised | turned)
  rather than GoT's power-play states (monitoring | probing | executing).
  Baum-Welch re-estimates transition/emission matrices from observable history
  so parameters are not purely hand-coded.
"""
from __future__ import annotations

from dhurandhar_oracle.optimisation.hmm import (
    HMMParams,
    viterbi,
    forward_backward,
    baum_welch,
)
from dhurandhar_oracle.schemas import BeliefGap, HMMResult
from dhurandhar_oracle.state import DhurandharState

_MOLE_DEFECTION_THRESHOLD  = 0.50
_MOLE_BELIEF_GAP_THRESHOLD = 0.60


def belief_node(state: DhurandharState) -> dict:
    """Run HMM over each high-threat adversary; compute belief gaps."""
    errors:   list[str] = []
    warnings: list[str] = []

    adversaries       = state.get("adversaries", [])
    high_threat       = set(state.get("high_threat_actors", []))
    shapley_result    = state.get("shapley")

    hmm_results: list[HMMResult]  = []
    belief_gaps: list[BeliefGap]  = []

    for adv in adversaries:
        if adv.actor not in high_threat:
            continue
        if not adv.observable_actions:
            warnings.append(f"belief_node: {adv.actor} has no observable actions — skipping HMM")
            continue

        # TODO: load actual observable_history sequence from character data
        # For now use a single-step sequence as placeholder
        obs_sequence = [0]   # placeholder index into observable_actions

        params = HMMParams.uniform(
            n_hidden=len(adv.hidden_states),
            n_obs=len(adv.observable_actions),
        )
        # Refine with Baum-Welch if sequence is long enough
        if len(obs_sequence) >= 3:
            params = baum_welch(params, [obs_sequence], n_iter=20)

        path_indices, _ = viterbi(params, obs_sequence)
        posteriors      = forward_backward(params, obs_sequence)

        most_likely = adv.hidden_states[path_indices[-1]]
        state_probs = {
            adv.hidden_states[i]: float(posteriors[-1, i])
            for i in range(len(adv.hidden_states))
        }

        hmm_results.append(HMMResult(
            actor=adv.actor,
            hidden_states=adv.hidden_states,
            most_likely_state=most_likely,
            state_probs=state_probs,
            viterbi_path=[adv.hidden_states[i] for i in path_indices],
        ))

        # ── Belief gap ─────────────────────────────────────────────────────
        # TODO: load operative's stated belief from turning_point JSON
        operative_belief = adv.hidden_states[0]   # placeholder: assumes operative thinks "loyal"
        gap = 0.0 if operative_belief == most_likely else (
            1.0 - state_probs.get(operative_belief, 0.0)
        )

        belief_gaps.append(BeliefGap(
            actor=adv.actor,
            operative_believed=operative_belief,
            hmm_inferred=most_likely,
            gap=round(gap, 4),
        ))

        # ── Mole warning ───────────────────────────────────────────────────
        if shapley_result:
            defection = shapley_result.defection_incentives.get(adv.actor, 0.0)
            if defection > _MOLE_DEFECTION_THRESHOLD and gap > _MOLE_BELIEF_GAP_THRESHOLD:
                warnings.append(
                    f"MOLE ALERT: {adv.actor} — defection incentive={defection:.2f}, "
                    f"belief gap={gap:.2f}"
                )

    return {
        "hmm_results":  hmm_results,
        "belief_gaps":  belief_gaps,
        "errors":       errors,
        "warnings":     warnings,
    }
