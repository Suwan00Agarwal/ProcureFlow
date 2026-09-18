-- ==============================================================================
-- ProcureFlow SQL Script 06: Pareto 80/20 & Vendor Concentration Risk Analysis
-- Demonstrates Advanced Window Functions for Cumulative Spend & Dependency Ratios
-- ==============================================================================

-- 1. Full Pareto Spend Concentration Curve Query (80/20 Rule)
WITH vendor_spend_summary AS (
    SELECT 
        v.vendor_id,
        v.vendor_name,
        v.vendor_category,
        v.region,
        COUNT(DISTINCT po.po_id) AS total_orders,
        SUM(poi.quantity * poi.unit_price * (1 - poi.discount)) AS vendor_spend,
        AVG(CASE WHEN po.status = 'Delivered' AND po.actual_delivery_date > po.expected_delivery_date THEN 1.0 ELSE 0.0 END) AS delay_rate
    FROM vendors v
    JOIN purchase_orders po ON v.vendor_id = po.vendor_id
    JOIN purchase_order_items poi ON po.po_id = poi.po_id
    GROUP BY v.vendor_id, v.vendor_name, v.vendor_category, v.region
),
ranked_spend AS (
    SELECT 
        vendor_id,
        vendor_name,
        vendor_category,
        region,
        total_orders,
        vendor_spend,
        delay_rate,
        ROW_NUMBER() OVER (ORDER BY vendor_spend DESC) AS vendor_rank,
        COUNT(*) OVER () AS total_vendor_count,
        SUM(vendor_spend) OVER (ORDER BY vendor_spend DESC) AS cumulative_spend,
        SUM(vendor_spend) OVER () AS grand_total_spend
    FROM vendor_spend_summary
)
SELECT 
    vendor_rank,
    vendor_name,
    vendor_category,
    region,
    total_orders,
    ROUND(vendor_spend, 2) AS vendor_spend,
    ROUND(100.0 * vendor_spend / grand_total_spend, 2) AS spend_share_pct,
    ROUND(100.0 * cumulative_spend / grand_total_spend, 2) AS cumulative_spend_pct,
    ROUND(100.0 * vendor_rank / total_vendor_count, 2) AS vendor_percentile_pct,
    ROUND(delay_rate * 100, 1) AS delay_rate_pct,
    CASE 
        WHEN (100.0 * cumulative_spend / grand_total_spend) <= 80.0 THEN 'Core 80% Spend Tier (High Concentration Risk)'
        ELSE 'Tail 20% Spend Tier'
    END AS pareto_tier
FROM ranked_spend
ORDER BY vendor_rank;

-- 2. Summary of Top Vendor Concentration (Top 5%, 10%, 20% Spend Shares)
WITH vendor_spend_summary AS (
    SELECT 
        v.vendor_id,
        SUM(poi.quantity * poi.unit_price * (1 - poi.discount)) AS vendor_spend
    FROM vendors v
    JOIN purchase_orders po ON v.vendor_id = po.vendor_id
    JOIN purchase_order_items poi ON po.po_id = poi.po_id
    GROUP BY v.vendor_id
),
ranked_spend AS (
    SELECT 
        vendor_spend,
        ROW_NUMBER() OVER (ORDER BY vendor_spend DESC) AS vendor_rank,
        COUNT(*) OVER () AS total_vendors,
        SUM(vendor_spend) OVER () AS grand_total_spend
    FROM vendor_spend_summary
)
SELECT 
    'Top 5% Vendors (Top 8)' AS vendor_tier,
    ROUND(SUM(CASE WHEN vendor_rank <= CAST(0.05 * total_vendors AS INT) THEN vendor_spend ELSE 0 END), 2) AS tier_spend,
    ROUND(100.0 * SUM(CASE WHEN vendor_rank <= CAST(0.05 * total_vendors AS INT) THEN vendor_spend ELSE 0 END) / MAX(grand_total_spend), 2) AS spend_share_pct
FROM ranked_spend
UNION ALL
SELECT 
    'Top 10% Vendors (Top 15)' AS vendor_tier,
    ROUND(SUM(CASE WHEN vendor_rank <= CAST(0.10 * total_vendors AS INT) THEN vendor_spend ELSE 0 END), 2) AS tier_spend,
    ROUND(100.0 * SUM(CASE WHEN vendor_rank <= CAST(0.10 * total_vendors AS INT) THEN vendor_spend ELSE 0 END) / MAX(grand_total_spend), 2) AS spend_share_pct
FROM ranked_spend
UNION ALL
SELECT 
    'Top 20% Vendors (Top 30)' AS vendor_tier,
    ROUND(SUM(CASE WHEN vendor_rank <= CAST(0.20 * total_vendors AS INT) THEN vendor_spend ELSE 0 END), 2) AS tier_spend,
    ROUND(100.0 * SUM(CASE WHEN vendor_rank <= CAST(0.20 * total_vendors AS INT) THEN vendor_spend ELSE 0 END) / MAX(grand_total_spend), 2) AS spend_share_pct
FROM ranked_spend;
