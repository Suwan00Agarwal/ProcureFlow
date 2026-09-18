# ProcureFlow Consulting Case Study Summary

**Client**: GlobalProcure Corporation  
**Engagement Title**: Procurement Optimization, Delivery Bottleneck Remediation & Supplier Risk Analytics  
**Advisory Firm**: EY Consulting Practice (Business Analytics & Supply Chain Advisory)  
**Timeline**: 2024–2025 Analytics Review  

---

## Executive Summary
GlobalProcure Corp engaged EY to diagnose escalating procurement expenditures and persistent delivery bottlenecks across its global operational footprint ($698.7M spend, 37,834 orders across 150 suppliers). 

Through advanced SQL profiling, relational database modeling, window function analytical query engineering, and multi-page BI dashboarding, the consulting team identified structural supply chain inefficiencies. 

Key findings include an **80.2% vendor spend concentration** among 20% of suppliers, a **42.4% purchase order delay rate**, and **15 chronic underperforming vendors** generating over $85M in late inventory flow. 

EY developed a 7-point strategic roadmap projected to deliver **$5.8M–$7.3M in annual ROI** through contract renegotiation, early payment cash discounts, and inventory carrying cost reduction.

---

## Engagement Methodology & Architecture

```
 Raw Data Ingestion ──► Data Cleaning & Profiling ──► PostgreSQL Schema & Views
                                                               │
 Business Recommendations ◄── Streamlit Dashboard ◄── SQL Advanced Analytics
```

1. **Data Quality Engineering**: Profiled raw transactional data, imputing null vendor ratings using category medians, correcting logical order date anomalies, deduplicating candidate entries, and fixing text casing.
2. **PostgreSQL Database Architecture**: Designed an ANSI SQL compliant relational schema with PK/FK relationships across 7 tables, complemented by composite B-tree performance indexes and analytical views.
3. **Advanced SQL Analytical Engine**: Engineered 25+ structured SQL scripts utilizing CTEs, window functions (`RANK`, `DENSE_RANK`, `LAG`, `SUM() OVER`), and conditional aggregations.
4. **Interactive BI Dashboarding**: Built a 4-page Streamlit & Plotly executive dashboard featuring an interactive financial ROI calculator.

---

## Core Findings Matrix

| Focus Area | Empirical Finding | Business Risk / Financial Impact |
| :--- | :--- | :--- |
| **Vendor Concentration** | Top 20% of suppliers account for **80.21% of total spend** ($560.5M). | Extreme single-source vulnerability and loss of pricing leverage. |
| **Delivery Reliability** | **42.37% of delivered orders are delayed**, with average lead times at 20.1 days. | Production stockouts and operational delays. |
| **Problem Suppliers** | 15 specific vendors exhibit persistent delay rates of **45%+**. | $85M+ in delayed inventory flow tied up in late shipments. |
| **Category Bottlenecks** | Raw Materials in LATAM & NA show **56.4%–57.3% delay rates**. | High factory downtime risk for manufacturing units. |
| **Payment Execution** | Invoice payment lag averages **44.2 days post-delivery**. | $32.5M tied up in overdue invoices, straining supplier relations. |

---

## Strategic Value Creation (Annual ROI)

```
==================================================================================
VALUE CREATION LEVER                                           ESTIMATED ANNUAL ROI
==================================================================================
1. Quadrant 2 Vendor Contract Renegotiation (3.5% Price Cut)    $3,250,000 / year
2. Early Payment Cash Discount Capture (2/10 Net 30 Terms)       $2,100,000 / year
3. Lead Time Reduction Inventory Holding Cost Savings               $850,000 / year
----------------------------------------------------------------------------------
TOTAL PROJECTED ANNUAL FINANCIAL IMPACT                         $6,200,000 / year
==================================================================================
```

---

## Implementation Roadmap (Phases 1–3)

- **Phase 1 (Months 1–3)**: Renegotiate contracts with 15 Quadrant 2 vendors; institute mandatory delay penalty clauses.
- **Phase 2 (Months 3–6)**: Roll out automated quarterly Supplier Scorecards and automate 3-way invoice matching.
- **Phase 3 (Months 6–12)**: Implement dual-sourcing for Raw Materials in LATAM and North America.
