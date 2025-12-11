"""
Profile Operations Module for QA Community Platform v2

Contains all database operations for profiles:
- CRUD operations (Create, Read, Update, Delete)
- Connection management
- Leaderboard queries
- Match suggestions

Uses the new Give/Ask data model.
"""

import streamlit as st
from datetime import datetime
from typing import Dict, List, Optional, Any
import uuid
import logging

from .database import get_profiles_collection
from .models import Profile, GiveSection, AskSection, QuestionResponse
from .constants import MAX_CONNECTIONS_PER_USER, DEFAULT_MATCH_LIMIT
from .matching import get_top_matches, calculate_match_score

logger = logging.getLogger(__name__)


def generate_user_id() -> str:
    """Generate a unique user ID."""
    return str(uuid.uuid4())


def dict_to_profile(data: Dict) -> Profile:
    """
    Convert a MongoDB document to a Profile object.
    
    Args:
        data: MongoDB document dict
        
    Returns:
        Profile object
    """
    if data is None:
        return None
    
    return Profile.from_dict(data)


def create_or_update_profile(profile_data: Dict[str, Any]) -> Optional[Dict]:
    """
    Creates a new profile or updates existing one (upsert by email).
    
    Handles the new Give/Ask data structure.
    
    Args:
        profile_data: Profile information including give/ask sections
        
    Returns:
        Created/updated profile dict or None on error
    """
    try:
        collection = get_profiles_collection()
        email = profile_data.get('email', '').lower().strip()
        
        if not email:
            logger.error("Email is required")
            return None
        
        # Check if profile exists
        existing = collection.find_one({"email": email})
        
        now = datetime.utcnow()
        
        if existing:
            # Update existing profile - preserve connections and points
            update_data = {
                "full_name": profile_data.get('full_name'),
                "phone": profile_data.get('phone', ''),
                "linkedin_url": profile_data.get('linkedin_url'),
                "current_company": profile_data.get('current_company', ''),
                "experience": profile_data.get('experience'),
                "current_role": profile_data.get('current_role'),
                "custom_role": profile_data.get('custom_role', ''),
                "give": profile_data.get('give', {}),
                "ask": profile_data.get('ask', {}),
                "updated_at": now
            }
            
            collection.update_one(
                {"email": email},
                {"$set": update_data}
            )
            
            # Return updated profile
            updated = collection.find_one({"email": email})
            if updated:
                updated['_id'] = str(updated['_id'])
            return updated
        else:
            # Create new profile
            new_profile = {
                "user_id": generate_user_id(),
                "full_name": profile_data.get('full_name'),
                "email": email,
                "phone": profile_data.get('phone', ''),
                "linkedin_url": profile_data.get('linkedin_url'),
                "current_company": profile_data.get('current_company', ''),
                "experience": profile_data.get('experience'),
                "current_role": profile_data.get('current_role'),
                "custom_role": profile_data.get('custom_role', ''),
                "give": profile_data.get('give', {
                    "companies": [],
                    "professional_activities": {"selected": [], "custom": []},
                    "technical_areas": {"selected": [], "custom": []},
                    "volunteering": {"selected": [], "custom": []},
                    "job_roles": {"selected": [], "custom": []},
                    "open_contribution": ""
                }),
                "ask": profile_data.get('ask', {
                    "companies": [],
                    "professional_activities": {"selected": [], "custom": []},
                    "technical_areas": {"selected": [], "custom": []},
                    "volunteering": {"selected": [], "custom": []},
                    "job_roles": {"selected": [], "custom": []},
                    "open_request": ""
                }),
                "points": 0,
                "connections_sent": [],
                "connections_received": [],
                "created_at": now,
                "updated_at": now
            }
            
            result = collection.insert_one(new_profile)
            new_profile['_id'] = str(result.inserted_id)
            
            logger.info(f"Created new profile: {email}")
            return new_profile
            
    except Exception as e:
        logger.error(f"Error in create_or_update_profile: {e}")
        return None


def get_profile_by_identifier(identifier: str) -> Optional[Dict]:
    """
    Fetches a profile by user_id, email, or phone.
    
    Args:
        identifier: user_id, email, or phone
        
    Returns:
        Profile dict or None
    """
    try:
        collection = get_profiles_collection()
        
        # Try different identifiers
        profile = collection.find_one({
            "$or": [
                {"user_id": identifier},
                {"email": identifier.lower()},
                {"phone": identifier}
            ]
        })
        
        if profile:
            profile['_id'] = str(profile['_id'])
            return profile
        
        return None
        
    except Exception as e:
        logger.error(f"Error in get_profile_by_identifier: {e}")
        return None


def get_all_profiles() -> List[Dict]:
    """
    Get all profiles from the database.
    
    Returns:
        List of profile dicts
    """
    try:
        collection = get_profiles_collection()
        
        profiles = list(collection.find())
        
        for profile in profiles:
            profile['_id'] = str(profile['_id'])
        
        return profiles
        
    except Exception as e:
        logger.error(f"Error in get_all_profiles: {e}")
        return []


def get_all_profiles_except(exclude_user_id: str) -> List[Dict]:
    """
    Get all profiles except the specified one.
    
    Args:
        exclude_user_id: User ID to exclude
        
    Returns:
        List of profile dicts
    """
    try:
        collection = get_profiles_collection()
        
        profiles = list(collection.find(
            {"user_id": {"$ne": exclude_user_id}}
        ))
        
        for profile in profiles:
            profile['_id'] = str(profile['_id'])
        
        return profiles
        
    except Exception as e:
        logger.error(f"Error in get_all_profiles_except: {e}")
        return []


def get_suggested_matches(identifier: str, limit: int = DEFAULT_MATCH_LIMIT) -> List[Dict]:
    """
    Get suggested matches for a user based on Give/Ask matching.
    
    Args:
        identifier: Email or user_id of the user
        limit: Maximum matches to return
        
    Returns:
        List of match results with scores and reasons
    """
    try:
        # Get the source profile
        source_dict = get_profile_by_identifier(identifier)
        if not source_dict:
            logger.error(f"Source profile not found: {identifier}")
            return []
        
        source = Profile.from_dict(source_dict)
        
        # Get all other profiles
        all_profiles_dict = get_all_profiles_except(source.user_id)
        all_profiles = [Profile.from_dict(p) for p in all_profiles_dict]
        
        # Get matches using the matching algorithm
        matches = get_top_matches(source, all_profiles, limit)
        
        return matches
        
    except Exception as e:
        logger.error(f"Error in get_suggested_matches: {e}")
        return []


def connect_profiles(initiator_id: str, target_id: str) -> Dict:
    """
    Connects two profiles and awards points.
    
    Rules:
    - Initiator gets 10 points, added to connections_sent
    - Target gets 20 points, added to connections_received
    - Can only connect once with same profile
    - Maximum 5 outgoing connections (connections_sent limit)
    
    Args:
        initiator_id: User ID of the one initiating connection
        target_id: User ID of the profile being connected to
        
    Returns:
        dict: Result with success status and message
    """
    try:
        collection = get_profiles_collection()
        
        # Fetch both profiles
        initiator = collection.find_one({"user_id": initiator_id})
        target = collection.find_one({"user_id": target_id})
        
        if not initiator:
            return {"success": False, "message": f"Initiator profile not found: {initiator_id}"}
        
        if not target:
            return {"success": False, "message": f"Target profile not found: {target_id}"}
        
        # Check if already connected
        connections_sent = initiator.get('connections_sent', [])
        if target_id in connections_sent:
            return {"success": False, "message": "Already connected with this profile"}
        
        # Check connection limit (only for outgoing connections)
        if len(connections_sent) >= MAX_CONNECTIONS_PER_USER:
            return {"success": False, "message": f"Maximum {MAX_CONNECTIONS_PER_USER} outgoing connections limit reached"}
        
        # Update initiator: add points, add to connections_sent
        collection.update_one(
            {"user_id": initiator_id},
            {
                "$inc": {"points": 10},
                "$addToSet": {"connections_sent": target_id}
            }
        )
        
        # Update target: add points, add to connections_received
        collection.update_one(
            {"user_id": target_id},
            {
                "$inc": {"points": 20},
                "$addToSet": {"connections_received": initiator_id}
            }
        )
        
        # Clear leaderboard cache since points changed
        clear_leaderboard_cache()
        
        logger.info(f"Connection made: {initiator_id} -> {target_id}")
        
        return {
            "success": True,
            "message": "Connection successful",
            "initiator_points": initiator.get('points', 0) + 10,
            "target_points": target.get('points', 0) + 20,
            "linkedin_url": target.get('linkedin_url', '')
        }
        
    except Exception as e:
        logger.error(f"Error in connect_profiles: {e}")
        return {"success": False, "message": str(e)}


@st.cache_data(ttl=300)  # Cache for 5 minutes
def get_leaderboard(limit: int = 100) -> Dict:
    """
    Get leaderboard rankings sorted by points.
    
    Cached for 5 minutes to reduce database load.
    
    Args:
        limit: Maximum number of profiles to return
        
    Returns:
        dict with profiles list and total count
    """
    try:
        collection = get_profiles_collection()
        
        profiles = list(collection.find().sort("points", -1).limit(limit))
        
        for profile in profiles:
            profile['_id'] = str(profile['_id'])
        
        return {
            "profiles": profiles,
            "total": len(profiles)
        }
        
    except Exception as e:
        logger.error(f"Error in get_leaderboard: {e}")
        return {"profiles": [], "total": 0}


def clear_leaderboard_cache():
    """Clear the leaderboard cache (call after connections)."""
    get_leaderboard.clear()


def get_connection_profiles(user_id: str, connection_type: str = "sent") -> List[Dict]:
    """
    Get profiles of connections.
    
    Args:
        user_id: The user's ID
        connection_type: "sent" or "received"
        
    Returns:
        List of connected profile dicts
    """
    try:
        collection = get_profiles_collection()
        
        # Get the user's profile
        user = collection.find_one({"user_id": user_id})
        if not user:
            return []
        
        # Get the connection list based on type
        if connection_type == "sent":
            connection_ids = user.get('connections_sent', [])
        else:
            connection_ids = user.get('connections_received', [])
        
        if not connection_ids:
            return []
        
        # Fetch all connected profiles
        profiles = list(collection.find({"user_id": {"$in": connection_ids}}))
        
        for profile in profiles:
            profile['_id'] = str(profile['_id'])
        
        return profiles
        
    except Exception as e:
        logger.error(f"Error in get_connection_profiles: {e}")
        return []


def delete_profile(email: str) -> bool:
    """
    Delete a profile by email (for admin/testing purposes).
    
    Args:
        email: Email of the profile to delete
        
    Returns:
        True if deleted, False otherwise
    """
    try:
        collection = get_profiles_collection()
        
        result = collection.delete_one({"email": email.lower()})
        
        if result.deleted_count > 0:
            logger.info(f"Deleted profile: {email}")
            return True
        
        return False
        
    except Exception as e:
        logger.error(f"Error in delete_profile: {e}")
        return False
