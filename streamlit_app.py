import streamlit as st
import streamlit.components.v1 as components
from jinja2 import Template

# Streamlit Page Setup
st.set_page_config(
    page_title="GreenAmmonia: Bio-Catalyst Design",
    page_icon="⚗️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Strip default Streamlit margins so the UI fills the screen
st.markdown("""
    <style>
    #MainMenu, footer, header { visibility: hidden !important; }
    .block-container { padding: 0 !important; max-width: 100% !important; }
    iframe { width: 100% !important; border: none !important; }
    </style>
""", unsafe_allow_html=True)

# Candidate catalog data
catalysts = [
    {
        "id": "pt_c",
        "name": "Pt/C Benchmark",
        "formula": "20 wt% Platinum Carbon",
        "score": 92.3,
        "energy_barrier": 8.5,
        "stability": "Very High",
        "selectivity": 0.98,
        "activity": 0.95,
        "potential": "High Potential"
    },
    {
        "id": "fe_n4_c",
        "name": "Fe-N₄-C",
        "formula": "Iron Tetra-Nitrogen Carbon",
        "score": 88.5,
        "energy_barrier": 11.2,
        "stability": "High",
        "selectivity": 0.96,
        "activity": 0.91,
        "potential": "High Potential"
    },
    {
        "id": "fe_co_nc",
        "name": "Fe-Co-N-C",
        "formula": "Dual Single-Atom Carbon",
        "score": 88.0,
        "energy_barrier": 10.8,
        "stability": "High",
        "selectivity": 0.95,
        "activity": 0.92,
        "potential": "High Potential"
    },
    {
        "id": "femoco_mimic",
        "name": "FeMoco Native Mimic",
        "formula": "MoFe₃S₄-Coordinated Pincer",
        "score": 85.9,
        "energy_barrier": 12.2,
        "stability": "High",
        "selectivity": 0.94,
        "activity": 0.89,
        "potential": "High Potential"
    },
    {
        "id": "g_c3n4_nv",
        "name": "g-C₃N₄-NV",
        "formula": "Graphitic Carbon Nitride (N-Vacancies)",
        "score": 82.2,
        "energy_barrier": 14.1,
        "stability": "High",
        "selectivity": 0.90,
        "activity": 0.84,
        "potential": "Moderate Potential"
    },
    {
        "id": "mo_graphene_sac",
        "name": "Mo/graphene SAC",
        "formula": "Single-Atom Molybdenum on Graphene",
        "score": 78.7,
        "energy_barrier": 15.8,
        "stability": "Moderate",
        "selectivity": 0.88,
        "activity": 0.82,
        "potential": "Moderate Potential"
    }
]

top_catalyst = catalysts[0]
total_candidates = len(catalysts)

try:
    with open("templates/index.html", "r", encoding="utf-8") as f:
        html_raw = f.read()

    with open("static/style.css", "r", encoding="utf-8") as f:
        css_content = f.read()

    # Replace Flask url_for with direct CSS style tag
    html_raw = html_raw.replace(
        '<link rel="stylesheet" href="{{ url_for(\'static\', filename=\'style.css\') }}">',
        f'<style>{css_content}</style>'
    )

    # Render Jinja variables (total, top, catalysts)
    template = Template(html_raw)
    rendered_html = template.render(
        catalysts=catalysts,
        top=top_catalyst,
        total=total_candidates
    )

    # Render completed dashboard
    components.html(rendered_html, height=1400, scrolling=True)

except Exception as err:
    st.error(f"Error rendering application: {err}")