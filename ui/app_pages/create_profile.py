"""
Create Profile Page - Profile creation form with tabbed navigation.
"""

import streamlit as st
from typing import List, Dict

from services import (
    EXPERIENCE_OPTIONS,
    ROLE_OPTIONS,
    PROFESSIONAL_ACTIVITIES,
    TECHNICAL_AREAS,
    VOLUNTEERING_ACTIVITIES,
    JOB_ROLES,
    GIVE_LABELS,
    ASK_LABELS,
    GIVE_PLACEHOLDERS,
    ASK_PLACEHOLDERS,
    create_or_update_profile,
    get_profile_by_identifier
)

from shared import (
    COUNTRY_CODES,
    render_checkbox_section,
    render_multiselect_section,
    render_company_input,
    validate_email,
    validate_linkedin_url,
    validate_phone,
    normalize_linkedin_url
)


def render_create_profile_page():
    """Profile creation form with 3 tabs and step-by-step navigation."""
    st.markdown("# ✨ Create Your Profile")
    
    # Initialize session state for current tab
    if 'create_tab' not in st.session_state:
        st.session_state.create_tab = 0
    
    # Initialize form data storage (persists across tab navigation)
    if 'form_data' not in st.session_state:
        st.session_state.form_data = {}
    
    # Tab labels
    tab_labels = ["📋 Personal Info", "💚 What I Give", "💙 What I Ask"]
    current_tab = st.session_state.create_tab
    
    # Show progress
    st.progress((current_tab + 1) / 3)
    st.caption(f"Step {current_tab + 1} of 3: {tab_labels[current_tab]}")
    
    st.markdown("---")
    
    # =========================================================================
    # TAB 1: PERSONAL INFORMATION
    # =========================================================================
    if current_tab == 0:
        st.markdown("### Basic Information")
        
        # Restore values from form_data if we're returning to this tab
        fd = st.session_state.form_data
        if 'basic_name' not in st.session_state and 'full_name' in fd:
            st.session_state.basic_name = fd['full_name']
        if 'basic_email' not in st.session_state and 'email' in fd:
            st.session_state.basic_email = fd['email']
        if 'basic_linkedin' not in st.session_state and 'linkedin_url' in fd:
            st.session_state.basic_linkedin = fd['linkedin_url']
        if 'basic_phone' not in st.session_state and 'phone_number' in fd:
            st.session_state.basic_phone = fd['phone_number']
        if 'basic_company' not in st.session_state and 'current_company' in fd:
            st.session_state.basic_company = fd['current_company']
        if 'phone_country' not in st.session_state and 'country_code' in fd:
            st.session_state.phone_country = fd['country_code']
        if 'basic_experience' not in st.session_state and 'experience' in fd:
            st.session_state.basic_experience = fd['experience']
        if 'basic_role' not in st.session_state and 'current_role' in fd:
            st.session_state.basic_role = fd['current_role']
        if 'basic_custom_role' not in st.session_state and 'custom_role' in fd:
            st.session_state.basic_custom_role = fd['custom_role']
        
        full_name = st.text_input("Full Name *", key="basic_name", placeholder="John Doe")
        email = st.text_input("Email *", key="basic_email", placeholder="john@example.com")
        
        linkedin_url = st.text_input(
            "LinkedIn URL *", 
            key="basic_linkedin",
            placeholder="linkedin.com/in/yourprofile"
        )
        
        st.markdown("**Phone Number**")
        phone_cols = st.columns([1, 2])
        with phone_cols[0]:
            country_code = st.selectbox(
                "Country Code",
                options=COUNTRY_CODES,
                index=2,
                key="phone_country",
                label_visibility="collapsed"
            )
        with phone_cols[1]:
            phone_number = st.text_input(
                "Phone",
                key="basic_phone",
                placeholder="9876543210",
                label_visibility="collapsed"
            )
        
        current_company = st.text_input("Current Company", key="basic_company", placeholder="Acme Corp")
        
        experience = st.selectbox(
            "Years of Experience *",
            options=EXPERIENCE_OPTIONS,
            index=1,
            key="basic_experience"
        )
        
        current_role = st.selectbox(
            "Current Role *",
            options=ROLE_OPTIONS,
            index=0,
            key="basic_role"
        )
        
        custom_role = ""
        if current_role == "Other":
            custom_role = st.text_input("Specify Your Role", key="basic_custom_role")
        
        st.markdown("---")
        
        # Navigation: Save & Next
        if st.button("Save & Next →", type="primary", use_container_width=True):
            # Validate
            errors = []
            if not full_name or len(full_name.strip()) < 2:
                errors.append("Please enter your full name")
            if not email:
                errors.append("Please enter your email")
            elif not validate_email(email):
                errors.append("Please enter a valid email address")
            if not linkedin_url:
                errors.append("Please enter your LinkedIn URL")
            elif not validate_linkedin_url(linkedin_url):
                errors.append("Please enter a valid LinkedIn URL")
            if phone_number and not validate_phone(phone_number):
                errors.append("Please enter a valid phone number")
            
            # Check if email exists
            existing = get_profile_by_identifier(email) if email else None
            if existing:
                errors.append("A profile with this email already exists. Go to 'My Profile' to view it.")
            
            if errors:
                for err in errors:
                    st.error(err)
            else:
                # Store form data before navigation (these keys get cleared when widget not rendered)
                st.session_state.form_data['full_name'] = full_name
                st.session_state.form_data['email'] = email
                st.session_state.form_data['linkedin_url'] = linkedin_url
                st.session_state.form_data['phone_number'] = phone_number
                st.session_state.form_data['country_code'] = country_code
                st.session_state.form_data['current_company'] = current_company
                st.session_state.form_data['experience'] = experience
                st.session_state.form_data['current_role'] = current_role
                st.session_state.form_data['custom_role'] = custom_role
                
                st.session_state.create_tab = 1
                st.rerun()
    
    # =========================================================================
    # TAB 2: GIVE SECTION
    # =========================================================================
    elif current_tab == 1:
        st.markdown("### What Can You Contribute?")
        st.caption("Share what you can offer to the community")
        
        give_companies = render_company_input(
            GIVE_LABELS["q1"],
            GIVE_PLACEHOLDERS["q1"],
            "give_q1"
        )
        
        st.markdown("")
        
        give_professional = render_checkbox_section(
            GIVE_LABELS["q2"],
            PROFESSIONAL_ACTIVITIES,
            "give_q2",
            GIVE_PLACEHOLDERS["q2"]
        )
        
        st.markdown("")
        
        give_technical = render_checkbox_section(
            GIVE_LABELS["q3"],
            TECHNICAL_AREAS,
            "give_q3",
            GIVE_PLACEHOLDERS["q3"]
        )
        
        st.markdown("")
        
        # Job Roles before Volunteering
        give_jobs = render_multiselect_section(
            GIVE_LABELS["q5"],
            JOB_ROLES,
            "give_q5",
            GIVE_PLACEHOLDERS["q5"]
        )
        
        st.markdown("")
        
        give_volunteering = render_checkbox_section(
            GIVE_LABELS["q4"],
            VOLUNTEERING_ACTIVITIES,
            "give_q4",
            GIVE_PLACEHOLDERS["q4"]
        )
        
        st.markdown("")
        
        st.markdown(f"**{GIVE_LABELS['open']}**")
        give_open = st.text_area(
            "Open",
            placeholder=GIVE_PLACEHOLDERS["open"],
            key="give_open",
            height=80,
            label_visibility="collapsed"
        )
        
        st.markdown("---")
        
        # Navigation: Previous | Save & Next
        col1, col2 = st.columns(2)
        with col1:
            if st.button("← Previous", use_container_width=True):
                st.session_state.create_tab = 0
                st.rerun()
        with col2:
            if st.button("Save & Next →", type="primary", use_container_width=True, key="tab2_next"):
                st.session_state.create_tab = 2
                st.rerun()
    
    # =========================================================================
    # TAB 3: ASK SECTION
    # =========================================================================
    elif current_tab == 2:
        st.markdown("### What Do You Need?")
        st.caption("Tell us what support you're looking for")
        
        ask_companies = render_company_input(
            ASK_LABELS["q1"],
            ASK_PLACEHOLDERS["q1"],
            "ask_q1"
        )
        
        st.markdown("")
        
        ask_professional = render_checkbox_section(
            ASK_LABELS["q2"],
            PROFESSIONAL_ACTIVITIES,
            "ask_q2",
            ASK_PLACEHOLDERS["q2"]
        )
        
        st.markdown("")
        
        ask_technical = render_checkbox_section(
            ASK_LABELS["q3"],
            TECHNICAL_AREAS,
            "ask_q3",
            ASK_PLACEHOLDERS["q3"]
        )
        
        st.markdown("")
        
        # Job Roles
        ask_jobs = render_multiselect_section(
            ASK_LABELS["q5"],
            JOB_ROLES,
            "ask_q5",
            ASK_PLACEHOLDERS["q5"]
        )
        
        st.markdown("")
        
        st.markdown(f"**{ASK_LABELS['open']}**")
        ask_open = st.text_area(
            "Open",
            placeholder=ASK_PLACEHOLDERS["open"],
            key="ask_open",
            height=80,
            label_visibility="collapsed"
        )
        
        st.markdown("---")
        
        # Navigation: Previous | Submit Profile
        col1, col2 = st.columns(2)
        with col1:
            if st.button("← Previous", use_container_width=True, key="tab3_prev"):
                st.session_state.create_tab = 1
                st.rerun()
        
        with col2:
            if st.button("🚀 Submit & Find Matches", type="primary", use_container_width=True):
                _submit_profile()


def _submit_profile():
    """Submit the profile and navigate to matches."""
    # Get all form values from stored form_data (persisted across tabs)
    fd = st.session_state.get('form_data', {})
    full_name = fd.get('full_name', '')
    email = fd.get('email', '')
    linkedin_url = fd.get('linkedin_url', '')
    phone_number = fd.get('phone_number', '')
    country_code = fd.get('country_code', '+91 (India)')
    current_company = fd.get('current_company', '')
    experience = fd.get('experience', '')
    current_role = fd.get('current_role', '')
    custom_role = fd.get('custom_role', '')
    
    # Final validation
    errors = []
    if not full_name or len(full_name.strip()) < 2:
        errors.append("Please enter your full name (go to Step 1)")
    if not email or not validate_email(email):
        errors.append("Please enter a valid email (go to Step 1)")
    if not linkedin_url or not validate_linkedin_url(linkedin_url):
        errors.append("Please enter a valid LinkedIn URL (go to Step 1)")
    
    if errors:
        for err in errors:
            st.error(err)
        return
    
    # Prepare phone
    full_phone = ""
    if phone_number:
        code = country_code.split(" ")[0]
        full_phone = f"{code} {phone_number}"
    
    # Gather Give data
    give_companies = _get_company_data("give_q1")
    give_professional = _get_checkbox_data("give_q2", len(PROFESSIONAL_ACTIVITIES))
    give_technical = _get_checkbox_data("give_q3", len(TECHNICAL_AREAS))
    give_jobs = _get_multiselect_data("give_q5")
    give_volunteering = _get_checkbox_data("give_q4", len(VOLUNTEERING_ACTIVITIES))
    give_open = st.session_state.get('give_open', '')
    
    # Gather Ask data
    ask_companies = _get_company_data("ask_q1")
    ask_professional = _get_checkbox_data("ask_q2", len(PROFESSIONAL_ACTIVITIES))
    ask_technical = _get_checkbox_data("ask_q3", len(TECHNICAL_AREAS))
    ask_jobs = _get_multiselect_data("ask_q5")
    ask_open = st.session_state.get('ask_open', '')
    
    # Prepare profile data
    profile_data = {
        "full_name": full_name.strip(),
        "email": email.strip().lower(),
        "phone": full_phone,
        "linkedin_url": normalize_linkedin_url(linkedin_url),
        "current_company": current_company.strip() if current_company else "",
        "experience": experience,
        "current_role": current_role,
        "custom_role": custom_role.strip() if custom_role else "",
        "give": {
            "companies": give_companies,
            "professional_activities": give_professional,
            "technical_areas": give_technical,
            "volunteering": give_volunteering,
            "job_roles": give_jobs,
            "open_contribution": give_open
        },
        "ask": {
            "companies": ask_companies,
            "professional_activities": ask_professional,
            "technical_areas": ask_technical,
            "volunteering": {"selected": [], "custom": []},
            "job_roles": ask_jobs,
            "open_request": ask_open
        }
    }
    
    with st.spinner("Creating your profile..."):
        result = create_or_update_profile(profile_data)
    
    if result:
        st.success("🎉 Profile created successfully!")
        st.toast("🎉 Profile created!", icon="✅")
        st.session_state.current_profile = result
        st.session_state.create_tab = 0  # Reset for next time
        st.session_state.form_data = {}  # Clear form data
        st.session_state.page = 'my_profile'
        st.rerun()
    else:
        st.error("Failed to create profile. Please try again.")


def _get_company_data(key: str) -> List[str]:
    """Get company data from session state."""
    text = st.session_state.get(key, '')
    return [x.strip() for x in text.split(",") if x.strip()] if text else []


def _get_checkbox_data(key_prefix: str, count: int) -> Dict:
    """Get checkbox selection data from session state."""
    selected = []
    options_map = {
        "give_q2": PROFESSIONAL_ACTIVITIES,
        "ask_q2": PROFESSIONAL_ACTIVITIES,
        "give_q3": TECHNICAL_AREAS,
        "ask_q3": TECHNICAL_AREAS,
        "give_q4": VOLUNTEERING_ACTIVITIES,
    }
    options = options_map.get(key_prefix, [])
    
    for idx in range(count):
        if st.session_state.get(f"{key_prefix}_{idx}", False):
            if idx < len(options):
                selected.append(options[idx])
    
    custom_text = st.session_state.get(f"{key_prefix}_custom", '')
    custom = [x.strip() for x in custom_text.split(",") if x.strip()] if custom_text else []
    
    return {"selected": selected, "custom": custom}


def _get_multiselect_data(key_prefix: str) -> Dict:
    """Get multiselect data from session state."""
    selected = st.session_state.get(f"{key_prefix}_multi", [])
    custom_text = st.session_state.get(f"{key_prefix}_custom", '')
    custom = [x.strip() for x in custom_text.split(",") if x.strip()] if custom_text else []
    return {"selected": selected, "custom": custom}
