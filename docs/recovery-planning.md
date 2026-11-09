# Recovery-point and retention review

Created by Jason Stys. `plan` compares captured recovery evidence for several points against **one** source head and objective set. It makes tradeoffs visible without restoring, forgetting, pruning or deleting any backup.

```text
python scripts/planning_demo.py --output out/recovery-catalog.json
python -m dr plan out/recovery-catalog.json --output out/recovery-review
```

Create `out` first; both output names must be new. The fictional dispatch-supply catalog has an old fast point losing two committed orders, a middle point losing one within budget, a newer point with too-slow restore and a newest untested point. Only the middle point meets the supplied RPO/RTO/loss objectives; newest is not automatically best. Open `recovery-review.html` for aggregate metrics/retention reasons and exact catalog/source fingerprints. Original customer/order rows and passwords are omitted.

The closed schema1 input includes `as_of_ms`, `source_head`, `objectives` (`rto_ms`, `rpo_ms`, `max_lost_orders`), `retention_minimum` and1–20 `points`. Each point requires full64-hex nonzero `id`, `created_at_ms`, `provenance` (`supplied_synthetic` or `measured_lab`), `snapshot`, `restored`, `elapsed_ms`, and boolean `legal_hold`. Ledger shape/financial consistency matches the existing evaluator. Source head must be append-only relative to each snapshot, clocks cannot precede included transactions, and created/source timestamps cannot be after the explicit review clock. Restore data/time are either both supplied or both null.

Every supplied restore is independently checked for exact snapshot equality, RTO, latest-original-commit RPO and lost-order count using the existing evaluator. An untested point exposes only potential RPO/loss **if exactly restored**, with unknown measured evaluation; zero RTO is never invented. Within each provenance group, eligible candidates sort by lowest observed RPO, then lost orders, then measured RTO and stable ID. Synthetic and declared measured-lab evidence are never ranked together. Provenance/timings are assertions in supplied captures, not authenticated backup acquisition or proven production measurements.

Retention advice keeps the newest configured minimum **per provenance group**, legal holds, each selected recovery point, untested points needing a drill and mismatched restorations needing investigation. Remaining entries are only MANUAL_RETIREMENT_REVIEW; that is not a delete approval. Check independent coverage, obligations and integrity before any retention decision. The command never generates or executes a delete/prune command and is separate from all restic operations.

Exit0 means at least one group has an eligible captured point; inspect groups because other groups may have none. Exit1 means none meets the objectives and still produces the useful review; exit2 rejects malformed/unavailable inputs/output. Supplied ledgers remain subject to the existing1MiB bounded reader/tree and row contracts. Keep real catalogs and reports private. Runtime remains standard-library only; reports are escaped, inert local HTML/JSON. Existing real restic integrity/encryption and isolated PostgreSQL/constraint drills remain required; this planning report is not PITR, an automated restore, a zero-loss guarantee or production recovery authorization.
