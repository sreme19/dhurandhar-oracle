"""
cli.py — Typer CLI for dhurandhar-oracle.

Usage:
  dhurandhar-oracle run hamza dakait-first-meeting
  dhurandhar-oracle run hamza dakait-first-meeting --action deepen_criminal_cover
  dhurandhar-oracle run rizwan-shah jamali-connection --no-narrative
  dhurandhar-oracle show-strategy hamza dakait-first-meeting
  dhurandhar-oracle list-turning-points hamza
  dhurandhar-oracle list-characters
"""
from __future__ import annotations

import json
from typing import Optional
from pathlib import Path

import typer
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich import print as rprint

from dhurandhar_oracle.graph import oracle_graph
from dhurandhar_oracle.forward_graph import forward_graph
from dhurandhar_oracle.io.loader import list_turning_points, list_characters, list_macro_arcs
from dhurandhar_oracle.data_quality import run_data_quality_audit, backfill_missing_outcomes

app     = typer.Typer(help="Dhurandhar intelligence oracle — POMDP, CPM, VoI, Stackelberg")
console = Console()


@app.command()
def run(
    operative:    str = typer.Argument(..., help="Operative ID (e.g. hamza, rizwan-shah)"),
    turning_point: str = typer.Argument(..., help="Turning point ID (e.g. dakait-first-meeting)"),
    action:       Optional[str] = typer.Option(None,  "--action",       help="Force a specific action (counterfactual)"),
    no_narrative: bool           = typer.Option(False, "--no-narrative", help="Skip Claude narrative (structured output only)"),
    output_json:  bool           = typer.Option(False, "--json",         help="Emit raw JSON state"),
) -> None:
    """Run the full oracle pipeline for an Indian operative at a turning point."""

    initial_state = {
        "operative":      operative,
        "turning_point":  turning_point,
        "action_override": action,
        "errors":   [],
        "warnings": [],
    }

    with console.status(f"[bold green]Running oracle for {operative} / {turning_point}…"):
        result = oracle_graph.invoke(initial_state)

    # ── Errors ──────────────────────────────────────────────────────────────
    if result.get("errors"):
        for e in result["errors"]:
            rprint(f"[bold red]ERROR:[/bold red] {e}")
        raise typer.Exit(1)

    # ── Warnings ────────────────────────────────────────────────────────────
    for w in result.get("warnings", []):
        rprint(f"[yellow]WARNING:[/yellow] {w}")

    if output_json:
        def _default(obj):
            if hasattr(obj, "model_dump"):
                return obj.model_dump()
            return str(obj)
        typer.echo(json.dumps(result, default=_default, indent=2))
        return

    # ── Structured Rich output ───────────────────────────────────────────────
    _print_pomdp(result)
    _print_critical_path(result)
    _print_voi(result)
    _print_stackelberg(result)
    _print_belief_gaps(result)
    _print_shapley(result)
    _print_simulation(result)

    if not no_narrative and result.get("narrative"):
        console.print(Panel(result["narrative"], title="War-Room Briefing", border_style="cyan"))


@app.command()
def show_strategy(
    operative:     str = typer.Argument(...),
    turning_point: str = typer.Argument(...),
) -> None:
    """Show only the POMDP strategy table (fast — skips narrative)."""
    initial_state = {
        "operative": operative,
        "turning_point": turning_point,
        "errors": [], "warnings": [],
    }
    result = oracle_graph.invoke(initial_state)
    if result.get("errors"):
        for e in result["errors"]:
            rprint(f"[bold red]ERROR:[/bold red] {e}")
        raise typer.Exit(1)
    _print_pomdp(result)


@app.command()
def list_turning_points_cmd(
    operative: str = typer.Argument(..., help="Operative ID"),
) -> None:
    """List available turning points for an operative."""
    points = list_turning_points(operative)
    if not points:
        rprint(f"[yellow]No turning points found for '{operative}'[/yellow]")
        return
    t = Table(title=f"Turning points — {operative}")
    t.add_column("ID")
    t.add_column("Film")
    t.add_column("Act")
    t.add_column("Description")
    for p in points:
        t.add_row(p.id, str(p.film), str(p.act), p.description[:70])
    console.print(t)


@app.command()
def list_characters_cmd() -> None:
    """List all Indian-side characters available to query."""
    chars = list_characters(side_filter="indian")
    t = Table(title="Indian-side operatives")
    t.add_column("ID")
    t.add_column("Name")
    t.add_column("Role")
    t.add_column("Films")
    t.add_column("Cover identity")
    for c in chars:
        t.add_row(
            c.id, c.name, c.role,
            ", ".join(map(str, c.films)),
            c.cover_identity or "—",
        )
    console.print(t)


@app.command("project-forward")
def project_forward_cmd(
    operative:    str  = typer.Argument(..., help="Operative ID (must be Indian-side and have a post-D2 macro-arc)"),
    until:        str  = typer.Option("today", "--until",  help="ISO date (YYYY-MM-DD) horizon; default = today"),
    force_event:  Optional[str] = typer.Option(None, "--force-event-response",
                                               help="Force a (event_id:action_id) override on the prescribed trajectory"),
    brief:        bool = typer.Option(False, "--brief",    help="Use Haiku for a shorter narrative"),
    markdown:     bool = typer.Option(False, "--markdown", help="Render narrative as Markdown"),
    no_narrative: bool = typer.Option(False, "--no-narrative", help="Skip Claude narrative"),
    output_json:  bool = typer.Option(False, "--json",     help="Emit raw JSON state"),
) -> None:
    """Project an Indian-side operative's career forward against real 2025-2026 events."""
    from datetime import date
    if until == "today":
        until = date.today().isoformat()

    forced = None
    if force_event:
        if ":" not in force_event:
            rprint("[red]--force-event-response must be event_id:action_id[/red]")
            raise typer.Exit(2)
        ev, ac = force_event.split(":", 1)
        forced = {"event_id": ev.strip(), "action_id": ac.strip()}

    initial_state = {
        "operative":            operative,
        "mode":                 "forward",
        "horizon_until":        until,
        "forced_event_action":  forced,
        "brief":                brief,
        "markdown":             markdown,
        "errors":   [], "warnings": [],
    }

    with console.status(f"[bold green]Projecting {operative} forward to {until}…"):
        result = forward_graph.invoke(initial_state)

    if result.get("errors"):
        for e in result["errors"]:
            rprint(f"[bold red]ERROR:[/bold red] {e}")
        raise typer.Exit(1)
    for w in result.get("warnings", []):
        rprint(f"[yellow]WARNING:[/yellow] {w}")

    if output_json:
        def _default(obj):
            if hasattr(obj, "model_dump"):
                return obj.model_dump()
            return str(obj)
        typer.echo(json.dumps(result, default=_default, indent=2))
        return

    _print_forward(result)
    if not no_narrative and result.get("narrative"):
        console.print(Panel(result["narrative"],
                            title="Forward Projection — Strategic Brief",
                            border_style="cyan"))


@app.command("audit-data")
def audit_data_cmd() -> None:
    """Run data quality audit for turning points/outcomes."""
    data_dir = Path(__file__).parent / "data"
    report = run_data_quality_audit(data_dir)

    rprint(f"[bold]Data Coverage[/bold] turning_points={report.turning_points_total} outcomes={report.outcomes_total}")
    if report.missing_outcomes:
        rprint(f"[red]Missing outcomes ({len(report.missing_outcomes)}):[/red] {', '.join(report.missing_outcomes)}")
    else:
        rprint("[green]No missing outcomes.[/green]")

    if report.turning_points_without_sources:
        rprint(f"[yellow]Turning points missing source_refs ({len(report.turning_points_without_sources)}).[/yellow]")
    if report.outcomes_without_sources:
        rprint(f"[yellow]Outcomes missing source_refs ({len(report.outcomes_without_sources)}).[/yellow]")
    if report.low_confidence_edges:
        rprint(f"[yellow]Low-confidence causal edges (<0.5): {len(report.low_confidence_edges)}[/yellow]")
    if report.invalid_turning_points:
        rprint(f"[red]Invalid turning points: {len(report.invalid_turning_points)}[/red]")
    if report.invalid_outcomes:
        rprint(f"[red]Invalid outcomes: {len(report.invalid_outcomes)}[/red]")


@app.command("backfill-outcomes")
def backfill_outcomes_cmd() -> None:
    """Create placeholder outcome files for turning points that have none."""
    data_dir = Path(__file__).parent / "data"
    created = backfill_missing_outcomes(data_dir)
    if not created:
        rprint("[green]No missing outcomes detected.[/green]")
        return
    rprint(f"[green]Created {len(created)} outcome templates.[/green]")
    for p in created[:10]:
        rprint(f"  - {p.name}")
    if len(created) > 10:
        rprint(f"  ... and {len(created) - 10} more")


# ── Rich print helpers ─────────────────────────────────────────────────────────

def _print_pomdp(result: dict) -> None:
    pomdp = result.get("pomdp")
    if not pomdp:
        return
    t = Table(title="POMDP — Optimal Policy")
    t.add_column("Action", style="bold")
    t.add_column("Q(b,a)")
    t.add_column("Note")
    for action, val in sorted(pomdp.action_values.items(), key=lambda x: -x[1]):
        note = "← OPTIMAL" if action == pomdp.optimal_action else ""
        t.add_row(action, f"{val:.3f}", note)
    console.print(t)
    rprint(f"  V(b) = {pomdp.belief_state_value:.2f} | "
           f"P(mission success) = {pomdp.mission_success_prob:.1%} | "
           f"P(cover intact) = {pomdp.cover_integrity_prob:.1%}")


def _print_critical_path(result: dict) -> None:
    cp = result.get("critical_path")
    if not cp:
        return
    rprint(f"\n[bold]Critical Path (CPM/PERT)[/bold]")
    rprint(f"  {' → '.join(cp.critical_path)}")
    rprint(f"  Total: {cp.total_duration_days:.0f}d  →  Optimal: {cp.optimal_duration_days:.0f}d  "
           f"([green]save {cp.days_saved:.0f}d[/green])")
    rprint(f"  Bottleneck: [red]{cp.bottleneck_task}[/red]")
    if cp.parallelisation_opportunities:
        pairs = ", ".join(f"{a}‖{b}" for a, b in cp.parallelisation_opportunities[:3])
        rprint(f"  Parallelisable: {pairs}")


def _print_voi(result: dict) -> None:
    voi = result.get("voi_result")
    if not voi or not voi.rankings:
        return
    t = Table(title=f"Value of Information  (total entropy={voi.total_entropy_bits:.2f} bits)")
    t.add_column("#")
    t.add_column("Target")
    t.add_column("VoI (bits)")
    t.add_column("Effort")
    t.add_column("Recommendation")
    for entry in voi.rankings:
        t.add_row(
            str(entry.priority_rank),
            entry.intelligence_target,
            f"{entry.voi_bits:.3f}",
            f"{entry.effort_required:.1f}",
            entry.recommendation[:60],
        )
    console.print(t)


def _print_stackelberg(result: dict) -> None:
    sg = result.get("stackelberg")
    if not sg:
        return
    rprint(f"\n[bold]Stackelberg Equilibrium[/bold]")
    rprint(f"  Handler commits to:        {sg.leader_action}")
    rprint(f"  Operative best response:   {sg.operative_best_response}")
    rprint(f"  Adversary counter:         {sg.follower_best_response}")
    rprint(f"  Indian payoff:             {sg.equilibrium_payoff_indian:.3f}")
    rprint(f"  Commitment value vs Nash:  +{sg.commitment_value:.3f}")


def _print_belief_gaps(result: dict) -> None:
    gaps = result.get("belief_gaps", [])
    if not gaps:
        return
    t = Table(title="Belief Gaps — HMM Mole Detection")
    t.add_column("Actor")
    t.add_column("Operative believed")
    t.add_column("HMM inferred")
    t.add_column("Gap")
    t.add_column("Alert")
    for bg in gaps:
        alert = "⚠ MOLE?" if bg.gap > 0.75 else ""
        t.add_row(bg.actor, bg.operative_believed, bg.hmm_inferred,
                  f"{bg.gap:.2f}", alert)
    console.print(t)


def _print_shapley(result: dict) -> None:
    shapley = result.get("shapley")
    if not shapley or not shapley.values:
        return
    t = Table(title="Shapley Values — Asset Coalition")
    t.add_column("Actor")
    t.add_column("φ (contribution)")
    t.add_column("Defection incentive")
    t.add_column("Risk")
    for actor in sorted(shapley.values, key=lambda a: -shapley.values[a]):
        phi     = shapley.values[actor]
        defect  = shapley.defection_incentives.get(actor, 0.0)
        risk    = "[red]HIGH[/red]" if defect > 0.5 else "[green]LOW[/green]"
        t.add_row(actor, f"{phi:.3f}", f"{defect:.3f}", risk)
    console.print(t)


def _print_forward(result: dict) -> None:
    fp = result.get("forward_projection")
    if not fp:
        return
    if fp.is_speculative_real_figure:
        rprint("[yellow][SPECULATIVE — projection of a real public figure][/yellow]")
    rprint(f"[bold]Forward projection:[/bold] {fp.operative}    "
           f"horizon {fp.arc_start} → {fp.horizon_until}")
    t = Table(title="Trajectory comparison")
    t.add_column("Event")
    t.add_column("Predicted action")
    t.add_column("Prescribed action")
    t.add_column("Status (prescribed)")
    pred_by_id = {s.event_id: s for s in fp.predicted.steps}
    for s in fp.prescribed.steps:
        pred = pred_by_id.get(s.event_id)
        pred_label = pred.action_label if pred else "—"
        marker = " ←" if pred and pred.chosen_action != s.chosen_action else ""
        t.add_row(s.event_date + " " + s.event_label[:30],
                  pred_label, s.action_label + marker, s.status_after)
    console.print(t)
    rprint(f"  Predicted scalar score:  {fp.predicted.scalar_score:+.2f}  "
           f"(final status: {fp.predicted.final_status})")
    rprint(f"  Prescribed scalar score: {fp.prescribed.scalar_score:+.2f}  "
           f"(final status: {fp.prescribed.final_status})")
    rprint(f"  Δ score: [bold green]+{fp.scalar_score_delta:.2f}[/bold green]")
    od = fp.objective_delta
    rprint(f"  Objective Δ: yield={od.mission_yield:+.2f}  impact={od.strategic_impact:+.2f}  "
           f"cost={od.personal_cost:+.2f}  network={od.network_durability:+.2f}  "
           f"attribution={od.attribution_risk:+.2f}")
    if fp.key_divergence_event:
        rprint(f"  Key divergence: [cyan]{fp.key_divergence_event}[/cyan]")


def _print_simulation(result: dict) -> None:
    sim_act = result.get("simulation_actual")
    sim_opt = result.get("simulation_optimal")
    if not sim_act or not sim_opt:
        return
    delta = sim_opt.p_mission_success - sim_act.p_mission_success
    rprint(f"\n[bold]Monte Carlo Simulation  ({sim_act.n_rollouts} rollouts)[/bold]")
    rprint(f"  Actual  ({sim_act.action}):   "
           f"P(success)={sim_act.p_mission_success:.1%}  "
           f"[{sim_act.ci_low:.1%}–{sim_act.ci_high:.1%}]")
    rprint(f"  Optimal ({sim_opt.action}):  "
           f"P(success)={sim_opt.p_mission_success:.1%}  "
           f"[{sim_opt.ci_low:.1%}–{sim_opt.ci_high:.1%}]")
    rprint(f"  Δ = [bold green]+{delta:.1%}[/bold green] if optimal path taken")
    if sim_opt.key_lever:
        rprint(f"  Key causal lever: {sim_opt.key_lever}")
