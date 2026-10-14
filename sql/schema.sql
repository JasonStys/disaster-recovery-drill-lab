-- Fictional order ledger with database-enforced keys, references and integer-money bounds. Jason Stys.
-- customers: synthetic customer_id/name; orders: immutable id, customer, total, commit timestamp.
-- lines: order/position composite key, sku, quantity and unit_cents; payments: one full payment per order.
-- BEGIN CODE MAP (generated; python scripts/code_map.py)
-- table: customers — line 20
-- column: customer_id — line 21
-- column: name — line 22
-- table: orders — line 24
-- column: order_id — line 25
-- column: total_cents — line 27
-- column: committed_at — line 28
-- table: lines — line 30
-- column: position — line 32
-- column: sku — line 33
-- column: quantity — line 34
-- column: unit_cents — line 35
-- table: payments — line 38
-- column: paid_cents — line 40
-- END CODE MAP
CREATE TABLE customers (
    customer_id BIGINT PRIMARY KEY,
    name TEXT NOT NULL CHECK (length(name) BETWEEN 1 AND 64)
);
CREATE TABLE orders (
    order_id BIGINT PRIMARY KEY,
    customer_id BIGINT NOT NULL REFERENCES customers,
    total_cents BIGINT NOT NULL CHECK (total_cents BETWEEN 1 AND 1000000000),
    committed_at TIMESTAMPTZ NOT NULL DEFAULT clock_timestamp()
);
CREATE TABLE lines (
    order_id BIGINT NOT NULL REFERENCES orders,
    position INTEGER NOT NULL CHECK (position BETWEEN 1 AND 100),
    sku TEXT NOT NULL,
    quantity INTEGER NOT NULL CHECK (quantity BETWEEN 1 AND 1000),
    unit_cents BIGINT NOT NULL CHECK (unit_cents BETWEEN 1 AND 1000000),
    PRIMARY KEY (order_id, position)
);
CREATE TABLE payments (
    order_id BIGINT PRIMARY KEY REFERENCES orders,
    paid_cents BIGINT NOT NULL CHECK (paid_cents BETWEEN 1 AND 1000000000)
);
