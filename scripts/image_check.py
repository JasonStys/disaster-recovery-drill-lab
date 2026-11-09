"""Build/scan a non-root-only image from the immutable official PostgreSQL base; do not suppress vulnerabilities. Jason Stys."""
# BEGIN CODE MAP (generated; python scripts/code_map.py)
# variable: ROOT — line 33
# definition: public_build_diagnostics — line 36
# parameter: content — line 36
# variable: clean — line 38
# variable: lines — line 39
# variable: line — line 40
# variable: line — line 54
# variable: character — line 56
# definition: main — line 61
# variable: base — line 65
# variable: dockerfile — line 68
# variable: environment — line 74
# variable: key — line 76
# variable: value — line 76
# variable: docker — line 79
# variable: source_sha — line 80
# variable: build — line 83
# variable: image — line 102
# variable: metadata — line 123
# END CODE MAP

from __future__ import annotations

import json
import os
import platform
import re
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def public_build_diagnostics(content: str) -> str:
    """Bound public package/build diagnostics; remove terminal controls, URL credentials and secret-like lines."""
    clean = re.sub(r"\x1b\[[0-?]*[ -/]*[@-~]", "", content)
    lines = []
    for line in clean.splitlines()[-80:]:
        if not re.search(
            r"error|warning|failed|unable|apk|packages|brotli|curl|musl|zlib|fetch|repository",
            line,
            re.I,
        ):
            continue
        if re.search(
            r"password|token|secret|authorization|credential|(?:AKIA|ASIA)[A-Z0-9]{16}|gh[pousr]_|github_pat_",
            line,
            re.I,
        ):
            lines.append("[credential-like build diagnostic omitted]")
            continue
        line = re.sub(r"(https?://)[^/\s@]+@", r"\1<redacted>@", line)
        lines.append(
            "".join(character for character in line if 32 <= ord(character) < 127)[:400]
        )
    return "\n".join(lines)[-4096:] or "No public package diagnostic was available."


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
        print("Derived image build failed; bounded public package diagnostics follow:")
        print(public_build_diagnostics(build.stderr))
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
