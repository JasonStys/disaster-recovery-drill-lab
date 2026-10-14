"""Actual isolated PostgreSQL logical-snapshot disaster drill; only uniquely owned synthetic containers. Jason Stys."""
# BEGIN CODE MAP (generated; python scripts/code_map.py)
# variable: ROOT — line 148
# definition: inspect_guard — line 156
# parameter: image — line 156
# parameter: name — line 156
# parameter: raw — line 156
# parameter: run_id — line 156
# variable: item — line 160
# variable: host — line 161
# variable: mount — line 193
# definition: Postgres — line 197
# definition: __init__ — line 200
# parameter: root — line 200
# parameter: self — line 200
# variable: key — line 218
# variable: value — line 218
# definition: command — line 233
# parameter: args — line 233
# parameter: self — line 233
# definition: run — line 239
# parameter: allow_failure — line 240
# parameter: args — line 240
# parameter: data — line 240
# parameter: self — line 240
# variable: result — line 243
# definition: inspect — line 255
# parameter: name — line 255
# parameter: self — line 255
# variable: value — line 259
# definition: start — line 263
# parameter: role — line 263
# parameter: self — line 263
# variable: name — line 267
# variable: existing — line 270
# variable: deadline — line 310
# variable: item — line 312
# variable: ready — line 315
# variable: process — line 330
# variable: configured — line 335
# definition: sql — line 345
# parameter: content — line 346
# parameter: name — line 346
# parameter: reject_state — line 346
# parameter: self — line 346
# variable: args — line 350
# variable: result — line 369
# definition: fixture — line 378
# parameter: filename — line 378
# parameter: name — line 378
# parameter: self — line 378
# definition: capture — line 384
# parameter: name — line 384
# parameter: self — line 384
# variable: value — line 386
# definition: dump — line 390
# parameter: name — line 390
# parameter: self — line 390
# variable: target — line 393
# variable: descriptor — line 394
# variable: output — line 395
# variable: result — line 396
# variable: content — line 422
# definition: restore — line 427
# parameter: archive — line 427
# parameter: name — line 427
# parameter: self — line 427
# variable: source — line 430
# variable: result — line 431
# definition: constraints — line 459
# parameter: baseline — line 459
# parameter: name — line 459
# parameter: self — line 459
# definition: stop — line 478
# parameter: name — line 478
# parameter: self — line 478
# definition: close — line 485
# parameter: self — line 485
# variable: removed — line 487
# variable: name — line 488
# variable: current — line 489
# variable: after — line 494
# variable: removed — line 497
# definition: execute — line 502
# parameter: root — line 502
# variable: measurements — line 504
# variable: database — line 505
# variable: stage — line 506
# variable: started — line 508
# variable: source — line 509
# variable: stage — line 521
# variable: started — line 522
# variable: baseline — line 525
# variable: dump — line 528
# variable: stage — line 536
# variable: started — line 537
# variable: backup — line 538
# variable: snapshot — line 539
# variable: stage — line 543
# variable: started — line 544
# variable: stage — line 547
# variable: started — line 548
# variable: head — line 554
# variable: stage — line 557
# variable: recovery_started — line 558
# variable: stage — line 565
# variable: started — line 566
# variable: recovered_dump — line 567
# variable: restored — line 570
# variable: recovered — line 572
# variable: stage — line 585
# variable: started — line 586
# variable: elapsed — line 593
# variable: stage — line 594
# variable: started — line 595
# variable: result — line 596
# variable: stage — line 608
# variable: started — line 609
# variable: strict — line 610
# variable: stage — line 620
# variable: started — line 621
# variable: repeated_dump — line 622
# variable: repeated — line 625
# variable: stage — line 635
# variable: started — line 636
# variable: removed — line 637
# variable: report — line 643
# definition: main — line 660
# variable: parser — line 662
# variable: args — line 667
# END CODE MAP

from __future__ import annotations

import argparse
import json
import os
import platform
import re
import secrets
import shutil
import subprocess
import sys
import time
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from dr.backup import Measurements, Restic, private_file, sha256, workspace  # noqa: E402
from dr.contracts import decode  # noqa: E402
from dr.evidence import publish  # noqa: E402
from dr.ledger import dataset, evaluate  # noqa: E402


def inspect_guard(raw: Any, name: str, run_id: str, image: str) -> None:
    """Require exact ownership, image and isolation before any exec/stop/removal; daemon/admin remain trusted."""
    if not isinstance(raw, list) or len(raw) != 1:
        raise ValueError("one owned container required")
    item = raw[0]
    host = item["HostConfig"]
    if (
        item["Config"].get("User") != "postgres"
        or host.get("CapDrop") != ["ALL"]
        or set(host.get("SecurityOpt", []))
        not in (
            {"no-new-privileges"},
            {"no-new-privileges=true"},
            {"no-new-privileges:true"},
        )
    ):
        raise ValueError("non-root capability boundary required")
    if (
        host.get("Memory") != 402653184
        or host.get("NanoCpus") != 1000000000
        or host.get("PidsLimit") != 128
        or set(host.get("Tmpfs", {})) != {"/var/lib/postgresql", "/var/run/postgresql"}
    ):
        raise ValueError("bounded disposable resources required")
    if (
        item["Name"] != "/" + name
        or item["Config"]["Labels"].get("recovery.lab.run") != run_id
        or item["Config"]["Image"] != image
    ):
        raise ValueError("container ownership mismatch")
    if (
        host["NetworkMode"] != "none"
        or host["Privileged"] is not False
        or host["ReadonlyRootfs"] is not True
        or host.get("PortBindings")
    ):
        raise ValueError("container isolation mismatch")
    if any(mount["Type"] != "tmpfs" for mount in item["Mounts"]):
        raise ValueError("persistent or host mount forbidden")


class Postgres:
    """Fixed local Linux Docker socket and three tracked names; no compose context, host data mount or network exposure."""

    def __init__(self, root: Path) -> None:
        """Require explicit Linux local daemon and an immutable official image; passwords are fresh synthetic env-file data."""
        if platform.system() != "Linux":
            raise ValueError("dedicated Linux Docker host required")
        self.root = root
        self.run_id = secrets.token_hex(8)
        self.prefix = "dr-lab-" + self.run_id
        self.image = json.loads((ROOT / "tools.lock.json").read_text(encoding="utf-8"))[
            "postgres_image"
        ]
        if not re.fullmatch(r"postgres:18-alpine@sha256:[0-9a-f]{64}", self.image):
            raise ValueError("pinned official PostgreSQL image required")
        self.binary = shutil.which("docker")
        if self.binary is None:
            raise ValueError("Docker CLI required")
        self.names: list[str] = []
        self.environment = {
            key: value
            for key, value in os.environ.items()
            if key not in {"DOCKER_HOST", "DOCKER_CONTEXT"}
        }
        self.env_file = root / "postgres.env"
        private_file(
            self.env_file,
            (
                "POSTGRES_USER=postgres\nPOSTGRES_DB=drill\nPOSTGRES_PASSWORD="
                + secrets.token_urlsafe(48)
                + "\n"
            ).encode(),
        )
        if self.run(["info", "--format", "{{.OSType}}"]).stdout.strip() != b"linux":
            raise ValueError("local Linux Docker engine required")

    def command(self, args: list[str]) -> list[str]:
        """Force the local socket on every call; inherited default/user Docker contexts are not used."""
        if self.binary is None:
            raise ValueError("Docker CLI missing")
        return [self.binary, "--host", "unix:///var/run/docker.sock", *args]

    def run(
        self, args: list[str], data: bytes | None = None, *, allow_failure: bool = False
    ) -> subprocess.CompletedProcess[bytes]:
        """Execute only program-authored argument arrays with a deadline; never expose stderr/credentials in public diagnostics."""
        result = subprocess.run(
            self.command(args),
            input=data,
            capture_output=True,
            env=self.environment,
            timeout=90,
            check=False,
        )
        if result.returncode and not allow_failure:
            raise ValueError("owned PostgreSQL operation failed")
        return result

    def inspect(self, name: str) -> dict[str, Any]:
        """Validate tracked ownership and fixed isolation before returning a private inspection record."""
        if name not in self.names:
            raise ValueError("untracked container")
        value = decode(self.run(["inspect", name]).stdout)
        inspect_guard(value, name, self.run_id, self.image)
        return value[0]  # type: ignore[no-any-return]

    def start(self, role: str) -> str:
        """Create a unique non-root, no-network, read-only container with bounded tmpfs; never reuse an existing name."""
        if role not in {"source", "restore-a", "restore-b"}:
            raise ValueError("owned role required")
        name = self.prefix + "-" + role
        if name in self.names:
            raise ValueError("name already used")
        existing = self.run(["inspect", name], allow_failure=True)
        if existing.returncode != 1 or b"no such object" not in existing.stderr.lower():
            raise ValueError("new unique container required")
        # Track before creation so partial creation is safely accounted for in cleanup.
        self.names.append(name)
        self.run(
            [
                "run",
                "--detach",
                "--name",
                name,
                "--label",
                "recovery.lab.run=" + self.run_id,
                "--network",
                "none",
                "--user",
                "postgres",
                "--read-only",
                "--cap-drop",
                "ALL",
                "--security-opt",
                "no-new-privileges=true",
                "--memory",
                "384m",
                "--cpus",
                "1",
                "--pids-limit",
                "128",
                "--tmpfs",
                "/var/lib/postgresql:rw,nosuid,noexec,size=128m,mode=1777",
                "--tmpfs",
                "/var/run/postgresql:rw,nosuid,noexec,size=16m,mode=1777",
                "--env-file",
                str(self.env_file),
                self.image,
                "postgres",
                "-c",
                "track_commit_timestamp=on",
            ]
        )
        deadline = time.monotonic() + 60
        while time.monotonic() < deadline:
            item = self.inspect(name)
            if not item["State"]["Running"]:
                raise ValueError("owned PostgreSQL did not start")
            ready = self.run(
                [
                    "exec",
                    "--user",
                    "postgres",
                    name,
                    "pg_isready",
                    "--username",
                    "postgres",
                    "--dbname",
                    "drill",
                ],
                allow_failure=True,
            )
            if ready.returncode == 0:
                process = self.run(
                    ["exec", "--user", "postgres", name, "cat", "/proc/1/comm"],
                    allow_failure=True,
                )
                if process.returncode == 0 and process.stdout.strip() == b"postgres":
                    configured = self.sql(
                        name,
                        b"SELECT current_database(), current_setting('track_commit_timestamp');",
                    )
                    if configured.strip() != b"drill|on":
                        raise ValueError("final database configuration mismatch")
                    return name
            time.sleep(0.5)
        raise ValueError("owned PostgreSQL readiness deadline")

    def sql(
        self, name: str, content: bytes, *, reject_state: str | None = None
    ) -> bytes:
        """Execute only reviewed fixture SQL on a guarded owned database; negative cases require an exact SQLSTATE."""
        self.inspect(name)
        args = [
            "exec",
            "--user",
            "postgres",
            "-i",
            name,
            "psql",
            "--username",
            "postgres",
            "--dbname",
            "drill",
            "--no-psqlrc",
            "--tuples-only",
            "--no-align",
            "--set",
            "ON_ERROR_STOP=1",
            "--set",
            "VERBOSITY=sqlstate",
        ]
        result = self.run(args, content, allow_failure=reject_state is not None)
        if reject_state is not None and (
            result.returncode == 0
            or ("ERROR:  " + reject_state).encode() not in result.stderr
            and ("ERROR: " + reject_state).encode() not in result.stderr
        ):
            raise ValueError("specific constraint rejection missing")
        return result.stdout

    def fixture(self, name: str, filename: str) -> None:
        """Run one program-selected tracked SQL fixture, not an uploaded or untrusted dump."""
        if filename not in {"schema.sql", "seed.sql", "after_snapshot.sql"}:
            raise ValueError("known fixture required")
        self.sql(name, (ROOT / "sql" / filename).read_bytes())

    def capture(self, name: str) -> dict[str, Any]:
        """Read a bounded JSON relational inventory and independently validate its complete ledger."""
        value = decode(self.sql(name, (ROOT / "sql/capture.sql").read_bytes()))
        dataset(value)
        return value  # type: ignore[no-any-return]

    def dump(self, name: str) -> Path:
        """Stream pg_dump's consistent custom archive into a new private file; source is settled, no copied live data directory."""
        self.inspect(name)
        target = self.root / "ledger.dump"
        descriptor = os.open(target, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600)
        with os.fdopen(descriptor, "wb") as output:
            result = subprocess.run(
                self.command(
                    [
                        "exec",
                        "--user",
                        "postgres",
                        name,
                        "pg_dump",
                        "--username",
                        "postgres",
                        "--dbname",
                        "drill",
                        "--format",
                        "custom",
                        "--no-owner",
                        "--no-acl",
                    ]
                ),
                stdout=output,
                stderr=subprocess.PIPE,
                env=self.environment,
                timeout=60,
                check=False,
            )
        if result.returncode or not 5 <= target.stat().st_size <= 64 * 1024 * 1024:
            raise ValueError("consistent dump failed")
        with target.open("rb") as content:
            if content.read(5) != b"PGDMP":
                raise ValueError("custom archive missing")
        return target

    def restore(self, name: str, archive: Path) -> None:
        """Restore only this drill's verified dump into a new empty owned DB in one transaction; not arbitrary SQL ingestion."""
        self.inspect(name)
        with archive.open("rb") as source:
            result = subprocess.run(
                self.command(
                    [
                        "exec",
                        "--user",
                        "postgres",
                        "-i",
                        name,
                        "pg_restore",
                        "--username",
                        "postgres",
                        "--dbname",
                        "drill",
                        "--single-transaction",
                        "--exit-on-error",
                        "--no-owner",
                        "--no-acl",
                    ]
                ),
                stdin=source,
                capture_output=True,
                env=self.environment,
                timeout=60,
                check=False,
            )
        if result.returncode:
            raise ValueError("transactional restore failed")

    def constraints(self, name: str, baseline: dict[str, Any]) -> None:
        """Verify real restored PK/FK/CHECK failures by SQLSTATE and prove negative attempts changed no data."""
        self.sql(
            name,
            b"INSERT INTO customers VALUES (1, 'duplicate');",
            reject_state="23505",
        )
        self.sql(
            name,
            b"INSERT INTO orders (order_id,customer_id,total_cents) VALUES (999,999,3000);",
            reject_state="23503",
        )
        self.sql(name, b"INSERT INTO payments VALUES (1,-1);", reject_state="23514")
        if (
            dataset(self.capture(name))["fingerprint"]
            != dataset(baseline)["fingerprint"]
        ):
            raise ValueError("constraint tests changed restored data")

    def stop(self, name: str) -> None:
        """Simulate loss of the owned source and verify actual stopped state; no production resource can be selected."""
        self.inspect(name)
        self.run(["stop", "--time", "10", name])
        if self.inspect(name)["State"]["Running"] is not False:
            raise ValueError("source still running")

    def close(self) -> int:
        """Remove only labeled names created by this run; refuse ambiguous/unowned resources and verify their absence."""
        removed = 0
        for name in reversed(self.names):
            current = self.run(["inspect", name], allow_failure=True)
            if current.returncode == 1 and b"no such object" in current.stderr.lower():
                continue
            inspect_guard(decode(current.stdout), name, self.run_id, self.image)
            self.run(["rm", "--force", name])
            after = self.run(["inspect", name], allow_failure=True)
            if after.returncode != 1 or b"no such object" not in after.stderr.lower():
                raise ValueError("owned cleanup not confirmed")
            removed += 1
        self.names.clear()
        return removed


def execute(root: Path) -> dict[str, Any]:
    """Measure encrypted snapshot, observed five-order loss, verified isolated recovery and cleanup on a dedicated Linux runner."""
    measurements = Measurements()
    database = Postgres(root)
    stage = "isolation"
    try:
        started = time.monotonic()
        source = database.start("source")
        measurements.check(
            "isolation",
            started,
            {
                "network": "none",
                "ports_published": False,
                "non_root": True,
                "read_only_root": True,
                "storage": "bounded-tmpfs",
            },
        )
        stage = "consistent_dump"
        started = time.monotonic()
        database.fixture(source, "schema.sql")
        database.fixture(source, "seed.sql")
        baseline = database.capture(source)
        if dataset(baseline)["orders"] != 40:
            raise ValueError("settled source count invalid")
        dump = database.dump(source)
        if database.capture(source) != baseline:
            raise ValueError("settled source changed during dump")
        measurements.check(
            stage,
            started,
            {"orders": 40, "settled_source": True, "format": "pg_dump-custom"},
        )
        stage = "encrypted_backup"
        started = time.monotonic()
        backup = Restic(root)
        snapshot = backup.backup(dump)
        measurements.check(
            stage, started, {"full_data_check": True, "engine": "restic"}
        )
        stage = "wrong_password"
        started = time.monotonic()
        backup.reject_password()
        measurements.check(stage, started, {"specifically_rejected": True})
        stage = "corrupt_pack"
        started = time.monotonic()
        backup.reject_corruption()
        measurements.check(
            stage, started, {"changed_byte_verified": True, "integrity_rejected": True}
        )
        database.fixture(source, "after_snapshot.sql")
        head = database.capture(source)
        if dataset(head)["orders"] != 45:
            raise ValueError("post-snapshot commits not observed")
        stage = "source_loss"
        recovery_started = time.monotonic()
        database.stop(source)
        measurements.check(
            stage,
            recovery_started,
            {"source_running": False, "head_orders": 45, "backed_up_orders": 40},
        )
        stage = "isolated_restore"
        started = time.monotonic()
        recovered_dump = backup.restore(snapshot, "restored")
        if sha256(recovered_dump) != sha256(dump):
            raise ValueError("restored archive differs")
        restored = database.start("restore-a")
        database.restore(restored, recovered_dump)
        recovered = database.capture(restored)
        if dataset(recovered)["fingerprint"] != dataset(baseline)["fingerprint"]:
            raise ValueError("whole restored ledger differs")
        measurements.check(
            stage,
            started,
            {
                "exact_dump_hash": True,
                "matching_ledger": True,
                "orders": 40,
                "single_transaction": True,
            },
        )
        stage = "constraints"
        started = time.monotonic()
        database.constraints(restored, recovered)
        measurements.check(
            stage,
            started,
            {"specific_sqlstate_checks": 3, "negative_writes_unchanged": True},
        )
        elapsed = int((time.monotonic() - recovery_started) * 1000)
        stage = "objectives"
        started = time.monotonic()
        result = evaluate(
            baseline,
            head,
            recovered,
            elapsed,
            {"rto_ms": 180_000, "rpo_ms": 60_000, "max_lost_orders": 5},
        )
        if result["result"] != "PASS" or result["lost_orders"] != 5:
            raise ValueError("explicit recovery objectives unmet")
        measurements.check(
            stage, started, {"rto_met": True, "rpo_met": True, "loss_reported": 5}
        )
        stage = "strict_objective_rejection"
        started = time.monotonic()
        strict = evaluate(
            baseline,
            head,
            recovered,
            elapsed,
            {"rto_ms": 1, "rpo_ms": 0, "max_lost_orders": 0},
        )
        if strict["result"] != "FAIL":
            raise ValueError("unmet objective was hidden")
        measurements.check(stage, started, {"zero_loss_requirement_rejected": True})
        stage = "repeat_restore"
        started = time.monotonic()
        repeated_dump = backup.restore(snapshot, "repeat-restored")
        if sha256(repeated_dump) != sha256(dump):
            raise ValueError("repeat archive mismatch")
        repeated = database.start("restore-b")
        database.restore(repeated, repeated_dump)
        if (
            dataset(database.capture(repeated))["fingerprint"]
            != dataset(baseline)["fingerprint"]
        ):
            raise ValueError("repeat ledger mismatch")
        measurements.check(
            stage, started, {"second_empty_environment": True, "matching_ledger": True}
        )
        stage = "owned_cleanup"
        started = time.monotonic()
        removed = database.close()
        if removed != 3:
            raise ValueError("owned cleanup count invalid")
        measurements.check(
            stage, started, {"containers_removed": 3, "absence_verified": True}
        )
        report = measurements.report("postgres", snapshot, dump, result)
        publish(report, root / "report")
        return report
    except Exception:
        print(
            json.dumps(
                {
                    "failed_stage": stage,
                    "error": "owned PostgreSQL drill failed; no raw logs or credentials published",
                }
            )
        )
        raise
    finally:
        database.close()


def main() -> int:
    """Require an acknowledged new disposable Linux workspace; refuse local Windows Docker and all production inputs."""
    parser = argparse.ArgumentParser(
        description="PostgreSQL recovery drill — Jason Stys"
    )
    parser.add_argument("--output", required=True, type=Path)
    parser.add_argument("--ack-disposable-docker", action="store_true")
    args = parser.parse_args()
    if not args.ack_disposable_docker or platform.system() != "Linux":
        parser.error("explicit dedicated Linux Docker acknowledgement required")
    try:
        print(json.dumps(execute(workspace(args.output)), sort_keys=True))
        return 0
    except (ValueError, OSError, subprocess.SubprocessError):
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
