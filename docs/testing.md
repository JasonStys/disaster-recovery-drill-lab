# Risk-based test strategy

Author: Jason Stys. All fixtures are fictional; fabricated report inputs are clearly test-only.

| Boundary/risk | Test and independent oracle |
| --- | --- |
| Ambiguous/malicious JSON | Duplicate/type/NaN/UTF8/byte/node/depth/ordinary-file boundaries |
| Wrong database content | Independent key/FK/money checks and canonical whole-ledger fingerprint; valid-but-wrong restore fails |
| Hidden loss or changed budgets | Explicit lost-ID count, timestamp window, append-only/backdate rejection and arithmetic property oracle |
| Encryption/integrity not actually exercised | Native official restic init/backup/full check/wrong-key/missing-ID/changed-pack/verified restore on every OS lane |
| Generic error counted as security proof | Failure-specific negatives reject unrelated command failure |
| Host/other project damaged | Fabricated ownership/isolation guard mutations; actual unique-resource inspect and verified cleanup on Linux CI |
| pg_dump/pg_restore false success | Real PostgreSQL source, controlled committed writes after snapshot, stopped source, two empty restore environments |
| Lost schema enforcement | Real restored PK/FK/CHECK SQLSTATE checks and unchanged data afterward |
| Privacy/report injection | Complete-suite/closed fields/false success rejection, inert escaped HTML and no overwrite |
| Supply chain/CI | Hash-locked dev audit, pinned tools/image/Actions, image HIGH/CRITICAL scan, full-history Gitleaks, actionlint/ShellCheck and CodeQL |

Four Python lanes: Linux3.12/3.14, Windows3.14, Intel macOS3.14. Each installs the reviewed native restic binary, runs unit/property and a real encrypted-file test, then a standalone CLI measured exercise. No tests are platform-skipped. Actual PostgreSQL runs only on ephemeral Linux CI; no local Docker repair/start.

Strict mypy covers dr/; Ruff covers dr/scripts/tests. Combined statement/branch coverage target ≥90% applies to dr/ only, no exclusions. Helpers and Docker orchestration are separately integration-tested, not included in that percentage. A count/coverage figure is not a complete code-path, cryptographic or adversarial sandbox audit.

Generated source line maps and exhaustive README inventory must remain current. SQL/YAML/Bash headers map their symbols. Benchmark runs five warmed batches of 100 actual evaluations with known correctness, reports allocation/time and imposes no machine-dependent performance threshold.

Gaps: production-scale throughput, concurrent writers, physical WAL/PITR, dirty/custom schemas, roles/global metadata, untrusted dumps, offsite/ransomware storage, disaster detection/routing, end-user identity/privacy enforcement, Windows/ARM database hosts, independently authenticated evidence. Do not infer these from green CI. Retain and explain failures; never suppress advisories or remove gates to claim success.
