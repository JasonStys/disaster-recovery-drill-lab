"""Independent recovery selection, unknown-time and no-pruning retention tests. Created by Jason Stys."""
# BEGIN CODE MAP (generated; python scripts/code_map.py)
# variable: BASE — line 53
# definition: ledger — line 56
# parameter: count — line 56
# variable: number — line 61
# variable: number — line 63
# variable: number — line 64
# definition: catalog — line 68
# variable: points — line 70
# variable: char — line 80
# variable: count — line 80
# variable: elapsed — line 80
# definition: test_tradeoffs_not_newest_wins — line 97
# variable: result — line 99
# variable: point — line 102
# variable: points — line 102
# definition: test_holds_mismatches_and_separate_provenance — line 113
# variable: data — line 115
# variable: result — line 119
# variable: group — line 120
# variable: held — line 125
# variable: point — line 125
# definition: test_catalog_boundaries — line 153
# parameter: bad — line 153
# variable: data — line 155
# variable: point — line 156
# definition: test_actual_recovery_operator_cli — line 187
# parameter: tmp_path — line 187
# variable: source — line 189
# variable: original — line 191
# variable: argv — line 192
# variable: page — line 197
# variable: result — line 203
# variable: rejected — line 206
# definition: test_generator_is_an_actual_command — line 215
# parameter: tmp_path — line 215
# variable: source — line 217
# variable: result — line 220
# END CODE MAP

import copy
import json
import runpy
from pathlib import Path
from unittest.mock import patch

import pytest

from dr.__main__ import main
from dr.planning import plan, publish

BASE = 1791500000000


def ledger(count: int) -> dict[str, object]:
    """Generate independently balanced fictional order/payment rows with advancing commit times."""
    return {
        "customers": [[1, "Fictional dispatch supplies"]],
        "orders": [
            [number, 1, 30, BASE + number * 1000] for number in range(1, count + 1)
        ],
        "lines": [[number, 1, "BANDAGE", 3, 10] for number in range(1, count + 1)],
        "payments": [[number, 30] for number in range(1, count + 1)],
    }


def catalog() -> dict[str, object]:
    """Older fast, middle viable, newest slow and untested points have deliberately different tradeoffs."""
    points = [
        {
            "id": char * 64,
            "created_at_ms": BASE + count * 1000,
            "provenance": "supplied_synthetic",
            "snapshot": ledger(count),
            "restored": ledger(count) if elapsed is not None else None,
            "elapsed_ms": elapsed,
            "legal_hold": False,
        }
        for char, count, elapsed in (
            ("a", 1, 50),
            ("b", 2, 100),
            ("c", 3, 900),
            ("d", 3, None),
        )
    ]
    return {
        "schema": 1,
        "as_of_ms": BASE + 4000,
        "source_head": ledger(3),
        "objectives": {"rto_ms": 500, "rpo_ms": 1500, "max_lost_orders": 1},
        "retention_minimum": 1,
        "points": points,
    }


def test_tradeoffs_not_newest_wins() -> None:
    """The middle point meets all budgets; newest failed/untested restore cannot replace known viable recovery."""
    result = plan(catalog())
    assert result["has_eligible_point"]
    assert result["groups"][0]["recommended_point"] == "b" * 64
    points = {point["id"]: point for point in result["points"]}
    assert points["a" * 64]["evaluation"]["observed_rpo_ms"] == 2000
    assert points["a" * 64]["evaluation"]["lost_orders"] == 2
    assert not points["c" * 64]["eligible"]
    assert points["d" * 64]["evaluation"] is None
    assert points["b" * 64]["retention_review"] == "KEEP_REVIEW"
    assert points["a" * 64]["retention_review"] == "MANUAL_RETIREMENT_REVIEW"
    assert "untested_restore_requires_drill" in points["d" * 64]["retention_reasons"]
    assert "Fictional dispatch supplies" not in json.dumps(result)


def test_holds_mismatches_and_separate_provenance() -> None:
    """Hold and unknown/mismatched restoration cannot become delete advice; synthetic points never outrank measured ones."""
    data = catalog()
    data["points"][0]["legal_hold"] = True
    data["points"][0]["provenance"] = "measured_lab"
    data["points"][0]["restored"] = ledger(2)
    result = plan(data)
    assert [group["provenance"] for group in result["groups"]] == [
        "measured_lab",
        "supplied_synthetic",
    ]
    assert result["groups"][0]["recommended_point"] is None
    held = next(point for point in result["points"] if point["id"] == "a" * 64)
    assert set(held["retention_reasons"]) == {
        "legal_hold",
        "newest_minimum",
        "restore_mismatch_requires_investigation",
    }
    data["objectives"]["rpo_ms"] = 0
    assert not plan(data)["has_eligible_point"]


@pytest.mark.parametrize(
    "bad",
    [
        "schema",
        "clock",
        "minimum",
        "empty",
        "duplicate",
        "id",
        "future",
        "transaction-after-backup",
        "provenance",
        "hold",
        "partial",
        "rewrite",
        "objective",
    ],
)
def test_catalog_boundaries(bad: str) -> None:
    """Unknown or incompatible points are rejected instead of inventing a zero-loss or zero-time success."""
    data = catalog()
    point = data["points"][0]
    if bad == "schema":
        data["schema"] = True
    elif bad == "clock":
        data["as_of_ms"] = BASE
    elif bad == "minimum":
        data["retention_minimum"] = True
    elif bad == "empty":
        data["points"] = []
    elif bad == "duplicate":
        data["points"].append(copy.deepcopy(point))
    elif bad == "id":
        point["id"] = "0" * 64
    elif bad == "future":
        point["created_at_ms"] = BASE + 5000
    elif bad == "transaction-after-backup":
        point["created_at_ms"] = BASE
    elif bad == "provenance":
        point["provenance"] = "guaranteed-production"
    elif bad == "hold":
        point["legal_hold"] = "false"
    elif bad == "partial":
        point["elapsed_ms"] = None
    elif bad == "rewrite":
        point["snapshot"]["customers"][0][1] = "Other customer"
    else:
        data["objectives"]["rto_ms"] = 0
    with pytest.raises(ValueError):
        plan(data)


def test_actual_recovery_operator_cli(tmp_path: Path) -> None:
    """Review captured points, open inert aggregate output, preserve source and refuse replacement."""
    source = tmp_path / "catalog.json"
    source.write_text(json.dumps(catalog()))
    original = source.read_bytes()
    argv = ["dr", "plan", str(source), "--output", str(tmp_path / "review")]
    with patch("sys.argv", argv):
        assert main() == 0
        assert main() == 2
    assert source.read_bytes() == original
    page = (tmp_path / "review/recovery-review.html").read_text()
    assert (
        "Jason Stys" in page
        and "Content-Security-Policy" in page
        and "<script" not in page
    )
    result = json.loads((tmp_path / "review/recovery-review.json").read_text())
    with pytest.raises(OSError):
        publish(result, tmp_path / "absent/new")
    rejected = catalog()
    rejected["objectives"]["rpo_ms"] = 0
    source.write_text(json.dumps(rejected))
    with patch(
        "sys.argv", ["dr", "plan", str(source), "--output", str(tmp_path / "none")]
    ):
        assert main() == 1


def test_generator_is_an_actual_command(tmp_path: Path) -> None:
    """The documented demo entrypoint creates usable input instead of silently leaving no file."""
    source = tmp_path / "demo.json"
    with patch("sys.argv", ["planning_demo", "--output", str(source)]):
        runpy.run_module("scripts.planning_demo", run_name="__main__")
    result = plan(json.loads(source.read_text()))
    assert result["groups"][0]["recommended_point"] == "b" * 64
    assert len(result["points"]) == 4
