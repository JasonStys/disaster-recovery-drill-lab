# Disaster Recovery Drill Lab

[![Validate](https://github.com/JasonStys/disaster-recovery-drill-lab/actions/workflows/ci.yml/badge.svg)](https://github.com/JasonStys/disaster-recovery-drill-lab/actions/workflows/ci.yml)
[![CodeQL](https://github.com/JasonStys/disaster-recovery-drill-lab/actions/workflows/codeql.yml/badge.svg)](https://github.com/JasonStys/disaster-recovery-drill-lab/actions/workflows/codeql.yml)

A runnable encrypted-backup and isolated PostgreSQL recovery lab. Created by **[Jason Stys](https://github.com/JasonStys)** · [Professional contact](https://www.linkedin.com/in/jason-stys-31b30b351/).

## What it demonstrates

- **Real encrypted backups:** hash-verified official restic, exact immutable snapshot IDs, full data integrity checks, verified restore, wrong-password and changed-pack rejection. No invented cryptography.
- **Real database recovery:** PostgreSQL custom logical dump, an empty isolated destination, single-transaction restore and independently checked customer/order/line/payment consistency. A second empty destination proves repeatability.
- **Honest objectives:** preserve actual original business-transaction commit timestamps before backup. After a 40-order snapshot, five additional committed orders are intentionally absent on recovery. Report their count and measured timestamp window, not a claim of zero loss. Stricter zero-loss/time budgets must fail.
- **Safe lab boundaries:** uniquely labeled non-root containers, no network or published ports, read-only roots, dropped capabilities, bounded temporary storage/CPU/memory, guarded ownership checks and verified exact-name cleanup.
- **Readable, tested evidence:** closed input contracts, meaningful negative/property cases, strict types/lint, measured benchmarks, escaped offline HTML/JSON, maintained source symbol/line maps, runbooks and storage-free CI.

This is an **educational synthetic logical-snapshot lab**, not a production backup service, WAL/PITR implementation, compliance certification, zero-loss guarantee or general-purpose untrusted-dump importer. Only the reviewed fictional schema is supported. Docker/host administrators remain trusted.

## First success in a few minutes (no Docker)

Python 3.12+ and Git are required. On Windows, from the committed repository root:

```powershell
python -m venv .venv
.venv/Scripts/python -m pip install --require-hashes -r requirements-dev.lock
.venv/Scripts/python scripts/bootstrap.py
.venv/Scripts/python -m dr evaluate examples/objective-evaluation.json
.venv/Scripts/python -m pytest --cov --cov-report=term-missing
.venv/Scripts/python scripts/native_drill.py --output out/my-first-backup
```

The offline example is deliberately fabricated, labeled in its [file guide](#every-tracked-file), and checks a one-order/400ms loss window. It is not a measured database restore. The native drill actually encrypts/checks/restores a generated file and rejects wrong passwords, missing snapshots and corrupted packs. Open `out/my-first-backup/report/drill.html` locally. No real files, user credentials, Docker Desktop or system settings are used.

On Linux/macOS replace `.venv/Scripts/python` with `.venv/bin/python`. Native restic installation is reviewed for Windows/Linux/macOS **amd64**, including Intel macOS CI; ARM and other platforms are not claimed tested. All output names must be new lowercase direct children of `out/`.

## Actual PostgreSQL disaster drill

Use the `postgres` job in [Actions](https://github.com/JasonStys/disaster-recovery-drill-lab/actions), or a **dedicated Linux amd64 Docker host**:

```bash
python scripts/bootstrap.py
python scripts/scanners.py trivy
python scripts/image_check.py
python scripts/postgres_drill.py --output out/my-first-database --ack-disposable-docker
```

The script forces the local Docker socket and creates only its own three random labeled containers. It never opens a host database port, mounts host data or targets an existing database. Docker Desktop is neither started nor repaired by native validation. The source is stopped to simulate its loss; two independent empty destinations verify recovery. Cleanup removes only proven owned resources.

The database image is built from an official digest-pinned PostgreSQL base, removing the unused vulnerable gosu root-switch helper and setting the default user to postgres. Root startup is intentionally unsupported. CI scans the actual derived image configuration digest for HIGH/CRITICAL findings before use; the drill requires a current-source scan receipt and records that digest. Plaintext dump/password/env files exist **only** inside the ignored private synthetic workspace; the restic repository is encrypted. Published reports contain selected hashes, durations, counts and booleans—not passwords, full container inspection, raw records or file paths. This is not protection against a local administrator.

RTO measures source-stop initiation through restored database/data/constraint validation; backup creation, image download, human detection, DNS, application cutover and repeatability testing are outside that interval. RPO is the latest original committed business-order time at source minus the latest recovered one, with explicit lost-order count. Defaults: RTO ≤180s, RPO ≤60s, at most five lost orders. Meeting those **lab objectives** does not make five lost orders acceptable for a real business. See [contracts](docs/contracts.md).

## Help, design and verification

[Architecture/ADR](docs/architecture.md) · [operating/recovery runbook](docs/runbook.md) · [contracts](docs/contracts.md) · [test strategy](docs/testing.md) · [measured validation](docs/reports/validation.md) · [security boundary](SECURITY.md) · [primary research](docs/research.md).

Architecture/testing/review guidance shaped the exact ownership guards, independent money oracle, failure-specific checks and explicit measurement boundaries. Each authored code file has a purpose and generated current symbol/parameter/variable line map. Functions/classes explain their contracts; JSON keeps its native format and is described below.

CLI help: `python -m dr --help`, `python scripts/native_drill.py --help`, `python scripts/postgres_drill.py --help`. Offline evaluation exits PASS=0, unmet objective=1, malformed input=2. Reports require complete distinct PASS suites and refuse existing output directories. Read [contributing](CONTRIBUTING.md) before changing parameters or claiming new measurements.

## Every tracked file

<!-- BEGIN FILE GUIDE -->

| File | Purpose |
| --- | --- |
| [.dockerignore](.dockerignore) | Excludes every project file except Dockerfile from the derived-image context. |
| [.gitattributes](.gitattributes) | Portable LF text handling. |
| [.github/workflows/ci.yml](.github/workflows/ci.yml) | Jason Stys: portable native encryption tests, real isolated PostgreSQL recovery and security; no artifacts/caches. |
| [.github/workflows/codeql.yml](.github/workflows/codeql.yml) | Jason Stys: security-extended Python analysis with scoped upload permissions and no database archive upload. |
| [.gitignore](.gitignore) | Excludes tools, runtime backups, passwords, caches and private drill outputs. |
| [CONTRIBUTING.md](CONTRIBUTING.md) | Contribution and coding conventions. |
| [Dockerfile](Dockerfile) | Jason Stys: derived non-root-only PostgreSQL lab image; remove unused vulnerable root-switch helper. |
| [LICENSE](LICENSE) | MIT license for authored code. |
| [README.md](README.md) | Disaster Recovery Drill Lab. |
| [SECURITY.md](SECURITY.md) | Security boundary and reporting. |
| [docs/architecture.md](docs/architecture.md) | ADR-001: observed, isolated logical-snapshot recovery. |
| [docs/contracts.md](docs/contracts.md) | Input, backup and recovery contracts. |
| [docs/reports/benchmark.json](docs/reports/benchmark.json) | Measured independent consistency/objective evaluation benchmark. |
| [docs/reports/ci.json](docs/reports/ci.json) | Immutable executable-source CI snapshot with actual completed checks. |
| [docs/reports/native.html](docs/reports/native.html) | Escaped inert HTML rendering of native measured results. |
| [docs/reports/native.json](docs/reports/native.json) | Measured native restic encryption/integrity/restore exercise. |
| [docs/reports/portfolio-sync-2026-10-22.md](docs/reports/portfolio-sync-2026-10-22.md) | <!-- File: docs/reports/portfolio-sync-2026-10-22.md; Purpose: certificate-bundle security repair and evidence by Jason Stys. -->. |
| [docs/reports/postgres.html](docs/reports/postgres.html) | Escaped inert HTML rendering of actual PostgreSQL results. |
| [docs/reports/postgres.json](docs/reports/postgres.json) | Actual isolated PostgreSQL restore and objective measurements. |
| [docs/reports/validation.md](docs/reports/validation.md) | Measured validation and author review. |
| [docs/research.md](docs/research.md) | Primary research and design rationale. |
| [docs/runbook.md](docs/runbook.md) | Operating and recovery runbook. |
| [docs/testing.md](docs/testing.md) | Risk-based test strategy. |
| [dr/\_\_init\_\_.py](dr/__init__.py) | Owned synthetic encrypted-backup and recovery evidence tools. Created by Jason Stys. |
| [dr/\_\_main\_\_.py](dr/__main__.py) | Offline JSON evaluation/report CLI; input files are data, never SQL or executable code. Jason Stys. |
| [dr/backup.py](dr/backup.py) | Fixed local restic operations on fresh synthetic workspaces; passwords/output remain private. Jason Stys. |
| [dr/contracts.py](dr/contracts.py) | Bounded strict JSON and ordinary-file contracts; no input becomes a command. Jason Stys. |
| [dr/evidence.py](dr/evidence.py) | Closed synthetic measured recovery reports with escaped, network-inert HTML. Jason Stys. |
| [dr/ledger.py](dr/ledger.py) | Independent relational/financial consistency oracle and snapshot recovery objectives. Jason Stys. |
| [examples/objective-evaluation.json](examples/objective-evaluation.json) | Explicitly synthetic offline ledger and recovery-objective fixture. |
| [pyproject.toml](pyproject.toml) | Strict types, lint, tests and combined statement/branch coverage gate. |
| [requirements-dev.in](requirements-dev.in) | Exact validation dependencies; standard-library application runtime. |
| [requirements-dev.lock](requirements-dev.lock) | Complete hash-pinned validation graph. |
| [scripts/benchmark.py](scripts/benchmark.py) | Informational measured canonical-ledger and recovery-evaluation timing/allocation, with correctness oracle. Jason Stys. |
| [scripts/bootstrap.py](scripts/bootstrap.py) | Install one official hash-pinned native restic binary; no shell installer or archive paths execute. Jason Stys. |
| [scripts/code\_map.py](scripts/code_map.py) | Generate/check exact Python, SQL, shell and YAML symbol positions. Created by Jason Stys. |
| [scripts/file\_guide.py](scripts/file_guide.py) | Generate exhaustive Git-tracked README summaries without including ignored runtime data. Jason Stys. |
| [scripts/image\_check.py](scripts/image_check.py) | Build/scan a non-root-only image from the immutable official PostgreSQL base; do not suppress vulnerabilities. Jason Stys. |
| [scripts/native\_drill.py](scripts/native_drill.py) | Run the actual encrypted synthetic-file exercise without Docker or real user data. Jason Stys. |
| [scripts/postgres\_drill.py](scripts/postgres_drill.py) | Actual isolated PostgreSQL logical-snapshot disaster drill; only uniquely owned synthetic containers. Jason Stys. |
| [scripts/scanners.py](scripts/scanners.py) | Install only hash-pinned official Linux scanner binaries. Created by Jason Stys. |
| [scripts/validate.sh](scripts/validate.sh) | Strict portable tests and maintained documentation/source invariants. Created by Jason Stys. |
| [scripts/validate\_repo.py](scripts/validate_repo.py) | Verify immutable workflow/tool controls and nonsecret tracked files; not a production security assessment. Jason Stys. |
| [sql/after\_snapshot.sql](sql/after_snapshot.sql) | Five committed orders deliberately outside the saved snapshot; loss must be reported. Jason Stys. |
| [sql/capture.sql](sql/capture.sql) | Canonical relational snapshot for independent Python verification; no secrets or real people. Jason Stys. |
| [sql/schema.sql](sql/schema.sql) | Fictional order ledger with database-enforced keys, references and integer-money bounds. Jason Stys. |
| [sql/seed.sql](sql/seed.sql) | One settled transaction before the consistent dump; all data is fictional. Jason Stys. |
| [tests/\_\_init\_\_.py](tests/__init__.py) | Synthetic test fixtures are not the published measured reports. Created by Jason Stys. |
| [tests/conftest.py](tests/conftest.py) | Independent small fictional ledgers and explicitly fake report fixtures for edge-case tests. Jason Stys. |
| [tests/test\_backup.py](tests/test_backup.py) | Real native restic encryption and negative oracles plus exclusive workspace guards. Jason Stys. |
| [tests/test\_contracts.py](tests/test_contracts.py) | Strict JSON, size/depth/shape/type and ordinary-file adversarial boundaries. Jason Stys. |
| [tests/test\_docker\_guards.py](tests/test_docker_guards.py) | Native ownership/isolation regressions use fabricated inspect fixtures; no local Docker call occurs. Jason Stys. |
| [tests/test\_evidence.py](tests/test_evidence.py) | Fabricated report fixtures validate rejection/privacy/escaping, not measured disaster-recovery claims. Jason Stys. |
| [tests/test\_ledger.py](tests/test_ledger.py) | Independent money/key oracles, snapshot equality and recovery-objective boundaries. Jason Stys. |
| [tools.lock.json](tools.lock.json) | Official restic/scanner archive hashes and immutable PostgreSQL image digest. |

<!-- END FILE GUIDE -->
