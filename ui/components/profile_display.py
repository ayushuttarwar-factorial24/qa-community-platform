"""
Profile Display Components

Components for displaying profile information in cards and detailed views.
"""

import streamlit as st
from typing import Dict, List, Optional


def display_profile_card_compact(
    profile: Dict,
    show_connect: bool = False,
    on_connect_key: str = None
) -> None:
    """
    Displays a compact profile card (for leaderboard, connections).
    
    Args:
        profile: Profile dict
        show_connect: Whether to show connect button
        on_connect_key: Unique key for connect button
    """
    col1, col2 = st.columns([3, 1])
    
    with col1:
        name = profile.get('full_name', profile.get('name', 'Unknown'))
        role = profile.get('current_role', profile.get('job_role', ''))
        custom_role = profile.get('custom_role', '')
        display_role = custom_role if role == "Other" and custom_role else role
        company = profile.get('current_company', '')
        
        st.markdown(f"**{name}**")
        if company:
            st.caption(f"{display_role} at {company}")
        else:
            st.caption(display_role)
    
    with col2:
        points = profile.get('points', 0)
        st.metric("Points", points, label_visibility="collapsed")


def display_match_card(
    match_result: Dict,
    rank: int,
    source_user_id: str,
    on_connect_callback=None
) -> None:
    """
    Displays a match result card with match reasons and connect button.
    
    Args:
        match_result: Match result dict with score, reasons, and profile
        rank: Match rank (1-based)
        source_user_id: ID of the user viewing matches
        on_connect_callback: Callback function when connect is clicked
    """
    profile = match_result.get('candidate_profile', {})
    score = match_result.get('total_score', 0)
    reasons = match_result.get('match_reasons', [])
    
    name = profile.get('full_name', 'Unknown')
    role = profile.get('current_role', '')
    custom_role = profile.get('custom_role', '')
    display_role = custom_role if role == "Other" and custom_role else role
    company = profile.get('current_company', '')
    experience = profile.get('experience', '')
    linkedin = profile.get('linkedin_url', '')
    
    with st.container():
        # Header
        header_col1, header_col2 = st.columns([3, 1])
        
        with header_col1:
            st.markdown(f"### 🏆 #{rank} - {name}")
            role_text = f"**{display_role}**"
            if company:
                role_text += f" at {company}"
            if experience:
                role_text += f" • {experience}"
            st.markdown(role_text)
        
        with header_col2:
            st.metric("Match", f"{score:.0f}%")
        
        # Match reasons
        if reasons:
            st.markdown("**🎯 Why this match:**")
            for reason in reasons[:4]:  # Limit to 4 reasons
                st.markdown(f"• {reason}")
        
        # Give/Ask summary
        give_section = profile.get('give', {})
        ask_section = profile.get('ask', {})
        
        # Show what they can offer (GIVE)
        with st.expander("💚 What they can GIVE", expanded=False):
            _display_give_ask_summary(give_section, is_give=True)
        
        # Show what they need (ASK)
        with st.expander("💙 What they ASK for", expanded=False):
            _display_give_ask_summary(ask_section, is_give=False)
        
        # Connect button
        if linkedin:
            st.link_button(
                "🤝 Connect on LinkedIn",
                linkedin,
                use_container_width=True,
                type="primary"
            )
        else:
            st.info("No LinkedIn profile available")
        
        # Contact details
        with st.expander("📧 Contact Details"):
            email = profile.get('email', '')
            phone = profile.get('phone', '')
            if email:
                st.markdown(f"✉️ **Email:** {email}")
            if phone:
                st.markdown(f"📱 **Phone:** {phone}")
        
        st.markdown("---")


def _display_give_ask_summary(section: Dict, is_give: bool = True) -> None:
    """
    Helper to display Give or Ask section summary.
    """
    if not section:
        st.write("No information available")
        return
    
    # Companies
    companies = section.get('companies', [])
    if companies:
        st.markdown(f"🏢 **Companies:** {', '.join(companies[:5])}")
    
    # Professional activities
    prof = section.get('professional_activities', {})
    prof_items = prof.get('selected', []) + prof.get('custom', [])
    if prof_items:
        st.markdown(f"💼 **Professional Activities:** {', '.join(prof_items[:3])}")
    
    # Technical areas
    tech = section.get('technical_areas', {})
    tech_items = tech.get('selected', []) + tech.get('custom', [])
    if tech_items:
        st.markdown(f"🔧 **Technical Areas:** {', '.join(tech_items[:3])}")
    
    # Volunteering
    vol = section.get('volunteering', {})
    vol_items = vol.get('selected', []) + vol.get('custom', [])
    if vol_items:
        st.markdown(f"🤲 **Volunteering:** {', '.join(vol_items[:3])}")
    
    # Job roles
    jobs = section.get('job_roles', {})
    job_items = jobs.get('selected', []) + jobs.get('custom', [])
    if job_items:
        st.markdown(f"💼 **Job Roles:** {', '.join(job_items[:3])}")
    
    # Open text
    open_text = section.get('open_contribution', section.get('open_request', ''))
    if open_text:
        st.markdown(f"📝 **Additional:** {open_text[:100]}...")


def display_my_profile_summary(profile: Dict) -> None:
    """
    Displays the current user's profile summary.
    
    Args:
        profile: User's profile dict
    """
    if not profile:
        st.warning("No profile data available")
        return
    
    # Basic info
    name = profile.get('full_name', 'Unknown')
    email = profile.get('email', '')
    phone = profile.get('phone', '')
    linkedin = profile.get('linkedin_url', '')
    company = profile.get('current_company', '')
    role = profile.get('current_role', '')
    custom_role = profile.get('custom_role', '')
    display_role = custom_role if role == "Other" and custom_role else role
    experience = profile.get('experience', '')
    points = profile.get('points', 0)
    
    # Header with points
    col1, col2 = st.columns([3, 1])
    with col1:
        st.markdown(f"## {name}")
        st.markdown(f"**{display_role}**" + (f" at {company}" if company else ""))
    with col2:
        st.metric("Points", points)
    
    # Basic info
    with st.expander("📋 Basic Information", expanded=True):
        st.markdown(f"📧 **Email:** {email}")
        if phone:
            st.markdown(f"📱 **Phone:** {phone}")
        if linkedin:
            st.markdown(f"🔗 **LinkedIn:** [View Profile]({linkedin})")
        st.markdown(f"⏱️ **Experience:** {experience}")
    
    # Give section
    st.markdown("### 💚 What I Can GIVE")
    give_section = profile.get('give', {})
    _display_full_give_ask_section(give_section, is_give=True)
    
    # Ask section
    st.markdown("### 💙 What I ASK For")
    ask_section = profile.get('ask', {})
    _display_full_give_ask_section(ask_section, is_give=False)
    
    # Connections
    st.markdown("### 🔗 Connections")
    connections_sent = profile.get('connections_sent', [])
    connections_received = profile.get('connections_received', [])
    
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Sent", len(connections_sent))
    with col2:
        st.metric("Received", len(connections_received))


def _display_full_give_ask_section(section: Dict, is_give: bool = True) -> None:
    """
    Displays complete Give or Ask section details.
    """
    if not section:
        st.write("No information provided yet")
        return
    
    # Companies
    companies = section.get('companies', [])
    if companies:
        _display_tags("🏢 Companies", companies)
    
    # Professional activities
    prof = section.get('professional_activities', {})
    prof_items = prof.get('selected', []) + prof.get('custom', [])
    if prof_items:
        _display_tags("💼 Professional Activities", prof_items)
    
    # Technical areas
    tech = section.get('technical_areas', {})
    tech_items = tech.get('selected', []) + tech.get('custom', [])
    if tech_items:
        _display_tags("🔧 Technical Areas", tech_items)
    
    # Volunteering
    vol = section.get('volunteering', {})
    vol_items = vol.get('selected', []) + vol.get('custom', [])
    if vol_items:
        _display_tags("🤲 Volunteering", vol_items)
    
    # Job roles
    jobs = section.get('job_roles', {})
    job_items = jobs.get('selected', []) + jobs.get('custom', [])
    if job_items:
        label = "💼 Hiring For" if is_give else "💼 Looking For"
        _display_tags(label, job_items)
    
    # Open text
    open_key = 'open_contribution' if is_give else 'open_request'
    open_text = section.get(open_key, '')
    if open_text:
        st.markdown(f"📝 **Additional Notes:**")
        st.info(open_text)


def _display_tags(label: str, items: List[str]) -> None:
    """Display items as styled tags."""
    if not items:
        return
    
    st.markdown(f"**{label}:**")
    tags_html = " ".join([
        f'<span style="background-color:#667eea;color:white;padding:4px 12px;'
        f'border-radius:15px;margin:2px 4px 2px 0;display:inline-block;font-size:13px;">{item}</span>'
        for item in items
    ])
    st.markdown(tags_html, unsafe_allow_html=True)
    st.markdown("")  # Spacing
