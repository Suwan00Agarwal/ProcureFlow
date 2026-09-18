"""
ProcureFlow - Interactive Consulting & Vendor Performance Analytics Dashboard
Built with Streamlit and Plotly for executive presentation and business analysis.
"""

import os
import sqlite3
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

st.set_page_config(
    page_title="ProcureFlow | Procurement & Vendor Performance Analytics",
    page_icon="📦",
    layout="wide",
    initial_sidebar_state="expanded"
)

DB_PATH = "procureflow.db"

@st.cache_data(ttl=600)
def load_data(query):
    if not os.path.exists(DB_PATH):
        st.error("Database procureflow.db not found. Please run `python python/clean_data.py` first.")
        st.stop()
    conn = sqlite3.connect(DB_PATH)
    df = pd.read_sql_query(query, conn)
    conn.close()
    return df

# CSS Styling for Consulting Theme
st.markdown("""
<style>
    .main-header { font-size: 2.2rem; font-weight: 700; color: #1E3A8A; margin-bottom: 0px; }
    .sub-header { font-size: 1.1rem; color: #4B5563; margin-bottom: 20px; }
    .kpi-card { background-color: #F8FAFC; border-left: 5px solid #1E3A8A; padding: 15px; border-radius: 6px; box-shadow: 0 1px 3px rgba(0,0,0,0.1); }
    .kpi-title { font-size: 0.85rem; font-weight: 600; color: #64748B; text-transform: uppercase; }
    .kpi-value { font-size: 1.7rem; font-weight: 700; color: #0F172A; }
    .kpi-subtext { font-size: 0.8rem; color: #10B981; font-weight: 500; }
    .kpi-subtext-alert { font-size: 0.8rem; color: #EF4444; font-weight: 500; }
</style>
""", unsafe_allow_html=True)

# Sidebar Navigation & Global Filters
st.sidebar.image("https://img.icons8.com/color/96/000000/logistics.png", width=70)
st.sidebar.title("ProcureFlow Analytics")
st.sidebar.caption("EY Consulting Practice | Procurement Optimization")

nav_page = st.sidebar.radio(
    "Select Analysis Page:",
    [
        "Page 1: Executive Overview",
        "Page 2: Vendor Performance & Risk",
        "Page 3: Procurement Efficiency",
        "Page 4: Consulting Insights & ROI"
    ]
)

st.sidebar.markdown("---")
st.sidebar.subheader("Global Filters")

# Global Filter Data
df_regions_raw = load_data("SELECT DISTINCT dept_region FROM vw_po_header_summary ORDER BY dept_region")
region_options = ["All Regions"] + list(df_regions_raw['dept_region'])
selected_region = st.sidebar.selectbox("Region Filter:", region_options)

df_cats_raw = load_data("SELECT DISTINCT vendor_category FROM vw_po_header_summary ORDER BY vendor_category")
category_options = ["All Categories"] + list(df_cats_raw['vendor_category'])
selected_category = st.sidebar.selectbox("Category Filter:", category_options)

# Dynamic WHERE clause builder
def build_where(extra_conditions=None):
    clauses = []
    if selected_region != "All Regions":
        clauses.append(f"dept_region = '{selected_region}'")
    if selected_category != "All Categories":
        clauses.append(f"vendor_category = '{selected_category}'")
    if extra_conditions:
        if isinstance(extra_conditions, list):
            clauses.extend(extra_conditions)
        else:
            clauses.append(extra_conditions)
    if clauses:
        return "WHERE " + " AND ".join(clauses)
    return ""

# ==============================================================================
# PAGE 1: EXECUTIVE OVERVIEW
# ==============================================================================
if nav_page == "Page 1: Executive Overview":
    st.markdown('<div class="main-header">ProcureFlow Executive Overview</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-header">Macro-level procurement KPIs, spend distribution, and historical volume trends</div>', unsafe_allow_html=True)

    # Executive KPI Scorecard
    kpi_sql = f"""
    SELECT 
        COUNT(DISTINCT po_id) AS total_orders,
        COALESCE(SUM(total_po_value), 0) AS total_spend,
        COALESCE(AVG(total_po_value), 0) AS avg_order_value,
        COALESCE(AVG(actual_lead_time_days), 0) AS avg_lead_time,
        ROUND(100.0 * SUM(CASE WHEN status = 'Delivered' AND is_delayed = 0 THEN 1 ELSE 0 END) / 
              NULLIF(SUM(CASE WHEN status = 'Delivered' THEN 1 ELSE 0 END), 0), 1) AS on_time_pct,
        ROUND(100.0 * SUM(CASE WHEN status = 'Delivered' AND is_delayed = 1 THEN 1 ELSE 0 END) / 
              NULLIF(SUM(CASE WHEN status = 'Delivered' THEN 1 ELSE 0 END), 0), 1) AS delay_pct,
        COUNT(DISTINCT vendor_id) AS vendor_count
    FROM vw_po_header_summary
    {build_where()};
    """
    kpi_df = load_data(kpi_sql)

    col1, col2, col3, col4, col5, col6 = st.columns(6)
    
    with col1:
        st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-title">Total Spend</div>
            <div class="kpi-value">${kpi_df['total_spend'].iloc[0]/1e6:.1f}M</div>
            <div class="kpi-subtext">37.8K Total Orders</div>
        </div>
        """, unsafe_allow_html=True)
        
    with col2:
        st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-title">Avg Order Value</div>
            <div class="kpi-value">${kpi_df['avg_order_value'].iloc[0]/1e3:.1f}K</div>
            <div class="kpi-subtext">Per PO Header</div>
        </div>
        """, unsafe_allow_html=True)

    with col3:
        on_time = kpi_df['on_time_pct'].iloc[0] or 0.0
        st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-title">On-Time Delivery</div>
            <div class="kpi-value">{on_time:.1f}%</div>
            <div class="kpi-subtext-alert">Target: 85.0%</div>
        </div>
        """, unsafe_allow_html=True)

    with col4:
        st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-title">Avg Lead Time</div>
            <div class="kpi-value">{kpi_df['avg_lead_time'].iloc[0]:.1f} days</div>
            <div class="kpi-subtext">Door-to-Door</div>
        </div>
        """, unsafe_allow_html=True)

    with col5:
        delay = kpi_df['delay_pct'].iloc[0] or 0.0
        st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-title">Delayed Orders</div>
            <div class="kpi-value">{delay:.1f}%</div>
            <div class="kpi-subtext-alert">Operational Lag</div>
        </div>
        """, unsafe_allow_html=True)

    with col6:
        st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-title">Active Vendors</div>
            <div class="kpi-value">{kpi_df['vendor_count'].iloc[0]}</div>
            <div class="kpi-subtext">Global Supplier Base</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # Monthly Trend Line Chart
    trend_sql = f"""
    SELECT 
        strftime('%Y-%m', order_date) AS order_month,
        SUM(total_po_value) AS monthly_spend,
        COUNT(po_id) AS order_count,
        AVG(actual_lead_time_days) AS avg_lead_time
    FROM vw_po_header_summary
    {build_where()}
    GROUP BY strftime('%Y-%m', order_date)
    ORDER BY order_month;
    """
    trend_df = load_data(trend_sql)

    fig_trend = go.Figure()
    fig_trend.add_trace(go.Bar(
        x=trend_df['order_month'],
        y=trend_df['monthly_spend'] / 1e6,
        name='Spend ($M)',
        marker_color='#1E3A8A'
    ))
    fig_trend.add_trace(go.Scatter(
        x=trend_df['order_month'],
        y=trend_df['avg_lead_time'],
        name='Avg Lead Time (Days)',
        yaxis='y2',
        line=dict(color='#E11D48', width=3)
    ))
    fig_trend.update_layout(
        title='Monthly Procurement Spend ($M) and Average Delivery Lead Time (Days)',
        xaxis_title='Order Month',
        yaxis_title='Procurement Spend ($ Millions)',
        yaxis2=dict(title='Avg Lead Time (Days)', overlaying='y', side='right'),
        template='plotly_white',
        height=420
    )
    st.plotly_chart(fig_trend, use_container_width=True)

    col_a, col_b = st.columns(2)
    with col_a:
        cat_sql = f"""
        SELECT 
            vendor_category,
            SUM(total_po_value) AS total_spend
        FROM vw_po_header_summary
        {build_where()}
        GROUP BY vendor_category
        ORDER BY total_spend DESC;
        """
        cat_df = load_data(cat_sql)
        fig_cat = px.bar(
            cat_df,
            x='total_spend',
            y='vendor_category',
            orientation='h',
            title='Procurement Spend Distribution by Product Category',
            labels={'total_spend': 'Total Spend ($)', 'vendor_category': 'Category'},
            color='total_spend',
            color_continuous_scale='Blues'
        )
        fig_cat.update_layout(template='plotly_white', height=380, showlegend=False)
        st.plotly_chart(fig_cat, use_container_width=True)

    with col_b:
        reg_sql = f"""
        SELECT 
            dept_region AS region,
            SUM(total_po_value) AS total_spend
        FROM vw_po_header_summary
        {build_where()}
        GROUP BY dept_region
        ORDER BY total_spend DESC;
        """
        reg_df = load_data(reg_sql)
        fig_reg = px.pie(
            reg_df,
            values='total_spend',
            names='region',
            title='Regional Spend Allocation Share (%)',
            hole=0.4,
            color_discrete_sequence=px.colors.qualitative.Set1
        )
        fig_reg.update_layout(template='plotly_white', height=380)
        st.plotly_chart(fig_reg, use_container_width=True)

# ==============================================================================
# PAGE 2: VENDOR PERFORMANCE & RISK
# ==============================================================================
elif nav_page == "Page 2: Vendor Performance & Risk":
    st.markdown('<div class="main-header">Vendor Performance & Concentration Risk Matrix</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-header">Evaluating supplier reliability, spend concentration, and strategic quadrant segmentation</div>', unsafe_allow_html=True)

    v_sql = f"""
    SELECT 
        vendor_id,
        vendor_name,
        vendor_category,
        vendor_region,
        COUNT(po_id) AS order_count,
        SUM(total_po_value) AS total_spend,
        AVG(actual_lead_time_days) AS avg_lead_time,
        ROUND(100.0 * SUM(CASE WHEN status = 'Delivered' AND is_delayed = 0 THEN 1 ELSE 0 END) / 
              NULLIF(SUM(CASE WHEN status = 'Delivered' THEN 1 ELSE 0 END), 0), 1) AS on_time_rate_pct
    FROM vw_po_header_summary
    {build_where()}
    GROUP BY vendor_id, vendor_name, vendor_category, vendor_region;
    """
    df_vendor = load_data(v_sql)

    avg_spend_b = df_vendor['total_spend'].mean()
    avg_ontime_b = df_vendor['on_time_rate_pct'].mean()

    def classify_quadrant(r):
        if r['total_spend'] >= avg_spend_b and r['on_time_rate_pct'] >= avg_ontime_b:
            return 'Q1: Strategic Partners (High Spend / High Perf)'
        elif r['total_spend'] >= avg_spend_b and r['on_time_rate_pct'] < avg_ontime_b:
            return 'Q2: High Risk Suppliers (High Spend / Low Perf)'
        elif r['total_spend'] < avg_spend_b and r['on_time_rate_pct'] >= avg_ontime_b:
            return 'Q3: Growth Candidates (Low Spend / High Perf)'
        else:
            return 'Q4: Phase-Out Targets (Low Spend / Low Perf)'

    df_vendor['quadrant'] = df_vendor.apply(classify_quadrant, axis=1)

    fig_scatter = px.scatter(
        df_vendor,
        x='total_spend',
        y='on_time_rate_pct',
        size='order_count',
        color='quadrant',
        hover_name='vendor_name',
        hover_data=['vendor_category', 'avg_lead_time'],
        title='Vendor Spend ($) vs On-Time Delivery Rate (%) Scatter Matrix',
        labels={'total_spend': 'Total Spend ($)', 'on_time_rate_pct': 'On-Time Delivery Rate (%)'},
        color_discrete_map={
            'Q1: Strategic Partners (High Spend / High Perf)': '#10B981',
            'Q2: High Risk Suppliers (High Spend / Low Perf)': '#EF4444',
            'Q3: Growth Candidates (Low Spend / High Perf)': '#3B82F6',
            'Q4: Phase-Out Targets (Low Spend / Low Perf)': '#F59E0B'
        }
    )
    fig_scatter.add_vline(x=avg_spend_b, line_dash="dash", line_color="gray", annotation_text="Avg Spend Threshold")
    fig_scatter.add_hline(y=avg_ontime_b, line_dash="dash", line_color="gray", annotation_text="Avg On-Time Threshold")
    fig_scatter.update_layout(template='plotly_white', height=480)
    st.plotly_chart(fig_scatter, use_container_width=True)

    col_p1, col_p2 = st.columns([1.2, 0.8])
    with col_p1:
        st.subheader("Top 25 Vendor Spend & Pareto Cumulative Concentration")
        pareto_sql = """
        WITH v_spend AS (
            SELECT 
                vendor_name,
                SUM(total_po_value) AS spend
            FROM vw_po_header_summary
            GROUP BY vendor_name
        ),
        ranked AS (
            SELECT 
                vendor_name,
                spend,
                SUM(spend) OVER (ORDER BY spend DESC) AS cum_spend,
                SUM(spend) OVER () AS total_spend
            FROM v_spend
        )
        SELECT 
            vendor_name,
            spend,
            ROUND(100.0 * cum_spend / total_spend, 1) AS cum_pct
        FROM ranked
        ORDER BY spend DESC
        LIMIT 25;
        """
        df_par = load_data(pareto_sql)
        fig_par = go.Figure()
        fig_par.add_trace(go.Bar(
            x=df_par['vendor_name'],
            y=df_par['spend'] / 1e6,
            name='Spend ($M)',
            marker_color='#1E3A8A'
        ))
        fig_par.add_trace(go.Scatter(
            x=df_par['vendor_name'],
            y=df_par['cum_pct'],
            name='Cumulative Spend %',
            yaxis='y2',
            line=dict(color='#E11D48', width=2)
        ))
        fig_par.update_layout(
            xaxis_title='Vendor',
            yaxis_title='Spend ($M)',
            yaxis2=dict(title='Cumulative Spend %', overlaying='y', side='right', range=[0, 105]),
            template='plotly_white',
            height=380,
            showlegend=False
        )
        st.plotly_chart(fig_par, use_container_width=True)

    with col_p2:
        st.subheader("Critical Risk Vendors (High Spend / Low On-Time)")
        df_high_risk = df_vendor[df_vendor['quadrant'].str.contains('High Risk')].sort_values(by='total_spend', ascending=False)
        st.dataframe(
            df_high_risk[['vendor_name', 'vendor_category', 'total_spend', 'on_time_rate_pct', 'avg_lead_time']].head(10),
            column_config={
                "vendor_name": "Vendor",
                "vendor_category": "Category",
                "total_spend": st.column_config.NumberColumn("Total Spend ($)", format="$%.0f"),
                "on_time_rate_pct": st.column_config.NumberColumn("On-Time %", format="%.1f%%"),
                "avg_lead_time": st.column_config.NumberColumn("Avg Lead Days", format="%.1f")
            },
            hide_index=True,
            use_container_width=True,
            height=350
        )

# ==============================================================================
# PAGE 3: PROCUREMENT EFFICIENCY & BOTTLENECK ANALYSIS
# ==============================================================================
elif nav_page == "Page 3: Procurement Efficiency":
    st.markdown('<div class="main-header">Procurement Process Efficiency & Bottlenecks</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-header">Lead time variance, delay heatmaps, and payment lag analysis</div>', unsafe_allow_html=True)

    col_e1, col_e2 = st.columns(2)
    
    with col_e1:
        st.subheader("Lead Time Distribution by Product Category")
        lead_sql = f"""
        SELECT 
            vendor_category,
            actual_lead_time_days
        FROM vw_po_header_summary
        {build_where(["status = 'Delivered'", "actual_lead_time_days IS NOT NULL"])};
        """
        df_lead = load_data(lead_sql)
        fig_box = px.box(
            df_lead,
            x='vendor_category',
            y='actual_lead_time_days',
            color='vendor_category',
            title='Actual Delivery Lead Time Dispersion (Days)',
            labels={'vendor_category': 'Category', 'actual_lead_time_days': 'Lead Time (Days)'}
        )
        fig_box.update_layout(template='plotly_white', height=400, showlegend=False)
        st.plotly_chart(fig_box, use_container_width=True)

    with col_e2:
        st.subheader("Delay Rate % Heatmap (Region vs Category)")
        hm_sql = f"""
        SELECT 
            vendor_category,
            dept_region,
            ROUND(100.0 * SUM(CASE WHEN is_delayed = 1 THEN 1 ELSE 0 END) / COUNT(po_id), 1) AS delay_rate
        FROM vw_po_header_summary
        {build_where("status = 'Delivered'")}
        GROUP BY vendor_category, dept_region;
        """
        df_hm = load_data(hm_sql)
        pivot_hm = df_hm.pivot(index='vendor_category', columns='dept_region', values='delay_rate').fillna(0)
        fig_hm = px.imshow(
            pivot_hm,
            labels=dict(x="Department Region", y="Vendor Category", color="Delay Rate %"),
            x=pivot_hm.columns,
            y=pivot_hm.index,
            color_continuous_scale='Reds',
            text_auto=True,
            title='Delivery Delay Rate (%) Heatmap Matrix'
        )
        fig_hm.update_layout(template='plotly_white', height=400)
        st.plotly_chart(fig_hm, use_container_width=True)

    st.markdown("---")
    col_prio, col_pay = st.columns(2)
    with col_prio:
        st.subheader("Delay Rate & Lead Time by Order Priority")
        prio_sql = f"""
        SELECT 
            priority,
            COUNT(po_id) AS total_orders,
            AVG(actual_lead_time_days) AS avg_actual_lead_time,
            ROUND(100.0 * SUM(CASE WHEN is_delayed = 1 THEN 1 ELSE 0 END) / COUNT(po_id), 1) AS delay_rate_pct
        FROM vw_po_header_summary
        {build_where("status = 'Delivered'")}
        GROUP BY priority;
        """
        df_prio = load_data(prio_sql)
        fig_prio = px.bar(
            df_prio,
            x='priority',
            y='delay_rate_pct',
            color='priority',
            title='Order Delay Rate (%) by Order Priority Level',
            labels={'delay_rate_pct': 'Delay Rate %', 'priority': 'Priority Level'},
            color_discrete_sequence=px.colors.qualitative.Dark2
        )
        fig_prio.update_layout(template='plotly_white', height=360, showlegend=False)
        st.plotly_chart(fig_prio, use_container_width=True)

    with col_pay:
        st.subheader("Payment Processing Lag After Delivery")
        pay_sql = """
        SELECT 
            p.payment_status,
            AVG(julianday(p.payment_date) - julianday(po.actual_delivery_date)) AS avg_payment_lag_days,
            SUM(p.payment_amount) AS total_value
        FROM payments p
        JOIN purchase_orders po ON p.po_id = po.po_id
        WHERE po.status = 'Delivered' AND po.actual_delivery_date IS NOT NULL
        GROUP BY p.payment_status;
        """
        df_pay = load_data(pay_sql)
        fig_pay = px.bar(
            df_pay,
            x='payment_status',
            y='avg_payment_lag_days',
            title='Average Payment Execution Lag (Days Post-Delivery)',
            labels={'avg_payment_lag_days': 'Avg Payment Lag (Days)', 'payment_status': 'Payment Status'},
            color='payment_status',
            color_discrete_sequence=px.colors.qualitative.Set2
        )
        fig_pay.update_layout(template='plotly_white', height=360, showlegend=False)
        st.plotly_chart(fig_pay, use_container_width=True)

# ==============================================================================
# PAGE 4: CONSULTING INSIGHTS & ROI CALCULATOR
# ==============================================================================
elif nav_page == "Page 4: Consulting Insights & ROI":
    st.markdown('<div class="main-header">Consulting Case Insights & ROI Calculator</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-header">Strategic recommendations, empirical root cause findings, and interactive financial savings estimator</div>', unsafe_allow_html=True)

    st.markdown("""
    ### Executive Findings Summary
    1. **High Vendor Concentration Risk**: Top 20% of vendors account for **80.2% of total spend** ($560.5M out of $698.7M), creating extreme operational vulnerability.
    2. **Severe Delivery Delays**: Overall **42.4% of delivered purchase orders** experienced delays past contractually expected dates, with average lead times stretching to **20.1 days**.
    3. **Chronic Problem Vendors**: 15 specific vendors exhibit persistent delay rates exceeding **45%**, contributing to over $85M in delayed inventory flow.
    4. **Raw Materials & Logistics Bottlenecks**: Raw Materials categories across Latin America and North America show the highest delay rates (56.4%–57.3%).
    """)

    st.markdown("---")
    st.subheader("Interactive Financial Impact & Savings ROI Calculator")
    st.caption("Estimate financial impact from contract renegotiation and delivery delay reduction")

    calc_c1, calc_c2, calc_c3 = st.columns(3)
    with calc_c1:
        renegotiate_target = st.slider("Target Spend Renegotiation (% High-Risk Vendors):", 5, 30, 15)
    with calc_c2:
        price_discount_est = st.slider("Negotiated Contract Price Savings (%):", 1.0, 10.0, 3.5, 0.5)
    with calc_c3:
        holding_cost_rate = st.slider("Annual Inventory Holding Cost Rate (%):", 10, 30, 18)

    # Calculate Savings
    total_spend_val = 698741716.32
    target_reneg_spend = total_spend_val * 0.802 * (renegotiate_target / 100.0)
    direct_price_savings = target_reneg_spend * (price_discount_est / 100.0)
    
    # Delayed spend inventory holding cost reduction
    delayed_spend_val = total_spend_val * 0.4237
    reduced_delay_days = 5  # Estimated 5-day reduction in avg lead time
    holding_cost_savings = (delayed_spend_val * (holding_cost_rate / 100.0) / 365.0) * reduced_delay_days

    total_estimated_roi = direct_price_savings + holding_cost_savings

    res_col1, res_col2, res_col3 = st.columns(3)
    with res_col1:
        st.metric("Direct Contract Savings", f"${direct_price_savings/1e6:.2f} Million", delta=f"{price_discount_est}% Price Cut")
    with res_col2:
        st.metric("Inventory Carrying Savings", f"${holding_cost_savings/1e6:.2f} Million", delta="5-Day Lead Time Cut")
    with res_col3:
        st.metric("Total Estimated Annual ROI", f"${total_estimated_roi/1e6:.2f} Million", delta="Annual Value Creation")

    st.markdown("---")
    st.subheader("Prioritized Implementation Roadmap")

    st.markdown("""
    | Phase | Initiative | Strategic Focus | Timeline | Expected Business Impact |
    | :--- | :--- | :--- | :--- | :--- |
    | **Phase 1** | **Contract Renegotiation** | Target 15 High-Spend / Low-Performance vendors in Quadrant 2 | Months 1–3 | $3.5M–$5.2M direct cost reduction |
    | **Phase 2** | **Supplier Scorecards & SLAs** | Establish category-specific delivery SLAs and monthly penalty clauses | Months 3–6 | 15% reduction in delivery delay rate |
    | **Phase 3** | **Regional Multi-Sourcing** | Diversify Raw Materials & Heavy Machinery vendors in LATAM/NA | Months 6–12 | Mitigation of concentration risk |
    """)
