"""
suggestion_node — rank Indian-side operatives as candidates for
project-forward or rewrite-arc.

Ranking signal:
  base_score = capability_score * film_presence * has_arc_or_tps
  + tier_bonus  (fictional > support > public_figure for forward mode;
                 all equal for rewrite mode)

For forward mode, candidates without a post_d2_arc/<id>.json are filtered
out (or shown in a "speculative — needs arc authored" subsection).
For rewrite mode, candidates need at least one turning point authored.
"""
from __future__ import annotations

from dhurandhar_oracle.io.loader import (
    list_characters,
    list_macro_arcs,
    list_turning_points,
)


def suggest(mode: str = "forward") -> dict:
    """Return a dict of ranked candidate lists by tier."""
    chars = [c for c in list_characters() if c.side == "indian"]
    arcs  = set(list_macro_arcs())
    if mode not in ("forward", "rewrite"):
        raise ValueError(f"suggest mode must be 'forward' or 'rewrite', got {mode!r}")

    # Build per-character info
    rows = []
    for c in chars:
        tps = list_turning_points(c.id)
        rows.append({
            "id":          c.id,
            "name":        c.name,
            "role":        c.role,
            "archetype":   c.archetype,
            "is_real":     c.is_real_public_figure,
            "films":       c.films,
            "has_arc":     c.id in arcs,
            "n_tps":       len(tps),
        })

    # Filter + score per mode
    def score(r: dict) -> float:
        base = float(len(r["films"])) + 0.05 * r["n_tps"]
        if r["archetype"] == "fictional_operative":
            base += 1.0
        elif r["archetype"] == "support_actor":
            base += 0.3
        return base

    if mode == "forward":
        ready    = [r for r in rows if r["has_arc"]]
        unready  = [r for r in rows if not r["has_arc"]]
        ready    = sorted(ready,   key=score, reverse=True)
        unready  = sorted(unready, key=score, reverse=True)
        # split unready into "fictional needing arc" vs "real public figure (speculative)"
        unready_fictional = [r for r in unready if not r["is_real"]]
        speculative       = [r for r in unready if r["is_real"]]
        return {
            "mode":              "forward",
            "ready":             ready,
            "unready_fictional": unready_fictional,
            "speculative":       speculative,
        }
    # rewrite mode
    eligible   = [r for r in rows if r["n_tps"] > 0]
    ineligible = [r for r in rows if r["n_tps"] == 0]
    eligible   = sorted(eligible,   key=score, reverse=True)
    ineligible = sorted(ineligible, key=score, reverse=True)
    return {
        "mode":      "rewrite",
        "eligible":  eligible,
        "ineligible": ineligible,
    }
