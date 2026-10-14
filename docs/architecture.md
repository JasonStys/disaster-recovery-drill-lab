# ADR-001: observed, isolated logical-snapshot recovery

Status: Accepted. Date: 2026-10-13. Author/decider: Jason Stys.

## Context and constraints

Add distinct disaster recovery, SQL and operational-security evidence to a portfolio. Requirements: genuine encrypted backup/restore, explicit objectives/loss, independent database consistency, repeated recovery, clear documentation and portable native tests. No production access, paid host, local Docker repair, user files or artifacts/caches. One fictional bounded ledger; PostgreSQL execution only on a dedicated ephemeral Linux runner.

## Decision and flow

```text
SQL fixture → settled PostgreSQL source → pg_dump custom archive → encrypted restic snapshot
                  ↓ 5 later committed orders                      ↓ exact snapshot ID
             source stopped                              verified decrypt/restore
                                                               ↓
                                                  empty isolated PostgreSQL destination
                                                               ↓
                                               keys/money/content/constraint verification
                                                               ↓
                                               measured RTO + explicit RPO/order loss
                                                               ↓
                                                canonical JSON + escaped offline HTML
```

Python supplies portable process/file ownership, bounded JSON validation, independent relational/money logic and evidence. SQL supplies native transactions and real PK/FK/CHECK enforcement. Bash runs fail-fast CI. Native HTML is escaped and network-inert; a framework/server is unnecessary.

## Options considered and trade-offs

- Logical pg_dump + restic (chosen): compact, actual PostgreSQL-aware consistent archive, straightforward isolated replay, proven encrypted-storage component. Does not provide WAL/PITR, role/global-state or whole-host recovery.
- Physical base backup + archived WAL: suitable future PITR exercise, more coverage but substantially more storage/cluster state/retention and timeline semantics. Not silently simulated here.
- Custom encryption: rejected; introduces avoidable cryptographic correctness/key-management risk.
- Mock database-only recovery: useful unit fixtures but cannot demonstrate real constraints, pg_restore or data-loss timing. Not accepted as live evidence.
- Hosted backup service/public dashboard: unnecessary account/cost/privacy surface for the portfolio learning goal.

## Contracts, performance and reliability

Four tables, integer money, bounded rows. Relational checks use dictionary/set joins O(n); canonical ordering is O(n log n) and O(n) memory. Three ledgers are independently checked; fingerprints are insensitive to row order, not to values. Semantically incorrect restores cannot pass by having good timing.

The source is deliberately settled before dump; this is not a concurrent-write benchmark. PostgreSQL commit tracking is enabled at startup. Immediately after each business transaction, its original xmin commit timestamp is persisted into the ledger before capture/dump. Restored rows keep those timestamps rather than using the restore transaction's new xmin. All source/head differences are append-only; backdated new timestamps fail.

Process deadlines, fresh outputs, verified owned resources and finite storage/CPU/memory keep the exercise bounded. Initial image download is outside RTO, as are human detection/application failover. Default objective limits are lab parameters, not recommendations for all businesses.

## Consequences and future decisions

Native encrypted-file tests run on reviewed amd64 Windows/Linux/macOS, with database evidence only from Linux CI. Selected measured evidence is published; private synthetic outputs remain local/ephemeral. Admin/daemon/toolchain are trusted; no certified sandbox or independent audit claim.

Revisit physical PITR, ongoing load, independently signed evidence, off-site/immutable storage, escrow/rotation, HA/multi-region failover, application cutover and production restore permissions in separate authorized designs. No production action is implied by this ADR.
