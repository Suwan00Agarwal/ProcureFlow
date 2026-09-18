-- ==============================================================================
-- ProcureFlow SQL Script 05: Cost & Price Variance Analysis
-- Analyzes unit costs, supplier pricing strategies, and payment terms impact
-- ==============================================================================

-- 1. Price Variance Analysis: Primary vs Secondary vs Spot Market Suppliers
SELECT 
    p.category,
    p.supplier_type,
    COUNT(DISTINCT poi.po_id) AS total_orders,
    ROUND(AVG(p.unit_cost), 2) AS catalog_unit_cost,
    ROUND(AVG(poi.unit_price), 2) AS actual_unit_price,
    ROUND(100.0 * (AVG(poi.unit_price) - AVG(p.unit_cost)) / AVG(p.unit_cost), 2) AS price_variance_pct,
    ROUND(AVG(poi.discount) * 100, 2) AS avg_discount_pct
FROM purchase_order_items poi
JOIN products p ON poi.product_id = p.product_id
GROUP BY p.category, p.supplier_type
ORDER BY p.category, p.supplier_type;

-- 2. Impact of Vendor Payment Terms on Spend and Delivery Performance
SELECT 
    v.payment_terms,
    COUNT(DISTINCT v.vendor_id) AS vendor_count,
    COUNT(DISTINCT po.po_id) AS total_orders,
    ROUND(SUM(poi.quantity * poi.unit_price * (1 - poi.discount)), 2) AS total_spend,
    ROUND(AVG(poi.quantity * poi.unit_price * (1 - poi.discount)), 2) AS avg_order_value,
    ROUND(AVG(julianday(po.actual_delivery_date) - julianday(po.order_date)), 1) AS avg_lead_time_days,
    ROUND(100.0 * SUM(CASE WHEN po.actual_delivery_date > po.expected_delivery_date THEN 1 ELSE 0 END) / COUNT(po.po_id), 2) AS delay_rate_pct
FROM vendors v
JOIN purchase_orders po ON v.vendor_id = po.vendor_id
JOIN purchase_order_items poi ON po.po_id = poi.po_id
WHERE po.status = 'Delivered'
GROUP BY v.payment_terms
ORDER BY total_spend DESC;

-- 3. Top 15 Product Subcategories by Total Procurement Spend
SELECT 
    p.category,
    p.subcategory,
    COUNT(DISTINCT poi.po_id) AS order_count,
    SUM(poi.quantity) AS total_units_purchased,
    ROUND(SUM(poi.quantity * poi.unit_price * (1 - poi.discount)), 2) AS total_spend,
    ROUND(AVG(poi.unit_price), 2) AS avg_unit_price
FROM purchase_order_items poi
JOIN products p ON poi.product_id = p.product_id
GROUP BY p.category, p.subcategory
ORDER BY total_spend DESC
LIMIT 15;
