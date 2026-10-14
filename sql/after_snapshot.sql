-- Five committed orders deliberately outside the saved snapshot; loss must be reported. Jason Stys.
-- BEGIN CODE MAP (generated; python scripts/code_map.py)
-- END CODE MAP
BEGIN;
INSERT INTO orders (order_id, customer_id, total_cents)
SELECT id, 1 + (id - 1) % 10, 3000 FROM generate_series(41, 45) AS id;
INSERT INTO lines SELECT order_id, 1, 'SENSOR-SAMPLE', 2, 1000 FROM orders WHERE order_id > 40;
INSERT INTO lines SELECT order_id, 2, 'CABLE-SAMPLE', 1, 1000 FROM orders WHERE order_id > 40;
INSERT INTO payments SELECT order_id, total_cents FROM orders WHERE order_id > 40;
COMMIT;
-- Only new orders receive their original transaction commit timestamp; baseline rows stay immutable.
UPDATE orders SET committed_at = pg_xact_commit_timestamp(xmin) WHERE order_id > 40;
