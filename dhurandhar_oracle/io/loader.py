"""
loader.py — JSON data loaders.

All Pydantic validation happens here at the boundary between raw JSON
and the typed world of schemas.py.

Mirrors got-oracle/got_oracle/io/loader.py, extended for:
  - CharacterProfile (replaces CharacterData)
  - TurningPoint (film + act instead of season + episode)
  - list_turning_points(operative) — returns TurningPoint list
  - list_characters(side_filter)   — returns CharacterProfile list
"""
from __future__ import annotations

import json
from pathlib import Path

from dhurandhar_oracle.schemas import CharacterProfile, OutcomeEntry, TurningPoint

_DATA_DIR = Path(__file__).parent.parent / "data"


# ── Loaders ────────────────────────────────────────────────────────────────────

def load_turning_point(turning_point_id: str) -> TurningPoint:
    """
    Load and validate a turning point from data/turning_points/<id>.json.
    Raises FileNotFoundError if the file does not exist.
    Raises pydantic.ValidationError if the JSON is malformed.
    """
    path = _DATA_DIR / "turning_points" / f"{turning_point_id}.json"
    if not path.exists():
        raise FileNotFoundError(f"Turning point not found: {path}")
    raw = json.loads(path.read_text())
    return TurningPoint.model_validate(raw)


def load_character(character_id: str) -> CharacterProfile:
    """
    Load and validate a character from data/characters/<id>.json.
    Raises FileNotFoundError if the file does not exist.
    """
    path = _DATA_DIR / "characters" / f"{character_id}.json"
    if not path.exists():
        raise FileNotFoundError(f"Character not found: {path}")
    raw = json.loads(path.read_text())
    return CharacterProfile.model_validate(raw)


def load_outcome(turning_point_id: str) -> OutcomeEntry:
    """
    Load and validate an outcome from data/outcomes/<id>.json.
    Returns None if no outcome file exists (mission still in progress).
    """
    path = _DATA_DIR / "outcomes" / f"{turning_point_id}.json"
    if not path.exists():
        raise FileNotFoundError(f"Outcome not found: {path}")
    raw = json.loads(path.read_text())
    return OutcomeEntry.model_validate(raw)


# ── Listing helpers ────────────────────────────────────────────────────────────

def list_turning_points(operative: str) -> list[TurningPoint]:
    """Return all turning points authored for the given operative."""
    tp_dir = _DATA_DIR / "turning_points"
    result: list[TurningPoint] = []
    for path in sorted(tp_dir.glob("*.json")):
        try:
            tp = load_turning_point(path.stem)
            if tp.operative == operative:
                result.append(tp)
        except Exception:
            continue
    return result


def list_characters(side_filter: str | None = None) -> list[CharacterProfile]:
    """
    Return all character profiles.
    If side_filter is given (e.g. "indian"), only return that side.
    """
    char_dir = _DATA_DIR / "characters"
    result: list[CharacterProfile] = []
    for path in sorted(char_dir.glob("*.json")):
        try:
            char = load_character(path.stem)
            if side_filter is None or char.side == side_filter:
                result.append(char)
        except Exception:
            continue
    return result
