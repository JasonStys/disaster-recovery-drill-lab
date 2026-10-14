"""Informational measured canonical-ledger and recovery-evaluation timing/allocation, with correctness oracle. Jason Stys."""
# BEGIN CODE MAP (generated; python scripts/code_map.py)
# variable: ROOT — line 26
# definition: main — line 32
# variable: fixture — line 34
# variable: samples — line 36
# variable: _ — line 38
# variable: started — line 39
# variable: _ — line 40
# variable: result — line 41
# variable: _ — line 44
# variable: peak — line 44
# variable: value — line 58
# END CODE MAP

from __future__ import annotations

import json
import platform
import statistics
import sys
import time
import tracemalloc
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from dr.contracts import load  # noqa: E402
from dr.ledger import evaluate  # noqa: E402


def main() -> int:
    """Measure five warmed batches of 100 actual evaluations; no hardware-dependent threshold or fabricated speedup."""
    fixture = load(ROOT / "examples/objective-evaluation.json")
    assert evaluate(**fixture)["lost_orders"] == 1
    samples = []
    tracemalloc.start()
    for _ in range(5):
        started = time.perf_counter()
        for _ in range(100):
            result = evaluate(**fixture)
            assert result["result"] == "PASS" and result["observed_rpo_ms"] == 400
        samples.append((time.perf_counter() - started) * 1000 / 100)
    _, peak = tracemalloc.get_traced_memory()
    tracemalloc.stop()
    print(
        json.dumps(
            {
                "author": "Jason Stys",
                "engine": "native-Python-evaluate",
                "python": platform.python_version(),
                "platform": platform.system(),
                "batches": 5,
                "evaluations_per_batch": 100,
                "baseline_orders": 2,
                "head_orders": 3,
                "median_ms": round(statistics.median(samples), 3),
                "samples_ms": [round(value, 3) for value in samples],
                "peak_python_bytes": peak,
                "includes_database_or_restic": False,
                "correctness_oracle": "PASS, one lost order, 400ms window",
            },
            sort_keys=True,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
