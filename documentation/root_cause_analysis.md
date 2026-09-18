# Consulting Root Cause Analysis - ProcureFlow

## Framework Overview
To move beyond surface-level reporting and discover the structural drivers of procurement inefficiencies at GlobalProcure Corp, the consulting team deployed a **Structured Root Cause Analysis** utilizing two management consulting frameworks:
1. **The 5 Whys Framework**
2. **Ishikawa (Fishbone) Cause-and-Effect Analysis**

---

## 1. Primary Operational Problem: Severe Delivery Delays
**Observed Metric**: 42.37% of delivered purchase orders are delayed past contractually expected dates, with average lead times reaching 20.1 days (vs. 15.0 day target).

### The 5 Whys Root Cause Investigation

- **Why 1: Why are 42.4% of purchase orders delayed?**
  - *Finding*: Delivery delays are concentrated in 15 chronic underperforming vendors and 2 specific product categories (Raw Materials & Heavy Machinery).
- **Why 2: Why are these 15 vendors consistently delivering late?**
  - *Finding*: Contracts with these suppliers lack enforced delivery SLA penalty clauses, and order volumes are allocated without reviewing past lead time performance.
- **Why 3: Why do buyers continue placing high order volumes with late suppliers?**
  - *Finding*: Procurement teams lack real-time supplier performance visibility, leading buyers to favor historical single-source relationships.
- **Why 4: Why are buyers relying on historical single-source relationships?**
  - *Finding*: 80.2% of global procurement spend is concentrated among the top 20% of vendors (30 vendors) due to an absence of category multi-sourcing guidelines.
- **Why 5: What is the Root Cause?**
  - *Root Cause Definition*: **Decentralized procurement governance without performance-linked supplier scorecards, combined with extreme vendor concentration in unmonitored supplier contracts.**

---

## 2. Fishbone (Ishikawa) Diagram Mapping

```
                       PROCUREMENT DELAY & COST DRIVERS
  
   PEOPLE / GOVERNANCE                PROCESS / SLAS
   ┌───────────────────────┐          ┌───────────────────────┐
   │ Decentralized buyers  │          │ No SLA penalty clauses│
   │ No KPI scorecards     │          │ Unmonitored lead times│
   │ Single-source bias    │          │ Manual PO approvals   │
   └───────────┬───────────┘          └───────────┬───────────┘
               │                                  │
               ├──────────────────────────────────┼───────────────► PRIMARY ISSUE:
               │                                  │                 42.4% Order Delays &
   ┌───────────┴───────────┐          ┌───────────┴───────────┐     $698.7M Unoptimized Spend
   │ Dominant vendor focus │          │ LATAM/NA shipping lag │
   │ No price benchmarks   │          │ Peak Q3/Q4 surge      │
   │ Spot market reliance  │          │ Raw Material bottleneck│
   └───────────────────────┘          └───────────────────────┘
   SUPPLIERS / CONTRACTS              ENVIRONMENT / LOGISTICS
```

---

## 3. Empirical Data Validation of Root Causes

| Hypothesis Tested | Analytical Technique Used | Empirically Confirmed? | Data Evidence |
| :--- | :--- | :--- | :--- |
| **H1: Vendor Concentration Drives Delays** | Window Function Pareto Analysis (`SUM OVER`) | **CONFIRMED** | Top 20% of vendors receive 80.2% of spend ($560.5M). 15 chronic vendors control $85M+ in spend with 45%+ delay rates. |
| **H2: Order Priority Causes Delay Spikes** | Conditional Aggregation by Priority | **REJECTED** | Critical priority orders have a 38.9% delay rate, proving that expediting tags do not resolve vendor capacity constraints. |
| **H3: Seasonal Demand Congestion** | Time-Series Monthly Aggregation | **CONFIRMED** | Q3/Q4 order volumes surge by 35%, increasing average lead times from 18.2 days to 23.8 days. |
| **H4: Regional Shipping Disparities** | Heatmap Matrix Aggregation | **CONFIRMED** | Raw Materials shipped to Latin America and North America show the highest delay rates (56.4%–57.3%). |
