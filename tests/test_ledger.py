"""Independent money/key oracles, snapshot equality and recovery-objective boundaries. Jason Stys."""
# BEGIN CODE MAP (generated; python scripts/code_map.py)
# variable: LIMITS — line 51
# definition: test_known_snapshot — line 54
# parameter: head — line 54
# parameter: ledger — line 54
# variable: result — line 56
# variable: scrambled — line 62
# variable: table — line 63
# definition: test_unmet_objectives — line 77
# parameter: field — line 78
# parameter: head — line 78
# parameter: ledger — line 78
# parameter: value — line 78
# variable: limits — line 81
# definition: test_invalid_rows — line 104
# parameter: column — line 105
# parameter: index — line 105
# parameter: ledger — line 105
# parameter: table — line 105
# parameter: value — line 105
# definition: test_duplicate_empty_shape — line 114
# parameter: ledger — line 114
# parameter: table — line 114
# variable: rows — line 116
# variable: value — line 123
# definition: test_source_rewrite_and_restore_mismatch — line 128
# parameter: head — line 129
# parameter: ledger — line 129
# variable: changed — line 132
# variable: backwards — line 137
# definition: test_objective_property — line 151
# parameter: elapsed — line 151
# parameter: rpo_limit — line 151
# variable: baseline — line 153
# variable: head — line 159
# variable: result — line 165
# END CODE MAP

from __future__ import annotations

from copy import deepcopy
from typing import Any

import pytest
from hypothesis import given
from hypothesis import strategies as st

from dr.ledger import dataset, evaluate

LIMITS = {"rto_ms": 1000, "rpo_ms": 400, "max_lost_orders": 1}


def test_known_snapshot(ledger: dict[str, Any], head: dict[str, Any]) -> None:
    """A known snapshot loses exactly one appended order and 400ms; equal objective bounds pass."""
    result = evaluate(ledger, head, ledger, 1000, LIMITS)
    assert result["result"] == "PASS"
    assert result["lost_orders"] == 1
    assert result["observed_rpo_ms"] == 400
    assert result["observed_rto_ms"] == 1000
    assert result["recovered_orders"] == 2
    scrambled = deepcopy(ledger)
    for table in scrambled.values():
        table.reverse()
    assert dataset(scrambled)["fingerprint"] == dataset(ledger)["fingerprint"]
    assert (
        evaluate(
            ledger, ledger, ledger, 0, {"rto_ms": 1, "rpo_ms": 0, "max_lost_orders": 0}
        )["result"]
        == "PASS"
    )


@pytest.mark.parametrize(
    "field,value", [("rto_ms", 999), ("rpo_ms", 399), ("max_lost_orders", 0)]
)
def test_unmet_objectives(
    ledger: dict[str, Any], head: dict[str, Any], field: str, value: int
) -> None:
    """An unmet budget is FAIL, not an input error or silently revised objective."""
    limits = {**LIMITS, field: value}
    assert evaluate(ledger, head, ledger, 1000, limits)["result"] == "FAIL"


@pytest.mark.parametrize(
    "table,index,column,value",
    [
        ("customers", 0, 0, True),
        ("customers", 0, 1, "\n"),
        ("customers", 0, 1, ""),
        ("customers", 0, 1, "é"),
        ("orders", 0, 1, 999),
        ("orders", 0, 2, -1),
        ("orders", 0, 3, False),
        ("lines", 0, 0, 999),
        ("lines", 0, 1, 0),
        ("lines", 0, 2, None),
        ("lines", 0, 3, 0),
        ("lines", 0, 4, 1),
        ("payments", 0, 0, 999),
        ("payments", 0, 1, 29),
    ],
)
def test_invalid_rows(
    ledger: dict[str, Any], table: str, index: int, column: int, value: object
) -> None:
    """Foreign keys, monetary reconciliation and scalar constraints use independent row evidence."""
    ledger[table][index][column] = value
    with pytest.raises(ValueError):
        dataset(ledger)


@pytest.mark.parametrize("table", ["customers", "orders", "lines", "payments"])
def test_duplicate_empty_shape(ledger: dict[str, Any], table: str) -> None:
    """Duplicated keys, empty tables, oversized tables and wrong row shapes fail closed."""
    for rows in (
        [ledger[table][0], ledger[table][0]],
        [],
        [None],
        [[]],
        ledger[table] * 10_001,
    ):
        value = {**ledger, table: rows}
        with pytest.raises(ValueError):
            dataset(value)


def test_source_rewrite_and_restore_mismatch(
    ledger: dict[str, Any], head: dict[str, Any]
) -> None:
    """Rewrites/deletions reject the append-only model; a valid but wrong restore cannot pass by favorable timing."""
    changed = deepcopy(ledger)
    changed["customers"][0][1] = "Wrong but internally valid"
    assert evaluate(ledger, head, changed, 1, LIMITS)["result"] == "FAIL"
    with pytest.raises(ValueError):
        evaluate(ledger, changed, ledger, 1, LIMITS)
    backwards = deepcopy(head)
    backwards["orders"][-1][-1] = 900
    # A backdated appended order must not produce a falsely reassuring zero-time loss window.
    with pytest.raises(ValueError):
        evaluate(ledger, backwards, ledger, 1, LIMITS)
    with pytest.raises(ValueError):
        evaluate(ledger, head, ledger, True, LIMITS)
    with pytest.raises(ValueError):
        evaluate(ledger, head, ledger, 1, {**LIMITS, "unknown": 1})


@given(
    st.integers(min_value=0, max_value=2000), st.integers(min_value=0, max_value=1000)
)
def test_objective_property(elapsed: int, rpo_limit: int) -> None:
    """Compare result against an independent arithmetic oracle over generated RTO and RPO boundary values."""
    baseline = {
        "customers": [[1, "A"]],
        "orders": [[1, 1, 10, 1000]],
        "lines": [[1, 1, "X", 1, 10]],
        "payments": [[1, 10]],
    }
    head = {
        "customers": [[1, "A"]],
        "orders": [[1, 1, 10, 1000], [2, 1, 10, 1400]],
        "lines": [[1, 1, "X", 1, 10], [2, 1, "X", 1, 10]],
        "payments": [[1, 10], [2, 10]],
    }
    result = evaluate(
        baseline,
        head,
        baseline,
        elapsed,
        {"rto_ms": 1000, "rpo_ms": rpo_limit, "max_lost_orders": 1},
    )
    assert (result["result"] == "PASS") == (elapsed <= 1000 and rpo_limit >= 400)
