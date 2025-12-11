"""
Role Normalizer Module

Handles normalization and similarity matching of job role titles.
Uses a combination of text normalization and synonym mapping to handle
variations in QA role naming conventions.
"""

import re
from typing import Set, Optional


# Synonym mapping: variations → canonical role
ROLE_SYNONYMS = {
    # QA Engineer variations
    "qa_engineer": [
        "qa engineer",
        "quality engineer",
        "quality assurance engineer",
        "software tester",
        "software test engineer",
        "test engineer",
        "qe",
    ],
    
    # SDET / Automation Engineer variations
    "sdet_automation": [
        "sdet",
        "software development engineer in test",
        "test automation engineer",
        "automation qa",
        "automation engineer",
        "automation tester",
        "qa automation engineer",
    ],
    
    # QA Lead / Manager variations
    "qa_lead": [
        "qa lead",
        "test lead",
        "qa team lead",
        "test manager",
        "qa manager",
        "quality assurance manager",
        "quality manager",
        "testing manager",
    ],
    
    # Manual Tester variations
    "manual_tester": [
        "manual tester",
        "manual qa",
        "manual qa engineer",
        "manual test engineer",
    ],
    
    # Senior roles
    "senior_qa": [
        "senior qa",
        "senior qa engineer",
        "senior sdet",
        "senior test engineer",
        "senior quality engineer",
    ],
    
    # Specialized roles
    "performance_tester": [
        "performance tester",
        "performance test engineer",
        "load tester",
        "performance qa",
    ],
    
    "security_tester": [
        "security tester",
        "security qa",
        "security test engineer",
        "penetration tester",
    ],
    
    "api_tester": [
        "api tester",
        "api test engineer",
        "api qa",
    ],
    
    "mobile_tester": [
        "mobile tester",
        "mobile qa",
        "mobile test engineer",
        "mobile app tester",
    ],
}


def normalize_role_text(role: str) -> str:
    """
    Normalizes a job role string for comparison.
    
    Steps:
    1. Convert to lowercase
    2. Remove special characters and extra whitespace
    3. Standardize spacing
    
    Args:
        role (str): Original job role string
        
    Returns:
        str: Normalized role string
        
    Example:
        >>> normalize_role_text("QA Engineer - Automation")
        "qa engineer automation"
    """
    if not role:
        return ""
    
    # Convert to lowercase
    normalized = role.lower()
    
    # Remove special characters (keep alphanumeric and spaces)
    normalized = re.sub(r'[^a-z0-9\s]', ' ', normalized)
    
    # Replace multiple spaces with single space
    normalized = re.sub(r'\s+', ' ', normalized)
    
    # Strip leading/trailing whitespace
    normalized = normalized.strip()
    
    return normalized


def get_canonical_role(role: str) -> Optional[str]:
    """
    Maps a role to its canonical representation using synonym mapping.
    
    Args:
        role (str): Job role to normalize
        
    Returns:
        Optional[str]: Canonical role name if match found, None otherwise
        
    Example:
        >>> get_canonical_role("Software Tester")
        "qa_engineer"
    """
    normalized = normalize_role_text(role)
    
    # Check each canonical role's synonyms
    for canonical, synonyms in ROLE_SYNONYMS.items():
        if normalized in synonyms:
            return canonical
    
    # No match found
    return None


def tokenize_role(role: str) -> Set[str]:
    """
    Tokenizes a role into individual words for partial matching.
    
    Args:
        role (str): Job role string
        
    Returns:
        Set[str]: Set of individual words (tokens)
        
    Example:
        >>> tokenize_role("Senior QA Engineer")
        {"senior", "qa", "engineer"}
    """
    normalized = normalize_role_text(role)
    tokens = set(normalized.split())
    
    # Remove common filler words
    stop_words = {"and", "or", "the", "in", "at", "of", "for"}
    tokens = tokens - stop_words
    
    return tokens


def calculate_role_similarity(role1: str, role2: str) -> float:
    """
    Calculates similarity score between two job roles.
    
    Matching strategy:
    1. If both map to same canonical role: high score (0.5)
    2. If roles share tokens: medium score (0.2)
    3. Otherwise: no bonus (0.0)
    
    Args:
        role1 (str): First job role
        role2 (str): Second job role
        
    Returns:
        float: Similarity score (0.0, 0.2, or 0.5)
        
    Example:
        >>> calculate_role_similarity("QA Engineer", "Quality Engineer")
        0.5
        >>> calculate_role_similarity("QA Engineer", "QA Lead")
        0.2
    """
    if not role1 or not role2:
        return 0.0
    
    # Check for exact canonical match
    canonical1 = get_canonical_role(role1)
    canonical2 = get_canonical_role(role2)
    
    if canonical1 and canonical2 and canonical1 == canonical2:
        return 0.5  # Exact match bonus
    
    # Check for token overlap
    tokens1 = tokenize_role(role1)
    tokens2 = tokenize_role(role2)
    
    if tokens1 and tokens2:
        intersection = tokens1 & tokens2
        if intersection:
            return 0.2  # Partial match bonus
    
    return 0.0  # No match
