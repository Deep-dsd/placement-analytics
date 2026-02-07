"""
Data loading, preprocessing, and derived-metric computation for the dashboard.
"""

from __future__ import annotations

import os
from typing import Dict, List, Optional, Tuple

import numpy as np
import pandas as pd
import streamlit as st


# ---------------------------------------------------------------------------
# Data loading
# ---------------------------------------------------------------------------
@st.cache_data(show_spinner=False)
def load_data(path: Optional[str] = None) -> pd.DataFrame:
    """Load placement data from CSV and perform basic preprocessing.

    Args:
        path: Optional path override; defaults to ``data/placement_data.csv``.

    Returns:
        Cleaned pandas DataFrame.
    """
    if path is None:
        path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data", "placement_data.csv")

    df = pd.read_csv(path)

    # Ensure correct dtypes
    df["year"] = df["year"].astype(int)
    numeric_cols = [
        "total_students", "placed_students", "unplaced_students",
        "placement_percentage", "highest_package_LPA", "median_package_LPA",
        "lowest_package_LPA", "avg_package_LPA",
        "top_company_1_students", "top_company_2_students", "top_company_3_students",
        "internship_conversion_rate_percent",
    ]
    for col in numeric_cols:
        df[col] = pd.to_numeric(df[col], errors="coerce")

    # Sort for consistency
    df.sort_values(["year", "branch"], inplace=True)
    df.reset_index(drop=True, inplace=True)

    return df


# ---------------------------------------------------------------------------
# Filtering
# ---------------------------------------------------------------------------
def filter_data(
    df: pd.DataFrame,
    years: List[int],
    branches: List[str],
    package_range: Tuple[float, float],
    placement_pct_range: Tuple[float, float],
) -> pd.DataFrame:
    """Apply sidebar filter selections to the DataFrame.

    Returns:
        Filtered DataFrame (may be empty).
    """
    mask = (
        df["year"].isin(years)
        & df["branch"].isin(branches)
        & df["avg_package_LPA"].between(package_range[0], package_range[1])
        & df["placement_percentage"].between(placement_pct_range[0], placement_pct_range[1])
    )
    return df.loc[mask].copy()


# ---------------------------------------------------------------------------
# Derived metrics
# ---------------------------------------------------------------------------
@st.cache_data(show_spinner=False)
def compute_derived_metrics(df: pd.DataFrame) -> Dict:
    """Compute aggregate KPIs from the (filtered) data.

    Returns a dict with:
        total_placed, total_students, overall_placement_pct,
        highest_package, highest_package_branch,
        weighted_avg_package, prev_year_placed, prev_year_avg_pkg,
        yoy_placed_change, yoy_avg_pkg_change
    """
    if df.empty:
        return _empty_metrics()

    total_placed = int(df["placed_students"].sum())
    total_students = int(df["total_students"].sum())
    overall_pct = round(total_placed / total_students * 100, 1) if total_students else 0.0

    # Highest package
    idx_max = df["highest_package_LPA"].idxmax()
    highest_pkg = df.loc[idx_max, "highest_package_LPA"]
    highest_pkg_branch = df.loc[idx_max, "branch"]

    # Weighted average package
    weighted_avg = round(
        (df["avg_package_LPA"] * df["placed_students"]).sum() / max(total_placed, 1), 2
    )

    # Year-over-year helpers
    years_sorted = sorted(df["year"].unique())
    yoy_placed_change: Optional[float] = None
    yoy_avg_change: Optional[float] = None
    prev_year_pct: Optional[float] = None

    if len(years_sorted) >= 2:
        latest, prev = years_sorted[-1], years_sorted[-2]
        cur = df[df["year"] == latest]
        prv = df[df["year"] == prev]

        cur_placed = int(cur["placed_students"].sum())
        prv_placed = int(prv["placed_students"].sum())
        if prv_placed:
            yoy_placed_change = round((cur_placed - prv_placed) / prv_placed * 100, 1)

        cur_total = int(cur["total_students"].sum())
        prv_total = int(prv["total_students"].sum())
        if prv_total:
            prev_year_pct = round(prv["placed_students"].sum() / prv_total * 100, 1)

        cur_wavg = (cur["avg_package_LPA"] * cur["placed_students"]).sum() / max(cur["placed_students"].sum(), 1)
        prv_wavg = (prv["avg_package_LPA"] * prv["placed_students"]).sum() / max(prv["placed_students"].sum(), 1)
        if prv_wavg:
            yoy_avg_change = round((cur_wavg - prv_wavg) / prv_wavg * 100, 1)

    # Overall placement pct trend (latest vs previous)
    pct_delta: Optional[float] = None
    if prev_year_pct is not None:
        latest_year = years_sorted[-1]
        lat = df[df["year"] == latest_year]
        lat_pct = round(lat["placed_students"].sum() / max(lat["total_students"].sum(), 1) * 100, 1)
        pct_delta = round(lat_pct - prev_year_pct, 1)

    return {
        "total_placed": total_placed,
        "total_students": total_students,
        "overall_placement_pct": overall_pct,
        "highest_package": highest_pkg,
        "highest_package_branch": highest_pkg_branch,
        "weighted_avg_package": weighted_avg,
        "yoy_placed_change": yoy_placed_change,
        "yoy_avg_pkg_change": yoy_avg_change,
        "pct_delta": pct_delta,
    }


def _empty_metrics() -> Dict:
    return {
        "total_placed": 0,
        "total_students": 0,
        "overall_placement_pct": 0.0,
        "highest_package": 0.0,
        "highest_package_branch": "N/A",
        "weighted_avg_package": 0.0,
        "yoy_placed_change": None,
        "yoy_avg_pkg_change": None,
        "pct_delta": None,
    }


# ---------------------------------------------------------------------------
# Utility helpers for charts
# ---------------------------------------------------------------------------
def get_company_data(df: pd.DataFrame) -> pd.DataFrame:
    """Aggregate top-company hiring numbers across all filtered rows."""
    records = []
    for _, row in df.iterrows():
        for i in range(1, 4):
            company = row.get(f"top_company_{i}")
            students = row.get(f"top_company_{i}_students")
            if pd.notna(company) and pd.notna(students):
                records.append({"company": company, "students": int(students)})
    if not records:
        return pd.DataFrame(columns=["company", "students"])
    agg = pd.DataFrame(records).groupby("company", as_index=False)["students"].sum()
    return agg.sort_values("students", ascending=False).head(10).reset_index(drop=True)


def get_role_data(df: pd.DataFrame) -> pd.DataFrame:
    """Aggregate job-role mentions across all filtered rows."""
    roles: Dict[str, int] = {}
    for _, row in df.iterrows():
        for i in range(1, 4):
            role = row.get(f"top_job_role_{i}")
            if pd.notna(role):
                roles[role] = roles.get(role, 0) + 1
    if not roles:
        return pd.DataFrame(columns=["role", "count"])
    rdf = pd.DataFrame(list(roles.items()), columns=["role", "count"])
    return rdf.sort_values("count", ascending=False).head(10).reset_index(drop=True)
