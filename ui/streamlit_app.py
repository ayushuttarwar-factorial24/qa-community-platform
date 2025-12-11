"""
Streamlit UI for QA Community Profile Matching Platform

User-friendly interface for creating profiles and viewing suggested matches.
"""

import streamlit as st
import streamlit.components.v1 as components
import requests
from typing import List, Dict, Any, Optional
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# API Configuration
API_BASE_URL = os.getenv("API_BASE_URL", "http://localhost:8000")
API_PROFILES_ENDPOINT = f"{API_BASE_URL}/api/v1/profiles"
DEFAULT_MATCH_LIMIT = int(os.getenv("DEFAULT_MATCH_LIMIT", "5"))

# Country codes for phone numbers
COUNTRY_CODES = [
    "+91 (India)", "+1 (USA/Canada)", "+44 (UK)", "+61 (Australia)", 
    "+65 (Singapore)", "+971 (UAE)", "+966 (Saudi Arabia)", "+81 (Japan)",
    "+86 (China)", "+49 (Germany)", "+33 (France)", "+39 (Italy)",
    "+34 (Spain)", "+7 (Russia)", "+55 (Brazil)", "+62 (Indonesia)",
    "+60 (Malaysia)", "+63 (Philippines)", "+82 (South Korea)", "+64 (New Zealand)"
]

# Page configuration - Mobile-first responsive design
st.set_page_config(
    page_title="QA Community - Profile Matching",
    page_icon="🤝",
    layout="wide",
    initial_sidebar_state="auto"
)

# Add mobile-friendly CSS
st.markdown("""
<style>
    /* Mobile-first responsive design */
    @media (max-width: 768px) {
        .stButton button {
            width: 100%;
            margin-bottom: 0.5rem;
            font-size: 16px !important;
            padding: 1rem !important;
            min-height: 48px;
        }
        .row-widget.stRadio > div {
            flex-direction: column;
        }
        section[data-testid="stSidebar"] {
            width: 100% !important;
        }
        [data-testid="column"] {
            min-width: 100% !important;
            flex: 1 1 100% !important;
        }
        .stMetric {
            background: #f0f2f6;
            padding: 1rem;
            border-radius: 10px;
            margin-bottom: 0.5rem;
        }
    }
    
    /* Improve button visibility */
    .stButton button {
        font-size: 16px;
        padding: 0.75rem 1.5rem;
        border-radius: 10px;
        font-weight: 500;
        transition: all 0.3s ease;
    }
    
    .stButton button:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(0,0,0,0.15);
    }
    
    /* Better touch targets */
    .stMultiSelect, .stSelectbox, .stTextInput {
        min-height: 44px;
    }
    
    /* Clean card style */
    .stContainer {
        padding: 1rem;
        border-radius: 15px;
    }
    
    /* Progress bar styling */
    .stProgress > div > div {
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        height: 8px;
        border-radius: 10px;
    }
    
    /* Link button improvements */
    .stLinkButton a {
        text-decoration: none;
    }
    
    /* Header improvements */
    h1, h2, h3 {
        margin-top: 0.5rem;
        margin-bottom: 1rem;
    }
    
    /* Metric improvements */
    [data-testid="stMetricValue"] {
        font-size: 1.5rem;
        font-weight: 600;
    }
</style>
""", unsafe_allow_html=True)

# Session state initialization
if 'current_profile' not in st.session_state:
    st.session_state.current_profile = None
if 'selected_strength_tags' not in st.session_state:
    st.session_state.selected_strength_tags = []
if 'selected_learn_tags' not in st.session_state:
    st.session_state.selected_learn_tags = []
if 'editing_profile' not in st.session_state:
    st.session_state.editing_profile = False
if 'viewing_matches' not in st.session_state:
    st.session_state.viewing_matches = False
if 'matches_loaded' not in st.session_state:
    st.session_state.matches_loaded = False
if 'current_match_index' not in st.session_state:
    st.session_state.current_match_index = 0
if 'matches_list' not in st.session_state:
    st.session_state.matches_list = []
if 'matches_message' not in st.session_state:
    st.session_state.matches_message = None


def get_skills_by_category() -> Dict[str, List[str]]:
    """
    Returns categorized QA skills for better UI organization.
    
    Returns:
        Dict with category names as keys and skill lists as values
    """
    return {
        "Testing Types": [
            "Manual Testing", "Automation Testing", "API Testing", "Performance Testing",
            "Load Testing", "Security Testing", "Mobile Testing", "Web Testing",
            "Database Testing", "Regression Testing", "Exploratory Testing"
        ],
        "Automation Tools": [
            "Selenium", "Cypress", "Playwright", "WebdriverIO", "Appium",
            "Robot Framework", "Katalon Studio", "Puppeteer"
        ],
        "Testing Frameworks": [
            "pytest", "unittest", "TestNG", "JUnit", "NUnit", "Mocha",
            "Jasmine", "Jest", "Cucumber", "SpecFlow", "Behave"
        ],
        "API Tools": [
            "Postman", "Newman", "Insomnia", "SoapUI", "REST Assured",
            "Karate Framework", "GraphQL Testing", "Swagger"
        ],
        "Performance Tools": [
            "JMeter", "LoadRunner", "Gatling", "Locust", "k6", "Artillery"
        ],
        "Programming Languages": [
            "Python", "Java", "JavaScript", "TypeScript", "C#", "Ruby",
            "Go", "SQL", "Shell Scripting"
        ],
        "CI/CD Tools": [
            "Jenkins", "GitLab CI", "GitHub Actions", "CircleCI", "Azure DevOps",
            "Docker", "Kubernetes"
        ],
        "Test Management": [
            "JIRA", "TestRail", "Zephyr", "Xray", "Azure Test Plans",
            "Test Case Design", "Test Planning", "Defect Management"
        ],
        "Methodologies": [
            "Agile Testing", "Scrum", "Kanban", "BDD", "TDD", "DevOps",
            "Continuous Testing", "Shift-Left Testing"
        ],
        "Version Control": [
            "Git", "GitHub", "GitLab", "Bitbucket"
        ],
        "Reporting Tools": [
            "Allure Reports", "ExtentReports", "TestNG Reports", "ReportPortal"
        ],
        "Specialized Testing": [
            "Microservices Testing", "Cloud Testing", "AI/ML Testing",
            "ETL Testing", "Accessibility Testing"
        ]
    }


def get_all_skills() -> List[str]:
    """Returns flat list of all skills."""
    skills_by_cat = get_skills_by_category()
    all_skills = []
    for skills in skills_by_cat.values():
        all_skills.extend(skills)
    return sorted(list(set(all_skills)))


def get_popular_skills() -> List[str]:
    """Returns list of most commonly used QA skills."""
    return [
        "Selenium", "Python", "Java", "API Testing", "JIRA", 
        "Automation Testing", "Manual Testing", "Playwright", 
        "Cypress", "TestNG", "pytest", "Postman", "Jenkins",
        "Git", "Agile Testing"
    ]





def get_profile_by_email(email: str) -> Optional[Dict]:
    """
    Fetch profile by email from API.
    
    Args:
        email: Email address
        
    Returns:
        Profile dict or None
    """
    try:
        response = requests.get(
            f"{API_PROFILES_ENDPOINT}/{email}",
            timeout=10
        )
        if response.status_code == 200:
            return response.json()
        return None
    except:
        return None


def create_profile(profile_data: Dict[str, Any]) -> Optional[Dict]:
    """
    Calls the API to create or update a profile.
    
    Args:
        profile_data: Profile information
        
    Returns:
        API response dict or None on error
    """
    try:
        response = requests.post(
            API_PROFILES_ENDPOINT + "/",
            json=profile_data,
            timeout=10
        )
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        st.error(f"Failed to create profile: {str(e)}")
        return None


def get_suggested_matches(identifier: str, limit: int = None) -> Optional[Dict]:
    """
    Calls the API to get suggested profile matches.
    
    Args:
        identifier: user_id, email, or phone
        limit: Number of matches to retrieve (uses DEFAULT_MATCH_LIMIT if None)
        
    Returns:
        API response dict or None on error
    """
    if limit is None:
        limit = DEFAULT_MATCH_LIMIT
        
    try:
        response = requests.get(
            f"{API_PROFILES_ENDPOINT}/{identifier}/suggested",
            params={"limit": limit, "include_breakdown": True},
            timeout=10
        )
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        st.error(f"Failed to get matches: {str(e)}")
        return None


def connect_with_profile(initiator_id: str, target_id: str) -> Optional[Dict]:
    """
    Connect with another profile via API.
    
    Args:
        initiator_id: User ID of initiator
        target_id: User ID of target profile
        
    Returns:
        API response dict or None on error
    """
    try:
        response = requests.post(
            f"{API_PROFILES_ENDPOINT}/{initiator_id}/connect/{target_id}",
            timeout=10
        )
        if response.status_code == 200:
            return response.json()
        else:
            error_detail = response.json().get("detail", "Connection failed")
            st.error(f"❌ {error_detail}")
            return None
    except requests.exceptions.RequestException as e:
        st.error(f"Failed to connect: {str(e)}")
        return None


def get_leaderboard() -> Optional[Dict]:
    """
    Fetch leaderboard from API.
    
    Returns:
        API response dict or None on error
    """
    try:
        response = requests.get(
            f"{API_PROFILES_ENDPOINT}/leaderboard",
            params={"limit": 100},
            timeout=10
        )
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        st.error(f"Failed to load leaderboard: {str(e)}")
        return None


def display_match_card(match: Dict, index: int):
    """
    Displays a single match result as a card.
    
    Args:
        match: Match result dict
        index: Match rank (1-based)
    """
    profile = match["profile"]
    score = match["score"]
    overlap_tags = match.get("overlap_tags", [])
    is_fallback = match.get("is_fallback", False)
    score_breakdown = match.get("score_breakdown")
    
    # Create card with border
    with st.container():
        # Header with rank and name
        col1, col2 = st.columns([3, 1])
        
        with col1:
            st.markdown(f"### 🏆 #{index} - {profile['name']}")
            st.markdown(f"**{profile['job_role']}** • {profile['years_exp']} years experience")
        
        with col2:
            st.metric("Match Score", f"{score:.1f}")
        
        # Overlap tags (if not fallback)
        if overlap_tags and not is_fallback:
            st.markdown("**🎯 Matching Skills:**")
            tags_html = " ".join([
                f'<span style="background-color:#1f77b4;color:white;padding:4px 8px;'
                f'border-radius:4px;margin:2px;display:inline-block;font-size:12px;">{tag}</span>'
                for tag in overlap_tags
            ])
            st.markdown(tags_html, unsafe_allow_html=True)
        
        # Strength tags preview
        st.markdown("**💪 Can Contribute In:**")
        strength_preview = profile['strength_tags'][:6]
        tags_html = " ".join([
            f'<span style="background-color:#2ca02c;color:white;padding:4px 8px;'
            f'border-radius:4px;margin:2px;display:inline-block;font-size:12px;">{tag}</span>'
            for tag in strength_preview
        ])
        if len(profile['strength_tags']) > 6:
            tags_html += f' <span style="color:#666;">+{len(profile["strength_tags"]) - 6} more</span>'
        st.markdown(tags_html, unsafe_allow_html=True)
        
        # Connect button - Primary action for mobile users
        if profile.get('linkedin'):
            linkedin_url = profile['linkedin']
            st.link_button(
                "🤝 Connect on LinkedIn",
                linkedin_url,
                use_container_width=True,
                type="primary"
            )
        else:
            st.info("💬 No LinkedIn profile available")
        
        # Additional contact information (collapsible on mobile)
        with st.expander("📧 View Contact Details"):
            if profile.get('email'):
                st.markdown(f"✉️ **Email:** {profile['email']}")
            if profile.get('phone'):
                st.markdown(f"📱 **Phone:** {profile['phone']}")
            if profile.get('github'):
                st.markdown(f"💻 [GitHub Profile]({profile['github']})")
        
        # Score breakdown (if available)
        if score_breakdown:
            with st.expander("📊 Score Breakdown"):
                cols = st.columns(4)
                cols[0].metric("Overlap", f"{score_breakdown.get('overlap_score', 0):.2f}")
                cols[1].metric("Experience", f"{score_breakdown.get('experience_score', 0):.2f}")
                cols[2].metric("Breadth", f"{score_breakdown.get('breadth_score', 0):.2f}")
                cols[3].metric("Role Match", f"{score_breakdown.get('role_score', 0):.2f}")
        
        st.markdown("---")


def render_swipe_card_interface(matches: List[Dict], source_user_id: str):
    """
    Renders swipe-style card interface for mobile-friendly match browsing.
    
    Args:
        matches: List of match dicts
        source_user_id: User ID of the profile viewing matches
    """
    if not matches:
        st.info("📭 No matches available")
        return
    
    # Initialize or get current index
    if 'current_match_index' not in st.session_state:
        st.session_state.current_match_index = 0
    
    current_idx = st.session_state.current_match_index
    
    # Check if we've gone through all matches
    if current_idx >= len(matches):
        st.success("🎉 You've viewed all matches!")
        if st.button("🔄 Start Over", use_container_width=True, type="primary"):
            st.session_state.current_match_index = 0
            st.rerun()
        return
    
    match = matches[current_idx]
    profile = match["profile"]
    score = match["score"]
    overlap_tags = match.get("overlap_tags", [])
    target_user_id = profile.get('user_id', profile.get('_id'))
    
    # Progress indicator - Mobile friendly
    progress_value = (current_idx + 1) / len(matches)
    st.progress(progress_value)
    st.markdown(f"<p style='text-align:center;color:#666;font-size:14px;'>Match {current_idx + 1} of {len(matches)}</p>", unsafe_allow_html=True)
    
    # Mobile-first card with clean design
    st.markdown("""
        <style>
        .match-card {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            padding: 30px 20px;
            border-radius: 20px;
            color: white;
            text-align: center;
            margin: 20px 0;
            box-shadow: 0 10px 30px rgba(0,0,0,0.2);
        }
        .match-name {
            font-size: 28px;
            font-weight: bold;
            margin-bottom: 8px;
        }
        .match-role {
            font-size: 16px;
            opacity: 0.9;
            margin-bottom: 20px;
        }
        </style>
    """, unsafe_allow_html=True)
    
    # Card header
    st.markdown(f"""
        <div class="match-card">
            <div class="match-name">{profile['name']}</div>
            <div class="match-role">{profile['job_role']} | {profile['years_exp']} yrs</div>
        </div>
    """, unsafe_allow_html=True)
    
    st.markdown("")
    
    # Matching skills - what they can teach you
    if overlap_tags:
        st.markdown("#### 🎯 Can Help You Learn:")
        tags_html = " ".join([
            f'<span style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);'
            f'color:white;padding:8px 16px;border-radius:20px;margin:4px;'
            f'display:inline-block;font-size:14px;font-weight:500;">{tag}</span>'
            for tag in overlap_tags[:5]
        ])
        st.markdown(tags_html, unsafe_allow_html=True)
    
    # Their key strengths (limited)
    st.markdown("#### 💪 Key Strengths:")
    key_skills = profile['strength_tags'][:4]
    skills_html = " ".join([
        f'<span style="background-color:#2ca02c;color:white;padding:6px 12px;'
        f'border-radius:15px;margin:4px;display:inline-block;font-size:13px;">{tag}</span>'
        for tag in key_skills
    ])
    if len(profile['strength_tags']) > 4:
        skills_html += f' <span style="color:#666;font-size:13px;">+{len(profile["strength_tags"]) - 4} more</span>'
    st.markdown(skills_html, unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Large action buttons for mobile
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("⏭️ Next", use_container_width=True, type="secondary", key=f"skip_{current_idx}", help="Skip to next match"):
            st.session_state.current_match_index += 1
            st.rerun()
    
    with col2:
        # Check if already connected
        current_profile = st.session_state.get('current_profile', {})
        connections_sent = current_profile.get('connections_sent', [])
        already_connected = target_user_id in connections_sent
        
        # Check connection limit (only for outgoing connections)
        connections_count = len(connections_sent)
        at_limit = connections_count >= 5
        
        if already_connected:
            st.button("✅ Connected", use_container_width=True, disabled=True, key=f"connected_{current_idx}")
        elif at_limit:
            st.button("⚠️ Limit Reached", use_container_width=True, disabled=True, key=f"limit_{current_idx}", help="Maximum 5 connections")
        else:
            if st.button("🤝 Connect", use_container_width=True, type="primary", key=f"connect_{current_idx}", help=f"Earn points! (+10 for you, +20 for them)"):
                # Make connection
                result = connect_with_profile(source_user_id, target_user_id)
                
                if result and result.get('success'):
                    st.success("✅ Connection successful!")
                    st.balloons()
                    
                    # Update current profile to reflect new connection
                    if st.session_state.current_profile:
                        if 'connections_sent' not in st.session_state.current_profile:
                            st.session_state.current_profile['connections_sent'] = []
                        st.session_state.current_profile['connections_sent'].append(target_user_id)
                        st.session_state.current_profile['points'] = result.get('initiator_points', st.session_state.current_profile.get('points', 0))
                    
                    # Open LinkedIn in new tab using JavaScript
                    if profile.get('linkedin'):
                        linkedin_url = profile['linkedin']
                        st.info("🔗 Opening LinkedIn profile in new tab...")
                        
                        # Use JavaScript to open in new tab
                        components.html(
                            f"""
                            <script>
                                window.open('{linkedin_url}', '_blank');
                            </script>
                            <p style="text-align:center;padding:10px;background:#0077b5;color:white;border-radius:5px;">
                                LinkedIn profile opened in new tab. If it didn't open, 
                                <a href="{linkedin_url}" target="_blank" style="color:white;text-decoration:underline;">click here</a>
                            </p>
                            """,
                            height=100
                        )
                    
                    st.rerun()


def render_leaderboard_page():
    """Renders the leaderboard page showing top QA professionals by points."""
    st.header("🏆 Leaderboard")
    
    # Fetch leaderboard data
    with st.spinner("Loading leaderboard..."):
        leaderboard_data = get_leaderboard()
    
    if not leaderboard_data:
        st.error("Failed to load leaderboard")
        return
    
    profiles = leaderboard_data.get("profiles", [])
    
    if not profiles:
        st.info("No profiles yet. Be the first to join!")
        return
    
    # Search bar
    search_query = st.text_input("🔍 Search by name:", placeholder="Type to search...", key="leaderboard_search")
    
    # Filter profiles based on search
    if search_query:
        filtered_profiles = [p for p in profiles if search_query.lower() in p['name'].lower()]
    else:
        filtered_profiles = profiles
    
    if not filtered_profiles:
        st.warning("No profiles found matching your search.")
        return
    
    st.markdown(f"**Showing {len(filtered_profiles)} profiles**")
    st.markdown("---")
    
    # Mobile-friendly tabular view
    for rank, profile in enumerate(filtered_profiles, 1):
        # Medal for top 3
        if rank == 1:
            medal = "🥇"
        elif rank == 2:
            medal = "🥈"
        elif rank == 3:
            medal = "🥉"
        else:
            medal = f"#{rank}"
        
        # Get connections received count
        connections_received = profile.get('connections_received', [])
        received_count = len(connections_received) if connections_received else 0
        
        # Show connections received only if > 0
        connections_display = f'<span style="color:#2ca02c;font-size:13px;margin-left:8px;">👥 {received_count}</span>' if received_count > 0 else ''
        
        # Single row with horizontal layout
        st.markdown(f"""
        <div style="background:#f8f9fa;padding:12px;border-radius:8px;margin-bottom:8px;display:flex;align-items:center;justify-content:space-between;">
            <div style="display:flex;align-items:center;gap:12px;flex:1;min-width:0;">
                <span style="font-size:20px;font-weight:bold;min-width:40px;">{medal}</span>
                <div style="flex:1;min-width:0;">
                    <div style="font-weight:600;font-size:14px;white-space:nowrap;overflow:hidden;text-overflow:ellipsis;">{profile['name']}&nbsp;&nbsp;&nbsp; {connections_display}</div>
                </div>
            </div>
            <div style="font-weight:bold;color:#667eea;font-size:16px;min-width:60px;text-align:right;">{profile.get('points', 0)} pts</div>
        </div>
        """, unsafe_allow_html=True)


def render_profile_form(profile_data: Optional[Dict] = None):
    """
    Renders the profile creation/editing form.
    
    Args:
        profile_data: Existing profile data for editing (optional)
    """
    is_editing = profile_data is not None
    
    if is_editing:
        st.info("✏️ Editing your profile. Update any fields and submit to save changes.")
    
    with st.form("profile_form", clear_on_submit=False):
        # Personal Information Section
        st.subheader("👤 Personal Information")
        
        col1, col2 = st.columns(2)
        
        with col1:
            name = st.text_input(
                "Full Name :red[*]",
                value=profile_data.get('name', '') if profile_data else '',
                placeholder="e.g., Rajesh Kumar"
            )
            
            email = st.text_input(
                "Email :red[*]",
                value=profile_data.get('email', '') if profile_data else '',
                placeholder="e.g., rajesh.kumar@example.com",
                disabled=is_editing  # Can't change email when editing
            )
        
        with col2:
            job_role = st.text_input(
                "Job Role :red[*]",
                value=profile_data.get('job_role', '') if profile_data else '',
                placeholder="e.g., QA Engineer, SDET, Test Lead"
            )
            
            years_exp = st.number_input(
                "Years of Experience :red[*]",
                min_value=0,
                max_value=50,
                value=profile_data.get('years_exp', 3) if profile_data else 3
            )
        
        # Phone with country code - FIXED ALIGNMENT
        st.markdown("**Phone Number** :red[*]")
        phone_cols = st.columns([1, 3])
        
        with phone_cols[0]:
            # Extract country code if editing
            default_code = "+91 (India)"
            if profile_data and profile_data.get('phone'):
                phone_val = profile_data['phone']
                for code in COUNTRY_CODES:
                    code_num = code.split()[0]
                    if phone_val.startswith(code_num):
                        default_code = code
                        break
            
            country_code = st.selectbox(
                "Country Code",
                options=COUNTRY_CODES,
                index=COUNTRY_CODES.index(default_code),
                label_visibility="collapsed"
            )
        
        with phone_cols[1]:
            # Extract phone number without country code
            phone_number = ""
            if profile_data and profile_data.get('phone'):
                phone_val = profile_data['phone']
                code_num = country_code.split()[0]
                phone_number = phone_val.replace(code_num, '').strip()
            
            phone_input = st.text_input(
                "Phone Number",
                value=phone_number,
                placeholder="e.g., 9876543210",
                label_visibility="collapsed"
            )
        
        # Social Information Section
        st.subheader("🔗 Social Information")
        
        col3, col4 = st.columns(2)
        
        with col3:
            linkedin = st.text_input(
                "LinkedIn Profile :red[*]",
                value=profile_data.get('linkedin', '') if profile_data else '',
                placeholder="https://linkedin.com/in/yourprofile",
                help="Required for connections"
            )
        
        with col4:
            github = st.text_input(
                "GitHub Profile",
                value=profile_data.get('github', '') if profile_data else '',
                placeholder="https://github.com/yourusername",
                help="Optional: Your GitHub profile URL"
            )
        
        # Skills Section
        st.subheader("🎯 Skills & Expertise")
        # st.markdown("*Share your expertise to help others. Learning goals are optional.*")
        
        # Get all available skills
        all_skills = get_all_skills()
        
        # Strength tags
        st.markdown("**💪 Skills You Can Contribute In** :red[*] (minimum 3)")
        strength_tags = st.multiselect(
            "Select from available skills:",
            options=all_skills,
            default=profile_data.get('strength_tags', []) if profile_data else [],
            help="Choose skills you're proficient in",
            key="strength_standard"
        )
        
        strength_custom = st.text_input(
            "Add custom skills (comma-separated):",
            value="",
            placeholder="e.g., Docker, Kubernetes, Custom Framework",
            help="Add any additional skills not in the list above",
            key="strength_custom"
        )
        
        st.markdown("")  # Spacing
        
        # Learn tags - OPTIONAL for experienced professionals
        st.markdown("**📚 Skills You Want to Learn** (optional - skip if you're here to mentor)")
        learn_tags = st.multiselect(
            "Select from available skills:",
            options=all_skills,
            default=profile_data.get('learn_tags', []) if profile_data else [],
            help="Optional: Choose skills you want to learn. Leave empty if you're primarily here to help others.",
            key="learn_standard"
        )
        
        learn_custom = st.text_input(
            "Add custom learning goals (comma-separated):",
            value="",
            placeholder="e.g., AI Testing, Blockchain QA (Optional)",
            help="Optional: Add any additional skills not in the list above",
            key="learn_custom"
        )
        
        # Submit button
        st.markdown("")
        submit_label = "💾 Update Profile & Get Matches" if is_editing else "🚀 Create Profile & Get Matches"
        submitted = st.form_submit_button(submit_label, type="primary", use_container_width=True)
        
        if submitted:
            # Validation
            if not all([name, email, phone_input, job_role, linkedin]):
                st.error("❌ Please fill in all required fields marked with *")
                return
            
            # Construct full phone number
            code_num = country_code.split()[0]
            full_phone = f"{code_num}{phone_input.strip()}"
            
            # Combine standard and custom tags
            all_strength_tags = strength_tags.copy()
            if strength_custom and strength_custom.strip():
                custom_tags = [tag.strip() for tag in strength_custom.split(",") if tag.strip()]
                all_strength_tags.extend(custom_tags)
            
            all_learn_tags = learn_tags.copy()
            if learn_custom and learn_custom.strip():
                custom_tags = [tag.strip() for tag in learn_custom.split(",") if tag.strip()]
                all_learn_tags.extend(custom_tags)
            
            # Remove duplicates while preserving order
            all_strength_tags = list(dict.fromkeys(all_strength_tags))
            all_learn_tags = list(dict.fromkeys(all_learn_tags))
            
            # Validate minimum skills (counting both selected and custom)
            if len(all_strength_tags) < 3:
                st.error(f"❌ Please add at least 3 skills you can contribute in (currently: {len(all_strength_tags)})")
                return
            
            # Validate LinkedIn URL
            if not linkedin or len(linkedin.strip()) < 10:
                st.error("❌ LinkedIn profile URL is required (minimum 10 characters)")
                return
            
            linkedin_lower = linkedin.lower()
            if 'linkedin.com/in/' not in linkedin_lower and 'linkedin.com/company/' not in linkedin_lower:
                st.error("❌ Please enter a valid LinkedIn profile URL (e.g., https://linkedin.com/in/yourname)")
                return
            
            # learn_tags is optional - no minimum validation needed
            # Experienced professionals can skip learning goals if they're here to mentor
            
            # Prepare profile data
            profile_payload = {
                "name": name,
                "email": email,
                "phone": full_phone,
                "linkedin": linkedin if linkedin else None,
                "github": github if github else None,
                "job_role": job_role,
                "years_exp": years_exp,
                "strength_tags": all_strength_tags,
                "learn_tags": all_learn_tags
            }
            
            # Create/Update profile
            with st.spinner("Saving profile..."):
                profile_response = create_profile(profile_payload)
            
            if profile_response:
                action = "updated" if is_editing else "created"
                st.success(f"✅ Profile {action} successfully!")
                
                # Get matches
                with st.spinner("Finding your matches..."):
                    matches_response = get_suggested_matches(profile_response['email'])
                
                if matches_response:
                    st.markdown("---")
                    st.header("🎯 Your Suggested Matches")
                    
                    matches = matches_response.get("matches", [])
                    using_fallback = matches_response.get("using_fallback", False)
                    message = matches_response.get("message")
                    
                    if message:
                        if using_fallback:
                            st.info(message)
                        else:
                            st.warning(message)
                    
                    if matches:
                        st.markdown(
                            f"Found **{len(matches)}** matches out of "
                            f"**{matches_response.get('total_candidates', 0)}** profiles"
                        )
                        
                        # Store matches and trigger view
                        st.session_state.matches_list = matches
                        st.session_state.current_match_index = 0
                        st.session_state.viewing_matches = True
                        st.session_state.matches_loaded = True
                        st.session_state.current_profile = profile_response
                        
                        st.info("👆 Scroll down to view your matches!")
                        st.balloons()
                        st.rerun()
                    else:
                        st.info("📭 No matches found yet. Check back when more profiles are added!")
                        st.balloons()


def render_my_profile_section():
    """Renders the My Profile section for viewing and editing."""
    st.header("👤 My Profile")
    
    # Email input to load profile
    col1, col2 = st.columns([3, 1])
    
    with col1:
        email_input = st.text_input(
            "Enter your email to load your profile:",
            placeholder="your.email@example.com",
            key="profile_email_input"
        )
    
    with col2:
        st.markdown("<br>", unsafe_allow_html=True)  # Spacing
        load_btn = st.button("🔍 Load Profile", type="primary", use_container_width=True)
    
    if load_btn and email_input:
        with st.spinner("Loading profile..."):
            profile = get_profile_by_email(email_input)
        
        if profile:
            st.session_state.current_profile = profile
            st.success(f"✅ Profile loaded: {profile['name']}")
        else:
            st.error("❌ Profile not found. Please check the email address.")
            return
    
    # Display current profile if loaded
    if st.session_state.current_profile:
        profile = st.session_state.current_profile
        
        # Display profile summary
        st.markdown("---")
        st.subheader(f"📋 Profile: {profile['name']}")
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("Job Role", profile['job_role'])
        
        with col2:
            st.metric("Experience", f"{profile['years_exp']} years")
        
        with col3:
            st.metric("🏆 Points", profile.get('points', 0))
        
        with col4:
            connections_sent = profile.get('connections_sent', [])
            sent_count = len(connections_sent) if connections_sent else 0
            st.metric("📤 Sent", f"{sent_count}/5")
        
        # Show connections received metric (if > 0)
        connections_received = profile.get('connections_received', [])
        received_count = len(connections_received) if connections_received else 0
        
        if received_count > 0:
            st.metric("📥 Connections Received", received_count)
        
        # Contact & Social
        st.markdown("**📧 Contact & Social:**")
        contact_col1, contact_col2 = st.columns(2)
        
        with contact_col1:
            st.markdown(f"✉️ {profile['email']}")
            st.markdown(f"📱 {profile['phone']}")
        
        with contact_col2:
            if profile.get('linkedin'):
                st.markdown(f"🔗 [LinkedIn]({profile['linkedin']})")
            if profile.get('github'):
                st.markdown(f"💻 [GitHub]({profile['github']})")
        
        # Skills
        st.markdown("**💪 Can Contribute In:**")
        strength_tags_html = " ".join([
            f'<span style="background-color:#2ca02c;color:white;padding:4px 8px;'
            f'border-radius:4px;margin:2px;display:inline-block;font-size:12px;">{tag}</span>'
            for tag in profile['strength_tags']
        ])
        st.markdown(strength_tags_html, unsafe_allow_html=True)
        
        st.markdown("**📚 Wants to Learn:**")
        learn_tags_html = " ".join([
            f'<span style="background-color:#ff7f0e;color:white;padding:4px 8px;'
            f'border-radius:4px;margin:2px;display:inline-block;font-size:12px;">{tag}</span>'
            for tag in profile['learn_tags']
        ])
        st.markdown(learn_tags_html, unsafe_allow_html=True)
        
        # Display Connections Sent
        st.markdown("---")
        connections_sent = profile.get('connections_sent', [])
        sent_count = len(connections_sent) if connections_sent else 0
        
        if sent_count > 0:
            with st.expander(f"📤 Connections Sent ({sent_count}/5) - Click to view"):
                st.markdown("*These are profiles you've connected with. Click LinkedIn to reach out if you haven't yet.*")
                
                # Fetch details for each connected profile
                for user_id in connections_sent:
                    try:
                        connected_profile = get_profile_by_email(user_id)
                        if not connected_profile:
                            # Try with user_id directly
                            response = requests.get(f"{API_PROFILES_ENDPOINT}/{user_id}", timeout=10)
                            if response.status_code == 200:
                                connected_profile = response.json()
                        
                        if connected_profile:
                            col_a, col_b = st.columns([3, 1])
                            
                            with col_a:
                                st.markdown(f"**{connected_profile['name']}**")
                                st.caption(f"{connected_profile['job_role']} • {connected_profile['years_exp']} yrs")
                            
                            with col_b:
                                if connected_profile.get('linkedin'):
                                    st.link_button(
                                        "🔗 LinkedIn",
                                        connected_profile['linkedin'],
                                        use_container_width=True
                                    )
                            
                            st.markdown("---")
                    except:
                        pass
        else:
            st.info("📤 No connections sent yet. View matches to start connecting!")
        
        # Display Connections Received
        connections_received = profile.get('connections_received', [])
        received_count = len(connections_received) if connections_received else 0
        
        if received_count > 0:
            with st.expander(f"📥 Connections Received ({received_count}) - Click to view"):
                st.markdown("*These people showed interest in connecting with you!*")
                
                # Fetch details for each profile that connected
                for user_id in connections_received:
                    try:
                        connected_profile = get_profile_by_email(user_id)
                        if not connected_profile:
                            response = requests.get(f"{API_PROFILES_ENDPOINT}/{user_id}", timeout=10)
                            if response.status_code == 200:
                                connected_profile = response.json()
                        
                        if connected_profile:
                            col_a, col_b = st.columns([3, 1])
                            
                            with col_a:
                                st.markdown(f"**{connected_profile['name']}**")
                                st.caption(f"{connected_profile['job_role']} • {connected_profile['years_exp']} yrs")
                            
                            with col_b:
                                if connected_profile.get('linkedin'):
                                    st.link_button(
                                        "🔗 LinkedIn",
                                        connected_profile['linkedin'],
                                        use_container_width=True
                                    )
                            
                            st.markdown("---")
                    except:
                        pass
        
        # Action buttons
        st.markdown("---")
        action_col1, action_col2 = st.columns(2)
        
        with action_col1:
            if st.button("✏️ Edit Profile", type="primary", use_container_width=True):
                st.session_state.editing_profile = True
                st.session_state.viewing_matches = False
                st.rerun()
        
        with action_col2:
            if st.button("🎯 View My Matches", type="secondary", use_container_width=True):
                st.session_state.viewing_matches = True
                st.session_state.editing_profile = False
                st.session_state.matches_loaded = False
                st.rerun()
        
        # Show matches if viewing_matches is True
        if st.session_state.get('viewing_matches', False):
            st.markdown("---")
            
            # Load matches only once
            if not st.session_state.get('matches_loaded', False):
                with st.spinner("🔍 Finding your perfect matches..."):
                    matches_response = get_suggested_matches(profile['user_id'])
                
                if matches_response:
                    matches = matches_response.get("matches", [])
                    message = matches_response.get("message")
                    
                    st.session_state.matches_list = matches
                    st.session_state.matches_message = message
                    st.session_state.current_match_index = 0
                    st.session_state.matches_loaded = True
                else:
                    st.error("❌ Failed to load matches. Please try again.")
                    if st.button("🔙 Back to Profile"):
                        st.session_state.viewing_matches = False
                        st.rerun()
                    return
            
            # Display matches
            st.header("🎯 Your Suggested Matches")
            
            if st.session_state.get('matches_message'):
                st.info(st.session_state.matches_message)
            
            matches = st.session_state.get('matches_list', [])
            
            if matches:
                render_swipe_card_interface(matches, profile['user_id'])
            else:
                st.info("📭 No matches found yet.")
            
            # Back button
            if st.button("🔙 Back to Profile", use_container_width=True):
                st.session_state.viewing_matches = False
                st.session_state.matches_loaded = False
                st.rerun()
        
        # If editing mode, show the form
        elif st.session_state.editing_profile:
            st.markdown("---")
            render_profile_form(profile)
            
            if st.button("❌ Cancel Editing"):
                st.session_state.editing_profile = False
                st.rerun()
    else:
        st.info("👆 Enter your email above to load and manage your profile")


def main():
    """Main application function."""
    
    # Header
    st.title("QA Community Profile Matching")
    # st.markdown(
    #     "**For Experienced QA Professionals** - Share your expertise, mentor others, and expand your network. "
    #     "Connect with professionals who can learn from your experience or help you explore new areas."
    # )
    
    # Sidebar for navigation
    with st.sidebar:
        st.header("🧭 Navigation")
        page = st.radio(
            "Choose a page:",
            ["🏠 Create Profile", "👤 My Profile", "🏆 Leaderboard"],
            label_visibility="collapsed"
        )
        
        st.markdown("---")
        # st.caption(f"💡 **Tip:** Up to {DEFAULT_MATCH_LIMIT} matches will be shown")
    
    # Route to appropriate page
    # if page == "ℹ️ About":
    #     st.header("ℹ️ About This Platform")
        
    #     col1, col2 = st.columns([2, 1])
        
    #     with col1:
    #         st.markdown("""
    #         ### 🎯 Purpose
    #         This platform connects **experienced QA professionals** to share knowledge, mentor others, and expand their network.
            
    #         ### 🔍 How It Works
    #         1. **Share Your Expertise**: Create a profile highlighting your skills and experience
    #         2. **Get Matched**: Our algorithm connects you with professionals who can benefit from your knowledge
    #         3. **Connect via LinkedIn**: Click "Connect on LinkedIn" to reach out and start mentoring
    #         4. **Optional Learning**: Add learning goals if you want to explore new areas too
            
    #         ### 📊 Matching Algorithm
    #         We use an intelligent multi-factor scoring system:
    #         - **Skill Overlap** (Primary): Matches your strengths with others' learning needs
    #         - **Experience Level**: Prioritizes experienced professionals (higher weight)
    #         - **Breadth of Expertise**: Values professionals with diverse skill sets
    #         - **Role Similarity**: Connects people in related roles
            
    #         ### 🤝 For Experienced Professionals
    #         - **Mentorship Focus**: Help less experienced QAs grow
    #         - **Optional Learning**: Learning goals are optional - you can be here purely to help others
    #         - **Quick Connect**: One-click LinkedIn connection for easy networking
    #         - **Mobile-Friendly**: Access from anywhere, perfect for busy professionals
            
    #         ### 🔒 Privacy
    #         This is a professional community platform. LinkedIn profiles are shared to facilitate
    #         meaningful professional connections.
    #         """)
        
    #     with col2:
    #         st.info(f"**Platform Stats**\n\n🎯 Default Matches: {DEFAULT_MATCH_LIMIT}\n\n📚 Skills Available: 150+\n\n🔧 Categories: 12")
        
    # elif page == "📚 Skills Catalog":
    #     st.header("📚 Skills Catalog")
    #     st.markdown("Browse all available skills organized by category:")
        
    #     # Search functionality
    #     search_skill = st.text_input("🔍 Search skills:", placeholder="Type to search...")
        
    #     skills_by_cat = get_skills_by_category()
        
    #     if search_skill:
    #         st.markdown(f"**Search results for '{search_skill}':**")
    #         found_skills = []
    #         for category, skills in skills_by_cat.items():
    #             matching = [s for s in skills if search_skill.lower() in s.lower()]
    #             if matching:
    #                 found_skills.extend([(category, s) for s in matching])
            
    #         if found_skills:
    #             for category, skill in found_skills:
    #                 st.markdown(f"• **{skill}** _(from {category})_")
    #         else:
    #             st.warning("No skills found matching your search.")
    #     else:
    #         for category, skills in skills_by_cat.items():
    #             with st.expander(f"{category} ({len(skills)} skills)"):
    #                 cols = st.columns(3)
    #                 for idx, skill in enumerate(sorted(skills)):
    #                     cols[idx % 3].markdown(f"• {skill}")
    
    if page == "👤 My Profile":
        render_my_profile_section()
    
    elif page == "🏆 Leaderboard":
        render_leaderboard_page()
    
    else:  # 🏠 Create Profile page
        st.header("📝 Create Your Profile")
        render_profile_form()
        
        # Show matches if viewing_matches is True (after profile creation)
        if st.session_state.get('viewing_matches', False) and st.session_state.get('matches_list'):
            st.markdown("---")
            st.header("🎯 Your Matches")
            
            profile = st.session_state.get('current_profile')
            if profile:
                render_swipe_card_interface(st.session_state.matches_list, profile.get('user_id'))


if __name__ == "__main__":
    main()
