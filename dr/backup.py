"""Fixed local restic operations on fresh synthetic workspaces; passwords/output remain private. Jason Stys."""
# BEGIN CODE MAP (generated; python scripts/code_map.py)
# variable: ROOT — line 112
# definition: workspace — line 115
# parameter: path — line 115
# variable: parent — line 117
# definition: private_file — line 133
# parameter: content — line 133
# parameter: path — line 133
# variable: descriptor — line 135
# variable: target — line 136
# definition: sha256 — line 140
# parameter: path — line 140
# variable: digest — line 143
# variable: source — line 144
# variable: data — line 145
# definition: revision — line 150
# definition: Restic — line 157
# definition: __init__ — line 160
# parameter: root — line 160
# parameter: self — line 160
# definition: run — line 171
# parameter: args — line 172
# parameter: repo — line 172
# parameter: self — line 172
# parameter: wrong — line 172
# variable: selected — line 175
# variable: environment — line 181
# variable: key — line 183
# variable: value — line 183
# definition: success — line 204
# parameter: args — line 204
# parameter: self — line 204
# variable: result — line 206
# definition: backup — line 211
# parameter: self — line 211
# parameter: source — line 211
# variable: snapshots — line 218
# variable: snapshot — line 221
# definition: reject_password — line 225
# parameter: self — line 225
# variable: result — line 227
# definition: reject_missing — line 234
# parameter: self — line 234
# variable: result — line 236
# variable: error — line 237
# variable: absent — line 238
# variable: message — line 246
# definition: reject_corruption — line 254
# parameter: self — line 254
# variable: copied — line 256
# variable: packs — line 258
# variable: path — line 258
# variable: pack — line 261
# variable: original — line 262
# variable: target — line 265
# variable: value — line 266
# variable: result — line 271
# variable: evidence — line 272
# variable: message — line 275
# definition: restore — line 285
# parameter: name — line 285
# parameter: self — line 285
# parameter: snapshot — line 285
# variable: target — line 290
# variable: path — line 294
# variable: paths — line 294
# definition: Measurements — line 301
# definition: __init__ — line 304
# parameter: self — line 304
# definition: check — line 308
# parameter: name — line 308
# parameter: proof — line 308
# parameter: self — line 308
# parameter: started — line 308
# definition: report — line 319
# parameter: dump — line 320
# parameter: engine — line 320
# parameter: recovery — line 320
# parameter: self — line 320
# parameter: snapshot — line 320
# definition: native_drill — line 336
# parameter: root — line 336
# variable: measurements — line 338
# variable: payload — line 339
# variable: backup — line 341
# variable: started — line 342
# variable: snapshot — line 343
# variable: started — line 347
# variable: started — line 350
# variable: started — line 353
# variable: started — line 360
# variable: recovered — line 361
# variable: report — line 367
# END CODE MAP

from __future__ import annotations

import hashlib
import os
import re
import secrets
import shutil
import subprocess
import time
from pathlib import Path
from typing import Any

from dr.contracts import decode, fingerprint, ordinary
from dr.evidence import publish

ROOT = Path(__file__).resolve().parents[1]


def workspace(path: Path) -> Path:
    """Create only a new named direct child of repo out/; no user files or existing output can be overwritten."""
    parent = ROOT / "out"
    if (
        parent.is_symlink()
        or parent.exists()
        and getattr(parent.lstat(), "st_file_attributes", 0) & 1024
    ):
        raise ValueError("ordinary output parent required")
    if path.parent.resolve() != parent.resolve() or not re.fullmatch(
        r"[a-z][a-z0-9-]{0,63}", path.name
    ):
        raise ValueError("new named out/ workspace required")
    parent.mkdir(mode=0o700, exist_ok=True)
    path.mkdir(mode=0o700, exist_ok=False)
    return path.resolve()


def private_file(path: Path, content: bytes) -> None:
    """Create a new private ordinary file exclusively; Windows relies additionally on inherited user ACLs."""
    descriptor = os.open(path, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600)
    with os.fdopen(descriptor, "wb") as target:
        target.write(content)


def sha256(path: Path) -> str:
    """Fingerprint a regular file with bounded chunks; no archive data is executed or printed."""
    ordinary(path)
    digest = hashlib.sha256()
    with path.open("rb") as source:
        while data := source.read(1024 * 1024):
            digest.update(data)
    return digest.hexdigest()


def revision() -> str:
    """Read the complete checked-out Git source revision; only committed sources produce measured reports."""
    return subprocess.check_output(
        ["git", "rev-parse", "HEAD"], cwd=ROOT, text=True, timeout=10
    ).strip()


class Restic:
    """Only fixed local backup operations; no remote repository, password command, inherited restic config or shell."""

    def __init__(self, root: Path) -> None:
        """Use a fresh private synthetic root; create random repository/wrong passwords, never accept real credentials."""
        self.root = root.resolve()
        self.repo = self.root / "repository"
        self.password = self.root / "repository.password"
        self.wrong = self.root / "wrong.password"
        self.binary = ROOT / ".tools" / ("restic.exe" if os.name == "nt" else "restic")
        ordinary(self.binary)
        private_file(self.password, (secrets.token_urlsafe(48) + "\n").encode())
        private_file(self.wrong, (secrets.token_urlsafe(48) + "\n").encode())

    def run(
        self, *args: str, repo: Path | None = None, wrong: bool = False
    ) -> subprocess.CompletedProcess[str]:
        """Invoke only an owned local repository and explicit password file; bounded deadline and fixed failure diagnostics."""
        selected = (repo or self.repo).resolve()
        if selected.parent != self.root or selected.name not in {
            "repository",
            "corrupted-copy",
        }:
            raise ValueError("owned local repository required")
        environment = {
            key: value
            for key, value in os.environ.items()
            if not key.upper().startswith("RESTIC_")
        }
        return subprocess.run(
            [
                str(self.binary),
                "--repo",
                str(selected),
                "--password-file",
                str(self.wrong if wrong else self.password),
                "--no-cache",
                *args,
            ],
            cwd=self.root,
            env=environment,
            text=True,
            capture_output=True,
            timeout=120,
            check=False,
        )

    def success(self, *args: str) -> str:
        """Require an actual successful restic operation without reflecting its paths or repository credentials."""
        result = self.run(*args)
        if result.returncode != 0:
            raise ValueError("owned backup operation failed")
        return result.stdout

    def backup(self, source: Path) -> str:
        """Initialize an encrypted repository and back up only a known direct-child ordinary file; return exact snapshot ID."""
        if source.parent.resolve() != self.root:
            raise ValueError("owned synthetic file required")
        ordinary(source)
        self.success("init")
        self.success("backup", "--json", "--host", "synthetic-lab", source.name)
        snapshots = decode(self.success("snapshots", "--json").encode())
        if not isinstance(snapshots, list) or len(snapshots) != 1:
            raise ValueError("one complete snapshot required")
        snapshot = fingerprint(snapshots[0]["id"])
        self.success("check", "--read-data")
        return snapshot

    def reject_password(self) -> None:
        """Prove a wrong key is specifically rejected, not a generic filesystem/transport failure."""
        result = self.run("snapshots", "--json", wrong=True)
        if (
            result.returncode == 0
            or "wrong password or no key found" not in result.stderr.lower()
        ):
            raise ValueError("wrong-key oracle failed")

    def reject_missing(self) -> None:
        """Require specific missing full snapshot rejection; never restore the floating latest selector."""
        result = self.run("ls", "0" * 64)
        error = result.stderr.lower()
        absent = self.repo / "snapshots" / ("0" * 64)
        if (
            result.returncode == 0
            or absent.exists()
            or "failed to load snapshot" not in error
            or "0" * 64 not in error
            or not any(
                message in error
                for message in (
                    "no such file or directory",
                    "system cannot find the file specified",
                )
            )
        ):
            raise ValueError("missing-snapshot oracle failed")

    def reject_corruption(self) -> None:
        """Copy only the fresh owned repo and flip one pack byte; require specific integrity rejection, preserve the original."""
        copied = self.root / "corrupted-copy"
        shutil.copytree(self.repo, copied)
        packs = sorted(path for path in (copied / "data").rglob("*") if path.is_file())
        if not packs:
            raise ValueError("actual pack data missing")
        pack = packs[0]
        original = sha256(pack)
        # Restic packs are deliberately read-only on POSIX. Only the NEW disposable copy is made writable for injection.
        os.chmod(pack, 0o600)
        with pack.open("r+b") as target:
            value = target.read(1)
            target.seek(0)
            target.write(bytes([value[0] ^ 1]))
        if sha256(pack) == original:
            raise ValueError("corruption injection missing")
        result = self.run("check", "--read-data", repo=copied)
        evidence = (result.stdout + result.stderr).lower()
        if result.returncode == 0 or not any(
            message in evidence
            for message in (
                "does not match",
                "invalid data",
                "ciphertext verification failed",
                "unexpected pack id",
                "failed to decrypt",
            )
        ):
            raise ValueError("corruption oracle failed")

    def restore(self, snapshot: str, name: str) -> Path:
        """Restore an exact full snapshot into a new fixed-name target and require its ordinary payload file."""
        fingerprint(snapshot)
        if name not in {"restored", "repeat-restored"}:
            raise ValueError("owned restore name required")
        target = self.root / name
        target.mkdir(mode=0o700, exist_ok=False)
        self.success("restore", snapshot, "--target", str(target), "--verify")
        # Relative backup source names produce a single fixed payload beneath the target.
        paths = [path for path in target.rglob("*") if path.is_file()]
        if len(paths) != 1:
            raise ValueError("one restored payload required")
        ordinary(paths[0])
        return paths[0]


class Measurements:
    """Collect only small selected aggregates after actual assertions; never fabricate process success."""

    def __init__(self) -> None:
        """Start an empty per-run measured case list."""
        self.checks: list[dict[str, Any]] = []

    def check(self, name: str, started: float, proof: dict[str, Any]) -> None:
        """Record monotonic duration after the caller's oracle has passed."""
        self.checks.append(
            {
                "name": name,
                "result": "PASS",
                "duration_ms": int((time.monotonic() - started) * 1000),
                "evidence": proof,
            }
        )

    def report(
        self, engine: str, snapshot: str, dump: Path, recovery: Any = None
    ) -> dict[str, Any]:
        """Construct selected immutable-source evidence; passwords/private paths never enter the public result."""
        return {
            "schema": 1,
            "author": "Jason Stys",
            "synthetic": True,
            "engine": engine,
            "source_sha": revision(),
            "snapshot_id": snapshot,
            "dump_sha256": sha256(dump),
            "checks": self.checks,
            "recovery": recovery,
        }


def native_drill(root: Path) -> dict[str, Any]:
    """Actually encrypt, fully read/check, wrong-key/tamper test and restore a synthetic file; not a database recovery claim."""
    measurements = Measurements()
    payload = root / "synthetic.txt"
    private_file(payload, b"Fictional warehouse recovery sample; Jason Stys.\n" * 100)
    backup = Restic(root)
    started = time.monotonic()
    snapshot = backup.backup(payload)
    measurements.check(
        "encrypted_backup", started, {"engine": "restic", "full_data_check": True}
    )
    started = time.monotonic()
    backup.reject_password()
    measurements.check("wrong_password", started, {"specifically_rejected": True})
    started = time.monotonic()
    backup.reject_missing()
    measurements.check("missing_snapshot", started, {"full_id_rejected": True})
    started = time.monotonic()
    backup.reject_corruption()
    measurements.check(
        "corrupt_pack",
        started,
        {"changed_byte_verified": True, "integrity_rejected": True},
    )
    started = time.monotonic()
    recovered = backup.restore(snapshot, "restored")
    if sha256(recovered) != sha256(payload):
        raise ValueError("restored file mismatch")
    measurements.check(
        "exact_restore", started, {"matching_sha256": True, "verify_enabled": True}
    )
    report = measurements.report("native", snapshot, payload)
    publish(report, root / "report")
    return report
