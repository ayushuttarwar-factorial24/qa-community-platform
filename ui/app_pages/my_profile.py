"""
My Profile Page - View profile, find matches, manage connections.
"""

import streamlit as st
from typing import Dict, List

from services import (
    MAX_CONNECTIONS_PER_USER,
    DEFAULT_MATCH_LIMIT,
    get_profile_by_identifier,
    get_suggested_matches,
    connect_profiles,
    get_connection_profiles
)

from shared import (
    render_tags,
    get_all_items_from_section,
    validate_email
)


def render_my_profile_page():
    """Render My Profile page with integrated matches."""
    profile = st.session_state.current_profile
    
    if not profile:
        _render_login_form()
        return
    
    # Profile loaded - show profile + matches
    st.markdown("# 👤 My Profile")
    
    # Basic info header
    name = profile.get('full_name', 'Unknown')
    role = profile.get('current_role', '')
    if role == "Other":
        role = profile.get('custom_role', '')
    company = profile.get('current_company', '')
    points = profile.get('points', 0)
    
    col1, col2 = st.columns([3, 1])
    with col1:
        st.markdown(f"### {name}")
        st.caption(f"{role}{' at ' + company if company else ''}")
    with col2:
        st.metric("Points", points)
    
    st.markdown("---")
    
    # Tabs: Matches | Profile | Connections
    tab1, tab2, tab3 = st.tabs(["🎯 Matches", "📋 My Info", "🔗 Connections"])
    
    with tab1:
        _render_matches_tab(profile)
    
    with tab2:
        _render_info_tab(profile)
    
    with tab3:
        _render_connections_tab(profile)


def _render_login_form():
    """Render the profile loading form."""
    st.markdown("# 👤 My Profile")
    st.markdown("Enter your email to load your profile")
    
    email = st.text_input("Email", key="load_email", placeholder="john@example.com")
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("🔍 Load Profile", use_container_width=True, type="primary", key="load_profile_btn"):
            if email:
                if not validate_email(email):
                    st.error("Please enter a valid email address")
                    return
                
                loaded = get_profile_by_identifier(email.strip().lower())
                if loaded:
                    st.session_state.current_profile = loaded
                    st.toast("✅ Profile loaded!", icon="✅")
                    st.rerun()
                else:
                    st.error("Profile not found. Check your email or create a new profile.")
            else:
                st.warning("Please enter your email")
    
    with col2:
        if st.button("✨ Create Profile", use_container_width=True, key="goto_create"):
            st.session_state.page = 'create'
            st.rerun()


def _render_matches_tab(profile: Dict):
    """Render the matches tab content."""
    st.markdown("### Find Your Matches")
    
    if st.button("🔄 Find Matches", use_container_width=True, type="primary", key="find_matches_btn"):
        st.session_state.current_match_index = 0
        st.session_state.matches_list = get_suggested_matches(
            profile.get('email'),
            limit=DEFAULT_MATCH_LIMIT
        )
    
    if st.session_state.matches_list:
        _render_swipe_match_card(st.session_state.matches_list, profile)
    else:
        st.info("👆 Click 'Find Matches' to discover people you can connect with!")


def _render_swipe_match_card(matches: List[Dict], source_profile: Dict):
    """Render swipe-style match cards."""
    if not matches:
        st.info("😔 No matches found yet. As more people join, you'll see matches here!")
        return
    
    current_idx = st.session_state.current_match_index
    
    # Check bounds
    if current_idx >= len(matches):
        st.success("🎉 You've viewed all matches!")
        if st.button("🔄 Start Over", type="primary", use_container_width=True, key="restart_matches"):
            st.session_state.current_match_index = 0
            st.rerun()
        return
    
    match = matches[current_idx]
    match_profile = match.get('candidate_profile', {})
    reasons = match.get('match_reasons', [])
    
    # Progress indicator
    st.caption(f"Match {current_idx + 1} of {len(matches)}")
    
    # Match card
    name = match_profile.get('full_name', 'Unknown')
    role = match_profile.get('current_role', '')
    if role == "Other":
        role = match_profile.get('custom_role', 'Professional')
    company = match_profile.get('current_company', '')
    experience = match_profile.get('experience', '')
    linkedin = match_profile.get('linkedin_url', '')
    
    # Card HTML
    st.markdown(f"""
        <div class="match-card">
            <div class="match-name">{name}</div>
            <div class="match-role">{role}{' at ' + company if company else ''}</div>
            <div class="match-role" style="margin-top: 8px;">{experience} experience</div>
        </div>
    """, unsafe_allow_html=True)
    
    # Match reasons
    if reasons:
        st.markdown("**🎯 Why you might connect:**")
        for reason in reasons[:3]:
            st.markdown(f"• {reason}")
    
    # What they GIVE
    give = match_profile.get('give', {})
    st.markdown("**💚 They can help with:**")
    
    give_items = []
    for key in ['companies', 'professional_activities', 'technical_areas', 'job_roles']:
        items = get_all_items_from_section(give, key)
        if key == 'companies':
            items = give.get('companies', [])
        give_items.extend(items[:2])
    
    if give_items:
        render_tags(give_items[:4], "#2ca02c")
    else:
        st.caption("No specific items listed")
    
    st.markdown("")
    
    # Connect button
    if linkedin:
        target_user_id = match_profile.get('user_id')
        source_user_id = source_profile.get('user_id')
        
        connections_sent = source_profile.get('connections_sent', [])
        already_connected = target_user_id in connections_sent
        at_limit = len(connections_sent) >= MAX_CONNECTIONS_PER_USER
        
        if already_connected:
            st.success("✅ Already connected!")
            st.link_button("👤 View LinkedIn", linkedin, use_container_width=True)
        elif at_limit:
            st.warning(f"⚠️ Connection limit reached ({MAX_CONNECTIONS_PER_USER})")
            st.link_button("👀 View LinkedIn", linkedin, use_container_width=True)
        else:
            # Use an HTML link styled as a button that opens LinkedIn
            # When clicked, it also triggers the connection via a hidden button
            connect_key = f"pending_connect_{target_user_id}"
            
            # Check if connection was just made (from previous click)
            if st.session_state.get(connect_key):
                # Connection recorded, now show success
                st.success("✅ +10 points!")
                st.link_button("🔗 View LinkedIn Profile", linkedin, use_container_width=True, type="primary")
                # Clear the pending state
                del st.session_state[connect_key]
            else:
                # Show the connect button as an HTML anchor that opens LinkedIn
                # AND a hidden mechanism to record the connection
                
                # Create HTML button-styled link that opens LinkedIn in new tab
                st.markdown(f'''
                    <a href="{linkedin}" target="_blank" onclick="window.connectClicked=true" style="
                        display: inline-block;
                        width: 100%;
                        padding: 0.75rem 1rem;
                        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
                        color: white;
                        text-align: center;
                        text-decoration: none;
                        border-radius: 10px;
                        font-weight: 500;
                        font-size: 16px;
                        box-sizing: border-box;
                    ">🤝 Connect on LinkedIn</a>
                ''', unsafe_allow_html=True)
                
                # Small button below to confirm and record the connection
                st.caption("👆 Click above to open LinkedIn, then:")
                if st.button("✓ I've sent the request", use_container_width=True, key=f"confirm_connect_{current_idx}"):
                    result = connect_profiles(source_user_id, target_user_id)
                    if result.get('success'):
                        st.session_state[connect_key] = True
                        st.session_state.current_profile = get_profile_by_identifier(source_profile.get('email'))
                        st.rerun()
                    else:
                        st.error(result.get('message', 'Connection failed'))
    else:
        st.info("No LinkedIn profile available")
    
    # Navigation buttons
    st.markdown("---")
    col1, col2 = st.columns(2)
    
    with col1:
        if current_idx > 0:
            if st.button("← Previous", use_container_width=True, key="prev_match"):
                st.session_state.current_match_index -= 1
                st.rerun()
    
    with col2:
        if current_idx < len(matches) - 1:
            if st.button("Next →", use_container_width=True, key="next_match"):
                st.session_state.current_match_index += 1
                st.rerun()


def _render_info_tab(profile: Dict):
    """Render the profile info tab."""
    st.markdown("**📧 Email:** " + profile.get('email', ''))
    if profile.get('phone'):
        st.markdown("**📱 Phone:** " + profile.get('phone'))
    st.markdown("**🔗 LinkedIn:** " + profile.get('linkedin_url', ''))
    st.markdown("**⏱️ Experience:** " + profile.get('experience', ''))
    
    # Give section summary
    st.markdown("---")
    st.markdown("### 💚 What I GIVE")
    give = profile.get('give', {})
    
    if give.get('companies'):
        st.markdown("**Companies I can introduce to:**")
        render_tags(give['companies'])
    
    for key, label in [('professional_activities', 'Professional Help'),
                      ('technical_areas', 'Technical Training'),
                      ('volunteering', 'Volunteering'),
                      ('job_roles', 'Hiring For')]:
        items = get_all_items_from_section(give, key)
        if items:
            st.markdown(f"**{label}:**")
            render_tags(items)
    
    if give.get('open_contribution'):
        st.markdown(f"**Other:** {give['open_contribution']}")
    
    # Ask section summary
    st.markdown("---")
    st.markdown("### 💙 What I ASK")
    ask = profile.get('ask', {})
    
    if ask.get('companies'):
        st.markdown("**Companies I want intro to:**")
        render_tags(ask['companies'], "#1f77b4")
    
    for key, label in [('professional_activities', 'Professional Help Needed'),
                      ('technical_areas', 'Want to Learn'),
                      ('job_roles', 'Looking For Jobs In')]:
        items = get_all_items_from_section(ask, key)
        if items:
            st.markdown(f"**{label}:**")
            render_tags(items, "#1f77b4")
    
    if ask.get('open_request'):
        st.markdown(f"**Other:** {ask['open_request']}")


def _render_connections_tab(profile: Dict):
    """Render the connections tab with LinkedIn buttons."""
    sent = profile.get('connections_sent', [])
    received = profile.get('connections_received', [])
    
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Sent", f"{len(sent)}/{MAX_CONNECTIONS_PER_USER}")
    with col2:
        st.metric("Received", len(received))
    
    # Show sent connections with LinkedIn buttons
    if sent:
        st.markdown("---")
        st.markdown("**Connections You Made:**")
        st.caption("Check if they've accepted your LinkedIn request")
        
        sent_profiles = get_connection_profiles(profile.get('user_id'), 'sent')
        for idx, p in enumerate(sent_profiles):
            name = p.get('full_name', 'Unknown')
            role = p.get('current_role', '')
            linkedin = p.get('linkedin_url', '')
            
            col1, col2 = st.columns([3, 1])
            with col1:
                st.markdown(f"**{name}**")
                st.caption(role)
            with col2:
                if linkedin:
                    st.markdown(f'<a href="{linkedin}" target="_blank">🔗</a>', unsafe_allow_html=True)
    
    # Show received count only (no profile names)
    if received:
        st.markdown("---")
        st.markdown(f"**{len(received)} people connected with you!** 🎉")
