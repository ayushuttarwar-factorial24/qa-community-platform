"""
Shared utilities and components for the Streamlit app.
"""

from .components import (
    render_tags,
    render_checkbox_section,
    render_multiselect_section,
    render_company_input,
    get_all_items_from_section,
    validate_email,
    validate_linkedin_url,
    validate_phone,
    normalize_linkedin_url,
    COUNTRY_CODES
)

from .styles import apply_custom_styles

__all__ = [
    'render_tags',
    'render_checkbox_section',
    'render_multiselect_section',
    'render_company_input',
    'get_all_items_from_section',
    'validate_email',
    'validate_linkedin_url',
    'validate_phone',
    'normalize_linkedin_url',
    'COUNTRY_CODES',
    'apply_custom_styles'
]
