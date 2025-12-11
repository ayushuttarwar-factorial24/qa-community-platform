"""
Matching Service Module

Implements the core matching algorithm for profile suggestions.
Computes match scores based on skill overlap, experience, breadth, and role similarity.
"""

from typing import List, Tuple, Set
import logging

from app.models.profile import ProfileInDB, MatchResult, ProfileResponse
from app.utils.role_normalizer import calculate_role_similarity
from app.config import settings


logger = logging.getLogger(__name__)


class MatchingService:
    """
    Service class for profile matching operations.
    
    Implements the scoring algorithm that combines:
    - Skill overlap (primary factor)
    - Breadth of candidate's skills
    - Years of experience
    - Job role similarity
    """
    
    def __init__(self):
        """Initialize matching service with configuration."""
        self.overlap_weight = settings.overlap_weight
        self.breadth_weight = settings.breadth_weight
        self.experience_weight = settings.experience_weight
        self.max_experience_cap = settings.max_experience_cap
        self.max_breadth_cap = settings.max_breadth_cap
    
    def compute_match_score(
        self,
        source_profile: ProfileInDB,
        candidate_profile: ProfileInDB,
        include_breakdown: bool = False
    ) -> Tuple[float, List[str], dict]:
        """
        Computes match score between source and candidate profiles.
        
        Formula:
        - base_score = overlap_count (skills learner wants that candidate has)
        - breadth_bonus = min(candidate_strength_count, 10) / 10.0
        - exp_bonus = min(candidate_years_exp, 10) / 10.0
        - role_bonus = similarity score (0.0, 0.2, or 0.5)
        - total_score = (base_score × 2.0) + (breadth_bonus × 0.3) + 
                        (exp_bonus × 1.5) + role_bonus
        
        Args:
            source_profile (ProfileInDB): The profile requesting suggestions
            candidate_profile (ProfileInDB): A candidate profile to evaluate
            include_breakdown (bool): Whether to return detailed score breakdown
            
        Returns:
            Tuple[float, List[str], dict]: 
                - Total score
                - List of overlapping tags
                - Score breakdown dict (if include_breakdown=True)
        """
        # Convert to sets for efficient intersection
        # Handle optional learn_tags (empty list if user doesn't want to learn)
        learn_set: Set[str] = {tag.lower() for tag in (source_profile.learn_tags or [])}
        strength_set: Set[str] = {tag.lower() for tag in candidate_profile.strength_tags}
        
        # Calculate overlap
        overlap_set = learn_set & strength_set
        overlap_count = len(overlap_set)
        
        # Get original-case overlap tags for display
        overlap_tags = [
            tag for tag in candidate_profile.strength_tags
            if tag.lower() in overlap_set
        ]
        
        # If no overlap, return zero score
        if overlap_count == 0:
            breakdown = {
                "overlap_score": 0.0,
                "breadth_score": 0.0,
                "experience_score": 0.0,
                "role_score": 0.0,
                "total_score": 0.0
            } if include_breakdown else {}
            return 0.0, [], breakdown
        
        # Calculate base score from overlap
        base_score = float(overlap_count)
        overlap_score = base_score * self.overlap_weight
        
        # Calculate breadth bonus (capped at max_breadth_cap)
        strength_size = len(candidate_profile.strength_tags)
        breadth_normalized = min(strength_size, self.max_breadth_cap) / self.max_breadth_cap
        breadth_score = breadth_normalized * self.breadth_weight
        
        # Calculate experience bonus (capped at max_experience_cap)
        exp_normalized = min(candidate_profile.years_exp, self.max_experience_cap) / self.max_experience_cap
        experience_score = exp_normalized * self.experience_weight
        
        # Calculate role similarity bonus
        role_score = calculate_role_similarity(
            source_profile.job_role,
            candidate_profile.job_role
        )
        
        # Total score
        total_score = overlap_score + breadth_score + experience_score + role_score
        
        # Build breakdown if requested
        breakdown = {}
        if include_breakdown:
            breakdown = {
                "overlap_score": round(overlap_score, 2),
                "breadth_score": round(breadth_score, 2),
                "experience_score": round(experience_score, 2),
                "role_score": round(role_score, 2),
                "total_score": round(total_score, 2)
            }
        
        return total_score, overlap_tags, breakdown
    
    def compute_fallback_score(
        self,
        source_profile: ProfileInDB,
        candidate_profile: ProfileInDB
    ) -> float:
        """
        Computes fallback score when no direct skill overlap exists.
        
        Fallback strategy prioritizes:
        1. Years of experience (most important)
        2. Breadth of candidate's skills
        3. Shared learning interests
        
        Formula:
        fallback_score = (2 × years_exp) + len(strength_tags) + len(shared_learn_tags)
        
        Args:
            source_profile (ProfileInDB): The profile requesting suggestions
            candidate_profile (ProfileInDB): A candidate profile to evaluate
            
        Returns:
            float: Fallback score
        """
        # Experience factor (doubled for importance)
        exp_score = 2.0 * candidate_profile.years_exp
        
        # Breadth of skills
        breadth_score = float(len(candidate_profile.strength_tags))
        
        # Shared learning interests (handle optional learn_tags)
        source_learn_set = {tag.lower() for tag in (source_profile.learn_tags or [])}
        candidate_learn_set = {tag.lower() for tag in (candidate_profile.learn_tags or [])}
        shared_learn = len(source_learn_set & candidate_learn_set)
        
        fallback_score = exp_score + breadth_score + float(shared_learn)
        
        return fallback_score
    
    def get_top_matches(
        self,
        source_profile: ProfileInDB,
        candidate_profiles: List[ProfileInDB],
        limit: int = None,
        include_breakdown: bool = False
    ) -> Tuple[List[MatchResult], bool]:
        """
        Finds and returns top N matching profiles.
        
        Process:
        1. Compute match score for each candidate
        2. If at least one candidate has overlap > 0, use normal scoring
        3. Otherwise, use fallback scoring strategy
        4. Sort by score (descending) and return top N
        
        Args:
            source_profile (ProfileInDB): The profile requesting suggestions
            candidate_profiles (List[ProfileInDB]): List of candidate profiles
            limit (int): Maximum number of matches to return (default from config)
            include_breakdown (bool): Whether to include score breakdowns
            
        Returns:
            Tuple[List[MatchResult], bool]: 
                - List of match results (top N)
                - Boolean indicating if fallback was used
        """
        if limit is None:
            limit = settings.default_match_limit
        
        if not candidate_profiles:
            return [], False
        
        # Compute scores for all candidates
        scored_candidates = []
        has_any_overlap = False
        
        for candidate in candidate_profiles:
            score, overlap_tags, breakdown = self.compute_match_score(
                source_profile,
                candidate,
                include_breakdown=include_breakdown
            )
            
            if score > 0:
                has_any_overlap = True
            
            scored_candidates.append({
                "profile": candidate,
                "score": score,
                "overlap_tags": overlap_tags,
                "breakdown": breakdown
            })
        
        # Determine if we need fallback
        using_fallback = not has_any_overlap
        
        if using_fallback:
            # Recompute using fallback scoring
            logger.info("No overlaps found, using fallback scoring")
            
            for item in scored_candidates:
                fallback_score = self.compute_fallback_score(
                    source_profile,
                    item["profile"]
                )
                item["score"] = fallback_score
                item["overlap_tags"] = []  # No overlaps in fallback
        
        # Sort by score (descending)
        scored_candidates.sort(key=lambda x: x["score"], reverse=True)
        
        # Take top N
        top_candidates = scored_candidates[:limit]
        
        # Convert to MatchResult objects
        match_results = []
        for item in top_candidates:
            match_result = MatchResult(
                profile=ProfileResponse(**item["profile"].model_dump()),
                score=round(item["score"], 2),
                overlap_tags=item["overlap_tags"],
                is_fallback=using_fallback,
                score_breakdown=item.get("breakdown") if include_breakdown else None
            )
            match_results.append(match_result)
        
        logger.info(
            f"Generated {len(match_results)} matches for user {source_profile.user_id} "
            f"(fallback: {using_fallback})"
        )
        
        return match_results, using_fallback


# Global service instance
matching_service = MatchingService()


def get_matching_service() -> MatchingService:
    """
    Dependency injection function for FastAPI.
    
    Returns:
        MatchingService: The global matching service instance
    """
    return matching_service
