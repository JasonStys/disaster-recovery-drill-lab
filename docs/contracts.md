# Input, backup and recovery contracts

Author: Jason Stys.

## Offline data

Strict UTF8 JSON ≤1MiB, 50,000 nodes, depth ≤24. Reject duplicates, NaN/infinite values, non-JSON scalars, missing/extra keys. Explicit ordinary leaves only; no symlink/reparse input. Cooperative filesystem parents remain assumed. CLI never executes inputs or echoes malformed content.

Tables: customers [id, printable synthetic label]; orders [id, customer_id, integer total_cents, original commit_ms]; lines [order_id, position, printable sku, quantity, unit_cents]; payments [order_id, integer paid_cents]. Each nonempty table ≤10,000 rows. IDs positive; integer fields reject bool. Money totals equal summed line quantities × integer unit costs and one full payment per order. Keys and references are independently validated.

Snapshot/source/restored are independently valid ledgers. Source must retain all baseline rows and only append; new order commit timestamps must strictly exceed the latest baseline commit. The restored canonical whole-ledger fingerprint must exactly match baseline. General arbitrary deletes/updates/concurrent clocks are not this model.

## Objectives and timing

Explicit rto_ms (1–1,800,000), rpo_ms (0–1,800,000), max_lost_orders (0–10,000). RTO is monotonic measured milliseconds from initiating owned source stop through restored data AND database constraint checks. Does not include backup/key creation, initial image pull, human detection, DNS, app routing or repeatability/cleanup.

RPO is latest source original business-transaction commit_ms minus latest recovered one. PostgreSQL track_commit_timestamp is enabled at startup; after a business transaction commits, its original xmin commit time is saved into orders.committed_at. The subsequent metadata update is not a new business-order event. Restore replays this persisted timestamp; querying restored xmin instead would incorrectly measure the restore transaction. Milliseconds are floored; this is a small controlled append-only exercise, not universal wall-clock/WAL semantics.

Lost orders = source order IDs absent from restored snapshot; financial consistency is checked for recovered records. This does not claim to measure arbitrary data changes/side effects. Default live limits are 180s RTO, 60s RPO and five lost orders. A stricter 1ms/0ms/zero-order check must return FAIL. Objective failure is not malformed input; CLI returns 1 rather than changing configured limits.

## Local workspace and encrypted storage

Only new lowercase named direct children of repo out/; no existing output may be reused. POSIX private directories/files 0700/0600; Windows inherited user ACLs are assumed. Keys/env/dumps are synthetic and ignored; encrypted repository is not the same as encrypting plaintext working copies. No remote backend, ambient RESTIC_* configuration/password command, floating latest selector or real credentials. Full SHA256 snapshot IDs and verified restored archive hashes required. Full restic check --read-data plus restore --verify are mandatory.

Wrong password: specific wrong-key message. Missing snapshot: exact absent full ID, failed snapshot load and OS-specific missing-file error. Corruption: flip a byte in a copy, prove its fingerprint changed and require an integrity-specific failure. Unrelated exits do not pass these checks. The original repository remains intact.

## Docker and publication

Dedicated Linux local socket explicitly on every call, independent of user contexts. New random dr-lab names and ownership labels; same image/non-root/capabilities/resource/isolation guards before exec/stop/removal. No network or ports, writable root, host/persistent mounts. Image digest pinned. Source readiness requires final PostgreSQL PID 1 plus correct database/commit tracking, not temporary initdb server readiness. SQL archives are trusted program-created fixtures only.

Database restore uses one transaction and exit-on-error. Real restored PK/FK/CHECK negatives require SQLSTATE 23505/23503/23514 and unchanged ledger. A second independent empty container restores the same exact snapshot. Cleanup confirms absence of only the three owned containers.

Reports require exactly five native or twelve PostgreSQL distinct PASS cases, complete source SHA and snapshot/archive fingerprints. Native evidence cannot claim PostgreSQL RTO/RPO. Proofs contain bounded printable strings, ints and booleans; only selected aggregates, no secrets/raw records/private paths. JSON and escaped CSP-restricted HTML go into a new directory. Hashes do not authenticate the observer.
