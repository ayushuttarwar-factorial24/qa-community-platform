"""
Reusable form components and utility functions.
"""

import streamlit as st
import re
from typing import Dict, List


# =============================================================================
# COUNTRY CODES FOR PHONE
# =============================================================================
COUNTRY_CODES = [
    "+1 (USA/Canada)",
    "+44 (UK)",
    "+91 (India)",
    "+61 (Australia)",
    "+49 (Germany)",
    "+33 (France)",
    "+81 (Japan)",
    "+86 (China)",
    "+65 (Singapore)",
    "+971 (UAE)",
    "+972 (Israel)",
    "+31 (Netherlands)",
    "+46 (Sweden)",
    "+47 (Norway)",
    "+48 (Poland)",
    "+55 (Brazil)",
    "+52 (Mexico)",
    "+27 (South Africa)",
    "+64 (New Zealand)",
    "+353 (Ireland)",
]


# =============================================================================
# VALIDATION FUNCTIONS
# =============================================================================

def validate_email(email: str) -> bool:
    """Validate email format."""
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return bool(re.match(pattern, email))


def validate_linkedin_url(url: str) -> bool:
    """Validate LinkedIn URL format."""
    if not url:
        return False
    patterns = [
        r'^https?://(www\.)?linkedin\.com/in/[a-zA-Z0-9\-_%]+/?$',
        r'^https?://(www\.)?linkedin\.com/pub/[a-zA-Z0-9\-_%/]+/?$',
        r'^linkedin\.com/in/[a-zA-Z0-9\-_%]+/?$',
    ]
    url_lower = url.lower().strip()
    if not url_lower.startswith('http'):
        url_lower = 'https://' + url_lower
    
    for pattern in patterns:
        if re.match(pattern, url_lower, re.IGNORECASE):
            return True
    return False


def validate_phone(phone: str) -> bool:
    """Validate phone number (basic check - just digits and length)."""
    if not phone:
        return True  # Optional field
    digits = re.sub(r'\D', '', phone)
    return 6 <= len(digits) <= 15


def normalize_linkedin_url(url: str) -> str:
    """Normalize LinkedIn URL to have https://."""
    if not url:
        return url
    url = url.strip()
    if not url.startswith('http'):
        url = 'https://' + url
    return url


# =============================================================================
# HELPER FUNCTIONS
# =============================================================================

def render_tags(items: List[str], color: str = "#667eea") -> None:
    """Render items as colored tags."""
    if not items:
        return
    tags_html = " ".join([
        f'<span style="background-color:{color};color:white;padding:4px 12px;'
        f'border-radius:15px;margin:2px;display:inline-block;font-size:12px;">{item}</span>'
        for item in items[:6]
    ])
    if len(items) > 6:
        tags_html += f' <span style="color:#666;">+{len(items) - 6} more</span>'
    st.markdown(tags_html, unsafe_allow_html=True)


def get_all_items_from_section(section: Dict, key: str) -> List[str]:
    """Get all items (selected + custom) from a Give/Ask section."""
    if not section:
        return []
    data = section.get(key, {})
    if isinstance(data, dict):
        return data.get('selected', []) + data.get('custom', [])
    return []


# =============================================================================
# FORM COMPONENTS
# =============================================================================

def render_checkbox_section(label: str, options: List[str], key_prefix: str, 
                           placeholder: str = "Add others (comma-separated)"):
    """Render checkbox options with custom input field."""
    st.markdown(f"**{label}**")
    
    selected = []
    cols = st.columns(2)
    for idx, option in enumerate(options):
        with cols[idx % 2]:
            if st.checkbox(option, key=f"{key_prefix}_{idx}"):
                selected.append(option)
    
    custom_text = st.text_input(
        "Custom",
        placeholder=placeholder,
        key=f"{key_prefix}_custom",
        label_visibility="collapsed"
    )
    custom = [x.strip() for x in custom_text.split(",") if x.strip()] if custom_text else []
    
    return {"selected": selected, "custom": custom}


def render_multiselect_section(label: str, options: List[str], key_prefix: str,
                               placeholder: str = "Add custom roles"):
    """Render multiselect with custom input."""
    st.markdown(f"**{label}**")
    
    selected = st.multiselect(
        "Select options",
        options,
        key=f"{key_prefix}_multi",
        label_visibility="collapsed"
    )
    
    custom_text = st.text_input(
        "Custom",
        placeholder=placeholder,
        key=f"{key_prefix}_custom",
        label_visibility="collapsed"
    )
    custom = [x.strip() for x in custom_text.split(",") if x.strip()] if custom_text else []
    
    return {"selected": selected, "custom": custom}


def render_company_input(label: str, placeholder: str, key: str) -> List[str]:
    """Render company input field."""
    st.markdown(f"**{label}**")
    text = st.text_area(
        "Companies",
        placeholder=placeholder,
        key=key,
        height=80,
        label_visibility="collapsed"
    )
    return [x.strip() for x in text.split(",") if x.strip()] if text else []
