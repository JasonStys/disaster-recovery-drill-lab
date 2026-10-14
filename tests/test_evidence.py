"""Fabricated report fixtures validate rejection/privacy/escaping, not measured disaster-recovery claims. Jason Stys."""
# BEGIN CODE MAP (generated; python scripts/code_map.py)
# definition: test_bad_report — line 70
# parameter: fake_report — line 70
# parameter: field — line 70
# parameter: value — line 70
# definition: test_cases_and_proofs — line 77
# parameter: fake_report — line 77
# variable: valid — line 80
# variable: key — line 87
# variable: value — line 87
# variable: report — line 98
# variable: report — line 102
# definition: test_postgres_report — line 108
# parameter: fake_report — line 109
# parameter: head — line 109
# parameter: ledger — line 109
# variable: name — line 120
# variable: field — line 126
# variable: value — line 126
# variable: changed — line 137
# definition: test_html_and_no_overwrite — line 143
# parameter: fake_report — line 143
# parameter: tmp_path — line 143
# variable: output — line 146
# variable: text — line 148
# definition: test_cli_privacy — line 156
# parameter: tmp_path — line 157
# parameter: fake_report — line 158
# parameter: ledger — line 159
# parameter: head — line 160
# parameter: capsys — line 161
# variable: source — line 164
# variable: value — line 178
# END CODE MAP

from __future__ import annotations

import json
import sys
from copy import deepcopy
from pathlib import Path
from typing import Any
from unittest.mock import patch

import pytest

from dr.__main__ import main
from dr.evidence import CASES, publish, validate
from dr.ledger import evaluate


@pytest.mark.parametrize(
    "field,value",
    [
        ("schema", True),
        ("author", "other"),
        ("synthetic", False),
        ("engine", []),
        ("engine", "unknown"),
        ("source_sha", "0" * 40),
        ("source_sha", []),
        ("source_sha", "a" * 39),
        ("snapshot_id", "latest"),
        ("dump_sha256", "bad"),
        ("checks", []),
        ("recovery", {}),
    ],
)
def test_bad_report(fake_report: dict[str, Any], field: str, value: object) -> None:
    """Report identity and completeness cannot accept a forged success or wrong engine."""
    fake_report[field] = value
    with pytest.raises(ValueError):
        validate(fake_report)


def test_cases_and_proofs(fake_report: dict[str, Any]) -> None:
    """Unknown/duplicate/failed cases and nonbounded proof values fail; integer/bool/text aggregates pass."""
    assert validate(fake_report) == fake_report
    valid = deepcopy(fake_report)
    valid["checks"][0]["evidence"] = {
        "number": 1,
        "text": "<script>alert(1)</script>",
        "flag": True,
    }
    validate(valid)
    for key, value in (
        ("name", "unknown"),
        ("result", "FAIL"),
        ("duration_ms", True),
        ("evidence", {}),
        ("evidence", {"bad-key": 1}),
        ("evidence", {"n": -1}),
        ("evidence", {"n": 1.2}),
        ("evidence", {"secret": "\n"}),
        ("evidence", {"too_long": "x" * 129}),
    ):
        report = deepcopy(fake_report)
        report["checks"][0][key] = value
        with pytest.raises(ValueError):
            validate(report)
    report = deepcopy(fake_report)
    report["checks"][1]["name"] = report["checks"][0]["name"]
    with pytest.raises(ValueError):
        validate(report)


def test_postgres_report(
    fake_report: dict[str, Any], ledger: dict[str, Any], head: dict[str, Any]
) -> None:
    """Database reports require an exact recovery and actually met scalar budgets; native reports cannot claim RPO."""
    fake_report["engine"] = "postgres"
    fake_report["checks"] = [
        {
            "name": name,
            "result": "PASS",
            "duration_ms": 1,
            "evidence": {"fixture": True},
        }
        for name in sorted(CASES["postgres"])
    ]
    fake_report["recovery"] = evaluate(
        ledger, head, ledger, 100, {"rto_ms": 1000, "rpo_ms": 400, "max_lost_orders": 1}
    )
    validate(fake_report)
    for field, value in (
        ("result", "FAIL"),
        ("snapshot_matches", False),
        ("recovered_fingerprint", "bad"),
        ("recovered_orders", 0),
        ("rto_limit_ms", 0),
        ("observed_rto_ms", 1001),
        ("rpo_limit_ms", 399),
        ("lost_order_limit", 0),
        ("lost_orders", True),
    ):
        changed = deepcopy(fake_report)
        changed["recovery"][field] = value
        with pytest.raises(ValueError):
            validate(changed)


def test_html_and_no_overwrite(tmp_path: Path, fake_report: dict[str, Any]) -> None:
    """Escape proof strings and block network/script execution; never overwrite previous output."""
    fake_report["checks"][0]["evidence"] = {"fixture": "<script>alert(1)</script>"}
    output = tmp_path / "report"
    publish(fake_report, output)
    text = (output / "drill.html").read_text(encoding="utf-8")
    assert "<script>" not in text and "&lt;script&gt;" in text
    assert "default-src 'none'" in text and "Jason Stys" in text
    assert json.loads((output / "drill.json").read_text()) == fake_report
    with pytest.raises(FileExistsError):
        publish(fake_report, output)


def test_cli_privacy(
    tmp_path: Path,
    fake_report: dict[str, Any],
    ledger: dict[str, Any],
    head: dict[str, Any],
    capsys: pytest.CaptureFixture[str],
) -> None:
    """CLI returns deterministic 0/1/2 outcomes and never reflects malformed private input."""
    source = tmp_path / "input.json"
    source.write_text('{"secret":"DO_NOT_REFLECT", "secret": 2}')
    with patch.object(
        sys,
        "argv",
        ["dr", "report", str(source), "--output", str(tmp_path / "invalid")],
    ):
        assert main() == 2
    assert "DO_NOT_REFLECT" not in capsys.readouterr().out
    source.write_text(json.dumps(fake_report))
    with patch.object(
        sys, "argv", ["dr", "report", str(source), "--output", str(tmp_path / "valid")]
    ):
        assert main() == 0
    value = {
        "snapshot": ledger,
        "source_head": head,
        "restored": ledger,
        "elapsed_ms": 100,
        "objectives": {"rto_ms": 1000, "rpo_ms": 400, "max_lost_orders": 1},
    }
    source.write_text(json.dumps(value))
    with patch.object(sys, "argv", ["dr", "evaluate", str(source)]):
        assert main() == 0
    value["objectives"]["max_lost_orders"] = 0
    source.write_text(json.dumps(value))
    with patch.object(sys, "argv", ["dr", "evaluate", str(source)]):
        assert main() == 1
