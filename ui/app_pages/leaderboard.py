"""
Leaderboard Page - Display rankings with beautified UI.
"""

import streamlit as st
from services import get_leaderboard


def render_leaderboard_page():
    """Render beautified leaderboard - Rank, Name, Connections Received, Points."""
    st.markdown("# 🏆 Leaderboard")
    st.caption("Top contributors in the community")
    
    with st.spinner("Loading..."):
        data = get_leaderboard(limit=50)
    
    if not data or not data.get('profiles'):
        st.info("No profiles yet. Be the first!")
        return
    
    profiles = data['profiles']
    
    # Top 3 Podium
    if len(profiles) >= 1:
        st.markdown("### 🌟 Top Performers")
        
        # Display top 3 as special cards
        top_cols = st.columns(min(3, len(profiles)))
        
        for i, col in enumerate(top_cols):
            if i < len(profiles):
                p = profiles[i]
                name = p.get('full_name', p.get('name', 'Unknown'))
                received = len(p.get('connections_received', []))
                points = p.get('points', 0)
                
                medal = ["🥇", "🥈", "🥉"][i]
                bg_colors = ["#fff9e6", "#f8f9fa", "#fdf2e9"]
                border_colors = ["#f1c40f", "#bdc3c7", "#cd7f32"]
                
                with col:
                    st.markdown(f"""
                    <div style="
                        background: {bg_colors[i]};
                        border: 2px solid {border_colors[i]};
                        border-radius: 15px;
                        padding: 20px 15px;
                        text-align: center;
                        margin: 5px;
                    ">
                        <div style="font-size: 36px;">{medal}</div>
                        <div style="font-size: 16px; font-weight: 600; margin: 8px 0; color: #2d3436;">
                            {name[:15]}{'...' if len(name) > 15 else ''}
                        </div>
                        <div style="display: flex; justify-content: center; gap: 15px; margin-top: 10px;">
                            <div style="text-align: center;">
                                <div style="font-size: 18px; font-weight: bold; color: #667eea;">👤 {received}</div>
                            </div>
                            <div style="text-align: center;">
                                <div style="font-size: 18px; font-weight: bold; color: #f39c12;">⭐ {points}</div>
                            </div>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
        
        st.markdown("")
    
    # Full Rankings (after top 3)
    if len(profiles) > 3:
        st.markdown("---")
        st.markdown("### 📊 Full Rankings")
        
        for idx, p in enumerate(profiles[3:], 4):
            name = p.get('full_name', p.get('name', 'Unknown'))
            received = len(p.get('connections_received', []))
            points = p.get('points', 0)
            
            st.markdown(f"""
            <div style="
                background: linear-gradient(135deg, #f5f7fa 0%, #e8ecef 100%);
                border-radius: 10px;
                padding: 12px 16px;
                margin: 6px 0;
                display: flex;
                align-items: center;
            ">
                <div style="
                    font-size: 18px;
                    font-weight: bold;
                    color: #636e72;
                    min-width: 35px;
                ">{idx}</div>
                <div style="flex: 1; margin-left: 10px;">
                    <div style="font-size: 15px; font-weight: 500; color: #2d3436;">{name}</div>
                </div>
                <div style="display: flex; gap: 20px;">
                    <div style="text-align: center;">
                        <span style="font-size: 14px; color: #667eea;">👤 {received}</span>
                    </div>
                    <div style="text-align: center;">
                        <span style="font-size: 14px; color: #f39c12;">⭐ {points}</span>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)
    
    # Legend
    st.markdown("---")
    st.caption("👤 = Connections Received | ⭐ = Points")
