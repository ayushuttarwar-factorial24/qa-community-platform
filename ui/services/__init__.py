"""
UI Services Package for QA Community Platform v2

Provides direct database access and business logic for Streamlit.
Uses Give/Ask matching model.
"""

from .constants import (
    DATABASE_NAME,
    PROFILES_COLLECTION,
    DEFAULT_MATCH_LIMIT,
    MAX_CONNECTIONS_PER_USER,
    EXPERIENCE_OPTIONS,
    ROLE_OPTIONS,
    PROFESSIONAL_ACTIVITIES,
    TECHNICAL_AREAS,
    VOLUNTEERING_ACTIVITIES,
    JOB_ROLES,
    GIVE_LABELS,
    ASK_LABELS,
    GIVE_PLACEHOLDERS,
    ASK_PLACEHOLDERS
)

from .models import (
    QuestionResponse,
    GiveSection,
    AskSection,
    Profile
)

from .database import (
    get_mongo_client,
    get_database,
    get_profiles_collection
)

from .profile_ops import (
    create_or_update_profile,
    get_profile_by_identifier,
    get_all_profiles,
    get_all_profiles_except,
    get_suggested_matches,
    connect_profiles,
    get_leaderboard,
    clear_leaderboard_cache,
    get_connection_profiles,
    delete_profile
)

from .matching import (
    calculate_match_score,
    get_top_matches,
    get_match_explanation
)

__all__ = [
    # Constants
    'DATABASE_NAME',
    'PROFILES_COLLECTION',
    'DEFAULT_MATCH_LIMIT',
    'MAX_CONNECTIONS_PER_USER',
    'EXPERIENCE_OPTIONS',
    'ROLE_OPTIONS',
    'PROFESSIONAL_ACTIVITIES',
    'TECHNICAL_AREAS',
    'VOLUNTEERING_ACTIVITIES',
    'JOB_ROLES',
    'GIVE_LABELS',
    'ASK_LABELS',
    'GIVE_PLACEHOLDERS',
    'ASK_PLACEHOLDERS',
    # Models
    'QuestionResponse',
    'GiveSection',
    'AskSection',
    'Profile',
    # Database
    'get_mongo_client',
    'get_database',
    'get_profiles_collection',
    # Profile Operations
    'create_or_update_profile',
    'get_profile_by_identifier',
    'get_all_profiles',
    'get_all_profiles_except',
    'get_suggested_matches',
    'connect_profiles',
    'get_leaderboard',
    'clear_leaderboard_cache',
    'get_connection_profiles',
    'delete_profile',
    # Matching
    'calculate_match_score',
    'get_top_matches',
    'get_match_explanation'
]
