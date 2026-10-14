"""Offline JSON evaluation/report CLI; input files are data, never SQL or executable code. Jason Stys."""
# BEGIN CODE MAP (generated; python scripts/code_map.py)
# definition: main — line 25
# variable: parser — line 27
# variable: sub — line 30
# variable: check — line 31
# variable: report — line 36
# variable: args — line 41
# variable: raw — line 43
# variable: value — line 47
# variable: result — line 50
# END CODE MAP

from __future__ import annotations

import argparse
import json
from pathlib import Path

from dr.contracts import load, record
from dr.evidence import publish
from dr.ledger import evaluate


def main() -> int:
    """Evaluate three captured synthetic ledgers (PASS=0/FAIL=1) or publish a report; malformed input exits 2."""
    parser = argparse.ArgumentParser(
        description="Disaster Recovery Drill Lab — Jason Stys"
    )
    sub = parser.add_subparsers(dest="command", required=True)
    check = sub.add_parser(
        "evaluate",
        help="Evaluate captured synthetic ledgers and explicit objectives offline",
    )
    check.add_argument("input", type=Path)
    report = sub.add_parser(
        "report", help="Validate and render an aggregate into a new output directory"
    )
    report.add_argument("input", type=Path)
    report.add_argument("--output", required=True, type=Path)
    args = parser.parse_args()
    try:
        raw = load(args.input)
        if args.command == "report":
            publish(raw, args.output)
            return 0
        value = record(
            raw, {"snapshot", "source_head", "restored", "elapsed_ms", "objectives"}
        )
        result = evaluate(**value)
        print(json.dumps(result, sort_keys=True))
        return 0 if result["result"] == "PASS" else 1
    except (ValueError, OSError, RecursionError):
        print('{"error":"input or output contract failed"}')
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
