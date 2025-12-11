"""
QA Community Platform v2 - Streamlit Application

A community platform for QA professionals to connect based on 
what they can GIVE and what they ASK for.

Mobile-first design with direct MongoDB connection.
"""

import streamlit as st
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Import pages
from app_pages import (
    render_home_page,
    render_create_profile_page,
    render_my_profile_page,
    render_leaderboard_page
)

# Import shared styles
from shared import apply_custom_styles

# ============================================================================
# PAGE CONFIGURATION
# ============================================================================

st.set_page_config(
    page_title="ATAGTR QA Community",
    page_icon="🤝",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Apply custom CSS
apply_custom_styles()

# ============================================================================
# SESSION STATE INITIALIZATION
# ============================================================================

if 'current_profile' not in st.session_state:
    st.session_state.current_profile = None
if 'page' not in st.session_state:
    st.session_state.page = 'home'
if 'current_match_index' not in st.session_state:
    st.session_state.current_match_index = 0
if 'matches_list' not in st.session_state:
    st.session_state.matches_list = []

# ============================================================================
# MAIN APP
# ============================================================================

def main():
    """Main app entry point."""
    # Sidebar navigation
    with st.sidebar:
        st.markdown("## 📱 Menu")
        
        if st.button("🏠 Home", use_container_width=True, key="sidebar_home"):
            st.session_state.page = 'home'
            st.rerun()
        
        if st.button("✨ Create Profile", use_container_width=True, key="sidebar_create"):
            st.session_state.page = 'create'
            st.rerun()
        
        if st.button("👤 My Profile", use_container_width=True, key="sidebar_profile"):
            st.session_state.page = 'my_profile'
            st.rerun()
        
        if st.button("🏆 Leaderboard", use_container_width=True, key="sidebar_leaderboard"):
            st.session_state.page = 'leaderboard'
            st.rerun()
        
        # Show current user info (no logout button since no auth)
        if st.session_state.current_profile:
            st.markdown("---")
            p = st.session_state.current_profile
            st.caption(f"👤 {p.get('full_name', '')}")
            st.caption(f"⭐ {p.get('points', 0)} points")
    
    # Page routing
    page = st.session_state.page
    
    if page == 'home':
        render_home_page()
    elif page == 'create':
        render_create_profile_page()
    elif page == 'my_profile':
        render_my_profile_page()
    elif page == 'leaderboard':
        render_leaderboard_page()
    else:
        render_home_page()


if __name__ == "__main__":
    main()
