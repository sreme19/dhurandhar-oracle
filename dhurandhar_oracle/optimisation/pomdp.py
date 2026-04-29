"""
pomdp.py — Partially Observable Markov Decision Process solver.

Algorithm: Point-Based Value Iteration (PBVI)
  Pineau et al. (2003) "Point-based value iteration: An anytime algorithm
  for POMDPs"

NEW to this project series (not in ipl-oracle or got-oracle).

Why PBVI over exact value iteration?
  The exact belief-space value function is piecewise linear and convex (PWLC)
  over the continuous belief simplex. Exact VI is exponential in |S|.
  PBVI samples a finite set of reachable belief points and only computes
  α-vectors (hyperplanes) for those points — tractable for |S| ≤ ~50.

Key concepts:
  S = set of world states (cover_intact × mission_phase × adversary_knowledge)
  A = set of actions (available_actions from turning point)
  O = set of observations (trust_signal | intelligence_return | handler_report | …)
  T(s'|s,a) = transition probability  [derived from causal_dag edge strengths]
  Z(o|s',a) = observation probability [derived from adversary information_set]
  R(s,a)    = reward                  [+10 mission_success, -8 cover_blown, -1 per step]
  γ         = discount factor (0.95)

PBVI update:
  For each belief point b in B:
    For each action a:
      α_{a,o}(s) = Σ_{s'} T(s'|s,a) · Z(o|s',a) · α*(s')
      α_a(s)     = R(s,a) + γ · Σ_o max_{α} Σ_{s'} α_{a,o}(s')
    α*(b) = argmax_a  b · α_a
"""
from __future__ import annotations

import hashlib
import numpy as np
from dataclasses import dataclass, field
from typing import Optional

from dhurandhar_oracle.schemas import (
    AdversaryModel, CausalDAG, OperativeState, POOMDPResult, StackelbergResult,
)


@dataclass
class POMDPModel:
    """Discrete POMDP specification."""
    states:      list[str]          # world state IDs
    actions:     list[str]
    observations: list[str]
    T:           np.ndarray         # |S| × |A| × |S|  transition
    Z:           np.ndarray         # |A| × |S| × |O|  observation
    R:           np.ndarray         # |S| × |A|         reward
    gamma:       float = 0.95


@dataclass
class PBVISolver:
    """Point-Based Value Iteration solver."""
    model:        POMDPModel
    gamma:        float = 0.95
    n_belief_points: int = 50
    n_iterations: int = 100
    epsilon:      float = 1e-3
    alpha_vectors:        list[np.ndarray] = field(default_factory=list)
    alpha_actions:        list[int] = field(default_factory=list)
    belief_points:        list[np.ndarray] = field(default_factory=list)

    # ── PBVI ──────────────────────────────────────────────────────────────────
    def solve(self) -> None:
        """Run PBVI and populate self.alpha_vectors / self.alpha_actions."""
        n_s = len(self.model.states)
        n_a = len(self.model.actions)
        n_o = len(self.model.observations)
        T   = self.model.T
        Z   = self.model.Z
        R   = self.model.R

        if n_s == 0 or n_a == 0:
            self.alpha_vectors = []
            self.alpha_actions = []
            return

        # Sample / seed belief points (uniform + corners + caller-provided)
        self.belief_points = self._seed_belief_points(n_s)

        # Initialise alpha vectors at the lower bound (each action → flat α)
        r_min = float(R.min())
        lower = r_min / max(1e-6, 1.0 - self.gamma)
        self.alpha_vectors = [np.full(n_s, lower) for _ in range(n_a)]
        self.alpha_actions = list(range(n_a))

        prev_value = -np.inf
        for _ in range(self.n_iterations):
            new_alphas: list[np.ndarray] = []
            new_actions: list[int] = []

            # Pre-compute α_{a,o}(s) = Σ_{s'} T(s'|s,a) · Z(o|s',a) · α(s')
            # for every existing α and every (a, o) pair.
            # Shape: (|alpha|, |A|, |O|, |S|)
            # We expand inside loop to keep memory modest.
            for b in self.belief_points:
                best_val = -np.inf
                best_alpha: Optional[np.ndarray] = None
                best_action = 0

                for a in range(n_a):
                    # α_a(s) = R(s,a) + γ Σ_o max_α [Σ_{s'} T(s'|s,a) Z(o|s',a) α(s')] · 1[best for b]
                    ao_terms = np.zeros(n_s)
                    for o in range(n_o):
                        # Σ_{s'} T(s'|s,a) · Z(o|s',a) · α(s')
                        # candidates: shape (|alpha|, |S|)
                        if not self.alpha_vectors:
                            best_back = np.zeros(n_s)
                        else:
                            stacked = np.stack(self.alpha_vectors, axis=0)
                            tz = T[:, a, :] * Z[a, :, o][None, :]   # (S, S)
                            cand = stacked @ tz.T                    # (|alpha|, S)
                            scores = cand @ b                        # (|alpha|,)
                            best_back = cand[int(np.argmax(scores))]
                        ao_terms += best_back

                    alpha_a = R[:, a] + self.gamma * ao_terms
                    val = float(alpha_a @ b)
                    if val > best_val:
                        best_val = val
                        best_alpha = alpha_a
                        best_action = a

                if best_alpha is not None:
                    # Add only if not duplicate
                    if not _alpha_dominated(best_alpha, new_alphas):
                        new_alphas.append(best_alpha)
                        new_actions.append(best_action)

            if not new_alphas:
                break

            self.alpha_vectors, self.alpha_actions = _prune(
                new_alphas, new_actions, self.belief_points
            )

            # Convergence on max value across belief points
            cur_value = float(max(
                max(a @ b for a in self.alpha_vectors)
                for b in self.belief_points
            ))
            if abs(cur_value - prev_value) < self.epsilon:
                break
            prev_value = cur_value

    def _seed_belief_points(self, n_s: int) -> list[np.ndarray]:
        """Construct an initial set of belief points covering the simplex."""
        pts: list[np.ndarray] = []
        # Caller-provided initial belief is included by extract_result; here
        # we sample uniformly in the simplex + corners.
        rng = np.random.default_rng(7)
        for _ in range(self.n_belief_points):
            v = rng.dirichlet(np.ones(n_s))
            pts.append(v)
        # Corners (one-hot)
        for i in range(n_s):
            v = np.zeros(n_s)
            v[i] = 1.0
            pts.append(v)
        # Uniform
        pts.append(np.ones(n_s) / n_s)
        return pts

    # ── Extraction ────────────────────────────────────────────────────────────
    def extract_result(
        self,
        belief_state: dict[str, float],
        action_override: Optional[str] = None,
    ) -> POOMDPResult:
        """Extract optimal action and values from solved alpha vectors."""
        states = self.model.states
        actions = self.model.actions
        n_s = len(states)

        # Convert belief_state dict → numpy vector b in self.model.states order
        b = np.zeros(n_s)
        for i, s in enumerate(states):
            b[i] = float(belief_state.get(s, 0.0))
        if b.sum() <= 0:
            b = np.ones(n_s) / n_s
        else:
            b = b / b.sum()

        # V(b) = max_α (b · α)
        if not self.alpha_vectors:
            v_b = 0.0
            optimal_action = actions[0] if actions else ""
        else:
            scores = np.array([float(a @ b) for a in self.alpha_vectors])
            best_idx = int(np.argmax(scores))
            v_b = float(scores[best_idx])
            optimal_action = actions[self.alpha_actions[best_idx]]

        # Q(b, a) = max over α-vectors that originate from action a (if any),
        # else compute one-step look-ahead with current value function.
        action_values: dict[str, float] = {}
        for a_idx, a_name in enumerate(actions):
            qs = [
                float(alpha @ b)
                for alpha, alpha_a in zip(self.alpha_vectors, self.alpha_actions)
                if alpha_a == a_idx
            ]
            if qs:
                action_values[a_name] = max(qs)
            else:
                action_values[a_name] = self._one_step_q(b, a_idx)

        if action_override and action_override in actions:
            optimal_action = action_override

        # Marginal probabilities derived from state-name decoding
        cover_prob   = _decode_marginal(states, b, dim="cover")
        success_prob = _decode_marginal(states, b, dim="success")

        # Build a small "policy" map: belief_hash → optimal_action for
        # each seeded belief point.
        policy: dict[str, str] = {}
        for bp in self.belief_points[:10]:
            scores = np.array([float(a @ bp) for a in self.alpha_vectors]) if self.alpha_vectors else np.zeros(1)
            idx = int(np.argmax(scores))
            policy[_belief_hash(bp)] = actions[self.alpha_actions[idx]] if self.alpha_actions else (actions[0] if actions else "")

        return POOMDPResult(
            belief_state=dict(zip(states, [float(x) for x in b])),
            optimal_action=optimal_action,
            belief_state_value=round(v_b, 3),
            policy=policy,
            cover_integrity_prob=round(cover_prob, 4),
            mission_success_prob=round(success_prob, 4),
            action_values={k: round(v, 3) for k, v in action_values.items()},
        )

    def _one_step_q(self, b: np.ndarray, a_idx: int) -> float:
        """Q(b, a) = R(b, a) + γ Σ_o P(o|b,a) V(τ(b,a,o))."""
        n_s = len(self.model.states)
        n_o = len(self.model.observations)
        T = self.model.T
        Z = self.model.Z
        R = self.model.R
        r_ba = float(R[:, a_idx] @ b)

        future = 0.0
        for o in range(n_o):
            # P(o | b, a) = Σ_{s'} Σ_s b(s) T(s'|s,a) Z(o|s',a)
            tz = T[:, a_idx, :] * Z[a_idx, :, o][None, :]
            p_o = float(b @ tz.sum(axis=1))
            if p_o <= 1e-12:
                continue
            # τ(b, a, o)(s') = (1/p_o) Σ_s b(s) T(s'|s,a) Z(o|s',a)
            b_next = (b @ tz) / p_o
            if self.alpha_vectors:
                v_next = max(float(a_vec @ b_next) for a_vec in self.alpha_vectors)
            else:
                v_next = 0.0
            future += p_o * v_next
        return r_ba + self.gamma * future


def _alpha_dominated(candidate: np.ndarray, existing: list[np.ndarray]) -> bool:
    """True if candidate is pointwise <= some existing alpha vector."""
    for e in existing:
        if np.all(candidate <= e + 1e-9) and np.allclose(candidate, e, atol=1e-9):
            return True
    return False


def _prune(
    alphas: list[np.ndarray],
    actions: list[int],
    belief_points: list[np.ndarray],
) -> tuple[list[np.ndarray], list[int]]:
    """Keep only alphas that are best at some belief point."""
    if not alphas:
        return [], []
    keep: set[int] = set()
    for b in belief_points:
        scores = np.array([float(a @ b) for a in alphas])
        keep.add(int(np.argmax(scores)))
    kept_alphas = [alphas[i] for i in sorted(keep)]
    kept_actions = [actions[i] for i in sorted(keep)]
    return kept_alphas, kept_actions


def _belief_hash(b: np.ndarray) -> str:
    """Stable short hash of a belief vector for the policy map."""
    rounded = np.round(b, 3)
    return hashlib.md5(rounded.tobytes()).hexdigest()[:10]


def _decode_marginal(states: list[str], b: np.ndarray, dim: str) -> float:
    """
    Marginalise a belief vector along an interpreted dimension based on
    the conventional state name encoding:
        "cover_<status>_mission_<phase>_adv_<knowledge>"
    `dim` ∈ {"cover", "success"}.

    Success probability is approximated as a weighted sum over states using
    a viability score: cover (intact=1, suspected=0.5, blown=0) × adv_factor
    (unaware=1.0, suspicious=0.6, certain=0.2) × phase_factor (success=1.0,
    late=0.85, mid=0.65, early=0.5, stalled=0.05).
    """
    if dim == "cover":
        cover_w = {"intact": 1.0, "suspected": 0.5, "blown": 0.0}
        return float(sum(
            cover_w[_state_class(s)["cover"]] * p
            for s, p in zip(states, b)
        ))
    if dim == "success":
        cover_w = {"intact": 1.0, "suspected": 0.6, "blown": 0.0}
        adv_w   = {"unaware": 1.0, "suspicious": 0.7, "certain": 0.25}
        phase_w = {"success": 1.0, "late": 0.85, "mid": 0.65,
                   "early": 0.5,  "stalled": 0.05}
        total = 0.0
        for s, p in zip(states, b):
            c = _state_class(s)
            total += p * cover_w[c["cover"]] * adv_w[c["adv"]] * phase_w[c["phase"]]
        return float(min(1.0, total))
    return 0.0


# ── POMDP construction ───────────────────────────────────────────────────────

# Heuristic action keyword → effect on cover/mission, for transition shaping
_RISKY_KEYWORDS = (
    "trigger_early_exfil", "exfil", "kinetic", "strike", "attack",
    "expose", "raid", "confront", "extract", "abduct",
)
_COVER_DEEPENING_KEYWORDS = (
    "deepen", "consolidate", "accept", "marriage", "loyalty", "embed",
    "build_trust", "build", "blend", "infiltrate",
)
_INTEL_KEYWORDS = (
    "gather", "intel", "intelligence", "surveil", "observe", "scout",
    "report", "trace", "identify", "monitor",
)
_HANDLER_KEYWORDS = (
    "handler", "comms", "request", "backup", "report_to_handler",
    "coordinate", "consult", "delegate",
)


def _classify_action(name: str) -> str:
    """Map an action string to a coarse class for transition shaping."""
    low = name.lower()
    if any(k in low for k in _RISKY_KEYWORDS):
        return "risky"
    if any(k in low for k in _COVER_DEEPENING_KEYWORDS):
        return "cover"
    if any(k in low for k in _INTEL_KEYWORDS):
        return "intel"
    if any(k in low for k in _HANDLER_KEYWORDS):
        return "handler"
    return "neutral"


def _state_class(name: str) -> dict:
    """Decode a state-id into its conceptual coordinates."""
    low = name.lower()
    cover = (
        "blown" if "cover_blown" in low
        else "suspected" if "cover_suspected" in low
        else "intact"
    )
    if "mission_success" in low:
        phase = "success"
    elif "stalled" in low or "fail" in low:
        phase = "stalled"
    elif "exfil" in low or "extraction" in low or "late" in low:
        phase = "late"
    elif "mid" in low:
        phase = "mid"
    else:
        phase = "early"
    if "adv_certain" in low:
        adv = "certain"
    elif "adv_suspicious" in low:
        adv = "suspicious"
    else:
        adv = "unaware"
    return {"cover": cover, "phase": phase, "adv": adv}


_PHASE_ORDER = {"early": 0, "mid": 1, "late": 2, "success": 3, "stalled": 3}
_COVER_ORDER = {"intact": 0, "suspected": 1, "blown": 2}
_ADV_ORDER   = {"unaware": 0, "suspicious": 1, "certain": 2}


def _transition_score(s_from: dict, s_to: dict, action_class: str) -> float:
    """
    Heuristic transition affinity score (un-normalised).
    We bias movement along the (phase forward / cover degraded / adv knows more)
    axes depending on action class and source state.
    """
    # Terminal-ish states are sticky
    if s_from["phase"] in ("success", "stalled") and s_from == s_to:
        return 8.0
    if s_from["cover"] == "blown" and s_to["cover"] == "blown":
        return 6.0  # blown cover persists

    df_phase = _PHASE_ORDER[s_to["phase"]] - _PHASE_ORDER[s_from["phase"]]
    df_cover = _COVER_ORDER[s_to["cover"]] - _COVER_ORDER[s_from["cover"]]
    df_adv   = _ADV_ORDER[s_to["adv"]]    - _ADV_ORDER[s_from["adv"]]

    # Self-loop weight (always some inertia)
    if s_from == s_to:
        return 3.0

    score = 1.0
    # Phase: missions only progress forward (or stall)
    if df_phase < 0:
        return 0.05  # backward time travel near-zero
    if df_phase > 1:
        return 0.1

    # Class-conditional shaping
    if action_class == "risky":
        # Risky moves accelerate phase but degrade cover and tip adversary
        score *= 1.0 + 0.6 * df_phase
        score *= 1.0 + 0.7 * max(0, df_cover)
        score *= 1.0 + 0.5 * max(0, df_adv)
        score *= 1.0 - 0.4 * max(0, -df_cover)  # discourage cover repair
    elif action_class == "cover":
        # Cover-deepening: phase mild, cover stable or repaired, adv calmer
        score *= 1.0 + 0.3 * df_phase
        score *= 1.0 + 0.5 * max(0, -df_cover)  # encourage repair (intact ← suspected)
        score *= 1.0 - 0.5 * max(0, df_cover)   # discourage degradation
        score *= 1.0 - 0.3 * max(0, df_adv)
    elif action_class == "intel":
        # Intel gathering: small forward phase, slight risk to cover
        score *= 1.0 + 0.4 * df_phase
        score *= 1.0 + 0.2 * max(0, df_cover)
        score *= 1.0 + 0.2 * max(0, df_adv)
    elif action_class == "handler":
        # Handler comms: low risk, low phase shift
        score *= 1.0 + 0.2 * df_phase
        score *= 1.0 + 0.1 * max(0, df_cover)
        score *= 1.0 + 0.05 * max(0, df_adv)
    else:  # neutral
        score *= 1.0 + 0.2 * df_phase
        score *= 1.0 + 0.2 * max(0, df_cover)
        score *= 1.0 + 0.2 * max(0, df_adv)

    return max(score, 0.01)


def _action_cover_pressure(action_name: str, causal_dag: CausalDAG) -> float:
    """Total causal-DAG strength of cover-degrading effects from this action."""
    bad_terms = ("cover_blown", "identity_exposed", "cover_suspected",
                 "operative_captured", "exfil_burn")
    pressure = 0.0
    for e in causal_dag.edges:
        if e.cause == action_name and any(t in e.effect for t in bad_terms):
            pressure += float(e.strength)
    return pressure


def _action_mission_lift(action_name: str, causal_dag: CausalDAG) -> float:
    """Total causal-DAG strength of mission-progressing effects from this action."""
    good_terms = ("trust_increase", "intelligence_gain", "intelligence_extract",
                  "mission_success", "network_access", "cover_strengthen",
                  "intel_acquired", "trust_built", "asset_secured")
    lift = 0.0
    for e in causal_dag.edges:
        if e.cause == action_name and any(t in e.effect for t in good_terms):
            lift += float(e.strength)
    return lift


def _state_reward(state_name: str) -> float:
    """Base per-state reward."""
    s = _state_class(state_name)
    if s["phase"] == "success":
        return 10.0
    if s["phase"] == "stalled" or s["cover"] == "blown":
        return -8.0
    base = -0.1  # step cost
    if s["cover"] == "suspected":
        base -= 0.4
    if s["adv"] == "certain":
        base -= 1.5
    elif s["adv"] == "suspicious":
        base -= 0.5
    if s["phase"] == "late":
        base += 1.0
    return base


def build_pomdp(
    available_actions: list[str],
    causal_dag: CausalDAG,
    adversaries: list[AdversaryModel],
    state_vector: OperativeState,
    initial_belief: dict[str, float],
    stackelberg: Optional[StackelbergResult] = None,
) -> POMDPModel:
    """
    Construct a POMDPModel from turning-point data.

    World states are taken from initial_belief keys (typically already encoding
    cover_status × mission_phase × adversary_knowledge).

    Transitions T(s'|s,a) blend a heuristic affinity score with causal-DAG
    pressure (cover-degrading effects raise P(s' has worse cover); mission-
    progressing effects raise P(s' advances phase)).

    Observation Z(o|s',a) is derived from adversary capability: low-capability
    adversaries emit informative trust/intel signals; high-capability adversaries
    emit ambiguous signals more often.

    Reward R(s,a):
      Per-state base (terminal +10 / blown -8 / step cost) +
      action effort cost (Stackelberg-aligned actions get a small bonus).
    """
    # Always work in a stable state ordering
    states = list(initial_belief.keys()) or [
        "cover_intact_mission_early_adv_unaware",
        "cover_intact_mission_mid_adv_suspicious",
        "cover_suspected_mission_mid_adv_suspicious",
        "cover_blown_mission_stalled_adv_certain",
    ]
    n_s = len(states)
    n_a = len(available_actions)
    observations = ["trust_signal", "intelligence_return", "no_signal"]
    n_o = len(observations)

    # ── Transition matrix T(s'|s,a) ───────────────────────────────────────────
    decoded = [_state_class(s) for s in states]
    T = np.zeros((n_s, n_a, n_s))
    for ai, a_name in enumerate(available_actions):
        klass    = _classify_action(a_name)
        cov_pres = _action_cover_pressure(a_name, causal_dag)  # 0..several
        miss_lift = _action_mission_lift(a_name, causal_dag)

        for si, s_from in enumerate(decoded):
            row = np.zeros(n_s)
            for sj, s_to in enumerate(decoded):
                w = _transition_score(s_from, s_to, klass)
                # Apply DAG-derived nudges
                if s_to["cover"] == "blown" and s_from["cover"] != "blown":
                    w *= 1.0 + 0.8 * cov_pres
                if s_to["phase"] in ("late", "success") and s_from["phase"] in ("early", "mid"):
                    w *= 1.0 + 0.6 * miss_lift
                row[sj] = w
            row /= row.sum() if row.sum() > 0 else 1.0
            T[si, ai] = row

    # ── Observation matrix Z(o|s',a) ──────────────────────────────────────────
    avg_capability = (
        sum(a.capability for a in adversaries) / len(adversaries) / 10.0
        if adversaries else 0.4
    )
    Z = np.zeros((n_a, n_s, n_o))
    for ai, a_name in enumerate(available_actions):
        klass = _classify_action(a_name)
        for sj, s_to in enumerate(decoded):
            # Base (trust, intel, none) probabilities
            if klass == "intel":
                base = np.array([0.25, 0.55, 0.20])
            elif klass == "cover":
                base = np.array([0.55, 0.20, 0.25])
            elif klass == "handler":
                base = np.array([0.30, 0.30, 0.40])
            elif klass == "risky":
                base = np.array([0.20, 0.30, 0.50])
            else:
                base = np.array([0.33, 0.33, 0.34])

            # If adversary is more capable, observations get noisier
            base = base * (1.0 - 0.4 * avg_capability) + 0.4 * avg_capability * np.array([1 / 3] * 3)
            # If cover blown, no_signal dominates (operative likely loses comms)
            if s_to["cover"] == "blown":
                base = np.array([0.05, 0.05, 0.90])
            base = base / base.sum()
            Z[ai, sj] = base

    # ── Reward matrix R(s,a) ──────────────────────────────────────────────────
    R = np.zeros((n_s, n_a))
    leader_action = stackelberg.leader_action if stackelberg else None
    for ai, a_name in enumerate(available_actions):
        klass = _classify_action(a_name)
        for si, s_name in enumerate(decoded):
            r = _state_reward(states[si])
            # Action effort cost
            if klass == "risky":
                r -= 0.6
            elif klass == "intel":
                r -= 0.2
            elif klass == "cover":
                r -= 0.1
            elif klass == "handler":
                r -= 0.05
            # Stackelberg leader-aligned actions get a small bonus
            if leader_action and leader_action == a_name:
                r += 0.4
            # Penalise risky when already suspected
            if klass == "risky" and s_name["cover"] in ("suspected", "blown"):
                r -= 1.5
            R[si, ai] = r

    return POMDPModel(
        states=states,
        actions=available_actions,
        observations=observations,
        T=T,
        Z=Z,
        R=R,
        gamma=0.95,
    )
