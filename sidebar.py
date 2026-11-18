"""
src/components/sidebar.py
Collapsible Sidebar Component with Theme Toggle, View Navigation & Multi-dimensional Filters.
Includes seamless navigation back to the RetailPulse Welcome Screen.
Uses render_html utility to guarantee pure visual rendering without Markdown code-block traps.
"""

from typing import Dict, Any, Tuple
import streamlit as st
import pandas as pd
from src.theme import get_theme
from src.components.html_utils import render_html

def render_sidebar(raw_df: pd.DataFrame, daily_df: pd.DataFrame) -> Dict[str, Any]:
    """
    Renders sidebar controls, theme toggler, view selector, and global analytical filters.
    Returns dictionary with selected navigation view and active filter criteria.
    """
    theme = get_theme()
    current_theme = st.session_state.get("theme", "dark")
    
    with st.sidebar:
        # Header Branding
        header_brand = """
        <div style="display: flex; align-items: center; gap: 0.65rem; margin-bottom: 0.85rem;">
            <div style="width: 32px; height: 32px; border-radius: 8px; background: linear-gradient(135deg, #4F46E5, #EC4899); display: flex; align-items: center; justify-content: center; font-weight: 800; color: white;">⚡</div>
            <div>
                <div style="font-weight: 800; font-size: 1.1rem; letter-spacing: -0.01em;">RetailPulse</div>
                <div style="font-size: 0.7rem; color: #94A3B8;">Sales &amp; Demand Intelligence</div>
            </div>
        </div>
        """
        render_html(header_brand)

        # Return to Welcome Screen Action
        if st.button("🏠 Return to Welcome Screen", key="return_to_welcome_btn", use_container_width=True):
            st.session_state["page"] = "welcome"
            st.rerun()

        st.markdown("<div style='height: 0.5rem;'></div>", unsafe_allow_html=True)
        
        # Theme Toggle Switch
        col_t1, col_t2 = st.columns([1, 1])
        with col_t1:
            if st.button(
                "🌙 Dark Mode" if current_theme == "light" else "☀️ Light Mode",
                key="theme_toggle_btn",
                use_container_width=True
            ):
                st.session_state["theme"] = "dark" if current_theme == "light" else "light"
                st.rerun()
                
        with col_t2:
            theme_badge = f"""
            <div style="height: 100%; display: flex; align-items: center; justify-content: center; font-size: 0.72rem; font-weight: 600; color: {theme['text_muted']}; border: 1px solid {theme['border_color']}; border-radius: 8px; padding: 0.35rem;">
                Theme: <span style="color: {theme['accent_primary']}; margin-left: 4px; text-transform: uppercase;">{current_theme}</span>
            </div>
            """
            render_html(theme_badge)

        st.markdown("<hr style='border: none; border-top: 1px solid var(--border-color); margin: 1rem 0;'>", unsafe_allow_html=True)
        
        # View Navigation
        st.markdown("<div style='font-size: 0.72rem; font-weight: 700; text-transform: uppercase; letter-spacing: 0.08em; color: var(--text-muted); margin-bottom: 0.5rem;'>Navigation</div>", unsafe_allow_html=True)
        
        nav_options = [
            "📊 Executive Overview",
            "⚖️ Normal vs Festival Analysis",
            "📈 Next 7-Day Demand Forecasting",
            "🧠 AI Business Insights",
            "🔬 Model Diagnostics & Explainability"
        ]
        
        selected_view = st.radio(
            "Select Dashboard View",
            options=nav_options,
            label_visibility="collapsed",
            key="dashboard_active_view"
        )

        st.markdown("<hr style='border: none; border-top: 1px solid var(--border-color); margin: 1rem 0;'>", unsafe_allow_html=True)

        # Filters Section
        st.markdown("<div style='font-size: 0.72rem; font-weight: 700; text-transform: uppercase; letter-spacing: 0.08em; color: var(--text-muted); margin-bottom: 0.5rem;'>Data Filters</div>", unsafe_allow_html=True)

        # Date Range Filter
        min_date = raw_df["Date"].min().date()
        max_date = raw_df["Date"].max().date()
        
        selected_date_range = st.date_input(
            "Date Horizon",
            value=(min_date, max_date),
            min_value=min_date,
            max_value=max_date,
            key="filter_date_range"
        )
        
        # Season Type Filter
        all_seasons = sorted(raw_df["Season_Type"].unique().tolist())
        selected_seasons = st.multiselect(
            "Season Types",
            options=all_seasons,
            default=all_seasons,
            key="filter_seasons"
        )

        # Category Filter
        all_categories = sorted(raw_df["Category"].dropna().unique().tolist())
        selected_categories = st.multiselect(
            "Product Categories",
            options=all_categories,
            default=all_categories,
            key="filter_categories"
        )

        # Product Multi-select
        product_pool = raw_df[raw_df["Category"].isin(selected_categories) if selected_categories else True]
        all_products = sorted(product_pool["Description"].dropna().unique().tolist())
        selected_products = st.multiselect(
            "Products / SKUs",
            options=all_products,
            default=all_products,
            key="filter_products"
        )

        # Filter Reset Shortcut
        if st.button("↺ Reset All Filters", key="reset_filters_btn", use_container_width=True):
            st.session_state["filter_date_range"] = (min_date, max_date)
            st.session_state["filter_seasons"] = all_seasons
            st.session_state["filter_categories"] = all_categories
            st.session_state["filter_products"] = sorted(raw_df["Description"].dropna().unique().tolist())
            st.rerun()

        st.markdown("<hr style='border: none; border-top: 1px solid var(--border-color); margin: 1.25rem 0;'>", unsafe_allow_html=True)

        # System Status Micro-Card
        engine_status = f"""
        <div style="background: rgba(99, 102, 241, 0.08); border: 1px solid var(--border-color); border-radius: 12px; padding: 0.85rem; font-size: 0.72rem;">
            <div style="font-weight: 700; color: var(--accent); margin-bottom: 0.35rem; display: flex; align-items: center; gap: 0.4rem;">
                <span>⚡ Engine Status</span>
            </div>
            <div style="display: flex; justify-content: space-between; margin-bottom: 0.25rem; color: var(--text-secondary);">
                <span>Holdout MAE:</span>
                <strong style="color: var(--text-primary);">117.12 units</strong>
            </div>
            <div style="display: flex; justify-content: space-between; margin-bottom: 0.25rem; color: var(--text-secondary);">
                <span>Holdout R²:</span>
                <strong style="color: var(--text-primary);">0.676</strong>
            </div>
            <div style="display: flex; justify-content: space-between; color: var(--text-secondary);">
                <span>Rows:</span>
                <strong style="color: var(--text-primary);">{len(raw_df):,} Trans</strong>
            </div>
        </div>
        """
        render_html(engine_status)

    return {
        "view": selected_view,
        "date_range": selected_date_range,
        "seasons": selected_seasons if selected_seasons else all_seasons,
        "categories": selected_categories if selected_categories else all_categories,
        "products": selected_products if selected_products else all_products
    }
