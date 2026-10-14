-- Canonical relational snapshot for independent Python verification; no secrets or real people. Jason Stys.
-- BEGIN CODE MAP (generated; python scripts/code_map.py)
-- END CODE MAP
SELECT json_build_object(
    'customers', (SELECT json_agg(json_build_array(customer_id, name) ORDER BY customer_id) FROM customers),
    'orders', (SELECT json_agg(json_build_array(order_id, customer_id, total_cents, floor(extract(epoch FROM committed_at) * 1000)::bigint) ORDER BY order_id) FROM orders),
    'lines', (SELECT json_agg(json_build_array(order_id, position, sku, quantity, unit_cents) ORDER BY order_id, position) FROM lines),
    'payments', (SELECT json_agg(json_build_array(order_id, paid_cents) ORDER BY order_id) FROM payments)
);
