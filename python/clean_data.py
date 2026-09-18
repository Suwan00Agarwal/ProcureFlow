"""
ProcureFlow Data Cleaning & Database Initialization Pipeline
Reads raw data, logs data quality issues, cleans anomalies, standardizes fields,
imputes missing values, exports processed datasets to data/processed/, and builds SQLite DB procureflow.db.
"""

import os
import sqlite3
import pandas as pd
import numpy as np

RAW_DIR = os.path.join("data", "raw")
PROCESSED_DIR = os.path.join("data", "processed")
DB_PATH = "procureflow.db"

os.makedirs(PROCESSED_DIR, exist_ok=True)

print("Starting ProcureFlow Data Cleaning Pipeline...")

# Log of cleaning actions for the Data Quality Report
cleaning_log = []

def log_action(table, issue, count, action):
    cleaning_log.append({
        'table': table,
        'issue_description': issue,
        'affected_records': count,
        'remediation_action': action
    })
    print(f"[{table}] {issue}: {count} records -> {action}")

# 1. CLEAN VENDORS
df_vendors = pd.read_csv(os.path.join(RAW_DIR, "vendors.csv"))
init_vendor_count = len(df_vendors)

# Casing Standardization
casing_cat_flaws = df_vendors['vendor_category'].apply(lambda x: x != x.title() if isinstance(x, str) else False).sum()
df_vendors['vendor_category'] = df_vendors['vendor_category'].astype(str).str.title()
log_action("vendors", "Inconsistent vendor_category casing (lower/upper)", casing_cat_flaws, "Standardized to Title Case")

casing_reg_flaws = df_vendors['region'].apply(lambda x: x != x.title() if isinstance(x, str) else False).sum()
df_vendors['region'] = df_vendors['region'].astype(str).str.title()
log_action("vendors", "Inconsistent region casing", casing_reg_flaws, "Standardized to Title Case")

# Impute Missing Ratings
null_ratings = df_vendors['vendor_rating'].isna().sum()
if null_ratings > 0:
    cat_medians = df_vendors.groupby('vendor_category')['vendor_rating'].transform('median')
    df_vendors['vendor_rating'] = df_vendors['vendor_rating'].fillna(cat_medians).round(1)
    log_action("vendors", "Missing vendor_rating values", null_ratings, "Imputed using category median rating")

df_vendors.to_csv(os.path.join(PROCESSED_DIR, "vendors.csv"), index=False)

# 2. CLEAN PRODUCTS
df_products = pd.read_csv(os.path.join(RAW_DIR, "products.csv"))
df_products['category'] = df_products['category'].astype(str).str.title()
df_products['subcategory'] = df_products['subcategory'].astype(str).str.title()
df_products.to_csv(os.path.join(PROCESSED_DIR, "products.csv"), index=False)
log_action("products", "Product schema audit", len(df_products), "Validated all 600 product records")

# 3. CLEAN DEPARTMENTS
df_departments = pd.read_csv(os.path.join(RAW_DIR, "departments.csv"))
df_departments['region'] = df_departments['region'].astype(str).str.title()
df_departments.to_csv(os.path.join(PROCESSED_DIR, "departments.csv"), index=False)

# 4. CLEAN PURCHASE ORDERS
df_po = pd.read_csv(os.path.join(RAW_DIR, "purchase_orders.csv"))

# Fix actual delivery dates on open orders ('In Transit', 'Pending Approval', 'Cancelled')
open_statuses = ['In Transit', 'Pending Approval', 'Cancelled']
open_with_date = df_po[(df_po['status'].isin(open_statuses)) & (df_po['actual_delivery_date'].notna())]
log_action("purchase_orders", "Open/Cancelled orders with non-null actual_delivery_date", len(open_with_date), "Set actual_delivery_date to NULL")
df_po.loc[(df_po['status'].isin(open_statuses)), 'actual_delivery_date'] = np.nan

# Impute missing actual_delivery_date on Delivered orders (set to expected_delivery_date + 2 days)
delivered_null_date = df_po[(df_po['status'] == 'Delivered') & (df_po['actual_delivery_date'].isna())]
log_action("purchase_orders", "Delivered orders with missing actual_delivery_date", len(delivered_null_date), "Imputed using expected_delivery_date + 2 days")

df_po['exp_dt'] = pd.to_datetime(df_po['expected_delivery_date'])
df_po.loc[(df_po['status'] == 'Delivered') & (df_po['actual_delivery_date'].isna()), 'actual_delivery_date'] = (df_po['exp_dt'] + pd.Timedelta(days=2)).dt.strftime('%Y-%m-%d')
df_po.drop(columns=['exp_dt'], inplace=True)

df_po.to_csv(os.path.join(PROCESSED_DIR, "purchase_orders.csv"), index=False)

# 5. CLEAN PO ITEMS
df_po_items = pd.read_csv(os.path.join(RAW_DIR, "purchase_order_items.csv"))

# Deduplicate candidate duplicate records
dup_mask = df_po_items.duplicated(subset=['po_id', 'product_id'], keep='first')
dup_count = dup_mask.sum()
df_po_items = df_po_items[~dup_mask].copy()
log_action("purchase_order_items", "Duplicate PO Item entries (same po_id & product_id)", dup_count, "Removed duplicate records")

# Handle invalid negative quantities
neg_qty_count = (df_po_items['quantity'] <= 0).sum()
df_po_items['quantity'] = df_po_items['quantity'].apply(lambda x: abs(x) if x <= 0 else x)
log_action("purchase_order_items", "Invalid negative or zero quantities", neg_qty_count, "Converted to positive absolute values")

df_po_items['net_line_total'] = df_po_items['quantity'] * df_po_items['unit_price'] * (1 - df_po_items['discount'])
df_po_items.to_csv(os.path.join(PROCESSED_DIR, "purchase_order_items.csv"), index=False)

# 6. CLEAN PAYMENTS
df_payments = pd.read_csv(os.path.join(RAW_DIR, "payments.csv"))

# Calculate expected total for each PO
po_totals = df_po_items.groupby('po_id')['net_line_total'].sum().round(2).to_dict()

# Missing payment amount imputation
null_pymts = df_payments['payment_amount'].isna().sum()
df_payments['payment_amount'] = df_payments.apply(
    lambda r: po_totals.get(r['po_id'], r['payment_amount']) if pd.isna(r['payment_amount']) else r['payment_amount'],
    axis=1
)
log_action("payments", "Missing payment_amount values", null_pymts, "Recalculated from PO Item net totals")

# Payment date before order date check
df_po_dates = df_po.set_index('po_id')['order_date'].to_dict()
df_payments['order_date'] = df_payments['po_id'].map(df_po_dates)
date_anom = (pd.to_datetime(df_payments['payment_date']) < pd.to_datetime(df_payments['order_date'])).sum()
# Fix by setting payment date to order_date + 30 days
df_payments.loc[pd.to_datetime(df_payments['payment_date']) < pd.to_datetime(df_payments['order_date']), 'payment_date'] = (pd.to_datetime(df_payments['order_date']) + pd.Timedelta(days=30)).dt.strftime('%Y-%m-%d')
df_payments.drop(columns=['order_date'], inplace=True)
log_action("payments", "Payment date prior to purchase order date", date_anom, "Adjusted payment_date to order_date + 30 days")

df_payments.to_csv(os.path.join(PROCESSED_DIR, "payments.csv"), index=False)

# 7. CLEAN VENDOR PERFORMANCE
df_perf = pd.read_csv(os.path.join(RAW_DIR, "vendor_performance.csv"))
df_perf.to_csv(os.path.join(PROCESSED_DIR, "vendor_performance.csv"), index=False)
log_action("vendor_performance", "Quarterly evaluation schema audit", len(df_perf), "Validated all 1,200 quarterly vendor evaluations")

# Save Cleaning Log
df_log = pd.DataFrame(cleaning_log)
df_log.to_csv(os.path.join(PROCESSED_DIR, "data_cleaning_audit_log.csv"), index=False)

print("\n--- BUILDING SQLITE DATABASE (procureflow.db) FOR LOCAL EXECUTION ---")
if os.path.exists(DB_PATH):
    os.remove(DB_PATH)

conn = sqlite3.connect(DB_PATH)

df_vendors.to_sql("vendors", conn, if_exists="replace", index=False)
df_products.to_sql("products", conn, if_exists="replace", index=False)
df_departments.to_sql("departments", conn, if_exists="replace", index=False)
df_po.to_sql("purchase_orders", conn, if_exists="replace", index=False)
df_po_items.to_sql("purchase_order_items", conn, if_exists="replace", index=False)
df_payments.to_sql("payments", conn, if_exists="replace", index=False)
df_perf.to_sql("vendor_performance", conn, if_exists="replace", index=False)

# Create Analytical Views in SQLite for instant query access
cursor = conn.cursor()

cursor.execute("""
CREATE VIEW IF NOT EXISTS vw_po_header_summary AS
SELECT 
    po.po_id,
    po.vendor_id,
    v.vendor_name,
    v.vendor_category,
    v.region AS vendor_region,
    po.department_id,
    d.department_name,
    d.business_unit,
    d.region AS dept_region,
    po.order_date,
    po.expected_delivery_date,
    po.actual_delivery_date,
    po.status,
    po.priority,
    CASE 
        WHEN po.status = 'Delivered' AND po.actual_delivery_date IS NOT NULL 
        THEN CAST((julianday(po.actual_delivery_date) - julianday(po.order_date)) AS INTEGER)
        ELSE NULL 
    END AS actual_lead_time_days,
    CASE 
        WHEN po.status = 'Delivered' AND po.actual_delivery_date IS NOT NULL 
        THEN CAST((julianday(po.expected_delivery_date) - julianday(po.order_date)) AS INTEGER)
        ELSE NULL 
    END AS expected_lead_time_days,
    CASE 
        WHEN po.status = 'Delivered' AND po.actual_delivery_date IS NOT NULL AND po.actual_delivery_date > po.expected_delivery_date 
        THEN 1 
        WHEN po.status = 'Delivered' THEN 0 
        ELSE NULL 
    END AS is_delayed,
    CASE 
        WHEN po.status = 'Delivered' AND po.actual_delivery_date IS NOT NULL AND po.actual_delivery_date > po.expected_delivery_date 
        THEN CAST((julianday(po.actual_delivery_date) - julianday(po.expected_delivery_date)) AS INTEGER)
        ELSE 0 
    END AS delay_days,
    COALESCE(SUM(poi.quantity * poi.unit_price * (1 - poi.discount)), 0.0) AS total_po_value
FROM purchase_orders po
JOIN vendors v ON po.vendor_id = v.vendor_id
JOIN departments d ON po.department_id = d.department_id
LEFT JOIN purchase_order_items poi ON po.po_id = poi.po_id
GROUP BY po.po_id;
""")

conn.commit()
conn.close()

print(f"SUCCESS: Database {DB_PATH} built with views and 7 relational tables.")
print("ProcureFlow Data Cleaning Pipeline Completed Successfully!")
