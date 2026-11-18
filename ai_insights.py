"""
src/components/ai_insights.py
Dynamic Executive Business Intelligence & Inventory Advisory Engine.
Derives 100% of insights, ratios, risk levels, and recommendations directly from actual data.
Never hardcodes synthetic metrics, never invents supplier lead times or imaginary stock.
Uses render_html utility to guarantee pure visual rendering without Markdown code-block traps.
"""

from typing import Dict, Any, List
import pandas as pd
import numpy as np
import streamlit as st
from src.theme import get_theme
from src.components.html_utils import render_html

def generate_executive_ai_summary(
    raw_df: pd.DataFrame,
    daily_df: pd.DataFrame,
    comparison_df: pd.DataFrame
) -> Dict[str, Any]:
    """
    Computes dynamic financial, operational, and predictive metrics from filtered data slices.
    """
    # 1. Historical Actuals
    total_revenue = float(raw_df["Total Sales"].sum()) if "Total Sales" in raw_df.columns else 0.0
    total_quantity = float(raw_df["Quantity"].sum()) if "Quantity" in raw_df.columns else 0.0
    total_transactions = int(len(raw_df))
    aov = total_revenue / total_transactions if total_transactions > 0 else 0.0
    
    # 2. Seasonal Actuals (Historical Daily Run-rates)
    daily_seasonal = daily_df.groupby("Season_Type").agg(
        Total_Rev=("Revenue", "sum"),
        Total_Qty=("Quantity", "sum"),
        Days=("Date", "nunique")
    )
    
    normal_days = int(daily_seasonal.loc["Normal", "Days"]) if "Normal" in daily_seasonal.index else 1
    festive_days = int(daily_seasonal.loc["Festive", "Days"]) if "Festive" in daily_seasonal.index else 1
    
    normal_daily_rev = float(daily_seasonal.loc["Normal", "Total_Rev"]) / normal_days if "Normal" in daily_seasonal.index else 0.0
    festive_daily_rev = float(daily_seasonal.loc["Festive", "Total_Rev"]) / festive_days if "Festive" in daily_seasonal.index else 0.0
    
    seasonal_daily_ratio = festive_daily_rev / normal_daily_rev if normal_daily_rev > 0 else 1.0

    # 3. Model Predicted 7-Day Scenario Forecasts
    total_normal_7d = float(comparison_df["Normal_Predicted_7D"].sum()) if not comparison_df.empty else 0.0
    total_festive_7d = float(comparison_df["Festive_Predicted_7D"].sum()) if not comparison_df.empty else 0.0
    diff_units = total_festive_7d - total_normal_7d
    surge_pct = (diff_units / total_normal_7d * 100) if total_normal_7d > 0 else 0.0
    
    # 4. SKU-level Unit Prices & Projected Revenue Opportunity
    unit_prices = raw_df.groupby("StockCode")["UnitPrice"].mean().to_dict()
    
    comp_with_rev = comparison_df.copy()
    comp_with_rev["UnitPrice"] = comp_with_rev["StockCode"].map(unit_prices).fillna(0.0)
    comp_with_rev["Incremental_Revenue"] = comp_with_rev["Difference_Units"] * comp_with_rev["UnitPrice"]
    projected_incremental_rev = float(comp_with_rev["Incremental_Revenue"].sum())

    # 5. Top Surge and Highest Volume SKUs
    top_surge_row = comp_with_rev.sort_values("Variation_%", ascending=False).iloc[0] if not comp_with_rev.empty else None
    top_festive_demand_row = comp_with_rev.sort_values("Festive_Predicted_7D", ascending=False).iloc[0] if not comp_with_rev.empty else None

    # 6. Revenue Concentration (Top Products)
    prod_rev = raw_df.groupby(["StockCode", "Description"])["Total Sales"].sum().sort_values(ascending=False)
    top1_share = (prod_rev.iloc[0] / total_revenue * 100) if len(prod_rev) > 0 and total_revenue > 0 else 0.0
    top3_share = (prod_rev.iloc[:3].sum() / total_revenue * 100) if len(prod_rev) >= 3 and total_revenue > 0 else 0.0

    return {
        "total_revenue": total_revenue,
        "total_quantity": total_quantity,
        "total_transactions": total_transactions,
        "aov": aov,
        "normal_daily_rev": normal_daily_rev,
        "festive_daily_rev": festive_daily_rev,
        "seasonal_daily_ratio": seasonal_daily_ratio,
        "total_normal_7d": total_normal_7d,
        "total_festive_7d": total_festive_7d,
        "diff_units": diff_units,
        "surge_pct": surge_pct,
        "projected_incremental_rev": projected_incremental_rev,
        "top_surge_sku": top_surge_row["Description"] if top_surge_row is not None else "N/A",
        "top_surge_code": top_surge_row["StockCode"] if top_surge_row is not None else "N/A",
        "top_surge_pct": float(top_surge_row["Variation_%"]) if top_surge_row is not None else 0.0,
        "top_surge_diff": float(top_surge_row["Difference_Units"]) if top_surge_row is not None else 0.0,
        "top_volume_sku": top_festive_demand_row["Description"] if top_festive_demand_row is not None else "N/A",
        "top_volume_demand": float(top_festive_demand_row["Festive_Predicted_7D"]) if top_festive_demand_row is not None else 0.0,
        "top1_share": top1_share,
        "top3_share": top3_share
    }

def generate_replenishment_table(
    comparison_df: pd.DataFrame,
    raw_df: pd.DataFrame
) -> pd.DataFrame:
    """
    Constructs an objective Inventory Replenishment & Stockout Vulnerability assessment.
    """
    unit_prices = raw_df.groupby("StockCode")["UnitPrice"].mean().to_dict()
    
    table = comparison_df.copy()
    table["Unit_Price"] = table["StockCode"].map(unit_prices).fillna(0.0)
    table["Daily_Run_Rate"] = (table["Festive_Predicted_7D"] / 7.0).round(1)
    table["Surge_Multiplier"] = np.where(
        table["Normal_Predicted_7D"] > 0,
        (table["Festive_Predicted_7D"] / table["Normal_Predicted_7D"]).round(2),
        np.nan
    )
    table["Incremental_Revenue"] = (table["Difference_Units"] * table["Unit_Price"]).round(2)
    
    def assign_risk(var_pct: float) -> str:
        if pd.isna(var_pct):
            return "Unknown"
        elif var_pct >= 200.0:
            return "High"
        elif var_pct >= 100.0:
            return "Moderate"
        else:
            return "Stable"
            
    table["Stockout_Risk"] = table["Variation_%"].apply(assign_risk)
    
    def recommend_action(row) -> str:
        mult = row["Surge_Multiplier"]
        risk = row["Stockout_Risk"]
        if risk == "High":
            return f"Priority Procurement: Prepare ~{mult:.1f}x normal seasonal order quantity to absorb extreme surge."
        elif risk == "Moderate":
            return f"Buffer Staging: Procure ~{mult:.1f}x baseline stock; monitor replenishment cycle weekly."
        else:
            return f"Standard Replenishment: Projected run rate is ~{mult:.1f}x normal; align with routine restocking."
            
    table["Replenishment_Advice"] = table.apply(recommend_action, axis=1)
    return table

def render_ai_insights_view(
    raw_df: pd.DataFrame,
    daily_df: pd.DataFrame,
    comparison_df: pd.DataFrame,
    theme_name: str = "dark"
):
    """
    Renders the AI Business Insights & Inventory Planning view in Streamlit.
    """
    theme = get_theme(theme_name)
    summary = generate_executive_ai_summary(raw_df, daily_df, comparison_df)
    replenishment_df = generate_replenishment_table(comparison_df, raw_df)

    # Header Card
    header_html = f"""
    <div class="chart-container-card" style="margin-bottom: 1.5rem;">
        <div style="display: flex; align-items: center; justify-content: space-between; margin-bottom: 0.75rem;">
            <div style="display: flex; align-items: center; gap: 0.6rem;">
                <div style="width: 28px; height: 28px; border-radius: 6px; background: {theme['accent_gradient']}; display: flex; align-items: center; justify-content: center; font-size: 0.9rem; color: white;">🧠</div>
                <span style="font-weight: 700; font-size: 1.1rem; color: var(--text-primary);">Executive AI Business Summary</span>
            </div>
            <span class="chart-badge">Dynamic Data Synthesis</span>
        </div>
        <div style="color: var(--text-secondary); font-size: 0.88rem; line-height: 1.6;">
            Based on the active filtered scope of <strong>{summary['total_transactions']:,} transactions</strong> across 
            <strong>{len(comparison_df)} product SKUs</strong>, the Random Forest model projects a total 7-day festive demand of 
            <strong style="color: {theme['accent_primary']};">{summary['total_festive_7d']:,.1f} units</strong> compared to 
            <strong>{summary['total_normal_7d']:,.1f} units</strong> in the baseline normal period.
            This reflects an aggregate demand surge of <strong style="color: {theme['success']};">+{summary['diff_units']:+,.1f} units (+{summary['surge_pct']:.1f}%)</strong>, 
            representing an estimated <strong>${summary['projected_incremental_rev']:+,.2f}</strong> in incremental 7-day revenue potential.
        </div>
    </div>
    """
    render_html(header_html)

    # 4 Dynamic Insight Micro Cards
    c1, c2, c3, c4 = st.columns(4)
    with c1:
        render_html(f"""
        <div class="kpi-card">
            <div class="kpi-header">
                <span class="kpi-title">Incremental 7D Value</span>
                <span class="kpi-icon-wrap">💵</span>
            </div>
            <div class="kpi-value">${summary['projected_incremental_rev']:+,.0f}</div>
            <div class="kpi-footer">
                <span class="kpi-delta-pill kpi-delta-positive">{summary['diff_units']:+,.0f} units</span>
                <span class="kpi-subtext">vs Normal Baseline</span>
            </div>
        </div>
        """)
    with c2:
        render_html(f"""
        <div class="kpi-card">
            <div class="kpi-header">
                <span class="kpi-title">Festive Daily Velocity</span>
                <span class="kpi-icon-wrap">⚡</span>
            </div>
            <div class="kpi-value">{summary['seasonal_daily_ratio']:.2f}x</div>
            <div class="kpi-footer">
                <span class="kpi-delta-pill kpi-delta-positive">${summary['festive_daily_rev']:,.0f}/day</span>
                <span class="kpi-subtext">vs ${summary['normal_daily_rev']:,.0f} Normal</span>
            </div>
        </div>
        """)
    with c3:
        render_html(f"""
        <div class="kpi-card">
            <div class="kpi-header">
                <span class="kpi-title">Peak Surge SKU</span>
                <span class="kpi-icon-wrap">🚀</span>
            </div>
            <div class="kpi-value">+{summary['top_surge_pct']:.0f}%</div>
            <div class="kpi-footer">
                <span class="kpi-subtext" style="white-space: nowrap; overflow: hidden; text-overflow: ellipsis; max-width: 100%;">
                    {summary['top_surge_sku']}
                </span>
            </div>
        </div>
        """)
    with c4:
        render_html(f"""
        <div class="kpi-card">
            <div class="kpi-header">
                <span class="kpi-title">Top 3 SKUs Revenue Share</span>
                <span class="kpi-icon-wrap">📊</span>
            </div>
            <div class="kpi-value">{summary['top3_share']:.1f}%</div>
            <div class="kpi-footer">
                <span class="kpi-delta-pill kpi-delta-neutral">Concentration</span>
                <span class="kpi-subtext">Top 1 SKU: {summary['top1_share']:.1f}%</span>
            </div>
        </div>
        """)

    st.markdown("<div style='height: 1.25rem;'></div>", unsafe_allow_html=True)

    # Replenishment & Stockout Risk Table Header
    render_html("""
    <div style="display: flex; align-items: center; justify-content: space-between; margin-bottom: 0.75rem;">
        <div>
            <h3 style="margin: 0; font-size: 1.15rem; font-weight: 700;">📦 Inventory Replenishment &amp; Stockout Vulnerability Advisor</h3>
            <p style="margin: 0; font-size: 0.8rem; color: var(--text-muted);">
                Recommended procurement multipliers calculated directly from predicted festive demand vs normal run rate.
            </p>
        </div>
    </div>
    """)

    # Format table for display
    display_cols = [
        "Description", "Category", "Normal_Predicted_7D", "Festive_Predicted_7D",
        "Daily_Run_Rate", "Surge_Multiplier", "Variation_%", "Stockout_Risk", "Replenishment_Advice"
    ]
    formatted_df = replenishment_df[display_cols].copy()
    
    st.dataframe(
        formatted_df.style.format({
            "Normal_Predicted_7D": "{:.1f}",
            "Festive_Predicted_7D": "{:.1f}",
            "Daily_Run_Rate": "{:.1f} /day",
            "Surge_Multiplier": "{:.2f}x",
            "Variation_%": "{:+.1f}%"
        }),
        use_container_width=True,
        height=380
    )

    # Strategic Takeaways & Limitations Expander
    with st.expander("ℹ️ AI Analytical Methodology & Scientific Limitations", expanded=False):
        st.markdown(
            """
            #### Calculation Methodology
            - **Forecast Target**: 7-day forward rolling sum of units sold per SKU, modeled via Random Forest Regressor (`n_estimators=300, max_depth=10, min_samples_leaf=2`).
            - **Surge Multiplier**: Defined strictly as `Festive_Predicted_7D / Normal_Predicted_7D`. It indicates the relative scaling factor required if stocking for the holiday surge relative to baseline operations.
            - **Stockout Vulnerability Rating**:
              - **High Risk**: Projected demand variation $\\ge +200\\%$ (demands exceeds $3\\times$ baseline velocity).
              - **Moderate Risk**: Projected demand variation between $+100\\%$ and $+199.9\\%$.
              - **Stable**: Projected variation $< +100\\%$.
            - **Incremental Value**: Calculated by multiplying the predicted unit difference by the historical mean unit price: $\\Delta \\text{Units} \\times \\bar{P}_{\\text{unit}}$.
            
            #### Critical Limitations & Boundary Conditions
            - **No Current Inventory Data**: The dataset contains transaction records and daily features only; it does not record real-time warehouse inventory, safety stock thresholds, lead times, or supplier constraints. Recommendations are demand-oriented multipliers.
            - **Limited Sample**: Analysis is based on 10 SKUs across two distinct 61-day windows (April–May 2025 and October–November 2025).
            - **Non-Causal Notice**: Observed differences represent historical seasonal demand contrast between the two measured periods, not proven causal impact of festivals alone.
            """
        )
