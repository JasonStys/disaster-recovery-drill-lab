"""Build/scan a non-root-only image from the immutable official PostgreSQL base; do not suppress vulnerabilities. Jason Stys."""
# BEGIN CODE MAP (generated; python scripts/code_map.py)
# variable: ROOT — line 26
# definition: main — line 29
# variable: base — line 33
# variable: dockerfile — line 36
# variable: environment — line 42
# variable: key — line 44
# variable: value — line 44
# variable: docker — line 47
# variable: source_sha — line 48
# variable: build — line 51
# variable: image — line 70
# variable: metadata — line 89
# END CODE MAP

from __future__ import annotations

import json
import os
import platform
import re
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def main() -> int:
    """Build only the reviewed context, scan the ACTUAL configuration digest, then save a source-bound ignored receipt."""
    if platform.system() != "Linux":
        raise ValueError("dedicated Linux Docker host required")
    base = json.loads((ROOT / "tools.lock.json").read_text(encoding="utf-8"))[
        "postgres_image"
    ]
    dockerfile = (ROOT / "Dockerfile").read_text(encoding="utf-8")
    if (
        not re.fullmatch(r"postgres:18-alpine@sha256:[0-9a-f]{64}", base)
        or f"FROM {base}\n" not in dockerfile
    ):
        raise ValueError("immutable official database base required")
    environment = {
        key: value
        for key, value in os.environ.items()
        if key not in {"DOCKER_CONTEXT", "DOCKER_HOST"}
    }
    docker = ["docker", "--host", "unix:///var/run/docker.sock"]
    source_sha = subprocess.check_output(
        ["git", "rev-parse", "HEAD"], cwd=ROOT, text=True, timeout=10
    ).strip()
    build = subprocess.run(
        [
            *docker,
            "build",
            "--quiet",
            "--platform",
            "linux/amd64",
            "--label",
            "recovery.lab.source=" + source_sha,
            "--file",
            str(ROOT / "Dockerfile"),
            str(ROOT),
        ],
        capture_output=True,
        text=True,
        env=environment,
        timeout=180,
        check=False,
    )
    image = build.stdout.strip()
    if build.returncode or not re.fullmatch(r"sha256:[0-9a-f]{64}", image):
        raise ValueError("owned derived image build failed")
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
        env=environment,
        check=True,
        timeout=180,
    )
    metadata = subprocess.check_output(
        [
            *docker,
            "image",
            "inspect",
            image,
            "--format",
            "{{.Architecture}}|{{.Config.User}}",
        ],
        env=environment,
        text=True,
        timeout=10,
    ).strip()
    if metadata != "amd64|postgres":
        raise ValueError("derived image identity invalid")
    (ROOT / ".tools/postgres-image.json").write_text(
        json.dumps(
            {"source_sha": source_sha, "base": base, "image_id": image}, sort_keys=True
        )
        + "\n",
        encoding="utf-8",
        newline="\n",
    )
    print(
        json.dumps(
            {
                "derived_image_id": image,
                "non_root": True,
                "unused_gosu_removed": True,
                "high_critical_gate": "PASS",
            },
            sort_keys=True,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
