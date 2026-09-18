-- ==============================================================================
-- ProcureFlow: Query Optimization & Performance Indexes (PostgreSQL)
-- Defines B-tree & Composite Indexes for High-Volume Analytical Queries
-- ==============================================================================

-- Index on purchase_orders for filtering by vendor and order status
CREATE INDEX IF NOT EXISTS idx_po_vendor_status 
ON purchase_orders(vendor_id, status);

-- Composite Index on purchase_orders for time-series trend analysis & delivery calculation
CREATE INDEX IF NOT EXISTS idx_po_dates 
ON purchase_orders(order_date, expected_delivery_date, actual_delivery_date);

-- Composite Index on purchase_order_items for joining POs to Products
CREATE INDEX IF NOT EXISTS idx_po_items_po_prod 
ON purchase_order_items(po_id, product_id);

-- Index on products for category & cost filtering
CREATE INDEX IF NOT EXISTS idx_products_cat 
ON products(category, subcategory);

-- Index on vendors for regional & category segmentation
CREATE INDEX IF NOT EXISTS idx_vendors_region 
ON vendors(region, vendor_category);

-- Index on payments for financial lag & status audits
CREATE INDEX IF NOT EXISTS idx_payments_po 
ON payments(po_id, payment_status);

-- Commentary on Index Strategy:
-- 1. `idx_po_vendor_status` speeds up vendor-level performance aggregation (GROUP BY vendor_id WHERE status = 'Delivered').
-- 2. `idx_po_dates` optimizes date range filters (BETWEEN '2024-01-01' AND '2025-12-31') and lead-time calculations.
-- 3. `idx_po_items_po_prod` enables Index-Only Scans when joining order headers to line items for total value aggregation.
