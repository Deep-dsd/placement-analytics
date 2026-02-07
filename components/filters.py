"""
Sidebar filter panel for the Placement Analytics Dashboard.
Renders year, branch, package-range, and placement-percentage filters.
"""

from __future__ import annotations

from typing import Dict, List, Tuple

import pandas as pd
import streamlit as st


def render_sidebar_filters(df: pd.DataFrame) -> Dict:
    """Render sidebar filters and return current selections.

    Returns a dict with keys:
        years, branches, package_range, placement_pct_range, active_count
    """
    with st.sidebar:
        st.markdown("# Filters")

        # --- active-filter counter (computed at end, displayed here) ---
        badge_placeholder = st.empty()

        st.markdown("---")

        # ---- Year Selection ----
        st.markdown("### Year")
        all_years: List[int] = sorted(df["year"].unique().tolist(), reverse=True)
        default_years = all_years  # all selected by default

        selected_years = st.multiselect(
            "Select years",
            options=all_years,
            default=st.session_state.get("filter_years", default_years),
            key="ms_years",
            label_visibility="collapsed",
        )
        if not selected_years:
            selected_years = all_years

        # ---- Branch Selection ----
        st.markdown("### Branch")
        branch_order = ["Computer Science", "IT", "Electronics", "Mechanical", "Civil"]
        all_branches = [b for b in branch_order if b in df["branch"].unique()]
        default_branches = all_branches

        selected_branches = st.multiselect(
            "Select branches",
            options=all_branches,
            default=st.session_state.get("filter_branches", default_branches),
            key="ms_branches",
            label_visibility="collapsed",
        )
        if not selected_branches:
            selected_branches = all_branches

        # ---- Package Range ----
        st.markdown("### Avg Package (LPA)")
        pkg_min = float(df["avg_package_LPA"].min())
        pkg_max = float(df["avg_package_LPA"].max())
        pkg_default = (pkg_min, pkg_max)
        package_range: Tuple[float, float] = st.slider(
            "Average package range",
            min_value=pkg_min,
            max_value=pkg_max,
            value=st.session_state.get("filter_pkg", pkg_default),
            step=0.5,
            format="%.1f",
            key="sl_pkg",
            label_visibility="collapsed",
        )

        # ---- Placement Percentage ----
        st.markdown("### Placement %")
        pct_default = (0.0, 100.0)
        placement_pct_range: Tuple[float, float] = st.slider(
            "Placement percentage range",
            min_value=0.0,
            max_value=100.0,
            value=st.session_state.get("filter_pct", pct_default),
            step=1.0,
            format="%.0f%%",
            key="sl_pct",
            label_visibility="collapsed",
        )

        st.markdown("---")

        # ---- Reset Button ----
        col1, col2 = st.columns(2)
        with col1:
            if st.button("Reset All", use_container_width=True):
                for key in ["ms_years", "ms_branches", "sl_pkg", "sl_pct",
                            "filter_years", "filter_branches", "filter_pkg", "filter_pct"]:
                    st.session_state.pop(key, None)
                st.rerun()
        with col2:
            st.download_button(
                "Export CSV",
                data=df.to_csv(index=False).encode("utf-8"),
                file_name="placement_data_filtered.csv",
                mime="text/csv",
                use_container_width=True,
            )

        # ---- Count active filters ----
        active = 0
        if set(selected_years) != set(all_years):
            active += 1
        if set(selected_branches) != set(all_branches):
            active += 1
        if package_range != (pkg_min, pkg_max):
            active += 1
        if placement_pct_range != (0.0, 100.0):
            active += 1

        if active > 0:
            badge_placeholder.markdown(
                f'<span class="filter-badge">{active} active filter{"s" if active != 1 else ""}</span>',
                unsafe_allow_html=True,
            )

        # Persist in session state
        st.session_state["filter_years"] = selected_years
        st.session_state["filter_branches"] = selected_branches
        st.session_state["filter_pkg"] = package_range
        st.session_state["filter_pct"] = placement_pct_range

    return {
        "years": selected_years,
        "branches": selected_branches,
        "package_range": package_range,
        "placement_pct_range": placement_pct_range,
        "active_count": active,
    }
