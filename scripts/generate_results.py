"""
generate_results.py — Run the oracle pipeline across every (operative, turning_point)
pair and persist the structured outputs to results/.

For each turning point we save:
  - results/json/<operative>__<turning_point>.json   raw structured oracle state
  - results/markdown/<operative>__<turning_point>.md   human-readable briefing

Plus a top-level results/INDEX.md aggregator and results/SUMMARY.json.
"""
from __future__ import annotations

import json
import sys
import time
import traceback
from pathlib import Path

from dhurandhar_oracle.graph import oracle_graph
from dhurandhar_oracle.io.loader import list_characters, list_turning_points

ROOT          = Path(__file__).resolve().parent.parent
RESULTS_DIR   = ROOT / "results"
JSON_DIR      = RESULTS_DIR / "json"
MARKDOWN_DIR  = RESULTS_DIR / "markdown"


def _serialise(obj):
    if hasattr(obj, "model_dump"):
        return obj.model_dump()
    if isinstance(obj, dict):
        return {k: _serialise(v) for k, v in obj.items()}
    if isinstance(obj, (list, tuple)):
        return [_serialise(v) for v in obj]
    if isinstance(obj, (str, int, float, bool)) or obj is None:
        return obj
    return str(obj)


def _markdown_for(operative: str, tp_id: str, result: dict) -> str:
    lines = [f"# Oracle briefing — `{operative}` / `{tp_id}`", ""]
    desc = result.get("turning_point_description")
    if desc:
        lines += [f"> {desc}", ""]

    pomdp = result.get("pomdp")
    if pomdp:
        lines += [
            "## POMDP — Optimal Policy",
            "",
            f"- **Optimal action:** `{pomdp.optimal_action}`",
            f"- V(b): `{pomdp.belief_state_value:.3f}`",
            f"- P(mission success): `{pomdp.mission_success_prob:.1%}`",
            f"- P(cover intact): `{pomdp.cover_integrity_prob:.1%}`",
            "",
            "| Action | Q(b, a) |",
            "|---|---|",
        ]
        for a, q in sorted(pomdp.action_values.items(), key=lambda x: -x[1]):
            mark = " ← OPTIMAL" if a == pomdp.optimal_action else ""
            lines.append(f"| `{a}`{mark} | {q:.3f} |")
        lines.append("")

    cp = result.get("critical_path")
    if cp:
        lines += [
            "## Critical Path (CPM/PERT)",
            "",
            f"- Path: {' → '.join(f'`{x}`' for x in cp.critical_path)}",
            f"- Total: **{cp.total_duration_days:.0f} d**  →  Optimal: **{cp.optimal_duration_days:.0f} d**  (save {cp.days_saved:.0f} d)",
            f"- Bottleneck: `{cp.bottleneck_task}`",
        ]
        if cp.parallelisation_opportunities:
            opps = ", ".join(f"`{a}` ‖ `{b}`" for a, b in cp.parallelisation_opportunities[:5])
            lines.append(f"- Parallelisable: {opps}")
        lines.append("")

    voi = result.get("voi_result")
    if voi and voi.rankings:
        lines += [
            "## Value of Information",
            "",
            f"- Total entropy: **{voi.total_entropy_bits:.2f} bits**",
            f"- Top target: `{voi.top_target}`",
            "",
            "| Rank | Target | VoI (bits) | Effort | Recommendation |",
            "|---|---|---|---|---|",
        ]
        for v in voi.rankings:
            lines.append(
                f"| {v.priority_rank} | {v.intelligence_target} | {v.voi_bits:.2f} | {v.effort_required:.1f} | {v.recommendation} |"
            )
        lines.append("")

    sg = result.get("stackelberg")
    if sg:
        lines += [
            "## Stackelberg Equilibrium",
            "",
            f"- Handler commits to: `{sg.leader_action}`",
            f"- Operative best response: `{sg.operative_best_response}`",
            f"- Adversary counter: `{sg.follower_best_response}`",
            f"- Indian payoff: `{sg.equilibrium_payoff_indian:.3f}`",
            f"- Commitment value vs Nash: `+{sg.commitment_value:.3f}`",
            "",
        ]

    gaps = result.get("belief_gaps", [])
    if gaps:
        lines += [
            "## HMM Belief Gaps — Mole Detection",
            "",
            "| Actor | Operative believed | HMM inferred | Gap | Alert |",
            "|---|---|---|---|---|",
        ]
        for bg in gaps:
            alert = "⚠ MOLE?" if bg.gap > 0.75 else ""
            lines.append(f"| {bg.actor} | {bg.operative_believed} | {bg.hmm_inferred} | {bg.gap:.2f} | {alert} |")
        lines.append("")

    shapley = result.get("shapley")
    if shapley and shapley.values:
        lines += [
            "## Shapley Values — Asset Coalition",
            "",
            "| Actor | φ | Defection incentive |",
            "|---|---|---|",
        ]
        for actor, phi in sorted(shapley.values.items(), key=lambda x: -x[1]):
            d = shapley.defection_incentives.get(actor, 0.0)
            lines.append(f"| {actor} | {phi:.3f} | {d:.3f} |")
        lines.append("")

    sa = result.get("simulation_actual")
    so = result.get("simulation_optimal")
    if sa and so:
        delta = so.p_mission_success - sa.p_mission_success
        lines += [
            "## Monte Carlo Simulation",
            "",
            f"- Rollouts per arm: {sa.n_rollouts}",
            f"- Actual ({sa.action}): P(success)=**{sa.p_mission_success:.1%}**  [{sa.ci_low:.1%}–{sa.ci_high:.1%}]",
            f"- Optimal ({so.action}): P(success)=**{so.p_mission_success:.1%}**  [{so.ci_low:.1%}–{so.ci_high:.1%}]",
            f"- Δ = **{delta:+.1%}** if optimal path taken",
        ]
        if so.key_lever:
            lines.append(f"- Key causal lever: `{so.key_lever}`")
        lines.append("")

    threats = result.get("threat_scores")
    if threats:
        lines += [
            "## Threat Scores (SNA)",
            "",
            "| Actor | Score | Betweenness | Eigenvector | High-threat |",
            "|---|---|---|---|---|",
        ]
        for ts in threats:
            lines.append(
                f"| {ts.actor} | {ts.score:.3f} | {ts.betweenness:.3f} | {ts.eigenvector:.3f} | {'YES' if ts.is_high else 'no'} |"
            )
        lines.append("")

    warnings = result.get("warnings", [])
    if warnings:
        lines += ["## Warnings", ""]
        for w in warnings:
            lines.append(f"- {w}")
        lines.append("")

    return "\n".join(lines)


def run_one(operative: str, tp_id: str) -> dict:
    state = {
        "operative": operative,
        "turning_point": tp_id,
        "errors": [],
        "warnings": [],
    }
    return oracle_graph.invoke(state)


def main(argv: list[str]) -> int:
    JSON_DIR.mkdir(parents=True, exist_ok=True)
    MARKDOWN_DIR.mkdir(parents=True, exist_ok=True)

    summary: list[dict] = []

    operatives = [c.id for c in list_characters(side_filter="indian")]

    for operative in operatives:
        tps = list_turning_points(operative)
        if not tps:
            continue
        for tp in tps:
            slug = f"{operative}__{tp.id}"
            t0 = time.perf_counter()
            try:
                result = run_one(operative, tp.id)
                err = result.get("errors") or []
                if err:
                    summary.append({
                        "operative": operative, "turning_point": tp.id,
                        "status": "error", "errors": err,
                        "elapsed_s": round(time.perf_counter() - t0, 2),
                    })
                    print(f"[ERROR] {slug}: {err}")
                    continue
            except Exception as e:
                summary.append({
                    "operative": operative, "turning_point": tp.id,
                    "status": "exception", "errors": [str(e)],
                    "elapsed_s": round(time.perf_counter() - t0, 2),
                })
                print(f"[EXC]   {slug}: {e}")
                traceback.print_exc()
                continue

            (JSON_DIR / f"{slug}.json").write_text(
                json.dumps(_serialise(result), indent=2)
            )
            (MARKDOWN_DIR / f"{slug}.md").write_text(
                _markdown_for(operative, tp.id, result)
            )

            pomdp = result.get("pomdp")
            cp    = result.get("critical_path")
            so    = result.get("simulation_optimal")
            sa    = result.get("simulation_actual")
            voi   = result.get("voi_result")
            sg    = result.get("stackelberg")
            summary.append({
                "operative":           operative,
                "turning_point":       tp.id,
                "film":                tp.film,
                "act":                 tp.act,
                "status":              "ok",
                "optimal_action":      pomdp.optimal_action if pomdp else None,
                "v_belief":            pomdp.belief_state_value if pomdp else None,
                "p_mission_success":   pomdp.mission_success_prob if pomdp else None,
                "p_cover_intact":      pomdp.cover_integrity_prob if pomdp else None,
                "critical_path_total_d":  cp.total_duration_days if cp else None,
                "critical_path_optimal_d": cp.optimal_duration_days if cp else None,
                "critical_path_save_d":   cp.days_saved if cp else None,
                "bottleneck_task":      cp.bottleneck_task if cp else None,
                "stackelberg_leader":   sg.leader_action if sg else None,
                "stackelberg_payoff":   sg.equilibrium_payoff_indian if sg else None,
                "voi_top_target":       voi.top_target if voi else None,
                "voi_total_bits":       voi.total_entropy_bits if voi else None,
                "sim_actual_success":   sa.p_mission_success if sa else None,
                "sim_optimal_success":  so.p_mission_success if so else None,
                "elapsed_s":            round(time.perf_counter() - t0, 2),
            })
            print(f"[OK]    {slug}: optimal={pomdp.optimal_action if pomdp else 'N/A'}  V(b)={pomdp.belief_state_value if pomdp else 'N/A'}  ({summary[-1]['elapsed_s']}s)")

    # ── Summary outputs ───────────────────────────────────────────────────────
    (RESULTS_DIR / "SUMMARY.json").write_text(json.dumps(summary, indent=2))

    md = ["# Dhurandhar Oracle — Results Index", "",
          f"_Generated by `scripts/generate_results.py`._  ", "",
          "Per-turning-point oracle outputs computed via the LangGraph pipeline:",
          "POMDP (PBVI) → CPM/PERT → VoI → Stackelberg → HMM gaps → Shapley → Monte Carlo.",
          "", "## Summary table", "",
          "| Operative | Turning point | Film/Act | Optimal action | P(success) | P(cover intact) | CPM save (d) | Sim Δ |",
          "|---|---|---|---|---|---|---|---|"]
    for r in summary:
        if r["status"] != "ok":
            continue
        delta = (
            f"{(r['sim_optimal_success'] - r['sim_actual_success']) * 100:+.1f}%"
            if r["sim_actual_success"] is not None and r["sim_optimal_success"] is not None
            else "—"
        )
        md.append(
            f"| `{r['operative']}` | [`{r['turning_point']}`](markdown/{r['operative']}__{r['turning_point']}.md) "
            f"| F{r['film']} A{r['act']} | `{r['optimal_action']}` "
            f"| {r['p_mission_success']:.1%} | {r['p_cover_intact']:.1%} "
            f"| {r['critical_path_save_d']:.0f} | {delta} |"
        )

    failures = [r for r in summary if r["status"] != "ok"]
    if failures:
        md += ["", "## Failures", ""]
        for r in failures:
            md.append(f"- `{r['operative']}__{r['turning_point']}` ({r['status']}): {r['errors']}")

    (RESULTS_DIR / "INDEX.md").write_text("\n".join(md))

    print(f"\nDone. {sum(1 for r in summary if r['status']=='ok')} ok / {len(failures)} failed → {RESULTS_DIR}")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
