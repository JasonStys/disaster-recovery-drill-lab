"""Independent relational/financial consistency oracle and snapshot recovery objectives. Jason Stys."""
# BEGIN CODE MAP (generated; python scripts/code_map.py)
# definition: rows — line 78
# parameter: value — line 78
# parameter: width — line 78
# variable: row — line 82
# definition: text — line 87
# parameter: value — line 87
# variable: c — line 93
# definition: dataset — line 99
# parameter: raw — line 99
# variable: value — line 101
# variable: customers — line 103
# variable: customer_id — line 104
# variable: name — line 104
# variable: identifier — line 105
# variable: orders — line 110
# variable: times — line 111
# variable: committed_ms — line 112
# variable: customer_id — line 112
# variable: order_id — line 112
# variable: total — line 112
# variable: identifier — line 113
# variable: lines — line 118
# variable: totals — line 119
# variable: order_id — line 120
# variable: position — line 120
# variable: quantity — line 120
# variable: sku — line 120
# variable: unit_cents — line 120
# variable: identifier — line 121
# variable: key — line 122
# variable: amount — line 127
# variable: payments — line 129
# variable: amount — line 130
# variable: order_id — line 130
# variable: identifier — line 131
# variable: canonical — line 137
# parameter: row — line 139
# variable: key — line 141
# variable: encoded — line 143
# definition: evaluate — line 157
# parameter: elapsed_ms — line 158
# parameter: objectives — line 158
# parameter: restored — line 158
# parameter: snapshot — line 158
# parameter: source_head — line 158
# variable: baseline — line 161
# variable: head — line 162
# variable: recovered — line 163
# variable: duration — line 164
# variable: limits — line 165
# variable: rto — line 166
# variable: rpo — line 167
# variable: allowed_loss — line 168
# variable: table — line 170
# variable: old — line 171
# variable: row — line 171
# variable: new — line 172
# variable: row — line 172
# variable: baseline_ids — line 175
# variable: row — line 178
# variable: lost — line 182
# variable: gap — line 183
# variable: intact — line 184
# variable: passed — line 186
# END CODE MAP

from __future__ import annotations

import hashlib
import json
from typing import Any

from dr.contracts import bounded, integer, record


def rows(value: Any, width: int) -> list[list[Any]]:
    """Require bounded positional table rows; width is fixed by this synthetic schema."""
    if not isinstance(value, list) or not 1 <= len(value) <= 10_000:
        raise ValueError("bounded nonempty rows required")
    if any(not isinstance(row, list) or len(row) != width for row in value):
        raise ValueError("table row shape invalid")
    return value


def text(value: Any) -> str:
    """Require short printable synthetic identifiers, never controls or arbitrary report content."""
    if (
        not isinstance(value, str)
        or not 1 <= len(value) <= 64
        or not value.isascii()
        or any(ord(c) < 32 or ord(c) > 126 for c in value)
    ):
        raise ValueError("synthetic text invalid")
    return value


def dataset(raw: Any) -> dict[str, Any]:
    """Validate relationships in O(rows); canonical sorting/digest is O(rows log rows) with bounded memory."""
    value = record(raw, {"customers", "orders", "lines", "payments"})
    bounded(value)
    customers: set[int] = set()
    for customer_id, name in rows(value["customers"], 2):
        identifier = integer(customer_id, 1)
        text(name)
        if identifier in customers:
            raise ValueError("duplicate customer")
        customers.add(identifier)
    orders: dict[int, int] = {}
    times: list[int] = []
    for order_id, customer_id, total, committed_ms in rows(value["orders"], 4):
        identifier = integer(order_id, 1)
        if identifier in orders or integer(customer_id, 1) not in customers:
            raise ValueError("order key invalid")
        orders[identifier] = integer(total, 1, 1_000_000_000)
        times.append(integer(committed_ms, 1))
    lines: set[tuple[int, int]] = set()
    totals: dict[int, int] = {}
    for order_id, position, sku, quantity, unit_cents in rows(value["lines"], 5):
        identifier = integer(order_id, 1)
        key = (identifier, integer(position, 1, 100))
        text(sku)
        if identifier not in orders or key in lines:
            raise ValueError("line key invalid")
        lines.add(key)
        amount = integer(quantity, 1, 1000) * integer(unit_cents, 1, 1_000_000)
        totals[identifier] = totals.get(identifier, 0) + amount
    payments: dict[int, int] = {}
    for order_id, amount in rows(value["payments"], 2):
        identifier = integer(order_id, 1)
        if identifier not in orders or identifier in payments:
            raise ValueError("payment key invalid")
        payments[identifier] = integer(amount, 1, 1_000_000_000)
    if totals != orders or payments != orders:
        raise ValueError("financial consistency failed")
    canonical = {
        key: sorted(
            value[key], key=lambda row: tuple(row[:2]) if key == "lines" else row[0]
        )
        for key in value
    }
    encoded = json.dumps(
        canonical, sort_keys=True, separators=(",", ":"), ensure_ascii=True
    ).encode()
    return {
        "fingerprint": hashlib.sha256(encoded).hexdigest(),
        "customers": len(customers),
        "orders": len(orders),
        "lines": len(lines),
        "payments": len(payments),
        "latest_commit_ms": max(times),
        "order_ids": sorted(orders),
    }


def evaluate(
    snapshot: Any, source_head: Any, restored: Any, elapsed_ms: Any, objectives: Any
) -> dict[str, Any]:
    """Compare independently valid ledgers and measured failover time; loss is explicit, never hidden as zero RPO."""
    baseline = dataset(snapshot)
    head = dataset(source_head)
    recovered = dataset(restored)
    duration = integer(elapsed_ms, 0, 1_800_000)
    limits = record(objectives, {"rto_ms", "rpo_ms", "max_lost_orders"})
    rto = integer(limits["rto_ms"], 1, 1_800_000)
    rpo = integer(limits["rpo_ms"], 0, 1_800_000)
    allowed_loss = integer(limits["max_lost_orders"], 0, 10_000)
    # The drill is append-only: reject source rewrites/deletions or earlier timestamps.
    for table in ("customers", "orders", "lines", "payments"):
        old = {tuple(row) for row in snapshot[table]}
        new = {tuple(row) for row in source_head[table]}
        if not old <= new:
            raise ValueError("source is not append-only")
    baseline_ids = set(baseline["order_ids"])
    if any(
        row[3] <= baseline["latest_commit_ms"]
        for row in source_head["orders"]
        if row[0] not in baseline_ids
    ):
        raise ValueError("appended commit clock did not advance")
    lost = len(set(head["order_ids"]) - set(recovered["order_ids"]))
    gap = head["latest_commit_ms"] - recovered["latest_commit_ms"]
    intact = baseline["fingerprint"] == recovered["fingerprint"]
    # Only exact baseline recovery can meet objectives; additional/wrong rows do not compensate for loss.
    passed = intact and 0 <= gap <= rpo and duration <= rto and lost <= allowed_loss
    return {
        "result": "PASS" if passed else "FAIL",
        "snapshot_matches": intact,
        "recovered_orders": recovered["orders"],
        "lost_orders": lost,
        "observed_rpo_ms": max(0, gap),
        "observed_rto_ms": duration,
        "rto_limit_ms": rto,
        "rpo_limit_ms": rpo,
        "lost_order_limit": allowed_loss,
        "recovered_fingerprint": recovered["fingerprint"],
    }
