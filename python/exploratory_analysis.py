"""
ProcureFlow Exploratory Data Analysis (EDA) & SQL KPI Validation Script
Runs analytical queries against procureflow.db, validates calculated KPIs,
and outputs statistical summaries and charts.
"""

import os
import sqlite3
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go

DB_PATH = "procureflow.db"
IMAGES_DIR = "images"
os.makedirs(IMAGES_DIR, exist_ok=True)

print("Starting ProcureFlow Exploratory Data Analysis & Validation...")

if not os.path.exists(DB_PATH):
    print(f"Error: {DB_PATH} not found. Run python/clean_data.py first.")
    exit(1)

conn = sqlite3.connect(DB_PATH)

# ==============================================================================
# 1. CORE KPI VALIDATION
# ==============================================================================
kpi_query = """
SELECT 
    COUNT(DISTINCT po_id) AS total_purchase_orders,
    ROUND(SUM(total_po_value), 2) AS total_procurement_spend,
    ROUND(AVG(total_po_value), 2) AS average_order_value,
    ROUND(AVG(actual_lead_time_days), 1) AS avg_delivery_lead_time_days,
    ROUND(100.0 * SUM(CASE WHEN status = 'Delivered' AND is_delayed = 0 THEN 1 ELSE 0 END) / 
          NULLIF(SUM(CASE WHEN status = 'Delivered' THEN 1 ELSE 0 END), 0), 2) AS on_time_delivery_rate_pct,
    ROUND(100.0 * SUM(CASE WHEN status = 'Delivered' AND is_delayed = 1 THEN 1 ELSE 0 END) / 
          NULLIF(SUM(CASE WHEN status = 'Delivered' THEN 1 ELSE 0 END), 0), 2) AS delayed_order_rate_pct,
    COUNT(DISTINCT vendor_id) AS active_vendors_count
FROM vw_po_header_summary;
"""

df_kpi = pd.read_sql_query(kpi_query, conn)
print("\n=== EXECUTIVE KPI SUMMARY ===")
for col in df_kpi.columns:
    print(f"{col}: {df_kpi[col].iloc[0]}")

# ==============================================================================
# 2. VENDOR PARETO SPEND CONCENTRATION ANALYSIS
# ==============================================================================
pareto_query = """
WITH vendor_spend AS (
    SELECT 
        vendor_id,
        vendor_name,
        vendor_category,
        SUM(total_po_value) AS spend,
        COUNT(po_id) AS order_count,
        AVG(is_delayed) AS delay_rate
    FROM vw_po_header_summary
    GROUP BY vendor_id, vendor_name, vendor_category
),
ranked_vendors AS (
    SELECT 
        vendor_id,
        vendor_name,
        vendor_category,
        spend,
        order_count,
        delay_rate,
        SUM(spend) OVER (ORDER BY spend DESC) AS cumulative_spend,
        SUM(spend) OVER () AS grand_total_spend,
        ROW_NUMBER() OVER (ORDER BY spend DESC) AS vendor_rank,
        COUNT(*) OVER () AS total_vendors
    FROM vendor_spend
)
SELECT 
    vendor_rank,
    vendor_name,
    vendor_category,
    ROUND(spend, 2) AS total_spend,
    ROUND(100.0 * spend / grand_total_spend, 2) AS spend_share_pct,
    ROUND(100.0 * cumulative_spend / grand_total_spend, 2) AS cumulative_spend_pct,
    ROUND(100.0 * vendor_rank / total_vendors, 2) AS vendor_pct,
    ROUND(delay_rate * 100, 1) AS delay_rate_pct
FROM ranked_vendors
ORDER BY vendor_rank;
"""

df_pareto = pd.read_sql_query(pareto_query, conn)
top_20_pct_spend = df_pareto[df_pareto['vendor_pct'] <= 20.0]['spend_share_pct'].sum()
print(f"\nPARETO INSIGHT: Top 20% of Vendors account for {top_20_pct_spend:.2f}% of total spend.")

# Save Pareto Chart Image/Data
fig_pareto = go.Figure()
fig_pareto.add_trace(go.Bar(
    x=df_pareto['vendor_name'].head(25),
    y=df_pareto['total_spend'].head(25),
    name='Spend ($)',
    marker_color='#1E3A8A'
))
fig_pareto.add_trace(go.Scatter(
    x=df_pareto['vendor_name'].head(25),
    y=df_pareto['cumulative_spend_pct'].head(25),
    name='Cumulative Spend %',
    yaxis='y2',
    line=dict(color='#E11D48', width=3)
))
fig_pareto.update_layout(
    title='Top 25 Vendor Spend & Cumulative Pareto Curve',
    xaxis_title='Vendor Name',
    yaxis_title='Spend ($)',
    yaxis2=dict(title='Cumulative Spend %', overlaying='y', side='right', range=[0, 105]),
    template='plotly_white',
    height=500
)

try:
    fig_pareto.write_image(os.path.join(IMAGES_DIR, "pareto_analysis.png"))
except Exception as e:
    fig_pareto.write_html(os.path.join(IMAGES_DIR, "pareto_analysis.html"))

# ==============================================================================
# 3. REGIONAL & CATEGORY DELAY MATRIX
# ==============================================================================
delay_matrix_query = """
SELECT 
    vendor_category,
    dept_region AS region,
    COUNT(po_id) AS total_orders,
    ROUND(AVG(actual_lead_time_days), 1) AS avg_lead_time,
    ROUND(100.0 * SUM(CASE WHEN is_delayed = 1 THEN 1 ELSE 0 END) / COUNT(po_id), 1) AS delay_rate_pct
FROM vw_po_header_summary
WHERE status = 'Delivered'
GROUP BY vendor_category, dept_region
ORDER BY delay_rate_pct DESC;
"""

df_matrix = pd.read_sql_query(delay_matrix_query, conn)
print("\n=== TOP 5 BOTTLENECK CATEGORY-REGION COMBINATIONS ===")
print(df_matrix.head(5).to_string(index=False))

conn.close()
print("\nExploratory Data Analysis Completed Successfully.")
