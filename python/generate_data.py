"""
ProcureFlow Synthetic Dataset Generator
Generates realistic procurement data for ProcureFlow: Procurement & Vendor Performance Analytics project.
Includes 7 relational tables with realistic business logic, embedded operational bottlenecks, and data quality flaws.
"""

import os
import random
import numpy as np
import pandas as pd
from datetime import datetime, timedelta

# Set random seed for reproducibility
np.random.seed(42)
random.seed(42)

RAW_DATA_DIR = os.path.join("data", "raw")
os.makedirs(RAW_DATA_DIR, exist_ok=True)

print("Starting ProcureFlow Synthetic Data Generation...")

# ==============================================================================
# 1. VENDORS (150 vendors)
# ==============================================================================
categories_list = [
    'Raw Materials', 'Electronics', 'Heavy Machinery', 'Office Supplies',
    'Logistics Services', 'Packaging & Storage', 'IT Hardware', 'Chemicals'
]

regions_list = [
    'North America', 'Europe', 'Asia-Pacific', 'Latin America', 'Middle East', 'Africa'
]

payment_terms_list = ['Net 30', 'Net 60', 'Net 90', 'Immediate', '2/10 Net 30']

# Generate 150 vendor profiles
vendor_names_prefix = [
    'Apex', 'Global', 'Titan', 'Nexus', 'Vanguard', 'Omega', 'Precision', 'Atlas',
    'Zenith', 'Pinnacle', 'Sterling', 'Quantum', 'Horizon', 'Matrix', 'Summit',
    'Beacon', 'Crest', 'Velocity', 'Frontier', 'Dynamic', 'Synergy', 'Integrity',
    'Prime', 'Core', 'Starlight', 'Olympus', 'Trident', 'Valiant', 'Alpha', 'Bravura'
]
vendor_names_suffix = [
    'Industries', 'Supplies', 'Logistics', 'Components', 'Solutions', 'Technologies',
    'Corporation', 'Enterprises', 'Group', 'Partners', 'International', 'Systems',
    'Trading', 'Manufacturing', 'Services', 'Global'
]

vendors_data = []
all_vendor_names = set()

while len(all_vendor_names) < 150:
    name = f"{random.choice(vendor_names_prefix)} {random.choice(vendor_names_suffix)}"
    all_vendor_names.add(name)

all_vendor_names = list(all_vendor_names)

# Designate specific "Problem Vendors" (15 vendors with chronic delivery delays & poor quality)
problem_vendor_ids = set([12, 18, 27, 34, 45, 53, 68, 77, 89, 94, 104, 118, 125, 132, 141])

# Designate "High Spend Dominant Vendors" (Top 20 vendors that get ~75% of contract allocation)
dominant_vendor_ids = set(range(1, 21))

for vid in range(1, 151):
    vname = all_vendor_names[vid - 1]
    
    # Introduce intentional casing inconsistency for raw data profiling
    c_rand = random.random()
    vcat = random.choice(categories_list)
    if c_rand < 0.08:
        vcat_raw = vcat.lower()
    elif c_rand < 0.12:
        vcat_raw = vcat.upper()
    else:
        vcat_raw = vcat
        
    r_rand = random.random()
    vregion = random.choice(regions_list)
    if r_rand < 0.08:
        vregion_raw = vregion.lower()
    elif r_rand < 0.12:
        vregion_raw = vregion.upper()
    else:
        vregion_raw = vregion

    # Start date between 2020 and 2023
    start_days_ago = random.randint(730, 1825)
    contract_start = datetime(2024, 1, 1) - timedelta(days=start_days_ago)
    contract_end = contract_start + timedelta(days=random.choice([365, 730, 1095, 1460]))

    # Ratings (1.0 - 5.0)
    if vid in problem_vendor_ids:
        rating = round(random.uniform(1.8, 3.2), 1)
    else:
        rating = round(random.uniform(3.5, 4.9), 1)
        
    # Introduce NULL ratings in ~6% of records for data quality testing
    if random.random() < 0.06:
        rating = None

    payment_terms = random.choice(payment_terms_list)

    vendors_data.append({
        'vendor_id': vid,
        'vendor_name': vname,
        'vendor_category': vcat_raw,
        'region': vregion_raw,
        'contract_start_date': contract_start.strftime('%Y-%m-%d'),
        'contract_end_date': contract_end.strftime('%Y-%m-%d'),
        'vendor_rating': rating,
        'payment_terms': payment_terms
    })

df_vendors = pd.DataFrame(vendors_data)
df_vendors.to_csv(os.path.join(RAW_DATA_DIR, "vendors.csv"), index=False)
print(f"Generated {len(df_vendors)} vendors.")

# ==============================================================================
# 2. PRODUCTS (600 products)
# ==============================================================================
subcategories_map = {
    'Raw Materials': ['Steel Sheets', 'Aluminum Ingot', 'Copper Wire', 'Resin Granules', 'Industrial Rubber'],
    'Electronics': ['Microcontrollers', 'Circuit Boards', 'Power Units', 'Sensors', 'Display Panels'],
    'Heavy Machinery': ['Hydraulic Pumps', 'Conveyor Motors', 'Industrial Compressors', 'Robotic Arms', 'Generators'],
    'Office Supplies': ['Printer Toner', 'Ergonomic Chairs', 'Paper Stock', 'Filing Systems', 'Desk Accessories'],
    'Logistics Services': ['Freight Container', 'Express Courier', 'Warehousing Pallet', 'Cold Chain Shipping', 'Customs Clearance'],
    'Packaging & Storage': ['Corrugated Boxes', 'Bubble Wrap Rolls', 'Plastic Drums', 'Wooden Pallets', 'Strapping Tape'],
    'IT Hardware': ['Enterprise Servers', 'Network Switches', 'Workstation Laptops', 'Storage Arrays', 'Monitors'],
    'Chemicals': ['Industrial Solvents', 'Polymer Additives', 'Cleaning Reagents', 'Lubricants', 'Catalysts']
}

supplier_types = ['Primary', 'Secondary', 'Spot Market']

products_data = []
pid = 1
for cat, subcats in subcategories_map.items():
    for sub in subcats:
        # Create 15 items per subcategory = 8 * 5 * 15 = 600 products
        for i in range(1, 16):
            pname = f"{sub} - Grade {chr(65 + (i % 5))}-{i:02d}"
            
            # Base cost varies by category
            if cat == 'Heavy Machinery':
                base_cost = random.uniform(800, 4500)
            elif cat == 'IT Hardware':
                base_cost = random.uniform(400, 2500)
            elif cat == 'Electronics':
                base_cost = random.uniform(50, 600)
            elif cat == 'Chemicals':
                base_cost = random.uniform(80, 750)
            elif cat == 'Raw Materials':
                base_cost = random.uniform(30, 350)
            elif cat == 'Logistics Services':
                base_cost = random.uniform(150, 1200)
            elif cat == 'Packaging & Storage':
                base_cost = random.uniform(5, 80)
            else: # Office Supplies
                base_cost = random.uniform(10, 250)
                
            unit_cost = round(base_cost, 2)
            stype = random.choice(supplier_types)

            products_data.append({
                'product_id': pid,
                'product_name': pname,
                'category': cat,
                'subcategory': sub,
                'unit_cost': unit_cost,
                'supplier_type': stype
            })
            pid += 1

df_products = pd.DataFrame(products_data)
df_products.to_csv(os.path.join(RAW_DATA_DIR, "products.csv"), index=False)
print(f"Generated {len(df_products)} products.")

# ==============================================================================
# 3. DEPARTMENTS (8 departments x 6 regions = 48 department locations)
# ==============================================================================
dept_names = ['Operations', 'Supply Chain', 'IT Operations', 'Manufacturing', 'Facilities', 'R&D', 'Logistics', 'Corporate Admin']
bu_map = {
    'Operations': 'Global Operations',
    'Supply Chain': 'Global Operations',
    'Manufacturing': 'Global Operations',
    'Logistics': 'Global Operations',
    'IT Operations': 'Technology & Infrastructure',
    'R&D': 'Product Innovation',
    'Facilities': 'Corporate Services',
    'Corporate Admin': 'Corporate Services'
}

departments_data = []
did = 1
for r in regions_list:
    for dname in dept_names:
        departments_data.append({
            'department_id': did,
            'department_name': dname,
            'business_unit': bu_map[dname],
            'region': r
        })
        did += 1

df_departments = pd.DataFrame(departments_data)
df_departments.to_csv(os.path.join(RAW_DATA_DIR, "departments.csv"), index=False)
print(f"Generated {len(df_departments)} department locations.")

# ==============================================================================
# 4. PURCHASE ORDERS (~35,000 orders) & 5. PO ITEMS (~45,000 items)
# ==============================================================================
print("Generating Purchase Orders & Items...")

start_date = datetime(2024, 1, 1)
end_date = datetime(2025, 12, 31)
total_days = (end_date - start_date).days

po_list = []
po_items_list = []

po_id_counter = 10001
po_item_counter = 50001

statuses = ['Delivered', 'Delivered', 'Delivered', 'Delivered', 'Delivered', 'Delivered', 'Delivered', 'In Transit', 'Pending Approval', 'Cancelled']
priorities = ['Low', 'Medium', 'High', 'Critical']
priority_weights = [0.4, 0.4, 0.15, 0.05]

# To generate ~35,000 POs across 730 days, ~48 POs per day average
for day_idx in range(total_days + 1):
    current_date = start_date + timedelta(days=day_idx)
    month = current_date.month
    
    # Seasonal volume multiplier: Q3 & Q4 (months 8-11) have higher order volumes
    if month in [8, 9, 10, 11]:
        daily_count = random.randint(55, 75)
    elif month in [1, 2]:
        daily_count = random.randint(30, 42)
    else:
        daily_count = random.randint(40, 56)
        
    for _ in range(daily_count):
        # Pareto Distribution for Vendor Selection
        # 75% of orders go to the 20 dominant vendors; 25% go to remaining 130 vendors
        if random.random() < 0.75:
            vid = random.choice(list(dominant_vendor_ids))
        else:
            vid = random.randint(1, 150)
            
        did = random.randint(1, len(df_departments))
        status = random.choice(statuses)
        priority = random.choices(priorities, weights=priority_weights)[0]
        
        # Expected lead time based on vendor & priority
        base_lead_days = random.randint(10, 30)
        if priority == 'Critical':
            expected_lead_days = max(5, base_lead_days - 7)
        elif priority == 'High':
            expected_lead_days = max(7, base_lead_days - 3)
        else:
            expected_lead_days = base_lead_days
            
        expected_delivery_date = current_date + timedelta(days=expected_lead_days)
        
        # Determine actual delivery date and delays
        if status == 'Delivered':
            # Is this vendor a problem vendor?
            if vid in problem_vendor_ids:
                # 45% chance of severe delay (10-35 days late)
                if random.random() < 0.45:
                    actual_delay = random.randint(10, 35)
                else:
                    actual_delay = random.randint(-2, 4)
            else:
                # Normal vendor: 10% chance of minor delay (1-7 days late)
                if random.random() < 0.10:
                    actual_delay = random.randint(1, 7)
                else:
                    actual_delay = random.randint(-4, 2)
                    
            # Q3/Q4 seasonal delay surge
            if month in [9, 10, 11] and random.random() < 0.15:
                actual_delay += random.randint(3, 10)
                
            actual_delivery_date = expected_delivery_date + timedelta(days=actual_delay)
            actual_delivery_str = actual_delivery_date.strftime('%Y-%m-%d')
        elif status in ['In Transit', 'Pending Approval']:
            actual_delivery_str = None
        else: # Cancelled
            actual_delivery_str = None

        # Data Quality Issue 1: Missing actual_delivery_date for ~0.5% delivered orders
        if status == 'Delivered' and random.random() < 0.005:
            actual_delivery_str = None
            
        # Data Quality Issue 2: Incorrect non-null actual_delivery_date on open orders (~0.3%)
        if status in ['In Transit', 'Pending Approval'] and random.random() < 0.003:
            actual_delivery_str = (expected_delivery_date + timedelta(days=2)).strftime('%Y-%m-%d')

        po_list.append({
            'po_id': po_id_counter,
            'vendor_id': vid,
            'department_id': did,
            'order_date': current_date.strftime('%Y-%m-%d'),
            'expected_delivery_date': expected_delivery_date.strftime('%Y-%m-%d'),
            'actual_delivery_date': actual_delivery_str,
            'status': status,
            'priority': priority
        })

        # Generate PO items (1 to 3 items per PO)
        num_items = random.choices([1, 2, 3], weights=[0.65, 0.25, 0.10])[0]
        chosen_products = random.sample(range(1, len(df_products) + 1), num_items)
        
        for pid in chosen_products:
            prod_row = df_products[df_products['product_id'] == pid].iloc[0]
            unit_cost = prod_row['unit_cost']
            
            # Unit price slightly fluctuates around base cost (-3% to +8%)
            unit_price = round(unit_cost * random.uniform(0.97, 1.08), 2)
            
            # Quantity depends on category cost
            if unit_cost > 1000:
                qty = random.randint(1, 10)
            elif unit_cost > 200:
                qty = random.randint(5, 50)
            else:
                qty = random.randint(20, 300)
                
            # Discount: 0% to 12%
            discount = round(random.choice([0.0, 0.0, 0.0, 0.02, 0.05, 0.08, 0.10, 0.12]), 2)
            
            # Data Quality Issue 3: Invalid Negative Quantity in 15 records
            if random.random() < 0.0003:
                qty = -abs(qty)

            po_items_list.append({
                'po_item_id': po_item_counter,
                'po_id': po_id_counter,
                'product_id': pid,
                'quantity': qty,
                'unit_price': unit_price,
                'discount': discount
            })
            po_item_counter += 1

        po_id_counter += 1

df_po = pd.DataFrame(po_list)
df_po_items = pd.DataFrame(po_items_list)

# Data Quality Issue 4: Duplicate PO Items (inserting 10 duplicate rows to test SQL deduplication)
duplicate_items = df_po_items.sample(10).copy()
duplicate_items['po_item_id'] = duplicate_items['po_item_id'] + 900000
df_po_items = pd.concat([df_po_items, duplicate_items], ignore_index=True)

df_po.to_csv(os.path.join(RAW_DATA_DIR, "purchase_orders.csv"), index=False)
df_po_items.to_csv(os.path.join(RAW_DATA_DIR, "purchase_order_items.csv"), index=False)
print(f"Generated {len(df_po)} purchase orders and {len(df_po_items)} PO items.")

# ==============================================================================
# 6. PAYMENTS (1 payment per delivered PO)
# ==============================================================================
print("Generating Payments...")

# Calculate total PO values
df_po_items['net_line_total'] = df_po_items['quantity'] * df_po_items['unit_price'] * (1 - df_po_items['discount'])
po_totals = df_po_items.groupby('po_id')['net_line_total'].sum().round(2).to_dict()

payments_list = []
payment_id_counter = 70001
payment_methods = ['ACH', 'Wire Transfer', 'Credit Card', 'Check']

delivered_pos = df_po[df_po['status'] == 'Delivered'].copy()

for _, row in delivered_pos.iterrows():
    poid = row['po_id']
    total_val = po_totals.get(poid, 0.0)
    
    if total_val <= 0:
        continue
        
    actual_del_str = row['actual_delivery_date']
    if actual_del_str and isinstance(actual_del_str, str):
        del_date = datetime.strptime(actual_del_str, '%Y-%m-%d')
    else:
        del_date = datetime.strptime(row['order_date'], '%Y-%m-%d') + timedelta(days=20)
        
    # Payment lag: 15 to 75 days after delivery
    payment_lag = random.randint(15, 75)
    payment_date = del_date + timedelta(days=payment_lag)
    
    if payment_lag > 60:
        p_status = random.choice(['Overdue', 'Paid', 'Paid'])
    elif payment_lag > 45:
        p_status = random.choice(['Paid', 'Paid', 'Paid', 'Pending'])
    else:
        p_status = 'Paid'
        
    # Data Quality Issue 5: Missing payment amount on 12 records
    p_amount = total_val
    if random.random() < 0.0008:
        p_amount = None
        
    # Data Quality Issue 6: Payment date before order date in 5 erroneous records
    if random.random() < 0.0003:
        payment_date = datetime.strptime(row['order_date'], '%Y-%m-%d') - timedelta(days=5)

    payments_list.append({
        'payment_id': payment_id_counter,
        'po_id': poid,
        'payment_date': payment_date.strftime('%Y-%m-%d'),
        'payment_amount': p_amount,
        'payment_status': p_status,
        'payment_method': random.choice(payment_methods)
    })
    payment_id_counter += 1

df_payments = pd.DataFrame(payments_list)
df_payments.to_csv(os.path.join(RAW_DATA_DIR, "payments.csv"), index=False)
print(f"Generated {len(df_payments)} payment records.")

# ==============================================================================
# 7. VENDOR PERFORMANCE (Quarterly evaluations: 8 quarters 2024-2025)
# ==============================================================================
print("Generating Vendor Quarterly Evaluations...")

eval_dates = [
    '2024-03-31', '2024-06-30', '2024-09-30', '2024-12-31',
    '2025-03-31', '2025-06-30', '2025-09-30', '2025-12-31'
]

perf_list = []
for vid in range(1, 151):
    is_problem = (vid in problem_vendor_ids)
    
    for edate in eval_dates:
        if is_problem:
            q_score = round(random.uniform(52.0, 75.0), 1)
            d_score = round(random.uniform(40.0, 68.0), 1)
            c_score = round(random.uniform(60.0, 80.0), 1)
        else:
            q_score = round(random.uniform(82.0, 99.0), 1)
            d_score = round(random.uniform(85.0, 99.5), 1)
            c_score = round(random.uniform(88.0, 100.0), 1)
            
        perf_list.append({
            'vendor_id': vid,
            'evaluation_date': edate,
            'quality_score': q_score,
            'delivery_score': d_score,
            'compliance_score': c_score
        })

df_perf = pd.DataFrame(perf_list)
df_perf.to_csv(os.path.join(RAW_DATA_DIR, "vendor_performance.csv"), index=False)
print(f"Generated {len(df_perf)} vendor performance evaluation records.")

print("\nSUCCESS: All 7 raw synthetic datasets generated in data/raw/")
