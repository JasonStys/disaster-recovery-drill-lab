"""Generate exhaustive Git-tracked README summaries without including ignored runtime data. Jason Stys."""
# BEGIN CODE MAP (generated; python scripts/code_map.py)
# variable: ROOT — line 32
# variable: BEGIN — line 33
# variable: END — line 33
# variable: SPECIAL — line 34
# definition: description — line 53
# parameter: path — line 53
# variable: content — line 57
# variable: line — line 65
# definition: main — line 71
# variable: parser — line 73
# variable: args — line 75
# variable: files — line 76
# variable: rows — line 84
# variable: path — line 85
# variable: label — line 86
# variable: readme — line 88
# variable: original — line 89
# variable: begin — line 90
# variable: end — line 90
# variable: expected — line 91
# END CODE MAP

from __future__ import annotations

import argparse
import ast
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BEGIN, END = "<!-- BEGIN FILE GUIDE -->", "<!-- END FILE GUIDE -->"
SPECIAL = {
    ".dockerignore": "Excludes every project file except Dockerfile from the derived-image context.",
    ".gitattributes": "Portable LF text handling.",
    ".gitignore": "Excludes tools, runtime backups, passwords, caches and private drill outputs.",
    "LICENSE": "MIT license for authored code.",
    "pyproject.toml": "Strict types, lint, tests and combined statement/branch coverage gate.",
    "requirements-dev.in": "Exact validation dependencies; standard-library application runtime.",
    "requirements-dev.lock": "Complete hash-pinned validation graph.",
    "tools.lock.json": "Official restic/scanner archive hashes and immutable PostgreSQL image digest.",
    "examples/objective-evaluation.json": "Explicitly synthetic offline ledger and recovery-objective fixture.",
    "docs/reports/native.json": "Measured native restic encryption/integrity/restore exercise.",
    "docs/reports/native.html": "Escaped inert HTML rendering of native measured results.",
    "docs/reports/postgres.json": "Actual isolated PostgreSQL restore and objective measurements.",
    "docs/reports/postgres.html": "Escaped inert HTML rendering of actual PostgreSQL results.",
    "docs/reports/benchmark.json": "Measured independent consistency/objective evaluation benchmark.",
    "docs/reports/ci.json": "Immutable executable-source CI snapshot with actual completed checks.",
}


def description(path: str) -> str:
    """Require an actual file purpose; unknown formats fail instead of silently omitting files."""
    if path in SPECIAL:
        return SPECIAL[path]
    content = (ROOT / path).read_text(encoding="utf-8")
    if path.endswith(".py"):
        return (ast.get_docstring(ast.parse(content)) or "").splitlines()[0]
    if path.endswith(".md"):
        return content.splitlines()[0].lstrip("# ") + "."
    if path.endswith((".yml", ".yaml", ".sh", ".sql")) or path == "Dockerfile":
        return next(
            line.lstrip("#- ")
            for line in content.splitlines()
            if line.startswith(("# ", "-- "))
        )
    raise ValueError("missing tracked-file purpose: " + path)


def main() -> int:
    """Generate/check summaries for every staged/tracked file; stage intended new files first."""
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    files = (
        subprocess.check_output(["git", "ls-files", "-z"], cwd=ROOT)
        .decode()
        .rstrip("\0")
        .split("\0")
    )
    if files == [""]:
        raise ValueError("stage intended files first")
    rows = ["| File | Purpose |", "| --- | --- |"]
    for path in sorted(files):
        label = path.replace("_", "\\_")
        rows.append(f"| [{label}]({path}) | {description(path).replace('|', '/')} |")
    readme = ROOT / "README.md"
    original = readme.read_text(encoding="utf-8")
    begin, end = original.index(BEGIN) + len(BEGIN), original.index(END)
    expected = original[:begin] + "\n\n" + "\n".join(rows) + "\n\n" + original[end:]
    if args.check and expected != original:
        raise ValueError("README inventory stale")
    if not args.check:
        readme.write_text(expected, encoding="utf-8", newline="\n")
    print(f"README inventory current: {len(files)} files")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
