"""
Matching Algorithm for QA Community Platform v2

Implements Give/Ask matching where:
- My GIVE matches with Others' ASK
- My ASK matches with Others' GIVE

All sections have equal weights in the final score.
"""

from typing import List, Dict, Any, Tuple
from .models import Profile, GiveSection, AskSection, QuestionResponse
import logging

logger = logging.getLogger(__name__)


def normalize_text(text: str) -> str:
    """Normalize text for comparison (lowercase, stripped)."""
    return text.lower().strip()


def get_all_items(response: QuestionResponse) -> List[str]:
    """Get all items from a QuestionResponse (selected + custom), normalized."""
    items = response.selected + response.custom
    return [normalize_text(item) for item in items if item]


def calculate_list_overlap(list1: List[str], list2: List[str]) -> float:
    """
    Calculate overlap score between two lists.
    
    Uses a modified Jaccard approach where we measure how much of the 
    smaller list is covered by the larger list.
    
    Args:
        list1: First list of items
        list2: Second list of items
        
    Returns:
        float: Overlap score (0.0 to 1.0)
    """
    if not list1 or not list2:
        return 0.0
    
    # Normalize both lists
    set1 = set(normalize_text(item) for item in list1 if item)
    set2 = set(normalize_text(item) for item in list2 if item)
    
    if not set1 or not set2:
        return 0.0
    
    # Calculate overlap based on intersection vs minimum size
    intersection = len(set1 & set2)
    min_size = min(len(set1), len(set2))
    
    return intersection / min_size if min_size > 0 else 0.0


def calculate_company_similarity(give_companies: List[str], ask_companies: List[str]) -> float:
    """
    Calculate similarity between company lists using partial matching.
    
    Allows for partial matches (e.g., "Google" matches "Google India").
    This is important because users may write company names differently.
    
    Args:
        give_companies: Companies person can introduce to
        ask_companies: Companies person wants introduction to
        
    Returns:
        float: Similarity score (0.0 to 1.0)
    """
    if not give_companies or not ask_companies:
        return 0.0
    
    normalized_give = [normalize_text(c) for c in give_companies if c]
    normalized_ask = [normalize_text(c) for c in ask_companies if c]
    
    if not normalized_give or not normalized_ask:
        return 0.0
    
    matches = 0
    for ask_company in normalized_ask:
        for give_company in normalized_give:
            # Partial match: either contains the other
            if ask_company in give_company or give_company in ask_company:
                matches += 1
                break
    
    return matches / len(normalized_ask) if normalized_ask else 0.0


def calculate_question_match(give_response: QuestionResponse, ask_response: QuestionResponse) -> float:
    """
    Calculate match score between Give and Ask responses for a question.
    
    Args:
        give_response: What the person offers
        ask_response: What the other person needs
        
    Returns:
        float: Match score (0.0 to 1.0)
    """
    give_items = get_all_items(give_response)
    ask_items = get_all_items(ask_response)
    
    return calculate_list_overlap(give_items, ask_items)


def calculate_match_score(source: Profile, candidate: Profile) -> Dict[str, Any]:
    """
    Calculate comprehensive match score between source and candidate.
    
    Matching Logic:
    - Source's GIVE → Candidate's ASK (How source can help candidate)
    - Source's ASK → Candidate's GIVE (How candidate can help source)
    
    All sections have equal weights (20% each for 5 sections).
    Both directions (give_to_ask and ask_to_give) are averaged.
    
    Args:
        source: The user looking for matches
        candidate: A potential match
        
    Returns:
        dict: Detailed match information including scores and match reasons
    """
    # Skip if same profile
    if source.email == candidate.email:
        return {"total_score": 0.0, "is_valid": False}
    
    # Initialize section scores
    section_scores = {
        "companies": {"give_to_ask": 0.0, "ask_to_give": 0.0},
        "professional_activities": {"give_to_ask": 0.0, "ask_to_give": 0.0},
        "technical_areas": {"give_to_ask": 0.0, "ask_to_give": 0.0},
        "volunteering": {"give_to_ask": 0.0, "ask_to_give": 0.0},
        "job_roles": {"give_to_ask": 0.0, "ask_to_give": 0.0},
    }
    
    match_reasons = []
    
    # Q1: Companies
    # Source can introduce → Candidate wants introduction
    section_scores["companies"]["give_to_ask"] = calculate_company_similarity(
        source.give.companies, candidate.ask.companies
    )
    # Candidate can introduce → Source wants introduction
    section_scores["companies"]["ask_to_give"] = calculate_company_similarity(
        candidate.give.companies, source.ask.companies
    )
    if section_scores["companies"]["give_to_ask"] > 0:
        match_reasons.append("You can introduce them to companies they want")
    if section_scores["companies"]["ask_to_give"] > 0:
        match_reasons.append("They can introduce you to companies you want")
    
    # Q2: Professional Activities
    section_scores["professional_activities"]["give_to_ask"] = calculate_question_match(
        source.give.professional_activities, candidate.ask.professional_activities
    )
    section_scores["professional_activities"]["ask_to_give"] = calculate_question_match(
        candidate.give.professional_activities, source.ask.professional_activities
    )
    if section_scores["professional_activities"]["give_to_ask"] > 0:
        match_reasons.append("You can help with their professional activities")
    if section_scores["professional_activities"]["ask_to_give"] > 0:
        match_reasons.append("They can help with your professional activities")
    
    # Q3: Technical Areas
    section_scores["technical_areas"]["give_to_ask"] = calculate_question_match(
        source.give.technical_areas, candidate.ask.technical_areas
    )
    section_scores["technical_areas"]["ask_to_give"] = calculate_question_match(
        candidate.give.technical_areas, source.ask.technical_areas
    )
    if section_scores["technical_areas"]["give_to_ask"] > 0:
        match_reasons.append("You can train them in technical areas")
    if section_scores["technical_areas"]["ask_to_give"] > 0:
        match_reasons.append("They can train you in technical areas")
    
    # Q4: Volunteering
    section_scores["volunteering"]["give_to_ask"] = calculate_question_match(
        source.give.volunteering, candidate.ask.volunteering
    )
    section_scores["volunteering"]["ask_to_give"] = calculate_question_match(
        candidate.give.volunteering, source.ask.volunteering
    )
    if section_scores["volunteering"]["give_to_ask"] > 0:
        match_reasons.append("You can guide them in volunteering")
    if section_scores["volunteering"]["ask_to_give"] > 0:
        match_reasons.append("They can guide you in volunteering")
    
    # Q5: Job Roles
    section_scores["job_roles"]["give_to_ask"] = calculate_question_match(
        source.give.job_roles, candidate.ask.job_roles
    )
    section_scores["job_roles"]["ask_to_give"] = calculate_question_match(
        candidate.give.job_roles, source.ask.job_roles
    )
    if section_scores["job_roles"]["give_to_ask"] > 0:
        match_reasons.append("You have job openings matching their search")
    if section_scores["job_roles"]["ask_to_give"] > 0:
        match_reasons.append("They have job openings matching your search")
    
    # Calculate total score with equal weights (20% per section)
    section_weight = 0.2  # 5 sections, equal weight
    
    total_score = 0.0
    for section, scores in section_scores.items():
        # Average of bidirectional match for each section
        section_avg = (scores["give_to_ask"] + scores["ask_to_give"]) / 2
        total_score += section_avg * section_weight
    
    # Normalize to 0-100 scale
    total_score = round(total_score * 100, 2)
    
    return {
        "total_score": total_score,
        "section_scores": section_scores,
        "match_reasons": match_reasons,
        "is_valid": total_score > 0,
        "candidate_profile": candidate.to_dict()
    }


def get_top_matches(source: Profile, all_profiles: List[Profile], limit: int = 5) -> List[Dict[str, Any]]:
    """
    Get top matching profiles for a source user.
    
    Excludes:
    - The source user themselves
    - Already connected profiles (both sent and received connections)
    
    Args:
        source: The user looking for matches
        all_profiles: List of all profiles in the system
        limit: Maximum number of matches to return
        
    Returns:
        List of match results sorted by score (highest first)
    """
    matches = []
    
    # Calculate match score for each candidate
    for candidate in all_profiles:
        # Skip self
        if candidate.email == source.email:
            continue
        
        # Skip already connected profiles
        if candidate.user_id in source.connections_sent or candidate.user_id in source.connections_received:
            continue
        
        match_result = calculate_match_score(source, candidate)
        
        if match_result["is_valid"]:
            matches.append(match_result)
    
    # Sort by total score (descending)
    matches.sort(key=lambda x: x["total_score"], reverse=True)
    
    return matches[:limit]


def get_match_explanation(source: Profile, candidate: Profile) -> str:
    """
    Generate a human-readable explanation of why two profiles match.
    
    Args:
        source: The user looking for matches
        candidate: The matched profile
        
    Returns:
        str: Detailed explanation of the match
    """
    match_result = calculate_match_score(source, candidate)
    
    if not match_result["is_valid"]:
        return "No significant match found."
    
    explanation_parts = [
        f"Match Score: {match_result['total_score']}%",
        "",
        "Why this is a good match:",
    ]
    
    for reason in match_result["match_reasons"]:
        explanation_parts.append(f"  • {reason}")
    
    return "\n".join(explanation_parts)
