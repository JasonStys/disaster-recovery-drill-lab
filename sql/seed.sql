-- One settled transaction before the consistent dump; all data is fictional. Jason Stys.
-- BEGIN CODE MAP (generated; python scripts/code_map.py)
-- END CODE MAP
BEGIN;
INSERT INTO customers SELECT id, 'Fictional customer ' || id FROM generate_series(1, 10) AS id;
INSERT INTO orders (order_id, customer_id, total_cents)
SELECT id, 1 + (id - 1) % 10, 3000 FROM generate_series(1, 40) AS id;
INSERT INTO lines SELECT order_id, 1, 'SENSOR-SAMPLE', 2, 1000 FROM orders;
INSERT INTO lines SELECT order_id, 2, 'CABLE-SAMPLE', 1, 1000 FROM orders;
INSERT INTO payments SELECT order_id, total_cents FROM orders;
COMMIT;
-- Preserve the original business transaction's actual commit time as ordinary snapshot data.
UPDATE orders SET committed_at = pg_xact_commit_timestamp(xmin);
