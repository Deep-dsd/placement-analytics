"""
Placement Analytics Dashboard
==============================
A modern Streamlit analytics dashboard for college placement data.
Run with:  streamlit run app.py
"""

from __future__ import annotations

import streamlit as st

# ---------------------------------------------------------------------------
# Page configuration (must be first Streamlit command)
# ---------------------------------------------------------------------------
st.set_page_config(
    page_title="Placement Analytics",
    page_icon="./assets/favicon.ico" if False else None,  # optional
    layout="wide",
    initial_sidebar_state="expanded",
)

# ---------------------------------------------------------------------------
# Imports
# ---------------------------------------------------------------------------
from components.filters import render_sidebar_filters
from components.metrics import render_kpi_metrics
from components.visualizations import (
    render_branch_comparison,
    render_growth_heatmap,
    render_internship_conversion,
    render_job_role_distribution,
    render_package_distribution,
    render_package_trends,
    render_placement_trends,
    render_scatter_performance,
    render_students_placed_bar,
    render_top_companies,
)
from utils.data_loader import compute_derived_metrics, filter_data, load_data
from utils.pdf_export import generate_pdf
from utils.styling import inject_custom_css

# ---------------------------------------------------------------------------
# Styling
# ---------------------------------------------------------------------------
inject_custom_css()

# ---------------------------------------------------------------------------
# Data
# ---------------------------------------------------------------------------
raw_df = load_data()

# ---------------------------------------------------------------------------
# Sidebar filters
# ---------------------------------------------------------------------------
selections = render_sidebar_filters(raw_df)
df = filter_data(
    raw_df,
    years=selections["years"],
    branches=selections["branches"],
    package_range=selections["package_range"],
    placement_pct_range=selections["placement_pct_range"],
)

# ---------------------------------------------------------------------------
# Header
# ---------------------------------------------------------------------------
st.markdown(
    '<div class="dashboard-header">'
    "<h1>Placement Analytics Dashboard</h1>"
    '<p class="dashboard-subtitle">Comprehensive insights into campus placement trends, '
    "packages, and recruiting patterns</p>"
    "</div>",
    unsafe_allow_html=True,
)

# ---------------------------------------------------------------------------
# Guard – empty data
# ---------------------------------------------------------------------------
if df.empty:
    st.warning("No records match the current filter selection. Try adjusting the filters in the sidebar.")
    st.stop()

# ---------------------------------------------------------------------------
# KPI Metrics
# ---------------------------------------------------------------------------
metrics = compute_derived_metrics(df)
render_kpi_metrics(metrics)

# ---------------------------------------------------------------------------
# Export PDF
# ---------------------------------------------------------------------------
_export_col1, _export_col2 = st.columns([8, 2])
with _export_col2:
    # Generate PDF lazily on first request, cache in session state
    if "pdf_bytes" not in st.session_state:
        st.session_state["pdf_bytes"] = None
        st.session_state["pdf_filter_hash"] = None

    # Recompute if filters changed
    _filter_hash = hash((
        tuple(selections["years"]),
        tuple(selections["branches"]),
        selections["package_range"],
        selections["placement_pct_range"],
    ))

    if st.button("Export as PDF", use_container_width=True, type="primary"):
        with st.spinner("Generating PDF report..."):
            pdf_bytes = generate_pdf(df, metrics)
            st.session_state["pdf_bytes"] = pdf_bytes
            st.session_state["pdf_filter_hash"] = _filter_hash

    if st.session_state.get("pdf_bytes") and st.session_state.get("pdf_filter_hash") == _filter_hash:
        st.download_button(
            label="Download PDF",
            data=st.session_state["pdf_bytes"],
            file_name="placement_analytics_report.pdf",
            mime="application/pdf",
            use_container_width=True,
        )

st.markdown("---")

# ---------------------------------------------------------------------------
# Row 1: Year-over-Year Trends
# ---------------------------------------------------------------------------
col1, col2 = st.columns(2)
with col1:
    render_placement_trends(df)
with col2:
    render_students_placed_bar(df)

# ---------------------------------------------------------------------------
# Row 2: Branch Comparison
# ---------------------------------------------------------------------------
col3, col4 = st.columns(2)
with col3:
    render_branch_comparison(df)
with col4:
    render_package_distribution(df)

# ---------------------------------------------------------------------------
# Row 3: Package Analysis
# ---------------------------------------------------------------------------
col5, col6 = st.columns(2)
with col5:
    render_package_trends(df)
with col6:
    render_scatter_performance(df)

# ---------------------------------------------------------------------------
# Row 4: Company & Role Insights
# ---------------------------------------------------------------------------
col7, col8 = st.columns(2)
with col7:
    render_top_companies(df)
with col8:
    render_job_role_distribution(df)

# ---------------------------------------------------------------------------
# Row 5: Internship & Heatmap
# ---------------------------------------------------------------------------
col9, col10 = st.columns(2)
with col9:
    render_internship_conversion(df)
with col10:
    render_growth_heatmap(df)

# ---------------------------------------------------------------------------
# Footer
# ---------------------------------------------------------------------------
st.markdown("---")
st.markdown(
    '<p class="app-footer">Placement Analytics Dashboard &middot; '
    "Data sourced from institutional placement records &middot; "
    "Built with Streamlit & Plotly</p>",
    unsafe_allow_html=True,
)
