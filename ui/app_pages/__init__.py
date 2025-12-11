"""
Pages module for the Streamlit app.
"""

from .home import render_home_page
from .create_profile import render_create_profile_page
from .my_profile import render_my_profile_page
from .leaderboard import render_leaderboard_page

__all__ = [
    'render_home_page',
    'render_create_profile_page',
    'render_my_profile_page',
    'render_leaderboard_page'
]
