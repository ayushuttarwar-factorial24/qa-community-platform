"""
Profile Service Module

Orchestrates profile-related business logic and coordinates between
repository and matching service layers.
"""

from typing import Optional, List
import logging

from app.models.profile import (
    ProfileCreateUpdate,
    ProfileInDB,
    ProfileResponse,
    MatchResponse,
    MatchResult,
    ProfileListResponse
)
from app.repo.profile_repo import ProfileRepository
from app.services.matching_service import MatchingService


logger = logging.getLogger(__name__)


class ProfileService:
    """
    Service class for profile business logic.
    
    Coordinates operations between the repository layer (data access)
    and other services (like matching).
    """
    
    def __init__(
        self,
        repository: ProfileRepository,
        matching_service: MatchingService
    ):
        """
        Initialize profile service with dependencies.
        
        Args:
            repository (ProfileRepository): Profile data repository
            matching_service (MatchingService): Matching algorithm service
        """
        self.repository = repository
        self.matching_service = matching_service
    
    async def create_or_update_profile(
        self,
        profile_data: ProfileCreateUpdate
    ) -> ProfileResponse:
        """
        Creates or updates a profile.
        
        Args:
            profile_data (ProfileCreateUpdate): Profile data to create/update
            
        Returns:
            ProfileResponse: The created or updated profile
            
        Raises:
            Exception: If operation fails
        """
        try:
            profile_in_db = await self.repository.create_or_update_profile(profile_data)
            return ProfileResponse(**profile_in_db.model_dump())
        except Exception as e:
            logger.error(f"Error in create_or_update_profile: {e}")
            raise
    
    async def get_profile(
        self,
        identifier: str
    ) -> Optional[ProfileResponse]:
        """
        Retrieves a profile by identifier.
        
        Args:
            identifier (str): user_id, email, or phone
            
        Returns:
            Optional[ProfileResponse]: Profile if found, None otherwise
        """
        try:
            profile_in_db = await self.repository.get_profile_by_identifier(identifier)
            
            if profile_in_db:
                return ProfileResponse(**profile_in_db.model_dump())
            
            return None
        except Exception as e:
            logger.error(f"Error in get_profile: {e}")
            return None
    
    async def list_all_profiles(self) -> ProfileListResponse:
        """
        Retrieves all profiles.
        
        Returns:
            ProfileListResponse: List of all profiles with count
        """
        try:
            profiles_in_db = await self.repository.list_all_profiles()
            
            profiles = [
                ProfileResponse(**p.model_dump())
                for p in profiles_in_db
            ]
            
            return ProfileListResponse(
                profiles=profiles,
                total=len(profiles)
            )
        except Exception as e:
            logger.error(f"Error in list_all_profiles: {e}")
            return ProfileListResponse(profiles=[], total=0)
    
    async def get_suggested_matches(
        self,
        identifier: str,
        limit: int = None,
        include_breakdown: bool = False
    ) -> Optional[MatchResponse]:
        """
        Gets suggested profile matches for a user.
        
        Excludes profiles that are already connected (both sent and received).
        
        Args:
            identifier (str): user_id, email, or phone of source user
            limit (int): Maximum number of matches to return
            include_breakdown (bool): Whether to include score breakdowns
            
        Returns:
            Optional[MatchResponse]: Match results if source profile found, None otherwise
        """
        try:
            # Get source profile
            source_profile = await self.repository.get_profile_by_identifier(identifier)
            
            if not source_profile:
                logger.warning(f"Source profile not found: {identifier}")
                return None
            
            # Get all other profiles
            all_candidate_profiles = await self.repository.list_other_profiles(identifier)
            
            if not all_candidate_profiles:
                logger.info("No other profiles available for matching")
                return MatchResponse(
                    source_user_id=source_profile.user_id,
                    matches=[],
                    total_candidates=0,
                    using_fallback=False,
                    message="No other profiles available yet. Be the first to connect!"
                )
            
            # Exclude already connected profiles (both sent and received)
            connections_sent = source_profile.connections_sent if hasattr(source_profile, 'connections_sent') else []
            connections_received = source_profile.connections_received if hasattr(source_profile, 'connections_received') else []
            excluded_ids = set(connections_sent + connections_received)
            
            candidate_profiles = [
                profile for profile in all_candidate_profiles
                if profile.user_id not in excluded_ids
            ]
            
            if not candidate_profiles:
                logger.info("No new profiles available (all already connected)")
                return MatchResponse(
                    source_user_id=source_profile.user_id,
                    matches=[],
                    total_candidates=len(all_candidate_profiles),
                    using_fallback=False,
                    message="You've already connected with all available profiles! Check back later for new members."
                )
            
            # Compute matches
            matches, using_fallback = self.matching_service.get_top_matches(
                source_profile,
                candidate_profiles,
                limit=limit,
                include_breakdown=include_breakdown
            )
            
            # Build response message
            message = None
            if using_fallback:
                message = (
                    "No direct skill matches found. Here are some nearby profiles "
                    "based on experience and expertise breadth."
                )
            elif not matches:
                message = "No suitable matches found at this time."
            
            return MatchResponse(
                source_user_id=source_profile.user_id,
                matches=matches,
                total_candidates=len(candidate_profiles),
                using_fallback=using_fallback,
                message=message
            )
            
        except Exception as e:
            logger.error(f"Error in get_suggested_matches: {e}")
            return None
    
    async def delete_profile(
        self,
        identifier: str
    ) -> bool:
        """
        Deletes a profile.
        
        Args:
            identifier (str): user_id, email, or phone
            
        Returns:
            bool: True if deleted, False otherwise
        """
        try:
            return await self.repository.delete_profile(identifier)
        except Exception as e:
            logger.error(f"Error in delete_profile: {e}")
            return False
    
    async def connect_profiles(
        self,
        initiator_id: str,
        target_id: str
    ) -> dict:
        """
        Connects two profiles and awards points.
        
        Rules:
        - Initiator gets 10 points, added to connections_sent
        - Target gets 20 points, added to connections_received
        - Can only connect once with same profile (prevent duplicates)
        - Maximum 5 outgoing connections (connections_sent limit)
        - Unlimited incoming connections (connections_received)
        
        Args:
            initiator_id: User ID of the one initiating connection
            target_id: User ID of the profile being connected to
            
        Returns:
            dict: Result with success status and message
        """
        try:
            # Fetch both profiles
            initiator = await self.repository.get_profile_by_identifier(initiator_id)
            target = await self.repository.get_profile_by_identifier(target_id)
            
            if not initiator:
                return {"success": False, "message": f"Initiator profile not found: {initiator_id}"}
            
            if not target:
                return {"success": False, "message": f"Target profile not found: {target_id}"}
            
            # Check if already connected (prevent duplicates)
            connections_sent = initiator.connections_sent if hasattr(initiator, 'connections_sent') else []
            if target.user_id in connections_sent:
                return {"success": False, "message": "Already connected with this profile"}
            
            # Check connection limit (only for outgoing connections)
            from app.config import settings
            max_connections = settings.max_connections_per_user
            if len(connections_sent) >= max_connections:
                return {"success": False, "message": f"Maximum {max_connections} outgoing connections limit reached"}
            
            # Award points and update connections
            await self.repository.award_points_and_connect(
                initiator_id=initiator.user_id,
                target_id=target.user_id,
                initiator_points=10,
                target_points=20
            )
            
            logger.info(
                f"Connection made: {initiator.user_id} -> {target.user_id}. "
                f"Points awarded: initiator +10, target +20"
            )
            
            return {
                "success": True,
                "message": "Connection successful",
                "initiator_points": initiator.points + 10,
                "target_points": target.points + 20
            }
            
        except Exception as e:
            logger.error(f"Error in connect_profiles: {e}")
            return {"success": False, "message": str(e)}


    async def get_leaderboard(self, limit: int = 100) -> ProfileListResponse:
        """
        Get leaderboard rankings sorted by points.
        
        Args:
            limit: Maximum number of profiles to return
            
        Returns:
            ProfileListResponse: Top profiles by points
        """
        try:
            profiles = await self.repository.get_leaderboard(limit)
            
            return ProfileListResponse(
                profiles=[ProfileResponse(**p.model_dump()) for p in profiles],
                total=len(profiles)
            )
            
        except Exception as e:
            logger.error(f"Error in get_leaderboard: {e}")
            return ProfileListResponse(profiles=[], total=0)



def get_profile_service(
    repository: ProfileRepository,
    matching_service: MatchingService
) -> ProfileService:
    """
    Factory function for creating ProfileService instance.
    
    Args:
        repository (ProfileRepository): Profile repository instance
        matching_service (MatchingService): Matching service instance
        
    Returns:
        ProfileService: Configured profile service
    """
    return ProfileService(repository, matching_service)
