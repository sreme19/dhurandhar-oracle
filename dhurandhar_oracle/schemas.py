"""
dhurandhar-oracle — Pydantic schemas.

All data contracts between agents live here.
Every agent reads/writes typed objects; raw dicts are only used
at the JSON I/O boundary in io/loader.py.

New vs got-oracle:
  OperativeState      replaces  PlayerState        (intelligence-ops 5-dim vector)
  MissionTask         new       CPM/PERT task node
  IntelligenceTarget  new       VoI input
  POOMDPResult        new       POMDP optimal policy output
  CriticalPathResult  new       CPM critical path output
  VoIEntry / VoIResult new      Value of Information output
  StackelbergResult   new       leader-follower equilibrium output
  CharacterProfile    replaces  CharacterData       (adds side + cover_identity gate)
"""
from __future__ import annotations

from typing import Literal, Optional
from pydantic import BaseModel, Field, model_validator


# ── Operative state ────────────────────────────────────────────────────────────

class OperativeState(BaseModel):
    """5-dimensional state vector for an operative at a specific turning point."""
    cover_integrity:    float = Field(..., ge=0, le=10,
                                     description="How intact the operative's false identity is")
    trust_capital:      float = Field(..., ge=0, le=10,
                                     description="Trust built with the target criminal/political network")
    intelligence_depth: float = Field(..., ge=0, le=10,
                                     description="Quality and quantity of intel gathered so far")
    network_strength:   float = Field(..., ge=0, le=10,
                                     description="Quality of handler / asset support network")
    exposure_risk:      float = Field(..., ge=0, le=10,
                                     description="How close the operative is to being discovered")


# ── Causal model (reused from got-oracle) ─────────────────────────────────────

class CausalEdge(BaseModel):
    cause:             str
    effect:            str
    strength:          float = Field(..., ge=0, le=1, description="P(effect | cause) approximately")
    known_confounders: list[str] = Field(default_factory=list)
    identified:        bool = Field(True, description="Whether do-calculus identification holds")
    confidence:        float = Field(0.5, ge=0, le=1, description="Confidence in strength estimate")
    strength_low:      Optional[float] = Field(None, ge=0, le=1)
    strength_high:     Optional[float] = Field(None, ge=0, le=1)
    estimation_method: Optional[str] = Field(None, description="How this edge strength was estimated")
    source_refs:       list[str] = Field(default_factory=list, description="Traceability references")


class CausalDAG(BaseModel):
    nodes: list[str]
    edges: list[CausalEdge]

    def successors(self, node: str) -> list[str]:
        return [e.effect for e in self.edges if e.cause == node]

    def predecessors(self, node: str) -> list[str]:
        return [e.cause for e in self.edges if e.effect == node]

    def get_edge(self, cause: str, effect: str) -> Optional[CausalEdge]:
        for e in self.edges:
            if e.cause == cause and e.effect == effect:
                return e
        return None


# ── Alliances (reused from got-oracle) ────────────────────────────────────────

class AllianceEdge(BaseModel):
    source:            str
    target:            str
    strength:          float = Field(..., ge=0, le=1)
    betrayal_history:  int   = Field(0, ge=0)
    in_coalition:      bool  = Field(True)
    trigger_condition: Optional[str] = None


# ── Adversary model (reused, Prospect Theory params kept) ─────────────────────

class ProspectParams(BaseModel):
    lam:   float = Field(2.25, description="Loss aversion λ")
    gamma: float = Field(0.65, description="Probability weighting γ")
    alpha: float = Field(0.88, description="Gain curvature α")
    beta:  float = Field(0.88, description="Loss curvature β")
    ref:   float = Field(0.0,  description="Reference point")


class AdversaryModel(BaseModel):
    actor:              str
    objective:          str
    capability:         float = Field(..., ge=0, le=10)
    trigger_threshold:  float = Field(..., ge=0, le=10)
    information_set:    list[str] = Field(default_factory=list)
    observable_actions: list[str] = Field(default_factory=list)
    hidden_states:      list[str] = Field(default_factory=list)
    prospect_params:    ProspectParams = Field(default_factory=ProspectParams)


# ── CPM / PERT task ────────────────────────────────────────────────────────────

class MissionTask(BaseModel):
    """A task node in the mission PERT network."""
    id:                    str
    name:                  str
    optimistic_days:       int  = Field(..., ge=1, description="PERT optimistic estimate")
    most_likely_days:      int  = Field(..., ge=1, description="PERT most-likely estimate")
    pessimistic_days:      int  = Field(..., ge=1, description="PERT pessimistic estimate")
    dependencies:          list[str] = Field(default_factory=list, description="IDs of predecessor tasks")
    parallelizable_with:   list[str] = Field(default_factory=list,
                                             description="Task IDs that can run concurrently")
    requires_cover:        bool = Field(True,  description="Does this task depend on cover integrity?")
    risk_to_cover:         float = Field(0.0, ge=0, le=1,
                                         description="Probability this task degrades cover if rushed")

    @property
    def pert_expected(self) -> float:
        """PERT expected duration: (O + 4M + P) / 6."""
        return (self.optimistic_days + 4 * self.most_likely_days + self.pessimistic_days) / 6

    @property
    def pert_variance(self) -> float:
        """PERT variance: ((P - O) / 6)²."""
        return ((self.pessimistic_days - self.optimistic_days) / 6) ** 2


# ── Intelligence targets (VoI inputs) ─────────────────────────────────────────

class IntelligenceTarget(BaseModel):
    """A piece of intelligence the operative could gather."""
    id:               str
    name:             str
    current_entropy:  float = Field(..., ge=0, description="Current uncertainty (bits) about this target")
    mission_relevance: float = Field(..., ge=0, le=1,
                                    description="How much this target affects mission success")
    access_difficulty: float = Field(..., ge=0, le=10,
                                    description="Effort / risk required to gather this intel")
    access_actions:   list[str] = Field(default_factory=list,
                                        description="Actions that would yield this intel")
    confidence:       float = Field(0.5, ge=0, le=1, description="Confidence in target scoring inputs")
    source_refs:      list[str] = Field(default_factory=list)


# ── Turning point ──────────────────────────────────────────────────────────────

class TurningPoint(BaseModel):
    id:                      str
    operative:               str
    film:                    int = Field(..., ge=1, le=4, description="1=Film1, 2=Film2, 3=Film3 (2016-2019), 4=Film4 (2020-2025+)")
    act:                     int = Field(..., ge=1, le=3)
    description:             str
    state_vector:            OperativeState
    available_actions:       list[str]
    mission_tasks:           list[MissionTask]
    causal_dag:              CausalDAG
    adversaries:             list[AdversaryModel]
    alliance_snapshot:       list[AllianceEdge]
    intelligence_targets:    list[IntelligenceTarget]
    belief_state:            dict[str, float] = Field(
        default_factory=dict,
        description="Initial POMDP belief distribution: world_state_id → probability"
    )
    real_world_correlation:  Optional[dict] = Field(
        None,
        description="Grounded real-world event data: dates, actors, forensic details. "
                    "Passed to narrator_node for Claude briefing context."
    )
    next_turning_point:      Optional[str] = Field(
        None,
        description="ID of the chronologically next TP — used to propagate terminal belief state forward"
    )
    terminal_belief:         Optional[dict[str, float]] = Field(
        None,
        description="Belief distribution at end of this TP — seeds next_turning_point initial belief"
    )
    source_refs:             list[str] = Field(default_factory=list)
    owner:                   Optional[str] = None
    updated_at:              Optional[str] = Field(None, description="ISO timestamp for last data revision")
    schema_version:          str = Field("1.1.0", description="Data schema version for turning points")


# ── Agent output schemas (new) ─────────────────────────────────────────────────

class POOMDPResult(BaseModel):
    """Output of strategy_node (POMDP Point-Based Value Iteration)."""
    belief_state:          dict[str, float]   # world_state → probability
    optimal_action:        str
    belief_state_value:    float              # V(b) at current belief
    policy:                dict[str, str]     # belief_hash → optimal_action (for nearby beliefs)
    cover_integrity_prob:  float = Field(..., ge=0, le=1)
    mission_success_prob:  float = Field(..., ge=0, le=1)
    action_values:         dict[str, float]   # action → Q(b, a)


class CriticalPathResult(BaseModel):
    """Output of critical_path_node (CPM + PERT)."""
    critical_path:                  list[str]            # task IDs in order
    total_duration_days:            float                # PERT expected total
    optimal_duration_days:          float                # if parallelisation exploited
    days_saved:                     float
    bottleneck_task:                str                  # highest-impact task on critical path
    slack_tasks:                    list[tuple[str, float]]  # (task_id, slack_days)
    parallelisation_opportunities:  list[tuple[str, str]]   # (task_a, task_b) pairs


class VoIEntry(BaseModel):
    """Single intelligence target ranked by Value of Information."""
    intelligence_target: str
    voi_bits:            float = Field(..., ge=0, description="Expected entropy reduction in bits")
    priority_rank:       int
    effort_required:     float
    recommendation:      str


class VoIResult(BaseModel):
    """Output of voi_node."""
    rankings:            list[VoIEntry]
    top_target:          str
    total_entropy_bits:  float


class StackelbergResult(BaseModel):
    """Output of adversary_node (Stackelberg leader-follower equilibrium)."""
    leader_action:              str    # what RAW / the handler committed to
    operative_best_response:    str    # what the operative should do given leader commitment
    follower_best_response:     str    # what the adversary (Dakait/Jamali) will do
    equilibrium_payoff_indian:  float
    equilibrium_payoff_adversary: float
    commitment_value:           float  # V(Stackelberg) - V(Nash): value of pre-commitment


# ── Agent output schemas (reused / adapted from got-oracle) ───────────────────

class CentralityScores(BaseModel):
    betweenness: dict[str, float]
    eigenvector: dict[str, float]
    clustering:  dict[str, float]
    communities: list[list[str]]


class ThreatScore(BaseModel):
    actor:       str
    score:       float
    betweenness: float
    eigenvector: float
    is_high:     bool


class ShapleyResult(BaseModel):
    values:               dict[str, float]
    defection_incentives: dict[str, float]


class HMMResult(BaseModel):
    actor:             str
    hidden_states:     list[str]
    most_likely_state: str
    state_probs:       dict[str, float]
    viterbi_path:      list[str]


class BeliefGap(BaseModel):
    actor:           str
    operative_believed: str
    hmm_inferred:    str
    gap:             float


class SimulationOutput(BaseModel):
    action:               str
    p_mission_success:    float = Field(..., ge=0, le=1)
    p_cover_blown:        float = Field(..., ge=0, le=1)
    ci_low:               float
    ci_high:              float
    n_rollouts:           int
    mode_outcome:         str
    key_lever:            Optional[str] = None


# ── Character profile ──────────────────────────────────────────────────────────

class ObservableActionEntry(BaseModel):
    film:   int
    act:    int
    action: str


class CharacterProfile(BaseModel):
    """
    Master character record.

    IMPORTANT: `side` gates oracle access.
    Only characters with side="indian" can be queried as operatives.
    Pakistani / unknown characters exist as adversary models only.
    """
    id:                   str
    name:                 str
    nationality:          str
    side:                 Literal["indian", "pakistani", "unknown"]
    role:                 str    # e.g. "RAW undercover operative", "NSA handler", "criminal"
    films:                list[int]
    cover_identity:       Optional[str] = None   # false name used in the field
    real_life_inspiration: Optional[str] = None
    state_by_act:         dict[str, OperativeState]   # "film1_act2" → state
    observable_history:   list[ObservableActionEntry] = Field(default_factory=list)
    adversary_model:      Optional[AdversaryModel] = None

    @model_validator(mode="after")
    def cover_identity_only_for_undercover(self) -> "CharacterProfile":
        if self.cover_identity and self.side != "indian":
            raise ValueError("cover_identity only applies to Indian operatives")
        return self


# ── Outcome record ─────────────────────────────────────────────────────────────

class OutcomeEntry(BaseModel):
    turning_point_id:  str
    actual_action:     str
    immediate_effects: list[str]
    terminal_state:    str   # "mission_success" | "cover_blown" | "exfil" | "kia" | "in_progress"
    days_elapsed:      int
    losses:            list[str] = Field(default_factory=list)
    intel_gained:      list[str] = Field(default_factory=list)
    cover_change:      float = Field(0.0, ge=-10, le=10, description="Delta in cover_integrity")
    confidence:        float = Field(0.5, ge=0, le=1)
    source_refs:       list[str] = Field(default_factory=list)
    owner:             Optional[str] = None
    updated_at:        Optional[str] = Field(None, description="ISO timestamp for last data revision")
    schema_version:    str = Field("1.1.0", description="Data schema version for outcomes")
