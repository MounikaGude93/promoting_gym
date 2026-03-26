"""Persistent content usage tracking for offline post generation."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from content_bank import TARGET_CONTENT

USAGE_FILE = Path(__file__).resolve().parent / "usage_state.json"


def _default_state() -> dict[str, Any]:
    return {
        target: {"used_days": []}
        for target in TARGET_CONTENT
    }


def _load_state() -> dict[str, Any]:
    if not USAGE_FILE.exists():
        state = _default_state()
        _save_state(state)
        return state

    with USAGE_FILE.open("r", encoding="utf-8") as f:
        state = json.load(f)

    # Self-heal state if targets were added/removed.
    for target in TARGET_CONTENT:
        state.setdefault(target, {"used_days": []})

    for target in list(state.keys()):
        if target not in TARGET_CONTENT:
            del state[target]

    _save_state(state)
    return state


def _save_state(state: dict[str, Any]) -> None:
    with USAGE_FILE.open("w", encoding="utf-8") as f:
        json.dump(state, f, indent=2)


def get_next_post(target: str) -> dict[str, Any] | None:
    """Return next unused post for target and mark it as used."""
    if target not in TARGET_CONTENT:
        return None

    state = _load_state()
    used_days = set(state[target].get("used_days", []))
    posts = TARGET_CONTENT[target]

    for idx, post in enumerate(posts, start=1):
        if idx not in used_days:
            state[target]["used_days"] = sorted(list(used_days | {idx}))
            _save_state(state)
            return {
                "day": idx,
                "total_days": len(posts),
                "target": target,
                "caption": post["caption"],
                "image_idea": post["image_idea"],
                "hashtags": post["hashtags"],
            }

    return None


def get_usage_progress(target: str) -> tuple[int, int]:
    """Return used count and total posts for a target."""
    if target not in TARGET_CONTENT:
        return 0, 0
    state = _load_state()
    used_count = len(state[target].get("used_days", []))
    total = len(TARGET_CONTENT[target])
    return used_count, total


def reset_target_usage(target: str) -> None:
    """Reset usage for a target."""
    if target not in TARGET_CONTENT:
        return
    state = _load_state()
    state[target]["used_days"] = []
    _save_state(state)
