"""
Profile Router Module

Defines FastAPI routes for profile-related operations.
Handles HTTP requests and responses for the profile matching API.
"""

from fastapi import APIRouter, HTTPException, status, Query, Depends
from typing import Optional
import logging

from app.models.profile import (
    ProfileCreateUpdate,
    ProfileResponse,
    MatchResponse,
    ProfileListResponse
)
from app.services.profile_service import ProfileService, get_profile_service
from app.services.matching_service import get_matching_service
from app.repo.profile_repo import get_profile_repository


logger = logging.getLogger(__name__)

# Create router
router = APIRouter(
    prefix="/api/v1/profiles",
    tags=["profiles"],
    responses={404: {"description": "Profile not found"}},
)


async def get_service() -> ProfileService:
    """
    Dependency that provides configured ProfileService instance.
    
    Returns:
        ProfileService: Configured service with dependencies
    """
    repository = await get_profile_repository()
    matching_svc = get_matching_service()
    return get_profile_service(repository, matching_svc)


@router.post(
    "/",
    response_model=ProfileResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create or update a profile",
    description=(
        "Creates a new profile or updates an existing one (upsert by email). "
        "Returns the complete profile with generated user_id and timestamps."
    )
)
async def create_or_update_profile(
    profile_data: ProfileCreateUpdate,
    service: ProfileService = Depends(get_service)
) -> ProfileResponse:
    """
    Create or update a profile.
    
    If a profile with the same email exists, all fields are updated.
    Otherwise, a new profile is created with a generated user_id.
    
    **Validation Rules:**
    - Minimum 3 skills in both strength_tags and learn_tags
    - Valid email format
    - Years of experience: 0-50
    - Phone number: 10-15 characters
    
    **Returns:**
    - 201: Profile created/updated successfully
    - 422: Validation error
    """
    try:
        profile = await service.create_or_update_profile(profile_data)
        logger.info(f"Profile created/updated: {profile.user_id}")
        return profile
    except Exception as e:
        logger.error(f"Error creating/updating profile: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to create/update profile"
        )

@router.get(
    "/leaderboard",
    response_model=ProfileListResponse,
    summary="Get leaderboard rankings",
    description="Returns profiles sorted by points (highest first)."
)
async def get_leaderboard(
    limit: int = Query(default=100, ge=1, le=500, description="Maximum profiles to return"),
    service: ProfileService = Depends(get_service)
):
    """
    Get leaderboard rankings.
    
    **Returns:**
    - 200: List of profiles sorted by points
    """
    return await service.get_leaderboard(limit)


@router.get(
    "/{identifier}",
    response_model=ProfileResponse,
    summary="Get a profile by identifier",
    description=(
        "Retrieves a profile by user_id, email, or phone number. "
        "The identifier is matched against all three fields."
    )
)
async def get_profile(
    identifier: str,
    service: ProfileService = Depends(get_service)
) -> ProfileResponse:
    """
    Get a profile by identifier.
    
    The identifier can be:
    - user_id (UUID)
    - email address
    - phone number
    
    **Returns:**
    - 200: Profile found and returned
    - 404: Profile not found
    """
    profile = await service.get_profile(identifier)
    
    if not profile:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Profile not found: {identifier}"
        )
    
    return profile


@router.get(
    "/{identifier}/suggested",
    response_model=MatchResponse,
    summary="Get suggested profile matches",
    description=(
        "Returns top N profile suggestions based on skill alignment, "
        "experience, and role similarity. Uses fallback strategy if no "
        "direct skill overlaps are found."
    )
)
async def get_suggested_profiles(
    identifier: str,
    limit: int = Query(
        default=5,
        ge=1,
        le=20,
        description="Maximum number of suggestions to return"
    ),
    include_breakdown: bool = Query(
        default=False,
        description="Include detailed score breakdown for each match"
    ),
    service: ProfileService = Depends(get_service)
) -> MatchResponse:
    """
    Get suggested profile matches for a user.
    
    **Matching Algorithm:**
    1. Primary: Overlap between learner's goals and candidate's strengths
    2. Experience: Years of experience (weighted)
    3. Breadth: Number of skills candidate possesses
    4. Role Similarity: Job role alignment
    
    **Fallback Strategy:**
    If no direct skill overlaps exist, suggestions are based on:
    - Experience level
    - Breadth of skills
    - Shared learning interests
    
    **Parameters:**
    - identifier: user_id, email, or phone of the source user
    - limit: Number of matches to return (1-20, default 5)
    - include_breakdown: Include score components in response
    
    **Returns:**
    - 200: Match results returned
    - 404: Source profile not found
    """
    match_response = await service.get_suggested_matches(
        identifier,
        limit=limit,
        include_breakdown=include_breakdown
    )
    
    if not match_response:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Source profile not found: {identifier}"
        )
    
    return match_response


@router.get(
    "/",
    response_model=ProfileListResponse,
    summary="List all profiles",
    description=(
        "Returns all profiles in the system. "
        "Intended for admin/debug purposes."
    )
)
async def list_all_profiles(
    service: ProfileService = Depends(get_service)
) -> ProfileListResponse:
    """
    List all profiles.
    
    Returns complete list of all profiles with total count.
    Useful for admin dashboards and debugging.
    
    **Returns:**
    - 200: List of all profiles
    """
    return await service.list_all_profiles()


@router.delete(
    "/{identifier}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete a profile",
    description="Deletes a profile by user_id, email, or phone number."
)
async def delete_profile(
    identifier: str,
    service: ProfileService = Depends(get_service)
):
    """
    Delete a profile.
    
    **Returns:**
    - 204: Profile deleted successfully
    - 404: Profile not found
    """
    deleted = await service.delete_profile(identifier)
    
    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Profile not found: {identifier}"
        )
    
    return None


@router.post(
    "/{initiator_id}/connect/{target_id}",
    response_model=dict,
    status_code=status.HTTP_200_OK,
    summary="Connect with another profile",
    description=(
        "Records a connection between two users. "
        "Initiator gets 10 points, target gets 20 points. "
        "Limited to 5 connections per user."
    )
)
async def connect_profiles(
    initiator_id: str,
    target_id: str,
    service: ProfileService = Depends(get_service)
):
    """
    Connect two profiles and award points.
    
    **Rules:**
    - Initiator gets 10 points
    - Target gets 20 points
    - Can only connect once with same profile
    - Maximum 5 connections per user
    
    **Returns:**
    - 200: Connection successful with points awarded
    - 400: Already connected or limit reached
    - 404: Profile not found
    """
    result = await service.connect_profiles(initiator_id, target_id)
    
    if not result["success"]:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=result["message"]
        )
    
    return result
