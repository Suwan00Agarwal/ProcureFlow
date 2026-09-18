-- ==============================================================================
-- ProcureFlow SQL Script 01: Data Quality & Profiling Audit
-- Detects null values, casing inconsistencies, duplicate records, and invalid values
-- ==============================================================================

-- 1. NULL Value Audit Across Key Tables
SELECT 
    'vendors' AS table_name,
    COUNT(*) AS total_records,
    SUM(CASE WHEN vendor_rating IS NULL THEN 1 ELSE 0 END) AS null_ratings,
    SUM(CASE WHEN region IS NULL THEN 1 ELSE 0 END) AS null_regions
FROM vendors
UNION ALL
SELECT 
    'purchase_orders' AS table_name,
    COUNT(*) AS total_records,
    SUM(CASE WHEN actual_delivery_date IS NULL AND status = 'Delivered' THEN 1 ELSE 0 END) AS missing_delivered_dates,
    SUM(CASE WHEN actual_delivery_date IS NOT NULL AND status IN ('In Transit', 'Pending Approval') THEN 1 ELSE 0 END) AS invalid_open_order_dates
FROM purchase_orders
UNION ALL
SELECT 
    'payments' AS table_name,
    COUNT(*) AS total_records,
    SUM(CASE WHEN payment_amount IS NULL THEN 1 ELSE 0 END) AS null_payment_amounts,
    0 AS placeholder
FROM payments;

-- 2. Detect Casing Inconsistencies in Raw Vendor Categories
SELECT 
    vendor_category,
    COUNT(*) AS record_count
FROM vendors
GROUP BY vendor_category
ORDER BY record_count DESC;

-- 3. Detect Duplicate Candidate Line Items (Same PO ID + Product ID)
SELECT 
    po_id,
    product_id,
    COUNT(*) AS duplicate_occurrences
FROM purchase_order_items
GROUP BY po_id, product_id
HAVING COUNT(*) > 1;

-- 4. Audit Invalid Negative or Zero Quantities
SELECT 
    po_item_id,
    po_id,
    product_id,
    quantity,
    unit_price
FROM purchase_order_items
WHERE quantity <= 0;

-- 5. Detect Date Sequence Anomalies (Payment Date Before Order Date)
SELECT 
    p.payment_id,
    p.po_id,
    po.order_date,
    p.payment_date,
    (julianday(p.payment_date) - julianday(po.order_date)) AS days_diff
FROM payments p
JOIN purchase_orders po ON p.po_id = po.po_id
WHERE p.payment_date < po.order_date;
