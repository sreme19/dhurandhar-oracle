"""
narrator_node — Claude war-room briefing.

Same pattern as got-oracle narrator, adapted for intelligence-ops output.

Responsibilities:
  1. Assemble the full DhurandharState trace into a structured prompt
  2. Call Claude to write a war-room briefing (ANTHROPIC_API_KEY required)
  3. Fall back to a Rich-formatted template if no API key is set

The briefing covers:
  - POMDP optimal action and action values
  - CPM critical path and days saved
  - VoI top intelligence targets
  - Stackelberg adversary response prediction
  - HMM belief gaps / mole alerts
  - Shapley asset rankings
  - Monte Carlo mission success delta (actual vs optimal)

Input  keys: (all populated state keys)
Output keys: narrative, errors, warnings
"""
from __future__ import annotations

import os

from dhurandhar_oracle.state import DhurandharState

_MODEL = "claude-opus-4-5"
_SYSTEM_PROMPT = """\
You are a RAW war-room analyst briefing the National Security Advisor of India.
You write concise, classified-style intelligence assessments.
Given a full quantitative analysis trace, produce a structured war-room briefing covering:
1. Recommended action (with POMDP confidence)
2. What was done suboptimally (CPM/PERT critical path)
3. Intelligence priorities (VoI ranking)
4. Anticipated adversary moves (Stackelberg)
5. Mole / loyalty alerts (HMM belief gaps)
6. Asset coalition health (Shapley)
7. Mission success delta vs optimal path (Monte Carlo)

Use a clipped, classified-document tone. No preamble. Start with: OPERATIVE: [name].
"""


def narrator_node(state: DhurandharState) -> dict:
    """Generate Claude narrative or Rich template fallback."""
    errors:   list[str] = []
    warnings: list[str] = []

    api_key = os.environ.get("ANTHROPIC_API_KEY", "")

    if api_key:
        narrative = _claude_narrative(state, api_key)
    else:
        warnings.append("narrator_node: ANTHROPIC_API_KEY not set — using template fallback")
        narrative = _template_narrative(state)

    return {"narrative": narrative, "errors": errors, "warnings": warnings}


def _claude_narrative(state: DhurandharState, api_key: str) -> str:
    """Call Claude to generate the war-room briefing."""
    import anthropic

    trace = _build_trace(state)
    client = anthropic.Anthropic(api_key=api_key)

    msg = client.messages.create(
        model=_MODEL,
        max_tokens=1024,
        system=_SYSTEM_PROMPT,
        messages=[{"role": "user", "content": trace}],
    )
    return msg.content[0].text


def _template_narrative(state: DhurandharState) -> str:
    """Rich-formatted template fallback (no LLM required)."""
    lines = [
        f"OPERATIVE: {state.get('operative', 'UNKNOWN').upper()}",
        f"TURNING POINT: {state.get('turning_point', 'UNKNOWN')}",
        "",
    ]

    # POMDP
    pomdp = state.get("pomdp")
    if pomdp:
        lines += [
            "── OPTIMAL ACTION (POMDP) ──────────────────────────────────────",
            f"  {pomdp.optimal_action}  (V(b) = {pomdp.belief_state_value:.2f})",
            f"  Mission success prob: {pomdp.mission_success_prob:.1%}",
            f"  Cover integrity prob: {pomdp.cover_integrity_prob:.1%}",
            "",
        ]

    # CPM
    cp = state.get("critical_path")
    if cp:
        lines += [
            "── CRITICAL PATH (CPM/PERT) ─────────────────────────────────────",
            f"  Total duration: {cp.total_duration_days:.0f}d  →  Optimal: {cp.optimal_duration_days:.0f}d  (save {cp.days_saved:.0f}d)",
            f"  Bottleneck: {cp.bottleneck_task}",
            f"  Critical path: {' → '.join(cp.critical_path)}",
            "",
        ]

    # VoI
    voi = state.get("voi_result")
    if voi and voi.rankings:
        lines += ["── INTELLIGENCE PRIORITIES (VoI) ───────────────────────────────"]
        for entry in voi.rankings[:3]:
            lines.append(f"  #{entry.priority_rank} {entry.intelligence_target}  VoI={entry.voi_bits:.2f}bits")
        lines.append("")

    # Stackelberg
    sg = state.get("stackelberg")
    if sg:
        lines += [
            "── ADVERSARY RESPONSE (STACKELBERG) ────────────────────────────",
            f"  Handler commits to: {sg.leader_action}",
            f"  Operative best response: {sg.operative_best_response}",
            f"  Adversary counter: {sg.follower_best_response}",
            f"  Commitment value: +{sg.commitment_value:.2f}",
            "",
        ]

    # Belief gaps
    gaps = state.get("belief_gaps", [])
    if gaps:
        lines += ["── BELIEF GAPS (HMM MOLE DETECTION) ────────────────────────────"]
        for bg in gaps:
            flag = " ← MOLE ALERT" if bg.gap > 0.75 else ""
            lines.append(f"  {bg.actor}: believed={bg.operative_believed}  actual={bg.hmm_inferred}  gap={bg.gap:.2f}{flag}")
        lines.append("")

    # Simulation delta
    sim_opt = state.get("simulation_optimal")
    sim_act = state.get("simulation_actual")
    if sim_opt and sim_act:
        delta = sim_opt.p_mission_success - sim_act.p_mission_success
        lines += [
            "── SIMULATION DELTA ────────────────────────────────────────────",
            f"  Actual action ({sim_act.action}):  P(success)={sim_act.p_mission_success:.1%}",
            f"  Optimal action ({sim_opt.action}): P(success)={sim_opt.p_mission_success:.1%}",
            f"  Δ = +{delta:.1%} if optimal path taken",
            "",
        ]

    return "\n".join(lines)


def _build_trace(state: DhurandharState) -> str:
    """Serialise relevant state fields into a text trace for Claude."""
    import json
    # Exclude raw graph data (too large), keep computed results
    trace_keys = [
        "operative", "turning_point",
        "pomdp", "critical_path", "voi_result", "stackelberg",
        "belief_gaps", "shapley", "simulation_actual", "simulation_optimal",
        "threat_scores", "warnings",
    ]
    trace = {k: state.get(k) for k in trace_keys if state.get(k) is not None}

    # Pydantic models → dicts
    def default(obj):
        if hasattr(obj, "model_dump"):
            return obj.model_dump()
        return str(obj)

    return json.dumps(trace, default=default, indent=2)
