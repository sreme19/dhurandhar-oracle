"""
Data quality utilities for dhurandhar-oracle datasets.
"""
from __future__ import annotations

import json
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path

from dhurandhar_oracle.io.loader import load_outcome, load_turning_point


@dataclass
class DataQualityReport:
    turning_points_total: int
    outcomes_total: int
    missing_outcomes: list[str]
    turning_points_without_sources: list[str]
    outcomes_without_sources: list[str]
    low_confidence_edges: list[str]
    invalid_turning_points: list[str]
    invalid_outcomes: list[str]


def _utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def run_data_quality_audit(data_dir: Path) -> DataQualityReport:
    tp_dir = data_dir / "turning_points"
    out_dir = data_dir / "outcomes"
    tp_ids = sorted(p.stem for p in tp_dir.glob("*.json"))
    out_ids = sorted(p.stem for p in out_dir.glob("*.json"))

    missing_outcomes = [tp_id for tp_id in tp_ids if tp_id not in out_ids]
    tps_wo_sources: list[str] = []
    outcomes_wo_sources: list[str] = []
    low_conf_edges: list[str] = []
    invalid_turning_points: list[str] = []
    invalid_outcomes: list[str] = []

    for tp_id in tp_ids:
        try:
            tp = load_turning_point(tp_id)
            if not tp.source_refs:
                tps_wo_sources.append(tp_id)
            for edge in tp.causal_dag.edges:
                if edge.confidence < 0.5:
                    low_conf_edges.append(f"{tp_id}:{edge.cause}->{edge.effect} ({edge.confidence:.2f})")
        except Exception:
            invalid_turning_points.append(tp_id)

    for out_id in out_ids:
        try:
            outcome = load_outcome(out_id)
            if not outcome.source_refs:
                outcomes_wo_sources.append(out_id)
        except Exception:
            invalid_outcomes.append(out_id)

    return DataQualityReport(
        turning_points_total=len(tp_ids),
        outcomes_total=len(out_ids),
        missing_outcomes=missing_outcomes,
        turning_points_without_sources=tps_wo_sources,
        outcomes_without_sources=outcomes_wo_sources,
        low_confidence_edges=low_conf_edges,
        invalid_turning_points=invalid_turning_points,
        invalid_outcomes=invalid_outcomes,
    )


def backfill_missing_outcomes(data_dir: Path) -> list[Path]:
    tp_dir = data_dir / "turning_points"
    out_dir = data_dir / "outcomes"
    out_dir.mkdir(parents=True, exist_ok=True)
    created: list[Path] = []

    for tp_path in sorted(tp_dir.glob("*.json")):
        tp_id = tp_path.stem
        out_path = out_dir / f"{tp_id}.json"
        if out_path.exists():
            continue

        raw_tp = json.loads(tp_path.read_text())
        operative = raw_tp.get("operative", "unknown")
        template = {
            "turning_point_id": tp_id,
            "actual_action": "unknown",
            "immediate_effects": [],
            "terminal_state": "in_progress",
            "days_elapsed": 0,
            "losses": [],
            "intel_gained": [],
            "cover_change": 0.0,
            "confidence": 0.0,
            "source_refs": [],
            "owner": None,
            "updated_at": _utc_now(),
            "schema_version": "1.1.0",
            "_TODO": f"Backfill with grounded outcome for {operative} at {tp_id}.",
        }
        out_path.write_text(json.dumps(template, indent=2) + "\n")
        created.append(out_path)

    return created
