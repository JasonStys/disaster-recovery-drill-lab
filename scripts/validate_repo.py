"""Verify immutable workflow/tool controls and nonsecret tracked files; not a production security assessment. Jason Stys."""
# BEGIN CODE MAP (generated; python scripts/code_map.py)
# variable: ROOT — line 22
# definition: main — line 25
# variable: lock — line 27
# variable: entry — line 32
# variable: workflow — line 37
# variable: source — line 38
# variable: token — line 43
# variable: action — line 52
# variable: files — line 57
# variable: path — line 65
# END CODE MAP

from __future__ import annotations

import json
import re
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def main() -> int:
    """Check pinned Actions/tools, no artifact/cache uploads, and absence of tracked runtime backups/passwords."""
    lock = json.loads((ROOT / "tools.lock.json").read_text(encoding="utf-8"))
    if not re.fullmatch(
        r"postgres:18-alpine@sha256:[0-9a-f]{64}", lock["postgres_image"]
    ):
        raise ValueError("immutable official database image required")
    for entry in [*lock["restic"].values(), *lock["tools"].values()]:
        if not re.fullmatch(r"[0-9a-f]{64}", entry["sha256"]) or not entry[
            "url"
        ].startswith("https://github.com/"):
            raise ValueError("reviewed official tool hash required")
    for workflow in (ROOT / ".github/workflows").glob("*.yml"):
        source = workflow.read_text(encoding="utf-8")
        if "contents: read" not in source or "persist-credentials: false" not in source:
            raise ValueError("least-privilege checkout required")
        if any(
            token in source
            for token in (
                "pull_request_target:",
                "actions/upload-artifact",
                "actions/cache",
                "cache: 'pip'",
                "persist-credentials: true",
            )
        ):
            raise ValueError("unsafe workflow event or storage use")
        for action in re.findall(r"uses: ([^\s]+)", source):
            if not re.fullmatch(
                r"[A-Za-z0-9_.-]+/[A-Za-z0-9_./-]+@[0-9a-f]{40}", action
            ):
                raise ValueError("pinned action revision required")
    files = (
        subprocess.check_output(["git", "ls-files", "-z"], cwd=ROOT)
        .decode()
        .split("\0")
    )
    if any(
        path.startswith(("out/", ".tools/", ".venv/"))
        or path.endswith((".dump", ".env", ".password"))
        for path in files
    ):
        raise ValueError("runtime secrets/backups must remain untracked")
    print(
        "Pinned tools/actions, read-only checkout and storage/privacy contracts passed"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
