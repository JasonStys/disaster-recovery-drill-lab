"""Scan only the immutable official PostgreSQL image used by the owned Linux drill. Jason Stys."""
# BEGIN CODE MAP (generated; python scripts/code_map.py)
# variable: ROOT — line 15
# definition: main — line 18
# variable: image — line 20
# END CODE MAP

from __future__ import annotations

import json
import re
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def main() -> int:
    """Require the fixed reviewed image name/digest and fail on any detected HIGH/CRITICAL finding; no suppressions."""
    image = json.loads((ROOT / "tools.lock.json").read_text(encoding="utf-8"))[
        "postgres_image"
    ]
    if not re.fullmatch(r"postgres:18-alpine@sha256:[0-9a-f]{64}", image):
        raise ValueError("immutable official database image required")
    subprocess.run(
        [
            str(ROOT / ".tools/trivy"),
            "image",
            "--severity",
            "HIGH,CRITICAL",
            "--exit-code",
            "1",
            "--scanners",
            "vuln",
            image,
        ],
        check=True,
        timeout=180,
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
