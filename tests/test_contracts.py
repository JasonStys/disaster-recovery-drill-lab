"""Strict JSON, size/depth/shape/type and ordinary-file adversarial boundaries. Jason Stys."""
# BEGIN CODE MAP (generated; python scripts/code_map.py)
# definition: test_bad_json — line 52
# parameter: content — line 52
# definition: test_input_bounds — line 58
# variable: value — line 61
# variable: nested — line 64
# variable: _ — line 65
# variable: nested — line 66
# definition: test_integer_type — line 74
# parameter: value — line 74
# definition: test_fingerprints — line 81
# parameter: value — line 81
# definition: test_closed_objects — line 88
# variable: value — line 91
# definition: test_files — line 96
# parameter: tmp_path — line 96
# variable: path — line 98
# END CODE MAP

from __future__ import annotations

import math
from pathlib import Path

import pytest

from dr.contracts import (
    CAP,
    bounded,
    decode,
    fingerprint,
    integer,
    load,
    ordinary,
    record,
)


@pytest.mark.parametrize(
    "content",
    [
        b'{"x":1,"x":2}',
        b'{"x":NaN}',
        b'{"x":Infinity}',
        b'{"x":-Infinity}',
        b"\xff",
        b'{"x":',
        b"[]" * 100,
    ],
)
def test_bad_json(content: bytes) -> None:
    """Malformed/ambiguous/nonfinite documents never silently load."""
    with pytest.raises(ValueError):
        decode(content)


def test_input_bounds() -> None:
    """Enforce byte/node/depth limits plus JSON-native keys/scalars."""
    assert decode(b'{"x":[1,true,null,"value"]}') == {"x": [1, True, None, "value"]}
    for value in ([0] * 50_001, {1: 2}, object(), math.inf):
        with pytest.raises(ValueError):
            bounded(value)
    nested: object = 1
    for _ in range(26):
        nested = [nested]
    with pytest.raises(ValueError):
        bounded(nested)
    with pytest.raises(ValueError):
        decode(b" " * (CAP + 1))


@pytest.mark.parametrize("value", [True, False, 1.0, -1, 2**53, None, "1"])
def test_integer_type(value: object) -> None:
    """Numeric aliases, bools and out-of-range values cannot satisfy integer contracts."""
    with pytest.raises(ValueError):
        integer(value)


@pytest.mark.parametrize("value", ["", "a" * 63, "A" * 64, "0" * 64, "a" * 65, None])
def test_fingerprints(value: object) -> None:
    """Only complete nonzero SHA256 syntax is accepted, not authenticity inferred."""
    with pytest.raises(ValueError):
        fingerprint(value)
    assert fingerprint("a" * 64) == "a" * 64


def test_closed_objects() -> None:
    """Reject missing/unknown fields and nonobjects."""
    assert record({"x": 1}, {"x"}) == {"x": 1}
    for value in ([], {}, {"x": 1, "extra": 2}):
        with pytest.raises(ValueError):
            record(value, {"x"})


def test_files(tmp_path: Path) -> None:
    """Regular explicit files load; directories, absent files and oversized content fail."""
    path = tmp_path / "input.json"
    path.write_bytes(b'{"value":1}')
    assert load(path) == {"value": 1}
    with pytest.raises(ValueError):
        ordinary(tmp_path)
    with pytest.raises(OSError):
        load(tmp_path / "absent")
    path.write_bytes(b" " * (CAP + 1))
    with pytest.raises(ValueError):
        load(path)
