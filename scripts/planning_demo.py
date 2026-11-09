"""Generate fictional multi-point dispatch-supply recovery review input. Created by Jason Stys."""
# BEGIN CODE MAP (generated; python scripts/code_map.py)
# definition: ledger — line 23
# parameter: count — line 23
# variable: number — line 29
# variable: number — line 31
# variable: number — line 32
# definition: main — line 36
# variable: parser — line 38
# variable: output — line 40
# variable: points — line 41
# variable: char — line 51
# variable: count — line 51
# variable: duration — line 51
# variable: stream — line 58
# END CODE MAP

import argparse
import json
from pathlib import Path


def ledger(count: int) -> dict[str, object]:
    """Create balanced synthetic stock-order lines and payments with explicit original commit timestamps."""
    return {
        "customers": [[1, "Fictional dispatch supplies"]],
        "orders": [
            [number, 1, 30, 1791500000000 + number * 1000]
            for number in range(1, count + 1)
        ],
        "lines": [[number, 1, "BANDAGE", 3, 10] for number in range(1, count + 1)],
        "payments": [[number, 30] for number in range(1, count + 1)],
    }


def main() -> None:
    """Exclusively create one synthetic catalog; no backup repository, password or raw real record is used."""
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, required=True)
    output = parser.parse_args().output
    points = [
        {
            "id": char * 64,
            "created_at_ms": 1791500000000 + count * 1000,
            "provenance": "supplied_synthetic",
            "snapshot": ledger(count),
            "restored": ledger(count) if duration is not None else None,
            "elapsed_ms": duration,
            "legal_hold": False,
        }
        for char, count, duration in (
            ("a", 1, 50),
            ("b", 2, 100),
            ("c", 3, 900),
            ("d", 3, None),
        )
    ]
    with output.open("x", encoding="utf-8") as stream:
        json.dump(
            {
                "schema": 1,
                "as_of_ms": 1791500004000,
                "source_head": ledger(3),
                "objectives": {"rto_ms": 500, "rpo_ms": 1500, "max_lost_orders": 1},
                "retention_minimum": 1,
                "points": points,
            },
            stream,
            indent=2,
        )
        stream.write("\n")


if __name__ == "__main__":
    main()
