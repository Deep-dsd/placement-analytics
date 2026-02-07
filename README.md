# Placement Analytics Dashboard

A modern, professional Streamlit dashboard that provides comprehensive insights into college campus placement data. Built with a clean, minimalist design using a slate-and-emerald color palette.

---

## Features

- **Interactive Filters** -- filter by year, branch, package range, and placement percentage via the sidebar
- **KPI Metric Cards** -- total placements, placement rate, highest package, and average package with year-over-year deltas
- **10 Visualizations** -- line charts, stacked bars, horizontal bars, box plots, area charts, scatter plots, donut charts, heatmaps, and trendline regressions
- **Auto-generated Insights** -- every chart includes a contextual one-liner highlighting key takeaways
- **Export** -- download filtered data as CSV directly from the sidebar
- **Responsive Layout** -- two-column chart grid that adapts to screen width

---

## Technology Stack

| Layer | Tool |
|-------|------|
| Frontend / Framework | [Streamlit](https://streamlit.io/) 1.31 |
| Charting | [Plotly](https://plotly.com/python/) 5.18 |
| Data Processing | [Pandas](https://pandas.pydata.org/) 2.2, [NumPy](https://numpy.org/) 1.26 |
| Statistics | [statsmodels](https://www.statsmodels.org/) 0.14+ (OLS trendlines) |
| Language | Python 3.9+ |

---

## Installation

### Prerequisites

- Python 3.9 or higher
- pip (or any Python package manager)

### Steps

```bash
# 1. Clone the repository
git clone <your-repo-url>
cd placement-analytics

# 2. Create a virtual environment (recommended)
python -m venv venv
source venv/bin/activate   # macOS/Linux
# venv\Scripts\activate    # Windows

# 3. Install dependencies
pip install -r requirements.txt
```

---

## Running the Application

```bash
streamlit run app.py
```

The dashboard opens at **http://localhost:8501** by default.

---

## Project Structure

```
placement-analytics/
├── app.py                      # Main Streamlit application
├── components/
│   ├── __init__.py
│   ├── filters.py             # Sidebar filter panel
│   ├── metrics.py             # KPI metric cards
│   └── visualizations.py      # All chart components
├── utils/
│   ├── __init__.py
│   ├── data_loader.py         # Data loading & preprocessing
│   └── styling.py             # Custom CSS & theming
├── data/
│   └── placement_data.csv     # Source data
├── assets/
│   └── custom.css             # External CSS reference
├── .streamlit/
│   └── config.toml            # Streamlit theme configuration
├── requirements.txt
├── .gitignore
└── README.md
```

---

## Data Schema

The dashboard expects a CSV (`data/placement_data.csv`) with the following columns:

| Column | Type | Description |
|--------|------|-------------|
| `year` | int | Academic year (e.g. 2020-2024) |
| `branch` | str | Engineering branch |
| `total_students` | int | Total students in the branch |
| `placed_students` | int | Students who received offers |
| `unplaced_students` | int | Students without offers |
| `placement_percentage` | float | Placement rate (%) |
| `highest_package_LPA` | float | Highest package (Lakhs per annum) |
| `median_package_LPA` | float | Median package |
| `lowest_package_LPA` | float | Lowest package |
| `avg_package_LPA` | float | Average package |
| `top_company_1/2/3` | str | Top three recruiting companies |
| `top_company_1/2/3_students` | int | Students placed per company |
| `top_job_role_1/2/3` | str | Most common job roles |
| `internship_conversion_rate_percent` | float | Internship-to-placement conversion rate |

---

## Features in Detail

### Filter Panel (Sidebar)

| Filter | Type | Default |
|--------|------|---------|
| Year | Multi-select | All years |
| Branch | Multi-select | All branches |
| Avg Package (LPA) | Range slider | Full range |
| Placement % | Range slider | 0 -- 100% |

An active-filter badge shows how many filters are currently applied. Use **Reset All** to return to defaults.

### Visualizations

1. **Placement Trends** -- multi-line chart of placement % by branch over years
2. **Students Placed vs Unplaced** -- stacked bar chart by year
3. **Branch-wise Placement Rate** -- horizontal bar with conditional coloring
4. **Package Distribution** -- box plot by branch
5. **Package Trends** -- area chart with highest, average, median, and lowest lines
6. **Placement Rate vs Avg Package** -- scatter plot with quadrant lines
7. **Top Recruiting Companies** -- horizontal bar chart, top 10
8. **Job Role Distribution** -- donut chart with center annotation
9. **Internship Conversion vs Placement** -- scatter with OLS trendline
10. **Placement Rate Heatmap** -- branch x year heatmap with diverging colors

---

## Deployment on Streamlit Cloud

1. Push this repository to GitHub.
2. Go to [share.streamlit.io](https://share.streamlit.io).
3. Sign in with your GitHub account.
4. Click **New app** and select the repository, branch (`main`), and main file (`app.py`).
5. Click **Deploy**. Streamlit Cloud installs `requirements.txt` automatically.
6. (Optional) Configure a custom subdomain under **Settings > Sharing**.

No secrets or environment variables are required -- all data ships with the repo.

---

## Customization Guide

- **Color Palette** -- edit `COLORS` and `CHART_COLORS` in `utils/styling.py`.
- **CSS Overrides** -- modify `_CUSTOM_CSS` in the same file.
- **Streamlit Theme** -- adjust `.streamlit/config.toml`.
- **Add New Charts** -- create a function in `components/visualizations.py` and call it from `app.py`.
- **Different Data** -- replace `data/placement_data.csv` while keeping the same column schema.

---

## Troubleshooting

| Issue | Fix |
|-------|-----|
| `ModuleNotFoundError` | Run `pip install -r requirements.txt` inside your virtual environment |
| Charts not rendering | Ensure Plotly is installed: `pip install plotly` |
| Port already in use | Run `streamlit run app.py --server.port 8502` |
| Filters not resetting | Clear browser cache or restart the Streamlit server |
| CSV encoding issues | Ensure the CSV is UTF-8 encoded |

---

## Future Enhancements

- Upload custom CSV files through the UI
- PDF report export
- Predictive analytics with ML-based forecasting
- Google Sheets integration for live data
- Email alerts for placement milestones
- Comparative analysis with peer institutions
- Admin panel for data management
- Dark mode toggle

---

## License

This project is provided for educational and institutional use. Modify and distribute as needed.
