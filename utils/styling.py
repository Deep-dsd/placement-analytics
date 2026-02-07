"""
Custom CSS styling and theming for the Placement Analytics Dashboard.
Defines the color palette, chart defaults, and injects custom CSS into Streamlit.
"""

import streamlit as st
from typing import Dict, Any

# ---------------------------------------------------------------------------
# Color Palette
# ---------------------------------------------------------------------------
COLORS: Dict[str, str] = {
    "primary_dark": "#1e293b",
    "primary_light": "#f8fafc",
    "accent_primary": "#10b981",
    "accent_secondary": "#f59e0b",
    "accent_tertiary": "#3b82f6",
    "text_primary": "#0f172a",
    "text_secondary": "#64748b",
    "border": "#e2e8f0",
    "white": "#ffffff",
    "success": "#10b981",
    "danger": "#ef4444",
    "card_bg": "#ffffff",
}

CHART_COLORS: list[str] = [
    "#10b981",  # emerald
    "#3b82f6",  # blue
    "#f59e0b",  # amber
    "#8b5cf6",  # violet
    "#ec4899",  # pink
    "#14b8a6",  # teal
    "#f97316",  # orange
    "#6366f1",  # indigo
    "#06b6d4",  # cyan
    "#84cc16",  # lime
]

# ---------------------------------------------------------------------------
# Plotly Layout Defaults
# ---------------------------------------------------------------------------
PLOTLY_LAYOUT_DEFAULTS: Dict[str, Any] = {
    "template": "plotly_white",
    "font": dict(family="Inter, Arial, sans-serif", color=COLORS["text_primary"], size=13),
    "paper_bgcolor": "rgba(0,0,0,0)",
    "plot_bgcolor": "rgba(0,0,0,0)",
    "margin": dict(l=40, r=30, t=50, b=40),
    "hoverlabel": dict(
        bgcolor=COLORS["white"],
        font_size=13,
        font_family="Inter, Arial, sans-serif",
        bordercolor=COLORS["border"],
    ),
    "legend": dict(
        orientation="h",
        yanchor="bottom",
        y=1.02,
        xanchor="right",
        x=1,
        font=dict(size=12),
    ),
}

PLOTLY_CONFIG: Dict[str, Any] = {
    "displayModeBar": False,
    "responsive": True,
}


# ---------------------------------------------------------------------------
# Custom CSS Injection
# ---------------------------------------------------------------------------
def inject_custom_css() -> None:
    """Inject custom CSS to style the Streamlit app."""
    st.markdown(_CUSTOM_CSS, unsafe_allow_html=True)


_CUSTOM_CSS = """
<style>
/* ===== Global ===== */
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');

html, body, [class*="css"] {
    font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
}

/* Hide Streamlit branding */
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
header {visibility: hidden;}

/* Main container */
.block-container {
    padding-top: 2rem;
    padding-bottom: 2rem;
    max-width: 1200px;
}

/* ===== Sidebar ===== */
[data-testid="stSidebar"] {
    background-color: #ffffff;
    border-right: 1px solid #e2e8f0;
}

[data-testid="stSidebar"] .block-container {
    padding-top: 1.5rem;
}

[data-testid="stSidebar"] [data-testid="stMarkdownContainer"] h1 {
    font-size: 1.2rem;
    font-weight: 700;
    color: #1e293b;
    letter-spacing: -0.01em;
}

[data-testid="stSidebar"] [data-testid="stMarkdownContainer"] h3 {
    font-size: 0.8rem;
    font-weight: 600;
    color: #64748b;
    text-transform: uppercase;
    letter-spacing: 0.05em;
    margin-bottom: 0.25rem;
}

/* ===== Typography ===== */
h1 {
    font-weight: 700 !important;
    color: #0f172a !important;
    letter-spacing: -0.02em !important;
    font-size: 1.75rem !important;
}

h2 {
    font-weight: 600 !important;
    color: #1e293b !important;
    font-size: 1.25rem !important;
    letter-spacing: -0.01em !important;
}

h3 {
    font-weight: 600 !important;
    color: #334155 !important;
    font-size: 1.05rem !important;
}

/* ===== Metric Cards ===== */
div[data-testid="stMetric"] {
    background-color: #ffffff;
    border: 1px solid #e2e8f0;
    border-radius: 8px;
    padding: 18px 20px 14px 20px;
    box-shadow: 0 1px 2px rgba(0,0,0,0.04);
}

div[data-testid="stMetric"] label {
    font-size: 0.8rem !important;
    font-weight: 500 !important;
    color: #64748b !important;
    text-transform: uppercase;
    letter-spacing: 0.04em;
}

div[data-testid="stMetric"] [data-testid="stMetricValue"] {
    font-size: 1.75rem !important;
    font-weight: 700 !important;
    color: #0f172a !important;
}

div[data-testid="stMetric"] [data-testid="stMetricDelta"] {
    font-size: 0.8rem !important;
    font-weight: 500 !important;
}

/* ===== Chart Containers ===== */
.chart-wrapper {
    background: #ffffff;
    border: 1px solid #e2e8f0;
    border-radius: 8px;
    padding: 20px 16px 12px 16px;
    margin-bottom: 1rem;
    box-shadow: 0 1px 2px rgba(0,0,0,0.04);
}

.chart-wrapper h3 {
    margin-top: 0 !important;
    margin-bottom: 4px !important;
    font-size: 0.95rem !important;
}

.chart-insight {
    font-size: 0.82rem;
    color: #64748b;
    line-height: 1.5;
    margin-top: 4px;
    padding-top: 6px;
    border-top: 1px solid #f1f5f9;
}

/* ===== Buttons ===== */
.stButton > button {
    border-radius: 6px;
    font-weight: 500;
    font-size: 0.85rem;
    padding: 0.4rem 1rem;
    border: 1px solid #e2e8f0;
    transition: background-color 0.15s ease, border-color 0.15s ease;
}

.stButton > button:hover {
    border-color: #cbd5e1;
    background-color: #f8fafc;
}

/* Primary action button */
.stButton > button[kind="primary"] {
    background-color: #10b981;
    color: #ffffff;
    border: none;
}

.stButton > button[kind="primary"]:hover {
    background-color: #059669;
}

/* ===== Multiselect / Select ===== */
[data-testid="stMultiSelect"] [data-baseweb="tag"] {
    background-color: #f0fdf4;
    border: 1px solid #bbf7d0;
    color: #166534;
    border-radius: 4px;
}

/* ===== Dividers ===== */
hr {
    border: none;
    border-top: 1px solid #e2e8f0;
    margin: 1.5rem 0;
}

/* ===== Tabs ===== */
.stTabs [data-baseweb="tab-list"] {
    gap: 4px;
}

.stTabs [data-baseweb="tab"] {
    font-size: 0.85rem;
    font-weight: 500;
    padding: 8px 16px;
    border-radius: 6px 6px 0 0;
}

/* ===== Expander ===== */
[data-testid="stExpander"] {
    border: 1px solid #e2e8f0;
    border-radius: 8px;
}

/* ===== Download button ===== */
.stDownloadButton > button {
    font-size: 0.8rem;
    padding: 0.3rem 0.75rem;
}

/* ===== Active filter badge ===== */
.filter-badge {
    display: inline-block;
    background-color: #f0fdf4;
    color: #166534;
    font-size: 0.75rem;
    font-weight: 600;
    padding: 2px 10px;
    border-radius: 12px;
    border: 1px solid #bbf7d0;
    margin-bottom: 0.5rem;
}

/* ===== Dashboard Header ===== */
.dashboard-header {
    padding-bottom: 0.5rem;
    margin-bottom: 0.25rem;
}

.dashboard-subtitle {
    color: #64748b;
    font-size: 0.95rem;
    margin-top: -0.5rem;
}

/* ===== Footer ===== */
.app-footer {
    text-align: center;
    color: #94a3b8;
    font-size: 0.75rem;
    padding: 1.5rem 0 0.5rem 0;
    border-top: 1px solid #e2e8f0;
    margin-top: 2rem;
}
</style>
"""
