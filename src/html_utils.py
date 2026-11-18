"""
src/components/html_utils.py
HTML Rendering Utility for Streamlit.
Guarantees clean HTML rendering without markdown indentation preformatted code block traps.
Uses native st.html() when available, with dedented st.markdown(unsafe_allow_html=True) fallback.
"""

import textwrap
import streamlit as st

def render_html(html_str: str):
    """
    Renders raw HTML safely in Streamlit without code block escapes.
    Dedents all leading indentation and strips trailing whitespaces.
    """
    clean_html = textwrap.dedent(html_str).strip()
    if hasattr(st, "html"):
        st.html(clean_html)
    else:
        st.markdown(clean_html, unsafe_allow_html=True)
