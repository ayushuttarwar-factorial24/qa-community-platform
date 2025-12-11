"""
Custom CSS styles for the Streamlit app.
Mobile-first responsive design.
"""

import streamlit as st


def apply_custom_styles():
    """Apply custom CSS styles to the app."""
    st.markdown("""
<style>
    /* Mobile-first responsive design */
    .stButton button {
        width: 100%;
        margin-bottom: 0.5rem;
        font-size: 16px !important;
        padding: 0.75rem 1rem !important;
        min-height: 48px;
        border-radius: 10px;
        font-weight: 500;
    }
    
    .stButton button[kind="primary"] {
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
    }
    
    @media (max-width: 768px) {
        [data-testid="column"] {
            min-width: 100% !important;
            flex: 1 1 100% !important;
        }
        .main .block-container {
            padding: 1rem 0.5rem !important;
        }
    }
    
    /* Match card styling */
    .match-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 25px 20px;
        border-radius: 20px;
        color: white;
        text-align: center;
        margin: 15px 0;
        box-shadow: 0 8px 25px rgba(0,0,0,0.15);
    }
    
    .match-name {
        font-size: 24px;
        font-weight: bold;
        margin-bottom: 5px;
    }
    
    .match-role {
        font-size: 14px;
        opacity: 0.9;
        margin: 5px 0;
    }
    
    /* Tag styling */
    .tag {
        background-color: #667eea;
        color: white;
        padding: 4px 12px;
        border-radius: 15px;
        margin: 2px;
        display: inline-block;
        font-size: 12px;
    }
    
    /* Leaderboard styling */
    .lb-card {
        background: linear-gradient(135deg, #f5f7fa 0%, #e4e8ec 100%);
        border-radius: 12px;
        padding: 12px 16px;
        margin: 8px 0;
        display: flex;
        align-items: center;
        box-shadow: 0 2px 8px rgba(0,0,0,0.08);
    }
    
    .lb-card-gold {
        background: linear-gradient(135deg, #fff9e6 0%, #ffeaa7 100%);
        border: 2px solid #f1c40f;
    }
    
    .lb-card-silver {
        background: linear-gradient(135deg, #f8f9fa 0%, #dfe6e9 100%);
        border: 2px solid #bdc3c7;
    }
    
    .lb-card-bronze {
        background: linear-gradient(135deg, #fdf2e9 0%, #f0d9c0 100%);
        border: 2px solid #cd7f32;
    }
    
    .lb-rank {
        font-size: 24px;
        font-weight: bold;
        min-width: 45px;
        text-align: center;
    }
    
    .lb-info {
        flex: 1;
        margin-left: 12px;
    }
    
    .lb-name {
        font-size: 16px;
        font-weight: 600;
        color: #2d3436;
    }
    
    .lb-stats {
        display: flex;
        gap: 15px;
        margin-top: 4px;
    }
    
    .lb-stat {
        font-size: 13px;
        color: #636e72;
    }
    
    /* Hide streamlit branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    
    /* Section headers */
    .section-header {
        font-size: 1.3rem;
        font-weight: 600;
        margin: 1.5rem 0 0.5rem 0;
        color: #333;
    }
    
    /* Connection card */
    .conn-card {
        background: #f8f9fa;
        border-radius: 10px;
        padding: 12px;
        margin: 8px 0;
        border-left: 4px solid #667eea;
    }
</style>
""", unsafe_allow_html=True)
