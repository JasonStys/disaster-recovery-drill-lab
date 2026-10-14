"""Independent small fictional ledgers and explicitly fake report fixtures for edge-case tests. Jason Stys."""
# BEGIN CODE MAP (generated; python scripts/code_map.py)
# definition: ledger — line 22
# definition: head — line 33
# parameter: ledger — line 33
# variable: value — line 35
# definition: fake_report — line 43
# variable: name — line 60
# END CODE MAP

from __future__ import annotations

from copy import deepcopy
from typing import Any

import pytest

from dr.evidence import CASES


@pytest.fixture
def ledger() -> dict[str, Any]:
    """Return an independent two-order integer-money ledger with known keys, sums and millisecond timestamps."""
    return {
        "customers": [[1, "Fictional A"]],
        "orders": [[1, 1, 30, 1000], [2, 1, 30, 1100]],
        "lines": [[1, 1, "SAMPLE", 3, 10], [2, 1, "SAMPLE", 3, 10]],
        "payments": [[1, 30], [2, 30]],
    }


@pytest.fixture
def head(ledger: dict[str, Any]) -> dict[str, Any]:
    """Append exactly one later order; baseline rows remain immutable."""
    value = deepcopy(ledger)
    value["orders"].append([3, 1, 30, 1500])
    value["lines"].append([3, 1, "SAMPLE", 3, 10])
    value["payments"].append([3, 30])
    return value


@pytest.fixture
def fake_report() -> dict[str, Any]:
    """Return explicitly fabricated native suite data solely for validator tests, never publish as measured evidence."""
    return {
        "schema": 1,
        "author": "Jason Stys",
        "synthetic": True,
        "engine": "native",
        "source_sha": "1" * 40,
        "snapshot_id": "2" * 64,
        "dump_sha256": "3" * 64,
        "checks": [
            {
                "name": name,
                "result": "PASS",
                "duration_ms": 1,
                "evidence": {"fixture": True},
            }
            for name in sorted(CASES["native"])
        ],
        "recovery": None,
    }
