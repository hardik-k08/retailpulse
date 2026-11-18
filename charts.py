"""
src/components/charts.py
Interactive Plotly Visualizations for Retail Intelligence BI Dashboard.
Styled for Dark and Light Enterprise SaaS themes with custom hover tooltips.
Solid card-matching backgrounds with high-contrast labels and gridlines.
"""

from typing import Optional, Dict, Any
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots

from src.theme import get_theme, get_plotly_layout

DAY_NAMES = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]

def render_timeline_chart(daily_df: pd.DataFrame, theme_name: str = "dark") -> go.Figure:
    """
    Renders Daily Revenue & Quantity timeline with dual-axis interactive hover.
    """
    theme = get_theme(theme_name)
    layout_cfg = get_plotly_layout(theme_name)
    is_dark = theme_name == "dark"
    
    # Aggregate by date across filtered daily data
    timeline = daily_df.groupby("Date", as_index=False).agg(
        Revenue=("Revenue", "sum"),
        Quantity=("Quantity", "sum")
    ).sort_values("Date")
    
    fig = make_subplots(specs=[[{"secondary_y": True}]])
    
    # Revenue Filled Area Trace
    fig.add_trace(
        go.Scatter(
            x=timeline["Date"],
            y=timeline["Revenue"],
            name="Daily Revenue ($)",
            mode="lines",
            line=dict(color=theme["accent_primary"], width=2.5),
            fill="tozeroy",
            fillcolor="rgba(99, 102, 241, 0.16)" if is_dark else "rgba(79, 70, 229, 0.1)",
            hovertemplate="<b>Date:</b> %{x|%b %d, %Y}<br><b>Daily Revenue:</b> $%{y:,.2f}<extra></extra>"
        ),
        secondary_y=False
    )
    
    # Quantity Stepped/Line Trace
    fig.add_trace(
        go.Scatter(
            x=timeline["Date"],
            y=timeline["Quantity"],
            name="Units Sold",
            mode="lines",
            line=dict(color=theme["success"], width=2, dash="dot"),
            hovertemplate="<b>Units Sold:</b> %{y:,.0f} units<extra></extra>"
        ),
        secondary_y=True
    )
    
    fig.update_layout(
        layout_cfg,
        title=dict(text="", font=dict(size=14)),
        hovermode="x unified",
        height=380,
        yaxis=dict(
            title=dict(text="Revenue ($)", font=dict(color=theme["accent_primary"], size=12)),
            showgrid=True,
            gridcolor="rgba(255, 255, 255, 0.08)" if is_dark else "#E2E8F0",
            tickprefix="$",
            tickfont=dict(color=theme["text_secondary"], size=11)
        ),
        yaxis2=dict(
            title=dict(text="Units Sold", font=dict(color=theme["success"], size=12)),
            showgrid=False,
            overlaying="y",
            side="right",
            tickfont=dict(color=theme["text_secondary"], size=11)
        ),
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1,
            font=dict(color=theme["text_secondary"], size=11)
        )
    )
    return fig

def render_scenario_comparison_chart(comparison_df: pd.DataFrame, theme_name: str = "dark") -> go.Figure:
    """
    Renders grouped horizontal bar chart comparing Normal 7D vs Festive 7D demand per SKU.
    Includes difference units and percentage variation in tooltips.
    """
    theme = get_theme(theme_name)
    layout_cfg = get_plotly_layout(theme_name)
    is_dark = theme_name == "dark"
    
    df_sorted = comparison_df.sort_values("Festive_Predicted_7D", ascending=True).copy()
    
    fig = go.Figure()
    
    # Normal Demand Bars
    fig.add_trace(
        go.Bar(
            y=df_sorted["Description"],
            x=df_sorted["Normal_Predicted_7D"],
            name="Normal Season Demand (7D)",
            orientation="h",
            marker=dict(
                color="#64748B" if is_dark else "#94A3B8",
                line=dict(width=0)
            ),
            customdata=np.stack((df_sorted["StockCode"], df_sorted["Difference_Units"], df_sorted["Variation_%"]), axis=-1),
            hovertemplate=(
                "<b>%{y}</b> (SKU: %{customdata[0]})<br>"
                "Normal Demand: <b>%{x:,.1f} units</b><br>"
                "Festive Delta: <b>%{customdata[1]:+,.1f} units (%{customdata[2]:+.1f}%)</b><extra></extra>"
            )
        )
    )
    
    # Festive Demand Bars
    fig.add_trace(
        go.Bar(
            y=df_sorted["Description"],
            x=df_sorted["Festive_Predicted_7D"],
            name="Festive Season Demand (7D)",
            orientation="h",
            marker=dict(
                color=theme["accent_primary"],
                line=dict(width=0)
            ),
            customdata=np.stack((df_sorted["StockCode"], df_sorted["Difference_Units"], df_sorted["Variation_%"]), axis=-1),
            hovertemplate=(
                "<b>%{y}</b> (SKU: %{customdata[0]})<br>"
                "Festive Demand: <b>%{x:,.1f} units</b><br>"
                "Festive Delta: <b>%{customdata[1]:+,.1f} units (%{customdata[2]:+.1f}%)</b><extra></extra>"
            )
        )
    )
    
    fig.update_layout(
        layout_cfg,
        barmode="group",
        height=420,
        margin=dict(l=10, r=20, t=25, b=20),
        xaxis=dict(
            title=dict(text="Predicted 7-Day Quantity (Units)", font=dict(color=theme["text_secondary"])),
            tickfont=dict(color=theme["text_secondary"], size=11)
        ),
        yaxis=dict(
            title="",
            tickfont=dict(color=theme["text_primary"], size=11)
        )
    )
    return fig

def render_category_treemap(transactions_df: pd.DataFrame, theme_name: str = "dark") -> go.Figure:
    """
    Renders hierarchical Treemap of Revenue contribution by Category and Product SKU.
    """
    theme = get_theme(theme_name)
    
    grouped = transactions_df.groupby(["Category", "Description", "StockCode"], as_index=False).agg(
        TotalRevenue=("Total Sales", "sum"),
        TotalQuantity=("Quantity", "sum")
    )
    
    total_rev = grouped["TotalRevenue"].sum()
    grouped["RevShare"] = (grouped["TotalRevenue"] / total_rev * 100).round(1)
    
    colors = [
        theme["accent_primary"],
        theme["accent_secondary"],
        theme["success"],
        theme["warning"],
        "#EC4899",
        "#14B8A6"
    ]
    
    fig = px.treemap(
        grouped,
        path=[px.Constant("All Categories"), "Category", "Description"],
        values="TotalRevenue",
        color="Category",
        color_discrete_sequence=colors,
        custom_data=["TotalQuantity", "RevShare"]
    )
    
    fig.update_traces(
        hovertemplate=(
            "<b>%{label}</b><br>"
            "Revenue: $%{value:,.2f}<br>"
            "Share of Total: %{customdata[1]}%<br>"
            "Total Units Sold: %{customdata[0]:,} units<extra></extra>"
        ),
        textinfo="label+value+percent parent"
    )
    
    layout_cfg = get_plotly_layout(theme_name)
    fig.update_layout(
        layout_cfg,
        margin=dict(t=20, l=10, r=10, b=10),
        height=380
    )
    return fig

def render_pareto_chart(transactions_df: pd.DataFrame, theme_name: str = "dark") -> go.Figure:
    """
    Renders Pareto 80/20 Revenue Analysis with cumulative percentage curve.
    """
    theme = get_theme(theme_name)
    layout_cfg = get_plotly_layout(theme_name)
    
    prod_rev = transactions_df.groupby("Description", as_index=False).agg(
        Revenue=("Total Sales", "sum"),
        Quantity=("Quantity", "sum")
    ).sort_values("Revenue", ascending=False).reset_index(drop=True)
    
    total_revenue = prod_rev["Revenue"].sum()
    prod_rev["Cum_Revenue"] = prod_rev["Revenue"].cumsum()
    prod_rev["Cum_Pct"] = (prod_rev["Cum_Revenue"] / total_revenue * 100).round(1)
    
    fig = make_subplots(specs=[[{"secondary_y": True}]])
    
    # Bar Chart for Product Revenue
    fig.add_trace(
        go.Bar(
            x=prod_rev["Description"],
            y=prod_rev["Revenue"],
            name="Revenue ($)",
            marker=dict(
                color=theme["accent_primary"],
                line=dict(width=0)
            ),
            hovertemplate="<b>%{x}</b><br>Revenue: $%{y:,.2f}<extra></extra>"
        ),
        secondary_y=False
    )
    
    # Cumulative Line
    fig.add_trace(
        go.Scatter(
            x=prod_rev["Description"],
            y=prod_rev["Cum_Pct"],
            name="Cumulative %",
            mode="lines+markers",
            line=dict(color=theme["warning"], width=2.5),
            marker=dict(size=6, color=theme["warning"]),
            hovertemplate="Cumulative Revenue: <b>%{y:.1f}%</b><extra></extra>"
        ),
        secondary_y=True
    )
    
    # 80% Benchmark Reference Line
    fig.add_hline(
        y=80,
        line_dash="dash",
        line_color=theme["danger"],
        annotation_text="80% Pareto Threshold",
        annotation_position="bottom right",
        annotation_font=dict(color=theme["danger"], size=10),
        secondary_y=True
    )
    
    fig.update_layout(
        layout_cfg,
        height=380,
        xaxis=dict(
            tickangle=-35,
            tickfont=dict(color=theme["text_secondary"], size=10)
        ),
        yaxis=dict(
            title=dict(text="Revenue ($)", font=dict(color=theme["text_secondary"])),
            tickprefix="$",
            tickfont=dict(color=theme["text_muted"])
        ),
        yaxis2=dict(
            title=dict(text="Cumulative %", font=dict(color=theme["warning"])),
            range=[0, 105],
            ticksuffix="%",
            tickfont=dict(color=theme["text_muted"])
        ),
        hovermode="x"
    )
    return fig

def render_seasonality_heatmap(daily_df: pd.DataFrame, theme_name: str = "dark") -> go.Figure:
    """
    Renders 2D Heatmap of Average Daily Sales by Day of Week across Months / Seasons.
    """
    theme = get_theme(theme_name)
    layout_cfg = get_plotly_layout(theme_name)
    is_dark = theme_name == "dark"
    
    df_copy = daily_df.copy()
    df_copy["DayName"] = df_copy["DayOfWeek"].map(lambda x: DAY_NAMES[x])
    df_copy["MonthName"] = df_copy["Date"].dt.strftime("%B %Y")
    
    month_order = (
        df_copy[["Date", "MonthName"]]
        .drop_duplicates()
        .sort_values("Date")["MonthName"]
        .tolist()
    )
    
    pivot = df_copy.pivot_table(
        index="DayName",
        columns="MonthName",
        values="Revenue",
        aggfunc="mean"
    ).reindex(DAY_NAMES)[month_order].fillna(0)
    
    color_scale = [
        [0.0, "#0F172A" if is_dark else "#F1F5F9"],
        [0.35, "rgba(99, 102, 241, 0.45)" if is_dark else "#C7D2FE"],
        [0.7, theme["accent_primary"]],
        [1.0, "#EC4899" if is_dark else "#4338CA"]
    ]
    
    fig = go.Figure(
        data=go.Heatmap(
            z=pivot.values,
            x=pivot.columns.tolist(),
            y=pivot.index.tolist(),
            colorscale=color_scale,
            hovertemplate=(
                "<b>%{y}</b> • <b>%{x}</b><br>"
                "Avg Daily Revenue: <b>$%{z:,.2f}</b><extra></extra>"
            ),
            colorbar=dict(
                title=dict(text="Avg Rev ($)", font=dict(color=theme["text_secondary"], size=10)),
                tickprefix="$",
                tickfont=dict(color=theme["text_muted"]),
                len=0.85
            )
        )
    )
    
    fig.update_layout(
        layout_cfg,
        height=340,
        margin=dict(t=20, l=10, r=10, b=20),
        xaxis=dict(
            title=dict(text="Calendar Period", font=dict(color=theme["text_secondary"])),
            tickfont=dict(color=theme["text_primary"])
        ),
        yaxis=dict(
            title="",
            tickfont=dict(color=theme["text_primary"])
        )
    )
    return fig

def render_feature_importance_chart(fi_df: pd.DataFrame, theme_name: str = "dark") -> go.Figure:
    """
    Renders horizontal bar chart of Random Forest feature importances for Model Explainability.
    """
    theme = get_theme(theme_name)
    layout_cfg = get_plotly_layout(theme_name)
    is_dark = theme_name == "dark"
    
    df_sorted = fi_df.sort_values("Importance", ascending=True).copy()
    df_sorted["Pct_Label"] = (df_sorted["Importance"] * 100).round(1).astype(str) + "%"
    
    fig = go.Figure(
        go.Bar(
            y=df_sorted["Feature_Label"],
            x=df_sorted["Importance"] * 100,
            orientation="h",
            marker=dict(
                color=df_sorted["Importance"],
                colorscale=[
                    [0.0, "rgba(99, 102, 241, 0.45)" if is_dark else "#C7D2FE"],
                    [1.0, theme["accent_primary"]]
                ],
                line=dict(width=0)
            ),
            text=df_sorted["Pct_Label"],
            textposition="outside",
            textfont=dict(color=theme["text_primary"], size=11, family="'Plus Jakarta Sans', sans-serif"),
            customdata=df_sorted["Feature"],
            hovertemplate=(
                "<b>%{y}</b> (<code>%{customdata}</code>)<br>"
                "Model Weight: <b>%{x:.2f}%</b><extra></extra>"
            )
        )
    )
    
    fig.update_layout(
        layout_cfg,
        height=380,
        margin=dict(l=10, r=45, t=20, b=20),
        xaxis=dict(
            title=dict(text="Relative Importance Weight (%)", font=dict(color=theme["text_secondary"])),
            tickfont=dict(color=theme["text_muted"]),
            range=[0, max(df_sorted["Importance"] * 100) * 1.18]
        ),
        yaxis=dict(
            title="",
            tickfont=dict(color=theme["text_primary"], size=11)
        )
    )
    return fig
