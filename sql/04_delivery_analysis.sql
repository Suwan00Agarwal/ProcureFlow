-- ==============================================================================
-- ProcureFlow SQL Script 04: Delivery Performance & Bottleneck Analysis
-- Investigates lead times, order priority impacts, regional delays, and seasonality
-- ==============================================================================

-- 1. Delivery Lead Time & Delay Breakdown by Order Priority
SELECT 
    priority,
    COUNT(po_id) AS total_orders,
    ROUND(AVG(julianday(expected_delivery_date) - julianday(order_date)), 1) AS avg_expected_lead_time,
    ROUND(AVG(julianday(actual_delivery_date) - julianday(order_date)), 1) AS avg_actual_lead_time,
    ROUND(AVG(CASE WHEN actual_delivery_date > expected_delivery_date THEN julianday(actual_delivery_date) - julianday(expected_delivery_date) ELSE 0 END), 1) AS avg_delay_days,
    ROUND(100.0 * SUM(CASE WHEN actual_delivery_date > expected_delivery_date THEN 1 ELSE 0 END) / COUNT(po_id), 2) AS delay_rate_pct
FROM purchase_orders
WHERE status = 'Delivered'
GROUP BY priority
ORDER BY 
    CASE priority 
        WHEN 'Critical' THEN 1 
        WHEN 'High' THEN 2 
        WHEN 'Medium' THEN 3 
        WHEN 'Low' THEN 4 
    END;

-- 2. Regional & Category Operational Delay Matrix
SELECT 
    v.vendor_category,
    d.region AS department_region,
    COUNT(po.po_id) AS total_orders,
    ROUND(AVG(julianday(po.actual_delivery_date) - julianday(po.order_date)), 1) AS avg_actual_lead_time,
    ROUND(100.0 * SUM(CASE WHEN po.actual_delivery_date > po.expected_delivery_date THEN 1 ELSE 0 END) / COUNT(po.po_id), 2) AS delay_rate_pct
FROM purchase_orders po
JOIN vendors v ON po.vendor_id = v.vendor_id
JOIN departments d ON po.department_id = d.department_id
WHERE po.status = 'Delivered'
GROUP BY v.vendor_category, d.region
ORDER BY delay_rate_pct DESC;

-- 3. Monthly Seasonal Delivery Delay & Order Volume Trends
SELECT 
    strftime('%Y-%m', order_date) AS order_month,
    COUNT(po_id) AS total_orders,
    ROUND(AVG(julianday(actual_delivery_date) - julianday(order_date)), 1) AS avg_lead_time_days,
    ROUND(100.0 * SUM(CASE WHEN actual_delivery_date > expected_delivery_date THEN 1 ELSE 0 END) / COUNT(po_id), 2) AS monthly_delay_rate_pct
FROM purchase_orders
WHERE status = 'Delivered'
GROUP BY strftime('%Y-%m', order_date)
ORDER BY order_month;
