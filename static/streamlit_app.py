import streamlit as st
import streamlit.components.v1 as components
import json

# Configure page settings
st.set_page_config(
    page_title="GreenAmmonia: Bio-Catalyst Design",
    page_icon="⚗️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Hide default Streamlit header, footer, and padding for clean fullscreen display
hide_st_style = """
    <style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    .block-container {
        padding-top: 0rem;
        padding-bottom: 0rem;
        padding-left: 0rem;
        padding-right: 0rem;
        max-width: 100%;
    }
    iframe {
        width: 100% !important;
        border: none !important;
    }
    </style>
"""
st.markdown(hide_st_style, unsafe_allow_html=True)

# Read HTML and CSS files
try:
    with open("templates/index.html", "r", encoding="utf-8") as f:
        html_content = f.read()

    with open("static/style.css", "r", encoding="utf-8") as f:
        css_content = f.read()

    # Inject static CSS directly into HTML so it renders properly without Flask url_for
    html_with_inline_css = html_content.replace(
        '<link rel="stylesheet" href="{{ url_for(\'static\', filename=\'style.css\') }}">',
        f'<style>{css_content}</style>'
    )

    # Render complete dashboard inside Streamlit component
    components.html(html_with_inline_css, height=1350, scrolling=True)

except Exception as e:
    st.error(f"Error loading dashboard: {e}")