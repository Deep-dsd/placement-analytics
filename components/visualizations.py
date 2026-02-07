"""
All chart / visualization components for the Placement Analytics Dashboard.

Each chart has a pair of functions:
  - ``build_*``  – creates and returns ``(fig, insight_text)``; pure logic, no Streamlit.
  - ``render_*`` – displays the chart inside a styled Streamlit container.

The ``build_*`` functions are also used by the PDF exporter.
"""

from __future__ import annotations

from typing import List, Optional, Tuple

import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

from utils.data_loader import get_company_data, get_role_data
from utils.styling import CHART_COLORS, COLORS, PLOTLY_CONFIG, PLOTLY_LAYOUT_DEFAULTS


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------
def _apply_layout(fig: go.Figure, **overrides) -> go.Figure:
    """Merge default layout with optional overrides."""
    layout = {**PLOTLY_LAYOUT_DEFAULTS, **overrides}
    fig.update_layout(**layout)
    return fig


def _wrap_render(title: str, fig: Optional[go.Figure], insight: str) -> None:
    """Render a chart inside a styled card in Streamlit."""
    if fig is None:
        st.info("No data available for the selected filters.")
        return
    ct = st.container()
    ct.markdown(f'<div class="chart-wrapper"><h3>{title}</h3>', unsafe_allow_html=True)
    ct.plotly_chart(fig, use_container_width=True, config=PLOTLY_CONFIG)
    ct.markdown(f'<p class="chart-insight">{insight}</p></div>', unsafe_allow_html=True)


# =====================================================================
# Chart 1 – Placement Trends Over Years (Line Chart)
# =====================================================================
def build_placement_trends(df: pd.DataFrame) -> Tuple[Optional[go.Figure], str]:
    if df.empty:
        return None, ""

    agg = df.groupby(["year", "branch"], as_index=False)["placement_percentage"].mean()

    fig = px.line(
        agg, x="year", y="placement_percentage", color="branch",
        markers=True,
        color_discrete_sequence=CHART_COLORS,
        labels={"placement_percentage": "Placement %", "year": "Year", "branch": "Branch"},
    )
    fig.update_traces(line=dict(width=2.5), marker=dict(size=7))
    fig.update_xaxes(dtick=1, gridcolor="#f1f5f9", gridwidth=1, griddash="dot")
    fig.update_yaxes(gridcolor="#f1f5f9", gridwidth=1, griddash="dot")
    _apply_layout(fig, height=420, legend=dict(orientation="h", yanchor="bottom", y=1.04, xanchor="right", x=1))

    best = agg.loc[agg["placement_percentage"].idxmax()]
    worst = agg.loc[agg["placement_percentage"].idxmin()]
    insight = (
        f"{best['branch']} reached the highest placement rate of {best['placement_percentage']:.1f}% "
        f"in {int(best['year'])}. {worst['branch']} had the lowest at {worst['placement_percentage']:.1f}% "
        f"in {int(worst['year'])}."
    )
    return fig, insight


def render_placement_trends(df: pd.DataFrame) -> None:
    fig, insight = build_placement_trends(df)
    _wrap_render("Placement Trends Over Years", fig, insight)


# =====================================================================
# Chart 2 – Students Placed by Year (Stacked Bar)
# =====================================================================
def build_students_placed_bar(df: pd.DataFrame) -> Tuple[Optional[go.Figure], str]:
    if df.empty:
        return None, ""

    yearly = df.groupby("year", as_index=False).agg(
        placed=("placed_students", "sum"),
        unplaced=("unplaced_students", "sum"),
        total=("total_students", "sum"),
    )
    yearly["placed_pct"] = (yearly["placed"] / yearly["total"] * 100).round(1)

    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=yearly["year"], y=yearly["placed"], name="Placed",
        marker_color=COLORS["accent_primary"],
        text=yearly.apply(lambda r: f"{r['placed']}<br>({r['placed_pct']:.0f}%)", axis=1),
        textposition="inside", textfont=dict(size=11, color="white"),
    ))
    fig.add_trace(go.Bar(
        x=yearly["year"], y=yearly["unplaced"], name="Unplaced",
        marker_color="#cbd5e1",
        text=yearly["unplaced"],
        textposition="inside", textfont=dict(size=11),
    ))
    fig.update_layout(barmode="stack", bargap=0.35)
    fig.update_xaxes(dtick=1)
    _apply_layout(fig, height=420, legend=dict(orientation="h", yanchor="bottom", y=1.04, xanchor="right", x=1))

    insight = ""
    if len(yearly) >= 2:
        first, last = yearly.iloc[0], yearly.iloc[-1]
        growth = ((last["placed"] - first["placed"]) / max(first["placed"], 1) * 100)
        insight = (
            f"Total placements grew {growth:.0f}% from "
            f"{int(first['year'])} to {int(last['year'])}, rising from "
            f"{first['placed']:,} to {last['placed']:,} students."
        )
    return fig, insight


def render_students_placed_bar(df: pd.DataFrame) -> None:
    fig, insight = build_students_placed_bar(df)
    _wrap_render("Students Placed vs Unplaced by Year", fig, insight)


# =====================================================================
# Chart 3 – Branch-wise Placement Comparison (Horizontal Bar)
# =====================================================================
def build_branch_comparison(df: pd.DataFrame) -> Tuple[Optional[go.Figure], str]:
    if df.empty:
        return None, ""

    agg = df.groupby("branch", as_index=False).agg(
        placed=("placed_students", "sum"),
        total=("total_students", "sum"),
    )
    agg["pct"] = (agg["placed"] / agg["total"] * 100).round(1)
    agg.sort_values("pct", ascending=True, inplace=True)

    colors = []
    for p in agg["pct"]:
        if p >= 80:
            colors.append(COLORS["accent_primary"])
        elif p >= 60:
            colors.append(COLORS["accent_secondary"])
        else:
            colors.append(COLORS["accent_tertiary"])

    fig = go.Figure(go.Bar(
        x=agg["pct"], y=agg["branch"], orientation="h",
        marker_color=colors,
        text=agg["pct"].apply(lambda v: f"{v:.1f}%"),
        textposition="outside", textfont=dict(size=12),
    ))
    fig.update_xaxes(range=[0, min(agg["pct"].max() + 12, 105)], title_text="Placement %")
    _apply_layout(fig, height=350, showlegend=False, margin=dict(l=120, r=40, t=40, b=40))

    top, bottom = agg.iloc[-1], agg.iloc[0]
    insight = (
        f"{top['branch']} leads with {top['pct']:.1f}% placement rate, "
        f"while {bottom['branch']} trails at {bottom['pct']:.1f}%."
    )
    return fig, insight


def render_branch_comparison(df: pd.DataFrame) -> None:
    fig, insight = build_branch_comparison(df)
    _wrap_render("Branch-wise Placement Rate", fig, insight)


# =====================================================================
# Chart 4 – Package Distribution (Box Plot)
# =====================================================================
def build_package_distribution(df: pd.DataFrame) -> Tuple[Optional[go.Figure], str]:
    if df.empty:
        return None, ""

    records = []
    for _, row in df.iterrows():
        branch = row["branch"]
        for pkg_col in ["lowest_package_LPA", "median_package_LPA", "avg_package_LPA", "highest_package_LPA"]:
            records.append({
                "branch": branch,
                "package": row[pkg_col],
                "type": pkg_col.replace("_LPA", "").replace("_package", "").replace("_", " ").title(),
            })

    long_df = pd.DataFrame(records)

    fig = px.box(
        long_df, x="branch", y="package", color="branch",
        color_discrete_sequence=CHART_COLORS,
        labels={"package": "Package (LPA)", "branch": "Branch"},
    )
    fig.update_traces(boxmean=True)
    _apply_layout(fig, height=420, showlegend=False)
    fig.update_xaxes(title_text="")

    median_by_branch = df.groupby("branch")["median_package_LPA"].mean()
    best_branch = median_by_branch.idxmax()
    insight = (
        f"{best_branch} offers the highest median package at "
        f"{median_by_branch.max():.1f} LPA on average across the selected years."
    )
    return fig, insight


def render_package_distribution(df: pd.DataFrame) -> None:
    fig, insight = build_package_distribution(df)
    _wrap_render("Package Distribution by Branch", fig, insight)


# =====================================================================
# Chart 5 – Average Package Trends (Area Chart)
# =====================================================================
def build_package_trends(df: pd.DataFrame) -> Tuple[Optional[go.Figure], str]:
    if df.empty:
        return None, ""

    yearly = df.groupby("year", as_index=False).agg(
        highest=("highest_package_LPA", "max"),
        average=("avg_package_LPA", "mean"),
        median=("median_package_LPA", "median"),
        lowest=("lowest_package_LPA", "min"),
    ).round(2)

    pkg_types = [
        ("highest", "Highest", CHART_COLORS[0]),
        ("average", "Average", CHART_COLORS[1]),
        ("median", "Median", CHART_COLORS[2]),
        ("lowest", "Lowest", CHART_COLORS[3]),
    ]

    fig = go.Figure()
    for col, name, color in pkg_types:
        fig.add_trace(go.Scatter(
            x=yearly["year"], y=yearly[col], name=name,
            mode="lines+markers",
            line=dict(color=color, width=2),
            marker=dict(size=6),
            fill="tonexty" if col != "highest" else None,
            fillcolor=f"rgba({int(color[1:3],16)},{int(color[3:5],16)},{int(color[5:7],16)},0.07)",
        ))

    fig.update_xaxes(dtick=1, gridcolor="#f1f5f9", griddash="dot")
    fig.update_yaxes(title_text="Package (LPA)", gridcolor="#f1f5f9", griddash="dot")
    _apply_layout(fig, height=420, legend=dict(orientation="h", yanchor="bottom", y=1.04, xanchor="right", x=1))

    insight = ""
    if len(yearly) >= 2:
        first_avg, last_avg = yearly.iloc[0]["average"], yearly.iloc[-1]["average"]
        growth = ((last_avg - first_avg) / max(first_avg, 0.01) * 100)
        insight = (
            f"Average packages grew {growth:.0f}% from "
            f"{yearly.iloc[0]['year']:.0f} to {yearly.iloc[-1]['year']:.0f}, "
            f"reaching {last_avg:.1f} LPA."
        )
    return fig, insight


def render_package_trends(df: pd.DataFrame) -> None:
    fig, insight = build_package_trends(df)
    _wrap_render("Package Trends Over Years", fig, insight)


# =====================================================================
# Chart 6 – Top vs Bottom Performers (Scatter)
# =====================================================================
def build_scatter_performance(df: pd.DataFrame) -> Tuple[Optional[go.Figure], str]:
    if df.empty:
        return None, ""

    fig = px.scatter(
        df, x="avg_package_LPA", y="placement_percentage",
        color="branch", size="total_students",
        hover_data=["year", "branch", "placed_students"],
        color_discrete_sequence=CHART_COLORS,
        labels={
            "avg_package_LPA": "Avg Package (LPA)",
            "placement_percentage": "Placement %",
            "total_students": "Total Students",
        },
    )

    med_x = df["avg_package_LPA"].median()
    med_y = df["placement_percentage"].median()
    fig.add_hline(y=med_y, line_dash="dash", line_color="#cbd5e1", line_width=1)
    fig.add_vline(x=med_x, line_dash="dash", line_color="#cbd5e1", line_width=1)

    fig.update_traces(marker=dict(opacity=0.8, line=dict(width=0.5, color="white")))
    _apply_layout(fig, height=440, legend=dict(orientation="h", yanchor="bottom", y=1.04, xanchor="right", x=1))

    insight = ""
    if len(df) >= 4:
        corr = df["avg_package_LPA"].corr(df["placement_percentage"])
        strength = "strong" if abs(corr) > 0.7 else "moderate" if abs(corr) > 0.4 else "weak"
        insight = (
            f"There is a {strength} positive correlation (r = {corr:.2f}) between "
            f"average package and placement rate."
        )
    return fig, insight


def render_scatter_performance(df: pd.DataFrame) -> None:
    fig, insight = build_scatter_performance(df)
    _wrap_render("Placement Rate vs Avg Package", fig, insight)


# =====================================================================
# Chart 7 – Top Recruiting Companies (Horizontal Bar)
# =====================================================================
def build_top_companies(df: pd.DataFrame) -> Tuple[Optional[go.Figure], str]:
    if df.empty:
        return None, ""

    comp_df = get_company_data(df)
    if comp_df.empty:
        return None, "No company data available."

    comp_df_sorted = comp_df.sort_values("students", ascending=True)
    n = len(comp_df_sorted)
    bar_colors = [
        f"rgba({16 + int(i/n*0)},{185 - int(i/n*60)},{129 - int(i/n*30)},{0.55 + i/n*0.45})"
        for i in range(n)
    ]

    fig = go.Figure(go.Bar(
        x=comp_df_sorted["students"], y=comp_df_sorted["company"],
        orientation="h",
        marker_color=bar_colors,
        text=comp_df_sorted["students"],
        textposition="outside", textfont=dict(size=12),
    ))
    fig.update_xaxes(title_text="Students Placed")
    _apply_layout(fig, height=max(350, n * 40), showlegend=False, margin=dict(l=130, r=50, t=40, b=40))

    top = comp_df.iloc[0]
    insight = (
        f"{top['company']} is the top recruiter with {top['students']:,} "
        f"students placed across the selected period."
    )
    return fig, insight


def render_top_companies(df: pd.DataFrame) -> None:
    fig, insight = build_top_companies(df)
    _wrap_render("Top Recruiting Companies", fig, insight)


# =====================================================================
# Chart 8 – Job Role Distribution (Donut)
# =====================================================================
def build_job_role_distribution(df: pd.DataFrame) -> Tuple[Optional[go.Figure], str]:
    if df.empty:
        return None, ""

    role_df = get_role_data(df)
    if role_df.empty:
        return None, "No role data available."

    fig = go.Figure(go.Pie(
        labels=role_df["role"], values=role_df["count"],
        hole=0.50,
        marker=dict(colors=CHART_COLORS[:len(role_df)], line=dict(color="white", width=2)),
        textinfo="label+percent",
        textposition="outside",
        textfont=dict(size=11),
        insidetextorientation="horizontal",
        pull=[0.03 if i == 0 else 0 for i in range(len(role_df))],
    ))

    total = role_df["count"].sum()
    fig.update_layout(
        annotations=[dict(
            text=f"<b>{total}</b><br><span style='font-size:11px;color:#64748b'>mentions</span>",
            x=0.5, y=0.5, font_size=20, showarrow=False,
        )],
    )
    _apply_layout(fig, height=440, showlegend=False, margin=dict(l=20, r=20, t=40, b=20))

    top_role = role_df.iloc[0]
    insight = (
        f"{top_role['role']} is the most common role, appearing {top_role['count']} "
        f"times ({top_role['count']/total*100:.0f}% of mentions)."
    )
    return fig, insight


def render_job_role_distribution(df: pd.DataFrame) -> None:
    fig, insight = build_job_role_distribution(df)
    _wrap_render("Job Role Distribution", fig, insight)


# =====================================================================
# Chart 9 – Internship Conversion Impact (Scatter + Trendline)
# =====================================================================
def build_internship_conversion(df: pd.DataFrame) -> Tuple[Optional[go.Figure], str]:
    if df.empty:
        return None, ""

    fig = px.scatter(
        df, x="internship_conversion_rate_percent", y="placement_percentage",
        color="branch",
        trendline="ols",
        color_discrete_sequence=CHART_COLORS,
        labels={
            "internship_conversion_rate_percent": "Internship Conversion Rate (%)",
            "placement_percentage": "Placement %",
        },
        hover_data=["year"],
    )
    fig.update_traces(marker=dict(size=10, opacity=0.8, line=dict(width=0.5, color="white")))
    _apply_layout(fig, height=420, legend=dict(orientation="h", yanchor="bottom", y=1.04, xanchor="right", x=1))

    insight = ""
    if len(df) >= 4:
        corr = df["internship_conversion_rate_percent"].corr(df["placement_percentage"])
        r2 = corr ** 2
        strength = "strong" if r2 > 0.6 else "moderate" if r2 > 0.3 else "weak"
        insight = (
            f"Internship conversion rate shows a {strength} positive correlation "
            f"with placement percentage (R\u00b2 = {r2:.2f})."
        )
    return fig, insight


def render_internship_conversion(df: pd.DataFrame) -> None:
    fig, insight = build_internship_conversion(df)
    _wrap_render("Internship Conversion vs Placement Rate", fig, insight)


# =====================================================================
# Chart 10 – Year-over-Year Growth Heatmap
# =====================================================================
def build_growth_heatmap(df: pd.DataFrame) -> Tuple[Optional[go.Figure], str]:
    if df.empty:
        return None, ""

    pivot = df.pivot_table(index="branch", columns="year", values="placement_percentage", aggfunc="mean")
    pivot = pivot.round(1)
    pivot = pivot.loc[pivot.mean(axis=1).sort_values(ascending=False).index]

    text_vals = pivot.values
    annotations_text = [[f"{v:.1f}%" if not np.isnan(v) else "" for v in row] for row in text_vals]

    fig = go.Figure(go.Heatmap(
        z=pivot.values,
        x=[str(c) for c in pivot.columns],
        y=pivot.index.tolist(),
        text=annotations_text,
        texttemplate="%{text}",
        textfont=dict(size=12),
        colorscale=[
            [0.0, "#fef2f2"],
            [0.35, "#fef9c3"],
            [0.55, "#f0fdf4"],
            [1.0, "#065f46"],
        ],
        colorbar=dict(title="Placement %", thickness=12, len=0.7),
        hovertemplate="Branch: %{y}<br>Year: %{x}<br>Placement: %{text}<extra></extra>",
    ))
    _apply_layout(fig, height=380, showlegend=False, margin=dict(l=130, r=30, t=40, b=40))
    fig.update_xaxes(side="bottom")

    insight = ""
    if pivot.shape[1] >= 2:
        first_col, last_col = pivot.columns[0], pivot.columns[-1]
        growth = pivot[last_col] - pivot[first_col]
        best = growth.idxmax()
        insight = (
            f"{best} showed the most improvement, gaining "
            f"{growth[best]:.1f} percentage points from {first_col} to {last_col}."
        )
    return fig, insight


def render_growth_heatmap(df: pd.DataFrame) -> None:
    fig, insight = build_growth_heatmap(df)
    _wrap_render("Placement Rate by Branch & Year", fig, insight)
