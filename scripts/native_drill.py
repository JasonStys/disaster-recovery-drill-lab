"""Run the actual encrypted synthetic-file exercise without Docker or real user data. Jason Stys."""
# BEGIN CODE MAP (generated; python scripts/code_map.py)
# variable: ROOT — line 18
# definition: main — line 23
# variable: parser — line 25
# variable: args — line 27
# variable: report — line 29
# END CODE MAP

from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from dr.backup import native_drill, workspace  # noqa: E402


def main() -> int:
    """Require a new named out/ directory; no existing backups, host settings or system services are modified."""
    parser = argparse.ArgumentParser(description="Native restic drill — Jason Stys")
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    try:
        report = native_drill(workspace(args.output))
        print(json.dumps(report, sort_keys=True))
        return 0
    except (ValueError, OSError, subprocess.SubprocessError):
        print('{"error":"owned native drill failed; private output retained"}')
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
