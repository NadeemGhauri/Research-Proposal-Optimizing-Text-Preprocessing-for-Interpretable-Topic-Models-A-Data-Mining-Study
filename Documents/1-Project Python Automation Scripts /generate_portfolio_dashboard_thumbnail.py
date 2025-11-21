"""
Generate an impressive dashboard screenshot (1024x768 PNG) for portfolio
- Revenue trend line chart
- Regional performance bar chart
- Product distribution pie chart
- KPI metric cards
- Professional dark theme with branding
Output: ./Fiverr Portfolio Data/dashboard_preview.png
"""

import os
from datetime import datetime
import numpy as np
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots

BRAND_PRIMARY = "#1a5490"  # Brand blue
BRAND_ACCENT = "#2ecc71"   # Accent green
BRAND_WARN = "#f39c12"     # Accent orange
BRAND_TEXT = "#e8e8e8"
OUTPUT_DIR = "Fiverr Portfolio Data"
OUTPUT_FILE = os.path.join(OUTPUT_DIR, "dashboard_preview.png")


def load_sales_data(path: str = "data/sales_data.csv") -> pd.DataFrame:
    df = pd.read_csv(path)
    # Standardize types if present
    if "Date" in df.columns:
        df["Date"] = pd.to_datetime(df["Date"], errors="coerce")
    if "Revenue" in df.columns:
        df["Revenue"] = pd.to_numeric(df["Revenue"], errors="coerce").fillna(0.0)
    return df


def compute_kpis(df: pd.DataFrame) -> dict:
    total_revenue = float(df["Revenue"].sum()) if "Revenue" in df else 0.0
    orders = len(df)
    avg_order_value = float(total_revenue / orders) if orders else 0.0

    # Growth vs previous month (if Date exists)
    growth = 0.0
    if "Date" in df.columns:
        m = df.dropna(subset=["Date"]).copy()
        if not m.empty:
            m["Month"] = m["Date"].dt.to_period("M")
            monthly = m.groupby("Month")["Revenue"].sum().sort_index()
            if len(monthly) >= 2:
                last, prev = monthly.iloc[-1], monthly.iloc[-2]
                if prev != 0:
                    growth = (last - prev) / prev * 100.0

    # Top product by revenue
    top_product = "N/A"
    if "Product" in df.columns and "Revenue" in df.columns and not df.empty:
        top_product = df.groupby("Product")["Revenue"].sum().sort_values(ascending=False).head(1).index[0]

    return {
        "total_revenue": total_revenue,
        "orders": orders,
        "avg_order_value": avg_order_value,
        "growth_pct": growth,
        "top_product": top_product,
    }


def build_dashboard(df: pd.DataFrame) -> go.Figure:
    # Prepare data pieces
    # Revenue trend (monthly)
    trend_x, trend_y = [], []
    if "Date" in df.columns:
        d = df.dropna(subset=["Date"]).copy()
        d["Month"] = d["Date"].dt.to_period("M")
        monthly = d.groupby("Month")["Revenue"].sum().sort_index()
        trend_x = [str(m) for m in monthly.index]
        trend_y = monthly.values

    # Regional performance
    regions = []
    region_vals = []
    if "Region" in df.columns:
        region_grp = df.groupby("Region")["Revenue"].sum().sort_values(ascending=True)
        regions = region_grp.index.tolist()
        region_vals = region_grp.values

    # Product distribution (top 6 + Others)
    pie_labels = []
    pie_vals = []
    if "Product" in df.columns:
        prod_grp = df.groupby("Product")["Revenue"].sum().sort_values(ascending=False)
        top = prod_grp.head(6)
        other = prod_grp.iloc[6:].sum() if len(prod_grp) > 6 else 0
        pie_labels = top.index.tolist() + (["Others"] if other > 0 else [])
        pie_vals = top.values.tolist() + ([other] if other > 0 else [])

    kpis = compute_kpis(df)

    # Layout: 2 rows, 4 columns
    fig = make_subplots(
        rows=2,
        cols=4,
        specs=[
            [{"type": "domain"}, {"type": "domain"}, {"type": "domain"}, {"type": "domain"}],
            [{"type": "xy"}, {"type": "xy"}, {"type": "domain"}, {"type": "domain"}],
        ],
        horizontal_spacing=0.06,
        vertical_spacing=0.11,
        subplot_titles=(
            "Total Revenue", "Orders", "Avg Order Value", "Growth vs Prev Mo",
            "Revenue Trend", "Regional Performance", "Product Distribution", ""
        ),
    )

    # KPI Indicators (Row 1)
    fig.add_trace(
        go.Indicator(
            mode="number",
            value=kpis["total_revenue"],
            number={"prefix": "$", "valueformat": ",.0f", "font": {"color": BRAND_TEXT}},
            title={"text": "Total Revenue", "font": {"color": BRAND_TEXT}},
            domain={"row": 0, "column": 0},
        ), row=1, col=1
    )
    fig.add_trace(
        go.Indicator(
            mode="number",
            value=kpis["orders"],
            number={"valueformat": ",", "font": {"color": BRAND_TEXT}},
            title={"text": "Orders", "font": {"color": BRAND_TEXT}},
            domain={"row": 0, "column": 1},
        ), row=1, col=2
    )
    fig.add_trace(
        go.Indicator(
            mode="number",
            value=kpis["avg_order_value"],
            number={"prefix": "$", "valueformat": ",.0f", "font": {"color": BRAND_TEXT}},
            title={"text": "Avg Order Value", "font": {"color": BRAND_TEXT}},
            domain={"row": 0, "column": 2},
        ), row=1, col=3
    )
    fig.add_trace(
        go.Indicator(
            mode="number+delta",
            value=round(kpis["growth_pct"], 2),
            number={"suffix": "%", "font": {"color": BRAND_TEXT}},
            delta={"reference": 0, "increasing": {"color": BRAND_ACCENT}, "decreasing": {"color": "#e74c3c"}},
            title={"text": "Monthly Growth", "font": {"color": BRAND_TEXT}},
            domain={"row": 0, "column": 3},
        ), row=1, col=4
    )

    # Revenue trend line (Row 2, Col 1)
    if len(trend_x) > 0:
        fig.add_trace(
            go.Scatter(x=trend_x, y=trend_y, mode="lines+markers",
                       line={"color": BRAND_ACCENT, "width": 3}, marker={"size": 7},
                       name="Revenue"),
            row=2, col=1
        )

    # Regional performance bar (Row 2, Col 2)
    if len(regions) > 0:
        fig.add_trace(
            go.Bar(y=regions, x=region_vals, orientation="h",
                   marker={"color": BRAND_PRIMARY}, name="Revenue by Region"),
            row=2, col=2
        )

    # Product distribution pie (Row 2, Col 3)
    if len(pie_labels) > 0:
        fig.add_trace(
            go.Pie(labels=pie_labels, values=pie_vals, hole=0.35,
                   textfont={"color": BRAND_TEXT},
                   marker={"line": {"color": "#111", "width": 1}}),
            row=2, col=3
        )

    # Branding card: add as a paper-level annotation (avoids domain subplot constraints)
    brand_text = "Dr. Mahad Nadeem\nPython Automation Suite"
    fig.add_shape(
        type="rect",
        xref="paper", yref="paper",
        x0=0.77, x1=0.98, y0=0.08, y1=0.45,
        line=dict(color=BRAND_PRIMARY, width=1),
        fillcolor="rgba(26,84,144,0.15)",
        layer="below"
    )
    fig.add_annotation(
        text=brand_text,
        xref="paper", yref="paper",
        x=0.875, y=0.265,
        showarrow=False,
        font=dict(size=16, color=BRAND_TEXT),
        align="center",
        bgcolor="rgba(0,0,0,0)"
    )

    # Update layout (dark theme)
    fig.update_layout(
        template="plotly_dark",
        paper_bgcolor="#0f141a",
        plot_bgcolor="#0f141a",
        font=dict(color=BRAND_TEXT),
        title=dict(
            text="Sales Performance Dashboard",
            x=0.5, xanchor="center", y=0.98,
            font=dict(size=22, color=BRAND_TEXT)
        ),
        margin=dict(l=40, r=40, t=70, b=40),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
    )

    # Axis styling
    fig.update_xaxes(gridcolor="#25313d")
    fig.update_yaxes(gridcolor="#25313d")

    return fig


def ensure_output_dir():
    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR, exist_ok=True)


def main():
    ensure_output_dir()
    df = load_sales_data()
    fig = build_dashboard(df)

    # Export PNG 1024x768
    fig.write_image(OUTPUT_FILE, width=1024, height=768, scale=1)
    print(f"✓ Saved portfolio dashboard: {OUTPUT_FILE}")


if __name__ == "__main__":
    main()
