"""
src/components/kpi_cards.py
Executive KPI Card Component for Business Intelligence Dashboards.
Uses render_html utility to guarantee pure visual rendering without Markdown code-block traps.
"""

from typing import Optional, List, Dict, Any
import streamlit as st
from src.theme import get_theme
from src.components.html_utils import render_html

def render_kpi_card(
    title: str,
    value: str,
    delta: Optional[str] = None,
    delta_type: str = "positive",   # positive, negative, neutral
    delta_label: Optional[str] = None,
    icon: str = "📈",
    badge: Optional[str] = None
) -> str:
    """
    Generates HTML for a single enterprise KPI card.
    """
    pill_class = "kpi-delta-neutral"
    if delta_type == "positive":
        pill_class = "kpi-delta-positive"
    elif delta_type == "negative":
        pill_class = "kpi-delta-negative"
        
    delta_markup = ""
    if delta:
        delta_markup = f"""
        <div class="kpi-footer">
            <span class="kpi-delta-pill {pill_class}">{delta}</span>
            {f'<span class="kpi-subtext">{delta_label}</span>' if delta_label else ''}
        </div>
        """
        
    badge_markup = ""
    if badge:
        badge_markup = f'<span class="chart-badge">{badge}</span>'

    card_html = f"""
    <div class="kpi-card">
        <div>
            <div class="kpi-header">
                <span class="kpi-title">{title}</span>
                <div style="display: flex; align-items: center; gap: 0.5rem;">
                    {badge_markup}
                    <div class="kpi-icon-wrap">{icon}</div>
                </div>
            </div>
            <div class="kpi-value">{value}</div>
        </div>
        {delta_markup}
    </div>
    """
    return card_html

def render_kpi_row(cards: List[Dict[str, Any]]):
    """
    Renders a row of KPI cards inside balanced Streamlit columns.
    """
    cols = st.columns(len(cards))
    for col, card in zip(cols, cards):
        with col:
            markup = render_kpi_card(
                title=card.get("title", ""),
                value=card.get("value", ""),
                delta=card.get("delta"),
                delta_type=card.get("delta_type", "neutral"),
                delta_label=card.get("delta_label"),
                icon=card.get("icon", "📈"),
                badge=card.get("badge")
            )
            render_html(markup)
