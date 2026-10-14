# Measured validation and author review

## Actions archive and follow-up audit (2026-10-14 UTC)

Remote main `f931e06604fc0a145a9790f91705dc09126312c8` was checked again: Validate and CodeQL succeeded, all seven jobs passed, and the open code-scanning alert count was zero. The archived failed run had native disposable-copy permission and upstream unused-helper advisory failures, already corrected in the accepted source. Its saved logs contained no artifact-storage error markers. No test or security gate was weakened, and no unnecessary runtime change was made.

At Jason's explicit request, obtainable old run logs, all attempt/job results and artifacts were saved privately with SHA-256/ZIP integrity checks before eligible old runs were removed online. Historical Actions links below may therefore no longer resolve; the immutable source commits and selected synthetic reports remain available. The local `GitHub-Actions-Archive/2026-10-14-pass-1` archive contains readable results and exact availability/deletion records. It is not published because full logs can contain private information. Current [Actions](https://github.com/JasonStys/disaster-recovery-drill-lab/actions) and README badges show live checks; this documentation update must pass the same full workflows. Newest workflow runs and active runs remain protected; this repo still uploads no Actions artifacts or caches.

Author: Jason Stys. Native Windows and actual hosted Linux/Windows/Intel macOS validation on 2026-10-14 UTC: **79 tests pass in each lane**, with **98.14% combined statement/branch coverage** of authored dr/ modules, no skips or exclusions. Strict Ruff/mypy, maintained source maps/file inventory and full hash-locked development advisory audit pass. Helpers/Docker orchestration are separately integration-tested and are not included in that coverage percentage.

## Immutable executable-source acceptance

Source [d739fd1d9857408831b85d60b5c7390f17a79e77](https://github.com/JasonStys/disaster-recovery-drill-lab/commit/d739fd1d9857408831b85d60b5c7390f17a79e77) passed all six jobs in [Validate run 38499688607](https://github.com/JasonStys/disaster-recovery-drill-lab/actions/runs/38499688607), completed 2026-10-14T02:12:17Z. Ubuntu3.12/3.14, Windows3.14 and Intel macOS3.14 independently ran the native restic tests and standalone committed-source CLI exercise. Security passed Gitleaks full history, complete development advisory audit, actionlint and ShellCheck.

[CodeQL run 38499688633](https://github.com/JasonStys/disaster-recovery-drill-lab/actions/runs/38499688633) passed security-extended Python analysis, completed 2026-10-14T02:11:55Z; the open-alert API returned zero at 2026-10-14T02:14:07Z. [ci.json](ci.json) records this immutable runtime-source snapshot. Report-only follow-ups must pass the same seven checks before final handoff; current Actions/badges show main. No self-referential commit hash or undocumented production approval is fabricated.

## Actual native backup measurements

[native.json](native.json) and its generated [inert HTML](native.html) contain the actual Windows committed-source exercise, not fake test fixtures. Five cases passed: real restic encryption/full data check (4,334ms), specific wrong-key rejection (504ms), exact missing-snapshot rejection (699ms), verified changed-pack rejection (966ms), and verified exact-byte restoration (718ms). The original repository and permissions remain untouched; only the disposable corruption copy is changed. Native file recovery does NOT imply a database RTO/RPO result.

The measured [benchmark](benchmark.json) records five warmed batches of 100 actual independent ledger/objective evaluations: median 0.486ms/evaluation, peak Python allocation 12,639 bytes on Windows/Python3.14.6. Baseline/head contain two/three orders. An independent one-lost-order/400ms oracle is asserted. This is informational, excludes restic/PostgreSQL/containers and is not a production throughput or comparative optimization claim.

## Actual PostgreSQL measurements

[postgres.json](postgres.json) is extracted from the completed Linux PostgreSQL job; [postgres.html](postgres.html) is generated from that validated aggregate. A 40-order snapshot was restored after the source had 45 committed orders and was stopped.

- Whole recovered ledger exactly matches the original snapshot: 40 orders, consistent customers, line totals and payments.
- **Observed RTO: 2,419ms** from source-stop initiation through decrypted-file, restored database/data and real constraint validation.
- **Observed RPO window: 6,291ms**, using persisted original PostgreSQL business-transaction commit timestamps.
- **Five committed orders are deliberately lost.** This meets the configured demonstration limits (180s/60s/five), not a universal business requirement. The explicit stricter 1ms/zero-time/zero-order test returned FAIL.
- Actual PK/FK/CHECK negatives produced their specific SQLSTATE rejections and left data unchanged. A second separate empty database restored the same exact snapshot.
- Only the three owned non-root/no-network/tmpfs containers were removed; their absence was verified.

| Case | Actual duration ms |
| --- | --- |
| isolation | 1,354 |
| consistent dump | 307 |
| encrypted backup | 4,877 |
| wrong password | 471 |
| corrupt pack | 690 |
| source loss | 96 |
| isolated restore | 2,124 |
| constraints | 198 |
| objectives | 1 |
| strict objective rejection | 1 |
| repeat restore | 2,138 |
| owned cleanup | 207 |

Actual derived image configuration digest: `sha256:4489db8abd200de282e3b1ccd720c1a6c05dbecf490a3d61d88904f399db2dc4`. It uses the verified official base and removes the unused root-only gosu component. The full actual-image HIGH/CRITICAL scan detected Alpine3.24.2, checked 53 OS packages, and returned zero such findings. No language-specific files remained. This is not a complete PostgreSQL/cryptographic source audit or proof against future vulnerabilities. The image digest is a local build fingerprint, not an OCI signature.

## Author-led review and release checklist

Architecture/testing/security review shaped bounded data, append-only time semantics, independent money/content validation, exact snapshots, ownership/resource/context guards and failure-specific oracles. Performance review covers set/dictionary joins O(n), canonical ordering O(n log n), bounded rows/trees/files and process/resource deadlines. No independent audit or certification is claimed.

- [x] Portable native tests/type/lint and actual encrypted-file exercise.
- [x] Actual logical dump, source loss, two isolated transactional restores, schema negatives and recovery objectives.
- [x] Dependency/image/secrets/workflow/CodeQL gates without suppression.
- [x] New-output/ownership/privacy contracts, documented cleanup/recovery limits and selected measured reports.
- Final-main acceptance rule: verify the exact report-only main commit through these same hosted gates before handoff; the immutable runtime evidence above is not presented as a self-referential final commit hash.
- Production deployment, migrations, hosted identities and production on-call approval: not applicable; no such actions are authorized or performed.

## Development failures retained and corrected

- Native development initially expected a short-ID diagnostic for a missing full snapshot. The exact absent full ID now requires snapshot-load ENOENT, not arbitrary failure.
- Review found backdated new order times could look like zero-time loss. Append-only new timestamps must advance; a regression rejects backdated data.
- Final PostgreSQL PID1/database/commit-tracking checks avoid accepting the temporary initdb server.
- Persisted original business commit timestamps prevent restore xmin from being mistaken for original transaction time.
- [Initial run 38499138631](https://github.com/JasonStys/disaster-recovery-drill-lab/actions/runs/38499138631) caught POSIX read-only packs in the disposable corruption copy. Only that new copy gets write permission for byte injection; original permissions stay intact.
- That run found 24 HIGH/one CRITICAL Go-library advisories in upstream gosu (OS findings zero). Upstream entrypoint uses gosu only for root startup. This enforced non-root-only image removes the unused component, and the actual result passes the full scan. No findings were ignored and no gate was removed.

At initial acceptance no failed runs had been deleted. Later user-authorized storage cleanup archived historical failures before removing eligible old runs, as disclosed above. No local Docker repair, production data access, paid deployment or user credentials were used. No backups/passwords/Actions artifacts/caches are uploaded. Private synthetic working copies and encryption keys remain ignored local/ephemeral data, not blanket disk encryption. Logical snapshots do not implement WAL/PITR, roles/global-state, offsite storage, application cutover or a production loss SLA; documented gaps remain explicit.
