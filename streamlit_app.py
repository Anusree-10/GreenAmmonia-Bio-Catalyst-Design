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

# Lock Streamlit wrapper viewport so the outer page never scrolls
st.markdown("""
    <style>
    #MainMenu, footer, header { display: none !important; visibility: hidden !important; }
    .block-container { 
        padding: 0 !important; 
        margin: 0 !important;
        max-width: 100% !important; 
        height: 100vh !important;
        overflow: hidden !important;
    }
    iframe { 
        width: 100% !important; 
        height: 100vh !important; 
        border: none !important; 
        display: block !important;
    }
    </style>
""", unsafe_allow_html=True)

# ALL 8 CANDIDATES DEFINED FOR JINJA TEMPLATE RENDERING
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
        "potential": "High Potential",
        "estimated_energy_reduction": 42.0,
        "estimated_co2_reduction": 38.5
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
        "potential": "High Potential",
        "estimated_energy_reduction": 36.5,
        "estimated_co2_reduction": 32.0
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
        "potential": "High Potential",
        "estimated_energy_reduction": 37.0,
        "estimated_co2_reduction": 33.5
    },
    {
        "id": "femoco_mimic",
        "name": "FeMoco Native Mimic",
        "formula": "MoFe₇S₉C-Coordinated Pincer",
        "score": 85.9,
        "energy_barrier": 12.2,
        "stability": "High",
        "selectivity": 0.94,
        "activity": 0.89,
        "potential": "High Potential",
        "estimated_energy_reduction": 33.0,
        "estimated_co2_reduction": 29.5
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
        "potential": "Moderate Potential",
        "estimated_energy_reduction": 28.0,
        "estimated_co2_reduction": 25.0
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
        "potential": "Moderate Potential",
        "estimated_energy_reduction": 24.5,
        "estimated_co2_reduction": 21.0
    },
    {
        "id": "schrock_cat",
        "name": "Schrock Catalyst",
        "formula": "[Mo(HIPTN₃N)] Coordination Complex",
        "score": 75.4,
        "energy_barrier": 17.5,
        "stability": "Moderate",
        "selectivity": 0.85,
        "activity": 0.79,
        "potential": "Moderate Potential",
        "estimated_energy_reduction": 20.0,
        "estimated_co2_reduction": 18.0
    },
    {
        "id": "fevco_biomimic",
        "name": "FeVco Bio-mimic",
        "formula": "VFe₇S₉C Vanadium-Nitrogenase Model",
        "score": 72.8,
        "energy_barrier": 19.1,
        "stability": "Moderate",
        "selectivity": 0.82,
        "activity": 0.76,
        "potential": "Moderate Potential",
        "estimated_energy_reduction": 17.0,
        "estimated_co2_reduction": 15.0
    }
]

top_catalyst = catalysts[0]
total_candidates = len(catalysts)

try:
    with open("templates/index.html", "r", encoding="utf-8") as f:
        html_raw = f.read()

    with open("static/style.css", "r", encoding="utf-8") as f:
        css_content = f.read()

    # Inline static styles directly into template
    html_raw = html_raw.replace(
        '<link rel="stylesheet" href="{{ url_for(\'static\', filename=\'style.css\') }}">',
        f'<style>{css_content}</style>'
    )

    # Render Jinja variables
    template = Template(html_raw)
    rendered_html = template.render(
        catalysts=catalysts,
        top=top_catalyst,
        total=total_candidates
    )

    # Render fullscreen component
    components.html(rendered_html, height=1000, scrolling=False)

except Exception as err:
    st.error(f"Error loading dashboard: {err}")