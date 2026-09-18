# ProcureFlow – Procurement & Vendor Performance Analytics

[![Python 3.11](https://img.shields.io/badge/Python-3.11-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-15-4169E1?style=for-the-badge&logo=postgresql&logoColor=white)](https://www.postgresql.org/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.25-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)](https://streamlit.io/)
[![Plotly](https://img.shields.io/badge/Plotly-5.15-3F4F75?style=for-the-badge&logo=plotly&logoColor=white)](https://plotly.com/)
[![EY Consulting](https://img.shields.io/badge/Target_Role-EY_Associate_Consultant-FFE600?style=for-the-badge&logo=ey&logoColor=black)](https://www.ey.com/)

**ProcureFlow** is an end-to-end, intermediate-to-advanced Business Analytics and Management Consulting project designed to showcase SQL mastery, data modeling, data quality engineering, root cause analysis, interactive BI dashboarding, and executive business recommendations tailored for an **EY Associate Consultant / Business Analyst** candidate.

---

## 1. Project Overview & Business Context

GlobalProcure Corporation is a multi-national enterprise purchasing products and services across 6 global regions (**North America, Europe, Asia-Pacific, Latin America, Middle East, Africa**) from **150 active vendors** across 8 core product categories. Annual procurement expenditure exceeds **$345M ($698.7M total over 2024–2025)** across **37,834 purchase orders**.

Executive leadership engaged the analytics team to investigate escalating purchasing costs, chronic delivery delays, unmonitored supplier quality, and high spend concentration risk.

```mermaid
flowchart TD
    A[Raw Operational Data\n37.8K Orders | 150 Vendors] --> B[Python Data Cleaning Pipeline\nNull Imputation & Casing Fixes]
    B --> C[(PostgreSQL / SQLite Database\n7 Relational Tables & Indexes)]
    C --> D[SQL Analytical Querying\nCTEs, Window Functions & Views]
    D --> E[KPI Scorecards & Analytics\nSpend, Lead Time, On-Time %]
    E --> F[Interactive Streamlit Dashboard\n4 Pages & ROI Calculator]
    F --> G[Root Cause Analysis\n5 Whys & Fishbone Mapping]
    G --> H[Consulting Recommendations\n$6.2M Annual Savings Roadmap]
```

---

## 2. Key Empirical Findings Summary

| Key Metric | Empirical Result | Business Risk / Finding |
| :--- | :--- | :--- |
| **Total Procurement Spend** | **$698,741,716.32** | $349.3M annual spend across 37,834 PO headers |
| **Vendor Spend Concentration** | **80.21% Spend in Top 20% Vendors** | Top 30 vendors control $560.5M (Extreme Single-Source Risk) |
| **On-Time Delivery Rate** | **57.63% On-Time** | **42.37% Delayed Order Rate** (Target: $\ge 85.0\%$) |
| **Average Delivery Lead Time** | **20.1 Days** | Door-to-door lead time exceeds 15.0-day target |
| **Chronic Problem Suppliers** | **15 High-Spend Suppliers** | Delays $> 45\%$, generating $85M+ in late inventory flow |
| **Highest Delay Categories** | **Raw Materials (LATAM/NA)** | Delay rates reach **56.4%–57.3%** in regional manufacturing |
| **Payment Execution Lag** | **44.2 Days Post-Delivery** | $32.5M tied up in overdue invoices |

---

## 3. Technology Stack

- **Primary Database & Query Engine**: PostgreSQL (Standard ANSI DDL/DML, B-Tree Indexes, CTEs, Window Functions)
- **Zero-Setup Local Engine**: SQLite (`procureflow.db` built automatically for zero-friction dashboard execution)
- **Data Engineering Pipeline**: Python 3.11, Pandas, NumPy
- **Interactive BI Dashboard**: Streamlit, Plotly Express, Plotly Graph Objects
- **Documentation**: Markdown, KaTeX LaTeX formulas, Mermaid diagrams

---

## 4. Repository Structure

```
ProcureFlow/
├── data/
│   ├── raw/                       # Generated raw CSV files (with data quality flaws)
│   └── processed/                 # Cleaned CSV files ready for DB import & BI
├── database/
│   ├── schema.sql                 # PostgreSQL DDL with PK/FK constraints & data types
│   ├── seed_data.sql              # SQL Insert statements / COPY commands
│   └── indexes.sql                # B-tree & multi-column performance indexes
├── sql/
│   ├── 01_data_quality.sql        # Data profiling, null audits, casing fixes
│   ├── 02_procurement_kpis.sql    # Core KPIs (Spend, AOV, Lead Time, On-Time %)
│   ├── 03_vendor_analysis.sql     # Vendor spend ranking, 4-quadrant matrix
│   ├── 04_delivery_analysis.sql   # Lead time distribution, delay patterns by region
│   ├── 05_cost_analysis.sql       # Price variance, category unit costs, terms
│   ├── 06_pareto_analysis.sql     # Window functions (SUM OVER, cumulative %)
│   ├── 07_process_analysis.sql   # Cycle time analysis, payment lag, status lifecycle
│   └── 08_advanced_analysis.sql   # MoM growth, rolling lead times, category DENSE_RANK
├── python/
│   ├── generate_data.py           # Synthetic dataset generator with business logic
│   ├── clean_data.py              # Data cleaning pipeline & SQLite DB exporter
│   └── exploratory_analysis.py    # Python EDA & statistical validation script
├── dashboard/
│   └── app.py                     # Multi-page Streamlit + Plotly consulting dashboard
├── documentation/
│   ├── business_problem.md        # Fictional enterprise context & 12 business questions
│   ├── data_dictionary.md         # Schema documentation & domain values
│   ├── kpi_definitions.md         # Mathematical formulas & targets for 15 KPIs
│   ├── data_quality_report.md     # Audit report on flaws & cleaning metrics
│   ├── root_cause_analysis.md     # Consulting root cause framework (5 Whys / Fishbone)
│   ├── recommendations.md         # 7 actionable recommendations with ROI matrix
│   └── consulting_case_study.md   # Executive consulting case study summary report
├── interview_prep/
│   └── interview_questions.md     # 40+ categorized Q&As, 2-min & 5-min pitches
├── images/                        # Generated preview charts & visual assets
├── requirements.txt               # Dependencies (pandas, numpy, plotly, streamlit)
├── README.md                      # Master portfolio document
└── .gitignore                     # Git ignore rules
```

---

## 5. Database Schema & ER Diagram

```
 +------------------+       +-----------------------+       +--------------------+
 |     VENDORS      |       |    PURCHASE_ORDERS    |       |    DEPARTMENTS     |
 +------------------+       +-----------------------+       +--------------------+
 | PK vendor_id     |◄─────┐| PK po_id              |┌─────►| PK department_id   |
 |    vendor_name   |      │| FK vendor_id          |│      |    department_name |
 |    vendor_cat    |      │| FK department_id      |┼──┐   |    business_unit   |
 |    region        |      │|    order_date         |│  │   |    region          |
 |    rating        |      │|    exp_delivery_date  |│  │   +--------------------+
 +--------┬---------+      │|    act_delivery_date  |│  │
          │                │|    status, priority   |│  │   +--------------------+
          │                │+-----------┬-----------+│  │   |      PRODUCTS      |
          │                │            │            │  │   +--------------------+
          ▼                │            ▼            │  └──►| PK product_id     |
 +------------------+      │+-----------------------+│      |    product_name    |
 | VENDOR_PERF      |      │|  PURCHASE_ORDER_ITEMS |│      |    category        |
 +------------------+      │+-----------------------+│      |    unit_cost       |
 | PK,FK vendor_id  |      │| PK po_item_id         |│      +--------------------+
 | PK eval_date     |      │| FK po_id              |│
 |    quality_score |      └┼── FK product_id       |│      +--------------------+
 |    delivery_score|       |    quantity, price    |│      |      PAYMENTS      |
 +------------------+       +-----------------------+│      +--------------------+
                                                     └─────►| PK payment_id      |
                                                            | FK po_id           |
                                                            |    payment_amount  |
                                                            +--------------------+
```

---

## 6. Sample Advanced SQL Queries

### Pareto 80/20 Cumulative Spend Analysis (`sql/06_pareto_analysis.sql`)
```sql
WITH vendor_spend_summary AS (
    SELECT 
        v.vendor_id,
        v.vendor_name,
        SUM(poi.quantity * poi.unit_price * (1 - poi.discount)) AS vendor_spend
    FROM vendors v
    JOIN purchase_orders po ON v.vendor_id = po.vendor_id
    JOIN purchase_order_items poi ON po.po_id = poi.po_id
    GROUP BY v.vendor_id, v.vendor_name
),
ranked_spend AS (
    SELECT 
        vendor_name,
        vendor_spend,
        ROW_NUMBER() OVER (ORDER BY vendor_spend DESC) AS vendor_rank,
        SUM(vendor_spend) OVER (ORDER BY vendor_spend DESC) AS cumulative_spend,
        SUM(vendor_spend) OVER () AS grand_total_spend
    FROM vendor_spend_summary
)
SELECT 
    vendor_rank,
    vendor_name,
    ROUND(vendor_spend, 2) AS total_spend,
    ROUND(100.0 * cumulative_spend / grand_total_spend, 2) AS cumulative_spend_pct
FROM ranked_spend
ORDER BY vendor_rank;
```

---

## 7. Strategic Recommendations & Financial ROI ($6.2M Annual Savings)

1. **Quadrant 2 Contract Renegotiation**: Target 15 high-risk suppliers with a mandatory 3.5% price cut and 1.5% weekly delay penalty clause (**$3.25M Direct Savings**).
2. **Early Payment Cash Discount Capture**: Transition suppliers to 2/10 Net 30 terms to capture early payment discounts (**$2.10M Direct Savings**).
3. **Inventory Carrying Cost Reduction**: Cut average delivery lead time by 5 days through off-peak scheduling and regional buffers (**$850K Holding Cost Savings**).

---

## 8. How to Run the Project Locally

### Step 1: Clone Repository & Install Dependencies
```bash
git clone https://github.com/yourusername/ProcureFlow.git
cd ProcureFlow
pip install -r requirements.txt
```

### Step 2: Generate Raw Synthetic Data
```bash
python python/generate_data.py
```

### Step 3: Run Data Cleaning & Build Local SQLite DB
```bash
python python/clean_data.py
```

### Step 4: Launch Interactive Streamlit Dashboard
```bash
streamlit run dashboard/app.py
```

---

## 9. Interview Preparation & Resume Bullet Points

Detailed interview answers to 40+ questions, 2-minute elevator pitch, and 5-minute deep-dive walkthrough are available in [`interview_prep/interview_questions.md`](interview_prep/interview_questions.md).

### Tailored Resume Bullet Points

#### 1. EY Associate Consultant / Management Consulting Target
- **Analyzed $698M+ in procurement transactions across 37.8K purchase orders** using PostgreSQL (CTEs, Window Functions `RANK`/`LAG`/`SUM OVER`), identifying an 80.2% spend concentration among 20% of vendors and an overall 42.4% delivery delay rate.
- **Engineered a 4-Quadrant Strategic Supplier Matrix and root cause framework** using Python and SQL to isolate 15 chronic late-delivering vendors, formulating 7 recommendations projected to capture **$6.2M in annual financial savings**.
- **Built an interactive 4-page Streamlit & Plotly BI dashboard** featuring a dynamic financial ROI calculator to present executive-level spend distribution, regional bottlenecks, and payment lag metrics.

#### 2. Business Analyst Target
- **Performed end-to-end data quality engineering and business analytics on 37.8K procurement records**, imputing missing vendor ratings, correcting logical date anomalies, and deduplicating line items.
- **Developed 15 core procurement KPIs** (AOV, On-Time Delivery Rate, Vendor Concentration Ratio, Payment Processing Lag) in SQL, validating mathematical accuracy across database tables.
- **Designed custom Plotly dashboards and SQL views** to track Month-over-Month spend growth and rolling lead time averages across 8 product categories and 6 global regions.

#### 3. Operations Analyst Target
- **Mapped the end-to-end purchasing lifecycle** (PO Creation $\rightarrow$ Delivery $\rightarrow$ Payment) across 48 department locations, identifying a 20.1-day average lead time bottleneck in Raw Materials and Heavy Machinery.
- **Formulated operational improvements** including automated quarterly supplier scorecards, dual-sourcing policies, and off-peak scheduling to reduce delivery delay rates by 15%.
