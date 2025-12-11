"""
UI Components for Give/Ask Form Sections

Provides reusable components for the Give and Ask form sections.
"""

import streamlit as st
from typing import List, Dict, Tuple


def render_checkbox_with_custom_input(
    label: str,
    options: List[str],
    placeholder: str,
    key_prefix: str,
    help_text: str = None
) -> Tuple[List[str], List[str]]:
    """
    Renders a checkbox group with a custom text input field.
    
    Args:
        label: Section label
        options: List of checkbox options
        placeholder: Placeholder for custom input
        key_prefix: Unique prefix for widget keys
        help_text: Optional help text
        
    Returns:
        Tuple of (selected_options, custom_items)
    """
    st.markdown(f"**{label}**")
    if help_text:
        st.caption(help_text)
    
    # Checkbox selections
    selected = []
    
    # Create columns for checkbox layout (2 per row on mobile, 3 on desktop)
    cols = st.columns(2)
    for idx, option in enumerate(options):
        with cols[idx % 2]:
            if st.checkbox(option, key=f"{key_prefix}_opt_{idx}"):
                selected.append(option)
    
    # Custom input field
    custom_text = st.text_input(
        "Add others (comma-separated)",
        placeholder=placeholder,
        key=f"{key_prefix}_custom",
        label_visibility="collapsed"
    )
    
    # Parse custom input
    custom_items = []
    if custom_text:
        custom_items = [item.strip() for item in custom_text.split(",") if item.strip()]
    
    return selected, custom_items


def render_company_input(
    label: str,
    placeholder: str,
    key: str
) -> List[str]:
    """
    Renders a text input for comma-separated company names.
    
    Args:
        label: Input label
        placeholder: Placeholder text
        key: Unique widget key
        
    Returns:
        List of company names
    """
    st.markdown(f"**{label}**")
    
    company_text = st.text_area(
        "Companies",
        placeholder=placeholder,
        key=key,
        height=80,
        label_visibility="collapsed"
    )
    
    companies = []
    if company_text:
        companies = [c.strip() for c in company_text.split(",") if c.strip()]
    
    return companies


def render_open_text_field(
    label: str,
    placeholder: str,
    key: str
) -> str:
    """
    Renders an open text field for free-form input.
    
    Args:
        label: Field label
        placeholder: Placeholder text
        key: Unique widget key
        
    Returns:
        Text input value
    """
    st.markdown(f"**{label}**")
    
    return st.text_area(
        "Open text",
        placeholder=placeholder,
        key=key,
        height=100,
        label_visibility="collapsed"
    )


def render_job_roles_input(
    label: str,
    options: List[str],
    placeholder: str,
    key_prefix: str
) -> Tuple[List[str], List[str]]:
    """
    Renders job roles selection with multiselect and custom input.
    
    Args:
        label: Section label
        options: List of job role options
        placeholder: Placeholder for custom input
        key_prefix: Unique prefix for widget keys
        
    Returns:
        Tuple of (selected_roles, custom_roles)
    """
    st.markdown(f"**{label}**")
    
    # Multiselect for predefined roles
    selected = st.multiselect(
        "Select roles",
        options,
        key=f"{key_prefix}_select",
        label_visibility="collapsed"
    )
    
    # Custom roles input
    custom_text = st.text_input(
        "Add custom roles (comma-separated)",
        placeholder=placeholder,
        key=f"{key_prefix}_custom",
        label_visibility="collapsed"
    )
    
    custom_items = []
    if custom_text:
        custom_items = [item.strip() for item in custom_text.split(",") if item.strip()]
    
    return selected, custom_items


def display_question_response_summary(
    label: str,
    selected: List[str],
    custom: List[str],
    icon: str = "✅"
) -> None:
    """
    Displays a summary of a question response.
    
    Args:
        label: Section label
        selected: Selected checkbox options
        custom: Custom text items
        icon: Icon to display
    """
    all_items = selected + custom
    
    if not all_items:
        return
    
    st.markdown(f"**{icon} {label}**")
    
    # Display as pills/tags
    tags_html = " ".join([
        f'<span style="background-color:#667eea;color:white;padding:4px 10px;'
        f'border-radius:15px;margin:2px;display:inline-block;font-size:12px;">{item}</span>'
        for item in all_items[:8]  # Limit display
    ])
    
    if len(all_items) > 8:
        tags_html += f' <span style="color:#666;font-size:12px;">+{len(all_items) - 8} more</span>'
    
    st.markdown(tags_html, unsafe_allow_html=True)


def display_companies_summary(
    label: str,
    companies: List[str],
    icon: str = "🏢"
) -> None:
    """
    Displays a summary of companies.
    
    Args:
        label: Section label
        companies: List of company names
        icon: Icon to display
    """
    if not companies:
        return
    
    st.markdown(f"**{icon} {label}**")
    st.write(", ".join(companies[:5]) + ("..." if len(companies) > 5 else ""))
