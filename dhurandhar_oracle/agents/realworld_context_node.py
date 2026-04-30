"""
realworld_context_node — load and summarise the real-world context files
referenced by macro-arc events.

For each MacroEvent.context_ref present in the arc, load the matching
data/context/<ref>.json and extract a few headline strings (description,
historical_phases summary, real_world_developments). The result is fed to
the narrator so the LinkedIn-grade output is anchored in real events, not
just the solver's reward vector.
"""
from __future__ import annotations

from dhurandhar_oracle.io.loader import load_context
from dhurandhar_oracle.state import DhurandharState


def realworld_context_node(state: DhurandharState) -> dict:
    arc = state.get("macro_arc")
    errors:   list[str] = []
    warnings: list[str] = []
    summaries: list[dict] = []

    if arc is None:
        return {
            "context_summaries": [],
            "errors":   errors,
            "warnings": warnings + ["realworld_context_node: no macro_arc"],
        }

    for event in arc.events:
        if not event.context_ref:
            summaries.append({"event_id": event.id, "context_ref": None, "summary": []})
            continue
        try:
            ctx = load_context(event.context_ref)
        except FileNotFoundError as exc:
            warnings.append(f"context missing for {event.id}: {exc}")
            summaries.append({"event_id": event.id, "context_ref": event.context_ref, "summary": []})
            continue
        summaries.append({
            "event_id":    event.id,
            "context_ref": event.context_ref,
            "summary":     _headline_bullets(ctx),
        })

    return {"context_summaries": summaries, "errors": errors, "warnings": warnings}


def _headline_bullets(ctx: dict) -> list[str]:
    """Extract short headline bullets from a context JSON. Heuristic, not exhaustive."""
    out: list[str] = []
    for key in ("formal_name", "description"):
        v = ctx.get(key)
        if isinstance(v, str) and v.strip():
            out.append(v.strip().split(". ")[0][:240])

    # phase summaries (e.g. punjab_khalistan_arc.historical_phases)
    phases = ctx.get("historical_phases")
    if isinstance(phases, dict):
        for pname, pdata in list(phases.items())[:1]:
            if isinstance(pdata, dict):
                d = pdata.get("description") or pdata.get("trigger")
                if isinstance(d, str):
                    out.append(f"{pname}: {d[:200]}")

    rwd = ctx.get("real_world_developments")
    if isinstance(rwd, dict):
        for k, v in list(rwd.items())[:1]:
            if isinstance(v, dict):
                ev = v.get("event") or v.get("description")
                if isinstance(ev, str):
                    out.append(f"{k}: {ev[:200]}")

    return out[:4]
