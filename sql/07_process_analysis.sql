-- ==============================================================================
-- ProcureFlow SQL Script 07: Procurement Lifecycle & Process Bottleneck Analysis
-- Maps cycle times from Order Date -> Delivery -> Payment and Payment Lag
-- ==============================================================================

-- 1. End-to-End Procurement Lifecycle Stage Durations
SELECT 
    v.vendor_category,
    COUNT(po.po_id) AS completed_orders,
    ROUND(AVG(julianday(po.expected_delivery_date) - julianday(po.order_date)), 1) AS avg_agreed_lead_time_days,
    ROUND(AVG(julianday(po.actual_delivery_date) - julianday(po.order_date)), 1) AS avg_actual_fulfillment_days,
    ROUND(AVG(julianday(p.payment_date) - julianday(po.actual_delivery_date)), 1) AS avg_payment_processing_lag_days,
    ROUND(AVG(julianday(p.payment_date) - julianday(po.order_date)), 1) AS avg_total_cycle_time_days
FROM purchase_orders po
JOIN vendors v ON po.vendor_id = v.vendor_id
JOIN payments p ON po.po_id = p.po_id
WHERE po.status = 'Delivered' AND po.actual_delivery_date IS NOT NULL
GROUP BY v.vendor_category
ORDER BY avg_total_cycle_time_days DESC;

-- 2. Payment Status & Cash Flow Bottleneck Analysis
SELECT 
    payment_status,
    payment_method,
    COUNT(payment_id) AS transaction_count,
    ROUND(SUM(payment_amount), 2) AS total_payment_value,
    ROUND(AVG(payment_amount), 2) AS avg_payment_value,
    ROUND(100.0 * SUM(payment_amount) / SUM(SUM(payment_amount)) OVER(), 2) AS payment_value_share_pct
FROM payments
GROUP BY payment_status, payment_method
ORDER BY total_payment_value DESC;

-- 3. Capital Tied Up in Overdue / Unsettled Invoices by Vendor
SELECT 
    v.vendor_name,
    v.vendor_category,
    v.payment_terms,
    COUNT(p.payment_id) AS overdue_invoice_count,
    ROUND(SUM(p.payment_amount), 2) AS total_overdue_amount,
    ROUND(AVG(julianday(p.payment_date) - julianday(po.actual_delivery_date)), 1) AS avg_payment_lag_days
FROM payments p
JOIN purchase_orders po ON p.po_id = po.po_id
JOIN vendors v ON po.vendor_id = v.vendor_id
WHERE p.payment_status = 'Overdue'
GROUP BY v.vendor_name, v.vendor_category, v.payment_terms
ORDER BY total_overdue_amount DESC
LIMIT 10;
