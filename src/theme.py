"""
src/theme.py
Enterprise SaaS Design System & Theming Engine for Retail Intelligence BI.
Supports Dark Mode (Obsidian / Navy Slate) and Light Mode (Crisp Studio / Soft Gray).
Guarantees solid, high-contrast backgrounds and readable typography across all Streamlit components.
"""

from typing import Dict, Any, Optional
import streamlit as st

THEMES = {
    "dark": {
        "name": "dark",
        "bg_primary": "#080C14",             # Solid Deep Obsidian Canvas
        "bg_secondary": "#0F172A",           # Solid Slate 900 for Sidebar/Headers
        "bg_card": "#131B2E",                # Solid Rich Navy Card Surface (No transparent bleed)
        "bg_card_hover": "#1A253D",          # Elevated Surface
        "border_color": "#1E293B",           # Visible Card Border
        "border_glow": "rgba(99, 102, 241, 0.4)",
        "text_primary": "#F8FAFC",           # Pure Crisp White
        "text_secondary": "#CBD5E1",         # Slate 300 (High-contrast body text)
        "text_muted": "#94A3B8",             # Slate 400
        "accent_primary": "#6366F1",         # Indigo
        "accent_secondary": "#8B5CF6",       # Purple
        "accent_gradient": "linear-gradient(135deg, #6366F1 0%, #8B5CF6 50%, #EC4899 100%)",
        "input_bg": "#0F172A",
        "input_border": "#334155",
        "input_text": "#F8FAFC",
        "success": "#10B981",                # Emerald
        "success_bg": "rgba(16, 185, 129, 0.16)",
        "warning": "#F59E0B",                # Amber
        "warning_bg": "rgba(245, 158, 11, 0.16)",
        "danger": "#F43F5E",                 # Rose
        "danger_bg": "rgba(244, 63, 94, 0.16)",
        "info": "#0EA5E9",                   # Sky
        "info_bg": "rgba(14, 165, 233, 0.16)",
        "shadow_sm": "0 2px 8px rgba(0, 0, 0, 0.5)",
        "shadow_md": "0 8px 24px rgba(0, 0, 0, 0.6)",
        "shadow_glow": "0 0 25px rgba(99, 102, 241, 0.3)"
    },
    "light": {
        "name": "light",
        "bg_primary": "#F8FAFC",             # Solid Luminous Canvas
        "bg_secondary": "#F1F5F9",           # Slate 100 for Sidebar
        "bg_card": "#FFFFFF",                # Solid Pure White Cards
        "bg_card_hover": "#F8FAFC",
        "border_color": "#E2E8F0",           # Crisp Slate 200 Border
        "border_glow": "rgba(79, 70, 229, 0.3)",
        "text_primary": "#0F172A",           # Slate 900 (High contrast dark)
        "text_secondary": "#334155",         # Slate 700
        "text_muted": "#64748B",             # Slate 500
        "accent_primary": "#4F46E5",         # Deep Indigo
        "accent_secondary": "#7C3AED",       # Violet
        "accent_gradient": "linear-gradient(135deg, #4F46E5 0%, #7C3AED 50%, #DB2777 100%)",
        "input_bg": "#FFFFFF",
        "input_border": "#CBD5E1",
        "input_text": "#0F172A",
        "success": "#059669",
        "success_bg": "#ECFDF5",
        "warning": "#D97706",
        "warning_bg": "#FFFBEB",
        "danger": "#E11D48",
        "danger_bg": "#FFF1F2",
        "info": "#0284C7",
        "info_bg": "#F0F9FF",
        "shadow_sm": "0 2px 8px rgba(15, 23, 42, 0.06)",
        "shadow_md": "0 8px 24px rgba(15, 23, 42, 0.08)",
        "shadow_glow": "0 0 25px rgba(79, 70, 229, 0.15)"
    }
}

def get_theme(override_theme: Optional[str] = None) -> Dict[str, Any]:
    """Retrieves current theme dictionary from session state or explicit override, defaulting to dark."""
    if override_theme and override_theme in THEMES:
        return THEMES[override_theme]
    try:
        theme_name = st.session_state.get("theme", "dark")
    except Exception:
        theme_name = "dark"
    return THEMES.get(theme_name, THEMES["dark"])

def inject_theme_css():
    """
    Injects high-fidelity enterprise SaaS CSS with solid backgrounds, readable contrast,
    and exhaustive overrides for Streamlit's native container tree.
    """
    theme = get_theme()
    is_dark = theme["name"] == "dark"
    
    css = f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&family=JetBrains+Mono:wght@400;500&display=swap');

    :root {{
        --bg-main: {theme['bg_primary']};
        --bg-sec: {theme['bg_secondary']};
        --bg-card: {theme['bg_card']};
        --bg-card-hover: {theme['bg_card_hover']};
        --border-color: {theme['border_color']};
        --border-glow: {theme['border_glow']};
        --text-primary: {theme['text_primary']};
        --text-secondary: {theme['text_secondary']};
        --text-muted: {theme['text_muted']};
        --accent: {theme['accent_primary']};
        --accent-grad: {theme['accent_gradient']};
        --input-bg: {theme['input_bg']};
        --input-border: {theme['input_border']};
        --input-text: {theme['input_text']};
        --success: {theme['success']};
        --success-bg: {theme['success_bg']};
        --warning: {theme['warning']};
        --warning-bg: {theme['warning_bg']};
        --danger: {theme['danger']};
        --danger-bg: {theme['danger_bg']};
        --info: {theme['info']};
        --info-bg: {theme['info_bg']};
        --shadow-sm: {theme['shadow_sm']};
        --shadow-md: {theme['shadow_md']};
        --shadow-glow: {theme['shadow_glow']};
    }}

    /* Exhaustive Container Background Overrides (Prevents white bleed-through) */
    html, body {{
        background-color: var(--bg-main) !important;
        color: var(--text-primary) !important;
        font-family: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif !important;
    }}

    .stApp,
    [data-testid="stAppViewContainer"],
    [data-testid="stAppViewBlockContainer"],
    [data-testid="stHeader"],
    [data-testid="stMain"],
    section.main,
    .main .block-container {{
        background-color: var(--bg-main) !important;
        color: var(--text-primary) !important;
    }}

    /* Global Headings & Typography */
    h1, h2, h3, h4, h5, h6 {{
        color: var(--text-primary) !important;
        font-family: 'Plus Jakarta Sans', sans-serif !important;
        letter-spacing: -0.02em !important;
    }}

    p, span, li, label {{
        color: var(--text-secondary);
        font-family: 'Plus Jakarta Sans', sans-serif !important;
    }}

    strong, b {{
        color: var(--text-primary) !important;
    }}

    /* Sidebar Styling */
    section[data-testid="stSidebar"],
    section[data-testid="stSidebar"] > div:first-child {{
        background-color: var(--bg-sec) !important;
        border-right: 1px solid var(--border-color) !important;
        box-shadow: var(--shadow-md) !important;
    }}

    section[data-testid="stSidebar"] h1,
    section[data-testid="stSidebar"] h2,
    section[data-testid="stSidebar"] h3,
    section[data-testid="stSidebar"] p,
    section[data-testid="stSidebar"] span,
    section[data-testid="stSidebar"] label {{
        color: var(--text-primary) !important;
    }}

    /* Top Executive Navbar */
    .top-navbar {{
        display: flex;
        align-items: center;
        justify-content: space-between;
        padding: 0.9rem 1.6rem;
        background: var(--bg-card) !important;
        border: 1px solid var(--border-color) !important;
        border-radius: 16px;
        margin-bottom: 1.75rem;
        box-shadow: var(--shadow-sm);
    }}

    .top-navbar-brand {{
        display: flex;
        align-items: center;
        gap: 0.75rem;
    }}

    .top-navbar-logo {{
        width: 36px;
        height: 36px;
        border-radius: 10px;
        background: var(--accent-grad);
        display: flex;
        align-items: center;
        justify-content: center;
        color: #FFFFFF !important;
        font-weight: 800;
        font-size: 1.15rem;
        box-shadow: 0 4px 12px rgba(99, 102, 241, 0.35);
    }}

    .top-navbar-title {{
        font-size: 1.2rem;
        font-weight: 800;
        color: var(--text-primary) !important;
        letter-spacing: -0.02em;
        line-height: 1.2;
    }}

    .top-navbar-subtitle {{
        font-size: 0.76rem;
        color: var(--text-muted) !important;
        font-weight: 500;
    }}

    .top-navbar-status {{
        display: inline-flex;
        align-items: center;
        gap: 0.45rem;
        background: var(--success-bg) !important;
        color: var(--success) !important;
        padding: 0.35rem 0.8rem;
        border-radius: 9999px;
        font-size: 0.75rem;
        font-weight: 700;
        border: 1px solid rgba(16, 185, 129, 0.3) !important;
    }}

    .status-pulse {{
        width: 7px;
        height: 7px;
        border-radius: 50%;
        background-color: var(--success) !important;
        box-shadow: 0 0 8px var(--success);
        animation: pulse 2s infinite;
    }}

    @keyframes pulse {{
        0% {{ transform: scale(0.95); box-shadow: 0 0 0 0 rgba(16, 185, 129, 0.7); }}
        70% {{ transform: scale(1); box-shadow: 0 0 0 6px rgba(16, 185, 129, 0); }}
        100% {{ transform: scale(0.95); box-shadow: 0 0 0 0 rgba(16, 185, 129, 0); }}
    }}

    /* KPI Card Component (Solid Surface) */
    .kpi-card {{
        background: var(--bg-card) !important;
        border: 1px solid var(--border-color) !important;
        border-radius: 16px;
        padding: 1.3rem 1.45rem;
        position: relative;
        overflow: hidden;
        box-shadow: var(--shadow-sm);
        height: 100%;
        display: flex;
        flex-direction: column;
        justify-content: space-between;
        transition: all 0.25s cubic-bezier(0.16, 1, 0.3, 1) !important;
    }}

    .kpi-card:hover {{
        background: var(--bg-card-hover) !important;
        border-color: var(--border-glow) !important;
        transform: translateY(-2px);
        box-shadow: var(--shadow-md);
    }}

    .kpi-card::before {{
        content: "";
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 3px;
        background: var(--accent-grad);
    }}

    .kpi-header {{
        display: flex;
        align-items: center;
        justify-content: space-between;
        margin-bottom: 0.65rem;
    }}

    .kpi-title {{
        font-size: 0.8rem;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 0.05em;
        color: var(--text-secondary) !important;
    }}

    .kpi-icon-wrap {{
        width: 32px;
        height: 32px;
        border-radius: 8px;
        background: rgba(99, 102, 241, 0.15) !important;
        color: var(--accent) !important;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 1rem;
    }}

    .kpi-value {{
        font-size: 1.9rem;
        font-weight: 800;
        letter-spacing: -0.03em;
        color: var(--text-primary) !important;
        font-variant-numeric: tabular-nums;
        line-height: 1.15;
        margin-bottom: 0.55rem;
    }}

    .kpi-footer {{
        display: flex;
        align-items: center;
        gap: 0.5rem;
        flex-wrap: wrap;
        font-size: 0.78rem;
    }}

    .kpi-delta-pill {{
        display: inline-flex;
        align-items: center;
        gap: 0.25rem;
        padding: 0.22rem 0.6rem;
        border-radius: 6px;
        font-weight: 700;
        font-size: 0.74rem;
        font-variant-numeric: tabular-nums;
    }}

    .kpi-delta-positive {{
        background: var(--success-bg) !important;
        color: var(--success) !important;
        border: 1px solid rgba(16, 185, 129, 0.3) !important;
    }}

    .kpi-delta-negative {{
        background: var(--danger-bg) !important;
        color: var(--danger) !important;
        border: 1px solid rgba(244, 63, 94, 0.3) !important;
    }}

    .kpi-delta-neutral {{
        background: rgba(148, 163, 184, 0.15) !important;
        color: var(--text-secondary) !important;
        border: 1px solid var(--border-color) !important;
    }}

    .kpi-subtext {{
        color: var(--text-muted) !important;
        font-weight: 500;
    }}

    /* Chart Container Card (Solid Surface) */
    .chart-container-card {{
        background: var(--bg-card) !important;
        border: 1px solid var(--border-color) !important;
        border-radius: 16px;
        padding: 1.45rem;
        margin-bottom: 1.5rem;
        box-shadow: var(--shadow-sm);
    }}

    .chart-header {{
        display: flex;
        align-items: center;
        justify-content: space-between;
        margin-bottom: 1rem;
        padding-bottom: 0.75rem;
        border-bottom: 1px solid var(--border-color) !important;
    }}

    .chart-title {{
        font-size: 1.05rem;
        font-weight: 700;
        color: var(--text-primary) !important;
        letter-spacing: -0.01em;
        display: flex;
        align-items: center;
        gap: 0.5rem;
    }}

    .chart-badge {{
        font-size: 0.72rem;
        font-weight: 700;
        padding: 0.22rem 0.6rem;
        border-radius: 6px;
        background: rgba(99, 102, 241, 0.18) !important;
        color: var(--accent) !important;
        border: 1px solid rgba(99, 102, 241, 0.3) !important;
    }}

    /* Form Controls: Inputs, Multiselect, Selectbox, Date Inputs */
    div[data-testid="stWidgetLabel"] label,
    div[data-testid="stWidgetLabel"] p {{
        color: var(--text-primary) !important;
        font-weight: 600 !important;
        font-size: 0.85rem !important;
    }}

    [data-baseweb="input"],
    [data-baseweb="select"] > div,
    [data-baseweb="base-input"] {{
        background-color: var(--input-bg) !important;
        border: 1px solid var(--input-border) !important;
        border-radius: 10px !important;
        color: var(--text-primary) !important;
    }}

    [data-baseweb="input"] input,
    [data-baseweb="base-input"] input {{
        color: var(--text-primary) !important;
        background-color: transparent !important;
    }}

    /* Multiselect Tags (Pills) */
    div[data-baseweb="tag"] {{
        background-color: rgba(99, 102, 241, 0.22) !important;
        border: 1px solid var(--accent) !important;
        border-radius: 6px !important;
    }}

    div[data-baseweb="tag"] span {{
        color: var(--text-primary) !important;
        font-weight: 600 !important;
    }}

    /* Dropdown Popovers */
    [data-baseweb="popover"],
    [data-baseweb="menu"],
    ul[role="listbox"] {{
        background-color: var(--bg-sec) !important;
        border: 1px solid var(--border-color) !important;
    }}

    li[role="option"] {{
        background-color: var(--bg-sec) !important;
        color: var(--text-primary) !important;
    }}

    li[role="option"]:hover,
    li[aria-selected="true"] {{
        background-color: rgba(99, 102, 241, 0.25) !important;
        color: var(--text-primary) !important;
    }}

    /* Buttons */
    .stButton>button {{
        background: var(--accent) !important;
        color: #FFFFFF !important;
        border-radius: 10px !important;
        border: none !important;
        font-weight: 700 !important;
        font-size: 0.85rem !important;
        padding: 0.55rem 1.15rem !important;
        box-shadow: 0 2px 8px rgba(99, 102, 241, 0.3) !important;
        transition: all 0.2s cubic-bezier(0.16, 1, 0.3, 1) !important;
    }}

    .stButton>button:hover {{
        filter: brightness(1.15) !important;
        transform: translateY(-1px) !important;
        box-shadow: 0 4px 14px rgba(99, 102, 241, 0.45) !important;
    }}

    /* Secondary Download Buttons */
    .stDownloadButton>button {{
        background: var(--bg-card) !important;
        color: var(--text-primary) !important;
        border: 1px solid var(--border-color) !important;
        border-radius: 10px !important;
        font-weight: 600 !important;
        font-size: 0.85rem !important;
        padding: 0.55rem 1.15rem !important;
        transition: all 0.2s ease !important;
    }}

    .stDownloadButton>button:hover {{
        background: var(--bg-card-hover) !important;
        border-color: var(--accent) !important;
        color: var(--accent) !important;
    }}

    /* Dataframe Container */
    div[data-testid="stDataFrame"] {{
        border: 1px solid var(--border-color) !important;
        border-radius: 12px !important;
        overflow: hidden !important;
        background: var(--bg-card) !important;
    }}

    /* Expander Container */
    div[data-testid="stExpander"] {{
        background-color: var(--bg-card) !important;
        border: 1px solid var(--border-color) !important;
        border-radius: 12px !important;
    }}
    div[data-testid="stExpander"] summary {{
        color: var(--text-primary) !important;
        font-weight: 600 !important;
    }}

    /* Responsive adjustments */
    @media (max-width: 768px) {{
        .top-navbar {{
            flex-direction: column;
            align-items: flex-start;
            gap: 0.75rem;
        }}
        .kpi-value {{
            font-size: 1.55rem;
        }}
    }}
    </style>
    """
    st.markdown(css, unsafe_allow_html=True)

def get_plotly_layout(theme_name: str = "dark") -> Dict[str, Any]:
    """
    Returns solid enterprise Plotly layout matching active theme with readable contrast.
    """
    theme = THEMES.get(theme_name, THEMES["dark"])
    is_dark = theme["name"] == "dark"
    
    font_family = "'Plus Jakarta Sans', -apple-system, sans-serif"
    
    # Solid background matching the card surface
    paper_bg = theme["bg_card"]
    plot_bg = theme["bg_card"]
    
    grid_color = "rgba(255, 255, 255, 0.08)" if is_dark else "#E2E8F0"
    zero_line_color = "rgba(255, 255, 255, 0.18)" if is_dark else "#CBD5E1"
    
    layout = {
        "paper_bgcolor": paper_bg,
        "plot_bgcolor": plot_bg,
        "font": {
            "family": font_family,
            "color": theme["text_secondary"],
            "size": 12
        },
        "margin": {"l": 25, "r": 25, "t": 35, "b": 25},
        "hoverlabel": {
            "bgcolor": theme["bg_secondary"],
            "font": {"family": font_family, "color": theme["text_primary"], "size": 12},
            "bordercolor": theme["border_color"]
        },
        "xaxis": {
            "showgrid": True,
            "gridcolor": grid_color,
            "zeroline": False,
            "showline": True,
            "linecolor": grid_color,
            "tickfont": {"family": font_family, "color": theme["text_muted"], "size": 11}
        },
        "yaxis": {
            "showgrid": True,
            "gridcolor": grid_color,
            "zeroline": True,
            "zerolinecolor": zero_line_color,
            "showline": False,
            "tickfont": {"family": font_family, "color": theme["text_muted"], "size": 11}
        },
        "legend": {
            "orientation": "h",
            "yanchor": "bottom",
            "y": 1.02,
            "xanchor": "right",
            "x": 1,
            "font": {"family": font_family, "color": theme["text_secondary"], "size": 11}
        }
    }
    return layout
