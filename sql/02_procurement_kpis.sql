-- ==============================================================================
-- ProcureFlow SQL Script 02: Core Procurement Business KPIs
-- Calculates macro-level operational metrics, lead times, spend, and fulfillment
-- ==============================================================================

-- 1. Executive Procurement Scorecard
WITH order_aggregates AS (
    SELECT 
        po.po_id,
        po.vendor_id,
        po.status,
        po.order_date,
        po.expected_delivery_date,
        po.actual_delivery_date,
        COALESCE(SUM(poi.quantity * poi.unit_price * (1 - poi.discount)), 0.0) AS po_value,
        CASE 
            WHEN po.status = 'Delivered' AND po.actual_delivery_date IS NOT NULL 
            THEN CAST((julianday(po.actual_delivery_date) - julianday(po.order_date)) AS INTEGER)
            ELSE NULL 
        END AS lead_time_days,
        CASE 
            WHEN po.status = 'Delivered' AND po.actual_delivery_date > po.expected_delivery_date THEN 1 
            WHEN po.status = 'Delivered' THEN 0 
            ELSE NULL 
        END AS is_delayed
    FROM purchase_orders po
    LEFT JOIN purchase_order_items poi ON po.po_id = poi.po_id
    GROUP BY po.po_id
)
SELECT 
    COUNT(DISTINCT po_id) AS total_purchase_orders,
    ROUND(SUM(po_value), 2) AS total_procurement_spend,
    ROUND(AVG(po_value), 2) AS average_order_value,
    COUNT(DISTINCT vendor_id) AS active_vendors_count,
    ROUND(AVG(lead_time_days), 1) AS average_delivery_lead_time_days,
    ROUND(100.0 * SUM(CASE WHEN status = 'Delivered' AND is_delayed = 0 THEN 1 ELSE 0 END) / 
          NULLIF(SUM(CASE WHEN status = 'Delivered' THEN 1 ELSE 0 END), 0), 2) AS on_time_delivery_rate_pct,
    ROUND(100.0 * SUM(CASE WHEN status = 'Delivered' AND is_delayed = 1 THEN 1 ELSE 0 END) / 
          NULLIF(SUM(CASE WHEN status = 'Delivered' THEN 1 ELSE 0 END), 0), 2) AS delayed_order_rate_pct,
    ROUND(100.0 * SUM(CASE WHEN status = 'Delivered' THEN 1 ELSE 0 END) / COUNT(po_id), 2) AS fulfillment_rate_pct
FROM order_aggregates;

-- 2. Procurement Spend & Order Volume by Region
SELECT 
    d.region AS department_region,
    COUNT(DISTINCT po.po_id) AS total_orders,
    ROUND(SUM(poi.quantity * poi.unit_price * (1 - poi.discount)), 2) AS regional_spend,
    ROUND(AVG(poi.quantity * poi.unit_price * (1 - poi.discount)), 2) AS avg_order_value,
    ROUND(100.0 * SUM(poi.quantity * poi.unit_price * (1 - poi.discount)) / 
          SUM(SUM(poi.quantity * poi.unit_price * (1 - poi.discount))) OVER(), 2) AS spend_share_pct
FROM purchase_orders po
JOIN departments d ON po.department_id = d.department_id
JOIN purchase_order_items poi ON po.po_id = poi.po_id
GROUP BY d.region
ORDER BY regional_spend DESC;

-- 3. Procurement Spend & Performance by Product Category
SELECT 
    p.category,
    COUNT(DISTINCT po.po_id) AS order_count,
    ROUND(SUM(poi.quantity * poi.unit_price * (1 - poi.discount)), 2) AS category_spend,
    ROUND(100.0 * SUM(poi.quantity * poi.unit_price * (1 - poi.discount)) / 
          SUM(SUM(poi.quantity * poi.unit_price * (1 - poi.discount))) OVER(), 2) AS category_spend_share_pct,
    ROUND(AVG(julianday(po.actual_delivery_date) - julianday(po.order_date)), 1) AS avg_lead_time_days
FROM purchase_orders po
JOIN purchase_order_items poi ON po.po_id = poi.po_id
JOIN products p ON poi.product_id = p.product_id
WHERE po.status = 'Delivered'
GROUP BY p.category
ORDER BY category_spend DESC;
