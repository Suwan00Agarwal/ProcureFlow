# Data Dictionary - ProcureFlow Relational Schema

## Overview
The ProcureFlow database consists of **7 primary relational tables** modeling the end-to-end procurement lifecycle from vendor contracting to invoice settlement.

---

### 1. `vendors` Table
Stores master information and baseline ratings for approved suppliers.

| Column Name | Data Type | Key / Constraint | Description | Domain Values / Range |
| :--- | :--- | :--- | :--- | :--- |
| `vendor_id` | INTEGER | PRIMARY KEY | Unique identifier for each vendor | 1 to 150 |
| `vendor_name` | VARCHAR(100) | NOT NULL | Official registered business name | Fictional vendor names |
| `vendor_category` | VARCHAR(50) | NOT NULL | Primary category of products/services supplied | Raw Materials, Electronics, etc. |
| `region` | VARCHAR(50) | NOT NULL | Geographic region of vendor headquarters | North America, Europe, Asia-Pacific, etc. |
| `contract_start_date` | DATE | NOT NULL | Date contract agreement initiated | YYYY-MM-DD (2020–2023) |
| `contract_end_date` | DATE | NOT NULL | Contract expiration date | YYYY-MM-DD |
| `vendor_rating` | NUMERIC(2,1) | CHECK (1.0–5.0) | Standardized vendor rating score | 1.0 to 5.0 (Imputed if null) |
| `payment_terms` | VARCHAR(30) | NOT NULL | Agreed invoice payment terms | Net 30, Net 60, Net 90, Immediate, 2/10 Net 30 |

---

### 2. `products` Table
Catalog of goods and services available for procurement.

| Column Name | Data Type | Key / Constraint | Description | Domain Values / Range |
| :--- | :--- | :--- | :--- | :--- |
| `product_id` | INTEGER | PRIMARY KEY | Unique product SKU identifier | 1 to 600 |
| `product_name` | VARCHAR(150) | NOT NULL | Descriptive product item title | e.g. Microcontrollers - Grade A-01 |
| `category` | VARCHAR(50) | NOT NULL | Broad product classification | 8 core categories |
| `subcategory` | VARCHAR(50) | NOT NULL | Specific item sub-classification | 40 subcategories |
| `unit_cost` | NUMERIC(10,2) | CHECK ($\ge 0$) | Baseline catalog cost per unit ($) | $5.00 to $4,500.00 |
| `supplier_type` | VARCHAR(30) | NOT NULL | Contracting tier | Primary, Secondary, Spot Market |

---

### 3. `departments` Table
Organizational units generating purchase requests.

| Column Name | Data Type | Key / Constraint | Description | Domain Values / Range |
| :--- | :--- | :--- | :--- | :--- |
| `department_id` | INTEGER | PRIMARY KEY | Unique department location ID | 1 to 48 |
| `department_name` | VARCHAR(50) | NOT NULL | Functional team name | Operations, Supply Chain, R&D, etc. |
| `business_unit` | VARCHAR(50) | NOT NULL | Executive division | Global Operations, Tech, Corp Services |
| `region` | VARCHAR(50) | NOT NULL | Geographic operating region | 6 global regions |

---

### 4. `purchase_orders` Table
Header records for purchase transactions.

| Column Name | Data Type | Key / Constraint | Description | Domain Values / Range |
| :--- | :--- | :--- | :--- | :--- |
| `po_id` | INTEGER | PRIMARY KEY | Unique Purchase Order ID | 10001 to 47834 |
| `vendor_id` | INTEGER | FK $\rightarrow$ `vendors` | Vendor receiving the order | 1 to 150 |
| `department_id` | INTEGER | FK $\rightarrow$ `departments` | Ordering department location | 1 to 48 |
| `order_date` | DATE | NOT NULL | Date PO issued | YYYY-MM-DD (2024-01-01 to 2025-12-31) |
| `expected_delivery_date`| DATE | CHECK ($\ge$ order_date) | Contractual agreed delivery date | YYYY-MM-DD |
| `actual_delivery_date` | DATE | NULLABLE | Actual date goods received | YYYY-MM-DD (NULL if open order) |
| `status` | VARCHAR(25) | CHECK IN (...) | Fulfillment status | Delivered, In Transit, Pending Approval, Cancelled |
| `priority` | VARCHAR(20) | CHECK IN (...) | Fulfillment urgency level | Low, Medium, High, Critical |

---

### 5. `purchase_order_items` Table
Line items associated with each purchase order.

| Column Name | Data Type | Key / Constraint | Description | Domain Values / Range |
| :--- | :--- | :--- | :--- | :--- |
| `po_item_id` | INTEGER | PRIMARY KEY | Line item primary key | 50001 to 104853 |
| `po_id` | INTEGER | FK $\rightarrow$ `purchase_orders` | Parent PO header ID | 10001 to 47834 |
| `product_id` | INTEGER | FK $\rightarrow$ `products` | Product SKU ID | 1 to 600 |
| `quantity` | INTEGER | CHECK ($> 0$) | Number of units ordered | 1 to 500 |
| `unit_price` | NUMERIC(10,2) | CHECK ($\ge 0$) | Negotiated purchase price per unit ($) | $4.85 to $4,650.00 |
| `discount` | NUMERIC(4,2) | CHECK (0.0–1.0) | Discount rate applied | 0.00 to 0.12 (0% to 12%) |

---

### 6. `payments` Table
Financial disbursement records for fulfilled purchase orders.

| Column Name | Data Type | Key / Constraint | Description | Domain Values / Range |
| :--- | :--- | :--- | :--- | :--- |
| `payment_id` | INTEGER | PRIMARY KEY | Unique payment transaction ID | 70001 to 96411 |
| `po_id` | INTEGER | FK $\rightarrow$ `purchase_orders` | Associated fulfilled PO ID | 10001 to 47834 |
| `payment_date` | DATE | NOT NULL | Invoice payment execution date | YYYY-MM-DD |
| `payment_amount` | NUMERIC(12,2)| CHECK ($\ge 0$) | Net payment amount disbursed ($) | Equal to PO net total |
| `payment_status` | VARCHAR(20) | CHECK IN (...) | Settlement status | Paid, Pending, Overdue, Failed |
| `payment_method` | VARCHAR(30) | NOT NULL | Financial transfer channel | ACH, Wire Transfer, Credit Card, Check |

---

### 7. `vendor_performance` Table
Quarterly evaluation scorecards for suppliers.

| Column Name | Data Type | Key / Constraint | Description | Domain Values / Range |
| :--- | :--- | :--- | :--- | :--- |
| `vendor_id` | INTEGER | PK, FK $\rightarrow$ `vendors` | Vendor evaluated | 1 to 150 |
| `evaluation_date` | DATE | PK | Quarter-end audit date | YYYY-MM-DD (8 quarters) |
| `quality_score` | NUMERIC(5,2)| CHECK (0–100) | Quality audit score | 40.00 to 100.00 |
| `delivery_score` | NUMERIC(5,2)| CHECK (0–100) | On-time delivery compliance score | 35.00 to 100.00 |
| `compliance_score` | NUMERIC(5,2)| CHECK (0–100) | Regulatory & SLA compliance score | 50.00 to 100.00 |
