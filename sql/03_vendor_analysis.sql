-- ==============================================================================
-- ProcureFlow SQL Script 03: Vendor Performance & Matrix Segmentation
-- Evaluates supplier reliability, spend concentration, and 4-Quadrant Matrix
-- ==============================================================================

-- 1. Comprehensive Vendor Performance Scorecard
WITH vendor_stats AS (
    SELECT 
        v.vendor_id,
        v.vendor_name,
        v.vendor_category,
        v.region,
        v.vendor_rating,
        COUNT(DISTINCT po.po_id) AS total_orders,
        SUM(poi.quantity * poi.unit_price * (1 - poi.discount)) AS total_spend,
        AVG(CASE WHEN po.status = 'Delivered' THEN julianday(po.actual_delivery_date) - julianday(po.order_date) ELSE NULL END) AS avg_lead_time,
        SUM(CASE WHEN po.status = 'Delivered' AND po.actual_delivery_date <= po.expected_delivery_date THEN 1 ELSE 0 END) AS on_time_orders,
        SUM(CASE WHEN po.status = 'Delivered' THEN 1 ELSE 0 END) AS delivered_orders
    FROM vendors v
    JOIN purchase_orders po ON v.vendor_id = po.vendor_id
    JOIN purchase_order_items poi ON po.po_id = poi.po_id
    GROUP BY v.vendor_id, v.vendor_name, v.vendor_category, v.region, v.vendor_rating
)
SELECT 
    vendor_id,
    vendor_name,
    vendor_category,
    region,
    vendor_rating,
    total_orders,
    ROUND(total_spend, 2) AS total_spend,
    ROUND(avg_lead_time, 1) AS avg_lead_time_days,
    ROUND(100.0 * on_time_orders / NULLIF(delivered_orders, 0), 2) AS on_time_delivery_rate_pct,
    ROUND(100.0 - (100.0 * on_time_orders / NULLIF(delivered_orders, 0)), 2) AS delay_rate_pct
FROM vendor_stats
ORDER BY total_spend DESC;

-- 2. 4-Quadrant Vendor Strategic Matrix Classification
WITH vendor_metrics AS (
    SELECT 
        v.vendor_id,
        v.vendor_name,
        v.vendor_category,
        SUM(poi.quantity * poi.unit_price * (1 - poi.discount)) AS total_spend,
        100.0 * SUM(CASE WHEN po.status = 'Delivered' AND po.actual_delivery_date <= po.expected_delivery_date THEN 1 ELSE 0 END) / 
        NULLIF(SUM(CASE WHEN po.status = 'Delivered' THEN 1 ELSE 0 END), 0) AS on_time_rate
    FROM vendors v
    JOIN purchase_orders po ON v.vendor_id = po.vendor_id
    JOIN purchase_order_items poi ON po.po_id = poi.po_id
    GROUP BY v.vendor_id, v.vendor_name, v.vendor_category
),
benchmarks AS (
    SELECT 
        AVG(total_spend) AS avg_vendor_spend,
        AVG(on_time_rate) AS avg_on_time_rate
    FROM vendor_metrics
)
SELECT 
    vm.vendor_id,
    vm.vendor_name,
    vm.vendor_category,
    ROUND(vm.total_spend, 2) AS total_spend,
    ROUND(vm.on_time_rate, 1) AS on_time_rate_pct,
    CASE 
        WHEN vm.total_spend >= b.avg_vendor_spend AND vm.on_time_rate >= b.avg_on_time_rate 
            THEN 'Q1: High Spend / High Performance (Strategic Partners)'
        WHEN vm.total_spend >= b.avg_vendor_spend AND vm.on_time_rate < b.avg_on_time_rate 
            THEN 'Q2: High Spend / Low Performance (HIGH RISK - Renegotiate)'
        WHEN vm.total_spend < b.avg_vendor_spend AND vm.on_time_rate >= b.avg_on_time_rate 
            THEN 'Q3: Low Spend / High Performance (Growth Candidate)'
        ELSE 'Q4: Low Spend / Low Performance (Phase-Out Target)'
    END AS strategic_quadrant
FROM vendor_metrics vm
CROSS JOIN benchmarks b
ORDER BY vm.total_spend DESC;
