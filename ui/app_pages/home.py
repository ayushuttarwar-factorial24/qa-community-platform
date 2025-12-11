"""
Home Page - Landing page for the QA Community Platform.
"""

import streamlit as st
from services import get_leaderboard


def render_home_page():
    """Render home/landing page."""
    st.markdown("# 🤝 ATAGTR QA Community")
    st.markdown("*Connect with QA professionals based on Give & Ask*")
    
    st.markdown("""
    ### How it works:
    1. **Create Profile** - Tell us about yourself
    2. **GIVE** - Share what you can offer
    3. **ASK** - Tell us what you need
    4. **Match** - Connect with people who can help!
    """)
    
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("✨ Create Profile", type="primary", use_container_width=True, key="home_create"):
            st.session_state.page = 'create'
            st.rerun()
    
    with col2:
        if st.button("👤 My Profile", use_container_width=True, key="home_profile"):
            st.session_state.page = 'my_profile'
            st.rerun()
    
    st.markdown("---")
    
    if st.button("🏆 View Leaderboard", use_container_width=True, key="home_leaderboard"):
        st.session_state.page = 'leaderboard'
        st.rerun()
    
    # Quick stats
    st.markdown("---")
    st.markdown("### 📊 Community Stats")
    
    try:
        lb = get_leaderboard(limit=1000)
        total = lb.get('total', 0) if lb else 0
    except:
        total = 0
    
    st.metric("👥 Total Members", total)
