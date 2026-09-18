-- ==============================================================================
-- ProcureFlow: Procurement & Vendor Performance Analytics
-- Relational Schema Definition (PostgreSQL Standard ANSI SQL)
-- ==============================================================================

-- Drop tables if exists (for clean execution)
DROP TABLE IF EXISTS vendor_performance CASCADE;
DROP TABLE IF EXISTS payments CASCADE;
DROP TABLE IF EXISTS purchase_order_items CASCADE;
DROP TABLE IF EXISTS purchase_orders CASCADE;
DROP TABLE IF EXISTS departments CASCADE;
DROP TABLE IF EXISTS products CASCADE;
DROP TABLE IF EXISTS vendors CASCADE;

-- 1. VENDORS TABLE
CREATE TABLE vendors (
    vendor_id INTEGER PRIMARY KEY,
    vendor_name VARCHAR(100) NOT NULL,
    vendor_category VARCHAR(50) NOT NULL,
    region VARCHAR(50) NOT NULL,
    contract_start_date DATE NOT NULL,
    contract_end_date DATE NOT NULL,
    vendor_rating NUMERIC(2,1),
    payment_terms VARCHAR(30) NOT NULL,
    CONSTRAINT chk_vendor_rating CHECK (vendor_rating IS NULL OR (vendor_rating >= 1.0 AND vendor_rating <= 5.0))
);

-- 2. PRODUCTS TABLE
CREATE TABLE products (
    product_id INTEGER PRIMARY KEY,
    product_name VARCHAR(150) NOT NULL,
    category VARCHAR(50) NOT NULL,
    subcategory VARCHAR(50) NOT NULL,
    unit_cost NUMERIC(10,2) NOT NULL CHECK (unit_cost >= 0),
    supplier_type VARCHAR(30) NOT NULL
);

-- 3. DEPARTMENTS TABLE
CREATE TABLE departments (
    department_id INTEGER PRIMARY KEY,
    department_name VARCHAR(50) NOT NULL,
    business_unit VARCHAR(50) NOT NULL,
    region VARCHAR(50) NOT NULL
);

-- 4. PURCHASE ORDERS TABLE
CREATE TABLE purchase_orders (
    po_id INTEGER PRIMARY KEY,
    vendor_id INTEGER NOT NULL REFERENCES vendors(vendor_id) ON DELETE CASCADE,
    department_id INTEGER NOT NULL REFERENCES departments(department_id) ON DELETE CASCADE,
    order_date DATE NOT NULL,
    expected_delivery_date DATE NOT NULL,
    actual_delivery_date DATE,
    status VARCHAR(25) NOT NULL CHECK (status IN ('Delivered', 'In Transit', 'Pending Approval', 'Cancelled')),
    priority VARCHAR(20) NOT NULL CHECK (priority IN ('Low', 'Medium', 'High', 'Critical')),
    CONSTRAINT chk_exp_date CHECK (expected_delivery_date >= order_date)
);

-- 5. PURCHASE ORDER ITEMS TABLE
CREATE TABLE purchase_order_items (
    po_item_id INTEGER PRIMARY KEY,
    po_id INTEGER NOT NULL REFERENCES purchase_orders(po_id) ON DELETE CASCADE,
    product_id INTEGER NOT NULL REFERENCES products(product_id) ON DELETE CASCADE,
    quantity INTEGER NOT NULL,
    unit_price NUMERIC(10,2) NOT NULL CHECK (unit_price >= 0),
    discount NUMERIC(4,2) NOT NULL DEFAULT 0.00 CHECK (discount >= 0.00 AND discount <= 1.00)
);

-- 6. PAYMENTS TABLE
CREATE TABLE payments (
    payment_id INTEGER PRIMARY KEY,
    po_id INTEGER NOT NULL REFERENCES purchase_orders(po_id) ON DELETE CASCADE,
    payment_date DATE NOT NULL,
    payment_amount NUMERIC(12,2),
    payment_status VARCHAR(20) NOT NULL CHECK (payment_status IN ('Paid', 'Pending', 'Overdue', 'Failed')),
    payment_method VARCHAR(30) NOT NULL
);

-- 7. VENDOR PERFORMANCE EVALUATIONS TABLE
CREATE TABLE vendor_performance (
    vendor_id INTEGER NOT NULL REFERENCES vendors(vendor_id) ON DELETE CASCADE,
    evaluation_date DATE NOT NULL,
    quality_score NUMERIC(5,2) NOT NULL CHECK (quality_score >= 0 AND quality_score <= 100),
    delivery_score NUMERIC(5,2) NOT NULL CHECK (delivery_score >= 0 AND delivery_score <= 100),
    compliance_score NUMERIC(5,2) NOT NULL CHECK (compliance_score >= 0 AND compliance_score <= 100),
    PRIMARY KEY (vendor_id, evaluation_date)
);
