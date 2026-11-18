"""
src/components/navbar.py
Top Executive Navigation Bar Component.
Provides RetailPulse branding, live model status pulse, and active view context.
"""

from src.theme import get_theme
from src.components.html_utils import render_html

def render_navbar(active_view: str = "Executive Overview"):
    """
    Renders top navigation bar with branding, live status pulse, and active context.
    """
    theme = get_theme()
    
    html = f"""
    <div class="top-navbar">
        <div class="top-navbar-brand">
            <div class="top-navbar-logo">⚡</div>
            <div>
                <div class="top-navbar-title">RetailPulse</div>
                <div class="top-navbar-subtitle">Sales Intelligence &amp; Demand Forecasting Platform</div>
            </div>
        </div>
        <div style="display: flex; align-items: center; gap: 1rem;">
            <div class="top-navbar-status">
                <span class="status-pulse"></span>
                <span>Random Forest 300T • Active</span>
            </div>
        </div>
    </div>
    """
    render_html(html)
