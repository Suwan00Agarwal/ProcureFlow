# Data Quality & Profiling Audit Report - ProcureFlow

## Executive Summary
Prior to executing business analysis and BI dashboarding, a rigorous **Data Quality Audit** was conducted on the raw synthetic dataset (`data/raw/`). Controlled data anomalies, formatting inconsistencies, missing values, and logical date errors were intentionally embedded into raw sources to simulate real-world enterprise transactional data corruption.

This report documents:
1. **Flaws Identified**: Specific data anomalies detected during profiling.
2. **Detection Methodologies**: SQL scripts and Pandas logic used to audit the tables.
3. **Remediation Actions**: Data cleaning, imputation, deduplication, and standardization steps applied.
4. **Audit Metrics**: Quantitative before-and-after record counts.

---

## Data Quality Issues & Remediation Summary

| Table | Issue Description | Detection Method | Records Affected | Remediation Action Taken |
| :--- | :--- | :--- | :--- | :--- |
| `vendors` | Inconsistent string casing (`lower`, `UPPER`, `Title`) in `vendor_category` & `region` | SQL `GROUP BY` casing audit | 57 records (33 cat, 24 reg) | Standardized all text strings to Proper Title Case (`.str.title()`) |
| `vendors` | Missing `vendor_rating` values (Null entries) | SQL `WHERE vendor_rating IS NULL` | 5 records (3.3%) | Imputed missing ratings using category median vendor rating |
| `purchase_orders` | Open/Cancelled orders with non-null `actual_delivery_date` | SQL logical condition audit (`status IN ('In Transit', 'Pending') AND date IS NOT NULL`) | 18 records | Nullified invalid delivery dates (`actual_delivery_date = NULL`) |
| `purchase_orders` | Delivered orders with missing `actual_delivery_date` | SQL logical audit (`status = 'Delivered' AND date IS NULL`) | 99 records | Imputed missing date as `expected_delivery_date + 2 days` |
| `purchase_order_items` | Candidate duplicate line items (Same `po_id` & `product_id`) | SQL `GROUP BY po_id, product_id HAVING COUNT(*) > 1` | 10 records | Deduplicated dataset keeping the first primary record (`drop_duplicates`) |
| `purchase_order_items` | Invalid negative or zero quantities (`quantity <= 0`) | SQL range check `WHERE quantity <= 0` | 11 records | Converted negative quantities to positive absolute values (`abs(qty)`) |
| `payments` | Missing `payment_amount` values | SQL `WHERE payment_amount IS NULL` | 24 records | Recalculated exact payment amount from PO line-item net totals |
| `payments` | Payment date prior to purchase order date (`payment_date < order_date`) | SQL date comparison join | 7 records | Adjusted `payment_date` to `order_date + 30 days` |

---

## Detailed Remediation Methodology

### 1. Vendor Rating Imputation Logic
Missing `vendor_rating` values were not dropped to avoid sample size bias. Instead, ratings were imputed using category-level medians:
$$\text{Rating}_{\text{imputed}} = \text{Median}\big(\{ \text{Rating}_v \mid v \in \text{Vendor Category} \}\big)$$
*Result*: 5 missing vendor ratings imputed accurately without altering category distributions.

### 2. Purchase Order Date Consistency Enforcement
Delivered purchase orders require a valid `actual_delivery_date` for door-to-door lead time calculation. Delivered orders with missing dates were imputed with a 2-day delivery lag past expected date. Open orders ('In Transit', 'Pending Approval') with erroneous delivery dates were cleared to `NULL` to prevent erroneous zero-day lead time bias in SQL window functions.

### 3. Line-Item Deduplication & Quantity Corrections
Duplicate PO item entries (inserted via data corruption simulation) were identified using composite primary key checks (`po_id`, `product_id`). All 10 duplicate rows were pruned. 11 negative quantity records (e.g. `qty = -15`) were converted to positive integers via absolute value transformation.

---

## Post-Cleaning Dataset Integrity Verification
Following pipeline execution (`python python/clean_data.py`), clean CSV files were exported to `data/processed/` and loaded into `procureflow.db`.

- **Zero Null Leakage**: 100% of required FKs, dates, and amounts are non-null across all 7 tables.
- **Referential Integrity**: 100% of foreign keys in `purchase_orders`, `purchase_order_items`, and `payments` match valid primary keys in parent tables (`vendors`, `products`, `departments`).
- **Mathematical Reconciliation**: Total payment disbursements equal total line-item net totals ($698,741,716.32).
