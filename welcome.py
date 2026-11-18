"""
src/components/welcome.py
RetailPulse Welcome / Landing Page Component.
Premium Enterprise SaaS Hero Screen with Animated Visual Accents, Feature Highlights, and Direct Dashboard Navigation.
Uses dedicated render_html utility to guarantee pure visual rendering without Markdown code-block traps.
"""

import textwrap
import streamlit as st
from src.theme import get_theme
from src.components.html_utils import render_html

def render_welcome_page():
    """
    Renders the full-screen welcome landing page for RetailPulse.
    Guarantees pure HTML visual rendering with zero raw markup displayed.
    """
    theme = get_theme()
    is_dark = theme["name"] == "dark"
    current_theme = st.session_state.get("theme", "dark")

    # 1. Inject Welcome Page Dedicated CSS
    welcome_css = f"""
    <style>
    /* Hide sidebar completely on welcome page */
    section[data-testid="stSidebar"] {{
        display: none !important;
    }}
    
    .main .block-container {{
        max-width: 1080px !important;
        padding-top: 1.5rem !important;
        padding-bottom: 3rem !important;
    }}

    /* Hero Wrapper */
    .welcome-wrapper {{
        display: flex;
        flex-direction: column;
        align-items: center;
        text-align: center;
        position: relative;
        padding: 1.5rem 1rem 0.5rem 1rem;
    }}

    /* Ambient Glowing Orbs */
    .glow-orb-1 {{
        position: absolute;
        top: -30px;
        left: 20%;
        width: 380px;
        height: 380px;
        background: radial-gradient(circle, rgba(99, 102, 241, 0.22) 0%, rgba(99, 102, 241, 0) 70%);
        border-radius: 50%;
        pointer-events: none;
        z-index: 0;
        animation: floatGlow 8s ease-in-out infinite alternate;
    }}

    .glow-orb-2 {{
        position: absolute;
        top: 60px;
        right: 15%;
        width: 420px;
        height: 420px;
        background: radial-gradient(circle, rgba(236, 72, 153, 0.16) 0%, rgba(139, 92, 246, 0) 70%);
        border-radius: 50%;
        pointer-events: none;
        z-index: 0;
        animation: floatGlow 10s ease-in-out infinite alternate-reverse;
    }}

    @keyframes floatGlow {{
        0% {{ transform: translate(0, 0) scale(1); }}
        50% {{ transform: translate(25px, 20px) scale(1.08); }}
        100% {{ transform: translate(-20px, 35px) scale(0.95); }}
    }}

    /* Brand Top Pill */
    .brand-badge {{
        display: inline-flex;
        align-items: center;
        gap: 0.5rem;
        padding: 0.4rem 1.1rem;
        background: {"rgba(99, 102, 241, 0.14)" if is_dark else "rgba(79, 70, 229, 0.08)"};
        border: 1px solid {"rgba(99, 102, 241, 0.35)" if is_dark else "rgba(79, 70, 229, 0.25)"};
        border-radius: 9999px;
        font-size: 0.78rem;
        font-weight: 700;
        letter-spacing: 0.08em;
        text-transform: uppercase;
        color: {theme["accent_primary"]};
        margin-bottom: 1.35rem;
        z-index: 1;
        backdrop-filter: blur(8px);
        box-shadow: 0 2px 10px rgba(99, 102, 241, 0.15);
    }}

    /* Main Brand Title */
    .brand-title {{
        font-size: clamp(2.8rem, 6.2vw, 4.6rem);
        font-weight: 900;
        letter-spacing: -0.03em;
        line-height: 1.05;
        margin-bottom: 0.85rem;
        background: {
            "linear-gradient(135deg, #FFFFFF 10%, #E2E8F0 40%, #818CF8 80%, #C084FC 100%)"
            if is_dark else
            "linear-gradient(135deg, #0F172A 0%, #1E293B 40%, #4F46E5 80%, #7C3AED 100%)"
        };
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        z-index: 1;
        text-shadow: {"0 10px 30px rgba(99, 102, 241, 0.25)" if is_dark else "none"};
    }}

    /* Subtitle & Tagline */
    .brand-subtitle {{
        font-size: clamp(1.15rem, 2.4vw, 1.45rem);
        font-weight: 700;
        color: {theme["text_primary"]};
        letter-spacing: -0.01em;
        margin-bottom: 0.6rem;
        z-index: 1;
    }}

    .brand-tagline {{
        font-size: clamp(0.95rem, 1.8vw, 1.15rem);
        font-weight: 400;
        color: {theme["text_secondary"]};
        max-width: 640px;
        line-height: 1.6;
        margin-bottom: 1.75rem;
        z-index: 1;
    }}

    /* Abstract Animated Wave Visualization */
    .visual-wave-container {{
        width: 100%;
        max-width: 780px;
        height: 110px;
        margin: 0 auto 2rem auto;
        position: relative;
        z-index: 1;
        display: flex;
        align-items: center;
        justify-content: center;
    }}

    .wave-svg {{
        width: 100%;
        height: 100%;
        overflow: visible;
    }}

    .wave-path {{
        stroke-dasharray: 1000;
        stroke-dashoffset: 1000;
        animation: drawLine 3.5s cubic-bezier(0.16, 1, 0.3, 1) forwards, floatWave 6s ease-in-out infinite alternate;
    }}

    @keyframes drawLine {{
        to {{ stroke-dashoffset: 0; }}
    }}

    @keyframes floatWave {{
        0% {{ transform: translateY(0); }}
        100% {{ transform: translateY(-5px); }}
    }}

    /* Feature Highlight Grid */
    .feature-grid {{
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
        gap: 1.25rem;
        width: 100%;
        max-width: 960px;
        margin: 0 auto 2rem auto;
        z-index: 1;
    }}

    .feature-item {{
        background: {theme["bg_card"]} !important;
        border: 1px solid {theme["border_color"]} !important;
        border-radius: 16px;
        padding: 1.4rem;
        text-align: left;
        transition: all 0.3s cubic-bezier(0.16, 1, 0.3, 1);
        position: relative;
        overflow: hidden;
        box-shadow: {theme["shadow_sm"]};
    }}

    .feature-item:hover {{
        transform: translateY(-4px);
        border-color: {theme["border_glow"]} !important;
        box-shadow: {theme["shadow_md"]};
    }}

    .feature-item::before {{
        content: "";
        position: absolute;
        top: 0;
        left: 0;
        width: 100%;
        height: 2px;
        background: {theme["accent_gradient"]};
    }}

    .feature-icon-box {{
        width: 42px;
        height: 42px;
        border-radius: 10px;
        background: {"rgba(99, 102, 241, 0.15)" if is_dark else "rgba(79, 70, 229, 0.1)"};
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 1.3rem;
        margin-bottom: 0.9rem;
    }}

    .feature-item-title {{
        font-size: 1rem;
        font-weight: 700;
        color: {theme["text_primary"]} !important;
        margin-bottom: 0.4rem;
        letter-spacing: -0.01em;
    }}

    .feature-item-desc {{
        font-size: 0.83rem;
        color: {theme["text_secondary"]} !important;
        line-height: 1.55;
    }}

    /* Prominent CTA Button Styling */
    .welcome-btn-wrapper button {{
        background: linear-gradient(135deg, #4F46E5 0%, #7C3AED 50%, #EC4899 100%) !important;
        color: #FFFFFF !important;
        border: none !important;
        border-radius: 14px !important;
        padding: 0.9rem 2.5rem !important;
        font-size: 1.15rem !important;
        font-weight: 800 !important;
        letter-spacing: -0.01em !important;
        box-shadow: 0 10px 30px rgba(99, 102, 241, 0.45) !important;
        transition: all 0.3s cubic-bezier(0.16, 1, 0.3, 1) !important;
        cursor: pointer !important;
    }}

    .welcome-btn-wrapper button:hover {{
        transform: translateY(-3px) scale(1.02) !important;
        box-shadow: 0 14px 40px rgba(124, 58, 237, 0.6) !important;
        filter: brightness(1.12) !important;
    }}

    /* Footer */
    .welcome-footer {{
        margin-top: 2.5rem;
        font-size: 0.78rem;
        color: {theme["text_muted"]} !important;
        letter-spacing: 0.05em;
        text-transform: uppercase;
        font-weight: 600;
        display: flex;
        align-items: center;
        justify-content: center;
        gap: 0.6rem;
        z-index: 1;
    }}

    .welcome-footer-dot {{
        width: 5px;
        height: 5px;
        border-radius: 50%;
        background-color: {theme["accent_primary"]};
    }}
    </style>
    """
    render_html(welcome_css)

    # 2. Top Bar (Theme Toggle)
    top_c1, top_c2 = st.columns([6, 1.2])
    with top_c2:
        if st.button(
            "🌙 Dark" if current_theme == "light" else "☀️ Light",
            key="welcome_theme_toggle_btn",
            use_container_width=True
        ):
            st.session_state["theme"] = "dark" if current_theme == "light" else "light"
            st.rerun()

    # 3. Main Hero Visual Interface
    hero_markup = f"""
    <div class="welcome-wrapper">
        <div class="glow-orb-1"></div>
        <div class="glow-orb-2"></div>
        
        <div class="brand-badge">
            <span>⚡</span>
            <span>Next-Generation Demand Intelligence</span>
        </div>
        
        <div class="brand-title">RETAILPULSE</div>
        <div class="brand-subtitle">Sales Intelligence &amp; Demand Forecasting Platform</div>
        <div class="brand-tagline">
            Turn Retail Data into Smarter Business Decisions.<br>
            Leverage machine learning, seasonal holiday simulations, and objective inventory recommendations.
        </div>

        <!-- Abstract Glowing Trendline Visualization -->
        <div class="visual-wave-container">
            <svg class="wave-svg" viewBox="0 0 800 120" fill="none" xmlns="http://www.w3.org/2000/svg">
                <defs>
                    <linearGradient id="waveGradient" x1="0%" y1="0%" x2="100%" y2="0%">
                        <stop offset="0%" stop-color="#4F46E5" stop-opacity="0.2"/>
                        <stop offset="35%" stop-color="#8B5CF6" stop-opacity="0.8"/>
                        <stop offset="70%" stop-color="#EC4899" stop-opacity="0.9"/>
                        <stop offset="100%" stop-color="#10B981" stop-opacity="0.8"/>
                    </linearGradient>
                    <linearGradient id="areaGradient" x1="0%" y1="0%" x2="0%" y2="100%">
                        <stop offset="0%" stop-color="#6366F1" stop-opacity="0.22"/>
                        <stop offset="100%" stop-color="#6366F1" stop-opacity="0.0"/>
                    </linearGradient>
                </defs>
                <path class="wave-path" d="M 0 95 Q 100 20, 200 65 T 400 35 T 600 80 T 800 25 L 800 120 L 0 120 Z" fill="url(#areaGradient)"/>
                <path class="wave-path" d="M 0 95 Q 100 20, 200 65 T 400 35 T 600 80 T 800 25" stroke="url(#waveGradient)" stroke-width="3.5" stroke-linecap="round" fill="none"/>
                <circle cx="200" cy="65" r="4.5" fill="#8B5CF6"/>
                <circle cx="400" cy="35" r="4.5" fill="#EC4899"/>
                <circle cx="600" cy="80" r="4.5" fill="#6366F1"/>
                <circle cx="800" cy="25" r="5.5" fill="#10B981"/>
            </svg>
        </div>

        <!-- 3 Feature Highlights Cards -->
        <div class="feature-grid">
            <div class="feature-item">
                <div class="feature-icon-box">📈</div>
                <div class="feature-item-title">Executive BI &amp; Analytics</div>
                <div class="feature-item-desc">
                    Dual-axis revenue timelines, category treemaps, and Pareto 80/20 revenue concentration curves.
                </div>
            </div>
            <div class="feature-item">
                <div class="feature-icon-box">🤖</div>
                <div class="feature-item-title">Random Forest Forecasting</div>
                <div class="feature-item-desc">
                    Next 7-day rolling demand forecasting validated on an 80/20 chronological holdout with an R² of 0.676.
                </div>
            </div>
            <div class="feature-item">
                <div class="feature-icon-box">⚖️</div>
                <div class="feature-item-title">Holiday Surge &amp; Buffer Advisor</div>
                <div class="feature-item-desc">
                    Normal vs Festive demand simulations, stockout vulnerability ratings, and empirical buffer multipliers.
                </div>
            </div>
        </div>
    </div>
    """
    render_html(hero_markup)

    # 4. Prominent CTA Button Centered in balanced layout
    col_l, col_btn, col_r = st.columns([1, 1.4, 1])
    with col_btn:
        st.markdown('<div class="welcome-btn-wrapper">', unsafe_allow_html=True)
        if st.button("Explore Dashboard →", key="enter_dashboard_cta_btn", use_container_width=True):
            st.session_state["page"] = "dashboard"
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

    # 5. Small Footer
    footer_markup = f"""
    <div class="welcome-footer">
        <span>Powered by Data Intelligence</span>
        <span class="welcome-footer-dot"></span>
        <span>RetailPulse Enterprise Platform</span>
        <span class="welcome-footer-dot"></span>
        <span>RF-300 Engine</span>
    </div>
    """
    render_html(footer_markup)
