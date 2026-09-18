# Procurement KPI Definitions & Mathematical Formulas

This document establishes the official mathematical definitions, operational targets, and business significance for the 15 procurement key performance indicators (KPIs) calculated in the ProcureFlow analytics engine.

---

### 1. Total Procurement Spend ($)
$$\text{Total Spend} = \sum_{i=1}^{N} \Big( \text{Quantity}_i \times \text{Unit Price}_i \times (1 - \text{Discount}_i) \Big)$$
- **Description**: Gross monetary expenditure across all fulfilled and active purchase orders.
- **Project Actual**: **$698,741,716.32** across 2024–2025.

---

### 2. Total Purchase Orders (Count)
$$\text{Total POs} = \text{Count}(\text{DISTINCT } \text{po\_id})$$
- **Description**: Aggregate number of purchase order headers issued across all regions and departments.
- **Project Actual**: **37,834 Orders**.

---

### 3. Average Order Value (AOV)
$$\text{AOV} = \frac{\text{Total Procurement Spend}}{\text{Total Purchase Orders}}$$
- **Description**: Average financial value per purchase order header.
- **Project Actual**: **$18,468.62**.

---

### 4. Average Delivery Lead Time (Days)
$$\text{Avg Lead Time} = \frac{\sum \big( \text{Actual Delivery Date} - \text{Order Date} \big)}{\text{Count of Delivered Orders}}$$
- **Description**: Door-to-door elapsed calendar days from PO placement to physical receiving.
- **Project Actual**: **20.1 Days** (Benchmark Target: $< 15.0$ Days).

---

### 5. On-Time Delivery Rate (%)
$$\text{On-Time Delivery Rate} = \frac{\text{Count of Delivered POs where Actual Delivery Date} \le \text{Expected Delivery Date}}{\text{Total Delivered POs}} \times 100$$
- **Description**: Percentage of completed orders delivered on or before the contractually agreed date.
- **Project Actual**: **57.63%** (Benchmark Target: $\ge 85.0\%$).

---

### 6. Delayed Order Rate (%)
$$\text{Delayed Order Rate} = \frac{\text{Count of Delivered POs where Actual Delivery Date} > \text{Expected Delivery Date}}{\text{Total Delivered POs}} \times 100$$
- **Description**: Percentage of completed orders experiencing operational shipment delays past expected date.
- **Project Actual**: **42.37%**.

---

### 7. Composite Vendor Performance Score (0–100)
$$\text{Vendor Score} = \big(0.40 \times \text{Delivery Score}\big) + \big(0.40 \times \text{Quality Score}\big) + \big(0.20 \times \text{Compliance Score}\big)$$
- **Description**: Weighted quarterly audit evaluation score combining timeliness, defect rates, and SLA compliance.
- **Benchmark Target**: $\ge 80.0$.

---

### 8. Procurement Spend by Region ($)
$$\text{Regional Spend}_r = \sum_{p \in \text{Region } r} \text{PO Value}_p$$
- **Description**: Total purchasing expenditure grouped by receiving department geographic location.

---

### 9. Procurement Spend Share by Category (%)
$$\text{Category Share}_c = \frac{\text{Spend in Category } c}{\text{Total Procurement Spend}} \times 100$$
- **Description**: Percentage proportion of global purchasing budget allocated to specific product classifications.

---

### 10. Vendor Spend Concentration Ratio (Top 20%)
$$\text{Concentration Ratio}_{20\%} = \frac{\sum_{k=1}^{\lfloor 0.20 \times V \rfloor} \text{Spend}_{\text{Vendor } k}}{\text{Total Procurement Spend}} \times 100$$
- **Description**: Proportion of global spend controlled by the top 20% highest-spend suppliers (Pareto concentration metric).
- **Project Actual**: **80.21%** ($560.5M controlled by 30 vendors).

---

### 11. Top 10 Vendors by Spend
- **Description**: Ranking of suppliers by total gross order value to identify dominant strategic contracts.

---

### 12. Vendor Dependency Ratio (%)
$$\text{Vendor Dependency Ratio}_v = \frac{\text{Spend with Vendor } v}{\text{Total Category Spend}_c} \times 100$$
- **Description**: Measure of category single-source vulnerability; vendor spend share within a specific category.

---

### 13. Average Payment Processing Lag (Days)
$$\text{Avg Payment Lag} = \frac{\sum \big( \text{Payment Date} - \text{Actual Delivery Date} \big)}{\text{Count of Settled Payments}}$$
- **Description**: Days elapsed between physical goods receipt and invoice payment disbursement.
- **Project Actual**: **44.2 Days** (Target: 30.0 Days).

---

### 14. Order Fulfillment Rate (%)
$$\text{Fulfillment Rate} = \frac{\text{Count of Status 'Delivered' POs}}{\text{Total POs Issued}} \times 100$$
- **Description**: Percentage of issued orders successfully fulfilled without cancellation.
- **Project Actual**: **69.81%** (Delivered POs: 26,411 out of 37,834).

---

### 15. Month-over-Month (MoM) Spend Growth Rate (%)
$$\text{MoM Growth}_t = \frac{\text{Spend}_t - \text{Spend}_{t-1}}{\text{Spend}_{t-1}} \times 100$$
- **Description**: Percentage change in total procurement spend compared to the prior calendar month.
