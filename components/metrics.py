"""
KPI metric cards rendered at the top of the dashboard.
"""

from __future__ import annotations

from typing import Dict, Optional

import streamlit as st


def _fmt_delta(value: Optional[float], suffix: str = "%") -> Optional[str]:
    """Format a delta value for display."""
    if value is None:
        return None
    sign = "+" if value > 0 else ""
    return f"{sign}{value}{suffix}"


def render_kpi_metrics(metrics: Dict) -> None:
    """Render four KPI cards in a single row.

    Args:
        metrics: dict returned by ``compute_derived_metrics``.
    """
    c1, c2, c3, c4 = st.columns(4)

    with c1:
        st.metric(
            label="Total Placements",
            value=f"{metrics['total_placed']:,}",
            delta=_fmt_delta(metrics.get("yoy_placed_change"), "%"),
            delta_color="normal",
        )

    with c2:
        st.metric(
            label="Placement Rate",
            value=f"{metrics['overall_placement_pct']}%",
            delta=_fmt_delta(metrics.get("pct_delta"), " pp"),
            delta_color="normal",
        )

    with c3:
        st.metric(
            label="Highest Package",
            value=f"{metrics['highest_package']} LPA",
            delta=metrics["highest_package_branch"],
            delta_color="off",
        )

    with c4:
        st.metric(
            label="Avg Package",
            value=f"{metrics['weighted_avg_package']} LPA",
            delta=_fmt_delta(metrics.get("yoy_avg_pkg_change"), "%"),
            delta_color="normal",
        )
