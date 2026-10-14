"""Bounded strict JSON and ordinary-file contracts; no input becomes a command. Jason Stys."""
# BEGIN CODE MAP (generated; python scripts/code_map.py)
# variable: CAP — line 50
# definition: integer — line 53
# parameter: high — line 53
# parameter: low — line 53
# parameter: value — line 53
# definition: record — line 60
# parameter: keys — line 60
# parameter: value — line 60
# definition: fingerprint — line 67
# parameter: value — line 67
# definition: bounded — line 78
# parameter: value — line 78
# variable: stack — line 80
# variable: count — line 81
# variable: depth — line 83
# variable: item — line 83
# variable: count — line 84
# variable: key — line 88
# variable: child — line 90
# variable: child — line 92
# definition: pairs — line 101
# parameter: items — line 101
# variable: result — line 103
# variable: key — line 104
# variable: value — line 104
# definition: reject_constant — line 111
# parameter: _value — line 111
# definition: decode — line 116
# parameter: content — line 116
# variable: value — line 120
# definition: ordinary — line 127
# parameter: path — line 127
# variable: info — line 129
# definition: load — line 138
# parameter: path — line 138
# variable: source — line 141
# END CODE MAP

from __future__ import annotations

import json
import math
import re
import stat
from pathlib import Path
from typing import Any

CAP = 1024 * 1024


def integer(value: Any, low: int = 0, high: int = 2**53 - 1) -> int:
    """Require a real bounded integer, never bool; low/high are inclusive."""
    if type(value) is not int or not low <= value <= high:
        raise ValueError("bounded integer required")
    return value


def record(value: Any, keys: set[str]) -> dict[str, Any]:
    """Require exactly the named string keys; unknown or missing fields fail closed."""
    if not isinstance(value, dict) or set(value) != keys:
        raise ValueError("closed object required")
    return value


def fingerprint(value: Any) -> str:
    """Require a complete nonzero lowercase SHA256 fingerprint, not a short ID or signature."""
    if (
        not isinstance(value, str)
        or not re.fullmatch(r"[0-9a-f]{64}", value)
        or value == "0" * 64
    ):
        raise ValueError("complete fingerprint required")
    return value


def bounded(value: Any) -> None:
    """Bound JSON trees to 50,000 nodes and depth 24; finite JSON-native scalars only."""
    stack = [(value, 0)]
    count = 0
    while stack:
        item, depth = stack.pop()
        count += 1
        if count > 50_000 or depth > 24:
            raise ValueError("tree limit exceeded")
        if isinstance(item, dict):
            if any(not isinstance(key, str) for key in item):
                raise ValueError("string keys required")
            stack.extend((child, depth + 1) for child in item.values())
        elif isinstance(item, list):
            stack.extend((child, depth + 1) for child in item)
        elif (
            type(item) not in (str, bool, int, float, type(None))
            or isinstance(item, float)
            and not math.isfinite(item)
        ):
            raise ValueError("JSON scalar required")


def pairs(items: list[tuple[str, Any]]) -> dict[str, Any]:
    """Reject duplicate keys instead of silently keeping a final contradictory value."""
    result: dict[str, Any] = {}
    for key, value in items:
        if key in result:
            raise ValueError("duplicate key")
        result[key] = value
    return result


def reject_constant(_value: str) -> None:
    """Reject nonfinite JSON tokens without reflecting input."""
    raise ValueError("nonfinite JSON")


def decode(content: bytes) -> Any:
    """Decode at most one MiB of strict UTF8 JSON; reject duplicates, NaN and excessive trees."""
    if len(content) > CAP:
        raise ValueError("document limit exceeded")
    value = json.loads(
        content.decode("utf-8"), object_pairs_hook=pairs, parse_constant=reject_constant
    )
    bounded(value)
    return value


def ordinary(path: Path) -> None:
    """Reject nonregular/symlink/reparse leaves; cooperative parent filesystem is assumed."""
    info = path.lstat()
    if (
        not stat.S_ISREG(info.st_mode)
        or path.is_symlink()
        or getattr(info, "st_file_attributes", 0) & 1024
    ):
        raise ValueError("ordinary file required")


def load(path: Path) -> Any:
    """Read a bounded explicit ordinary file; errors are handled without raw content by the CLI."""
    ordinary(path)
    with path.open("rb") as source:
        return decode(source.read(CAP + 1))
