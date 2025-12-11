"""
Profile Data Models

Defines Pydantic models for profile data validation and serialization.
These models are used for API request/response handling and database operations.
"""

from pydantic import BaseModel, Field, EmailStr, field_validator, ConfigDict
from typing import List, Optional
from datetime import datetime
import uuid


class ProfileCreateUpdate(BaseModel):
    """
    Model for creating or updating a profile.
    
    This is the input model used when users submit their profile information.
    All fields are validated according to business rules.
    """
    
    name: str = Field(
        ...,
        min_length=2,
        max_length=100,
        description="Full name of the user",
        examples=["John Doe"]
    )
    
    phone: str = Field(
        ...,
        min_length=10,
        max_length=15,
        description="Contact phone number",
        examples=["+1234567890"]
    )
    
    email: EmailStr = Field(
        ...,
        description="Email address (unique identifier)",
        examples=["john.doe@example.com"]
    )
    
    linkedin: str = Field(
        ...,
        min_length=10,
        max_length=200,
        description="LinkedIn profile URL (required for connections)",
        examples=["https://linkedin.com/in/johndoe"]
    )
    
    @field_validator('linkedin')
    @classmethod
    def validate_linkedin_url(cls, v: str) -> str:
        """Validate LinkedIn URL format."""
        if not v:
            raise ValueError('LinkedIn URL is required')
        
        v = v.strip()
        valid_patterns = [
            'linkedin.com/in/',
            'linkedin.com/company/',
            'www.linkedin.com/in/',
            'www.linkedin.com/company/',
            'https://linkedin.com/in/',
            'https://www.linkedin.com/in/',
            'http://linkedin.com/in/',
            'http://www.linkedin.com/in/'
        ]
        
        if not any(pattern in v.lower() for pattern in valid_patterns):
            raise ValueError('Please enter a valid LinkedIn profile URL (e.g., https://linkedin.com/in/yourname)')
        
        return v
    
    github: Optional[str] = Field(
        default=None,
        max_length=200,
        description="GitHub profile URL",
        examples=["https://github.com/johndoe"]
    )
    
    job_role: str = Field(
        ...,
        min_length=2,
        max_length=100,
        description="Current job role/title",
        examples=["QA Engineer", "SDET", "Test Automation Engineer"]
    )
    
    years_exp: int = Field(
        ...,
        ge=0,
        le=50,
        description="Years of professional experience",
        examples=[5]
    )
    
    strength_tags: List[str] = Field(
        ...,
        min_length=3,
        description="Skills the user can contribute (minimum 3)",
        examples=[["Selenium", "Python", "API Testing", "CI/CD"]]
    )
    
    learn_tags: List[str] = Field(
        default=[],
        min_length=0,
        description="Skills the user wants to learn (optional, for those seeking mentorship)",
        examples=[["Playwright", "Performance Testing", "Kubernetes"]]
    )
    
    @field_validator('strength_tags', 'learn_tags')
    @classmethod
    def validate_tags(cls, v: List[str], info) -> List[str]:
        """
        Validates and cleans tag lists.
        
        - strength_tags: Minimum 3 tags required
        - learn_tags: Optional (can be empty for experienced users helping others)
        - Removes empty strings and duplicates
        - Strips whitespace
        - Limits individual tag length
        """
        field_name = info.field_name
        
        # learn_tags can be empty (optional)
        if field_name == 'learn_tags' and (not v or len(v) == 0):
            return []
        
        # strength_tags must have at least 3
        if field_name == 'strength_tags' and (not v or len(v) < 3):
            raise ValueError("Minimum 3 strength tags required")
        
        # Clean tags: strip whitespace, remove empty strings
        cleaned = [tag.strip() for tag in v if tag and tag.strip()]
        
        # Remove duplicates while preserving order
        seen = set()
        unique_tags = []
        for tag in cleaned:
            tag_lower = tag.lower()
            if tag_lower not in seen:
                seen.add(tag_lower)
                unique_tags.append(tag)
        
        # Validate each tag length
        for tag in unique_tags:
            if len(tag) > 50:
                raise ValueError(f"Tag '{tag}' exceeds maximum length of 50 characters")
        
        # Final validation
        if field_name == 'strength_tags' and len(unique_tags) < 3:
            raise ValueError("Minimum 3 unique strength tags required after cleaning")
        
        return unique_tags
        
        return unique_tags
    
    @field_validator('email')
    @classmethod
    def validate_email(cls, v: str) -> str:
        """Normalizes email to lowercase."""
        return v.lower().strip()
    
    @field_validator('phone')
    @classmethod
    def validate_phone(cls, v: str) -> str:
        """Basic phone number validation and cleaning."""
        # Remove common separators
        cleaned = v.replace(" ", "").replace("-", "").replace("(", "").replace(")", "")
        
        if not cleaned:
            raise ValueError("Phone number cannot be empty")
        
        return cleaned


class ProfileResponse(BaseModel):
    """
    Model for profile responses from the API.
    
    Includes all profile data plus system-generated fields like user_id and timestamps.
    """
    
    model_config = ConfigDict(from_attributes=True)
    
    user_id: str = Field(
        ...,
        description="Unique user identifier (UUID)",
        examples=["123e4567-e89b-12d3-a456-426614174000"]
    )
    
    name: str
    phone: str
    email: EmailStr
    linkedin: str  # Now required, not Optional
    github: Optional[str] = None
    job_role: str
    years_exp: int
    strength_tags: List[str]
    learn_tags: List[str] = []
    points: int = Field(
        default=0,
        description="Points earned from connections"
    )
    connections_sent: List[str] = Field(
        default=[],
        description="List of user_ids this user has sent connection requests to (max 5)"
    )
    connections_received: List[str] = Field(
        default=[],
        description="List of user_ids who have connected with this user (unlimited)"
    )
    
    created_at: datetime = Field(
        ...,
        description="Profile creation timestamp"
    )
    
    updated_at: datetime = Field(
        ...,
        description="Profile last update timestamp"
    )


class ProfileInDB(ProfileResponse):
    """
    Internal model representing profile as stored in MongoDB.
    
    This may include additional fields for internal use that are not
    exposed in API responses.
    """
    # Override linkedin to be optional for backward compatibility with existing data
    linkedin: Optional[str] = Field(
        default=None,
        description="LinkedIn profile URL (optional in DB for backward compatibility)"
    )
    
    model_config = ConfigDict(
        from_attributes=True,
        populate_by_name=True,
        # Allow arbitrary types like ObjectId
        arbitrary_types_allowed=True
    )
    
    @classmethod
    def from_mongo(cls, data: dict):
        """
        Convert MongoDB document to Pydantic model.
        Handles ObjectId conversion.
        """
        if not data:
            return None
        
        # Convert ObjectId to string if present
        if "_id" in data:
            data["_id"] = str(data["_id"])
        
        return cls(**data)


class MatchResult(BaseModel):
    """
    Model for a single match result in profile suggestions.
    
    Contains the matched profile, score details, and overlap information.
    """
    
    profile: ProfileResponse = Field(
        ...,
        description="The matched profile"
    )
    
    score: float = Field(
        ...,
        ge=0.0,
        description="Overall match score",
        examples=[8.5]
    )
    
    overlap_tags: List[str] = Field(
        default_factory=list,
        description="Tags that overlap between learner's goals and candidate's strengths",
        examples=[["Selenium", "API Testing"]]
    )
    
    is_fallback: bool = Field(
        default=False,
        description="Whether this result is from fallback matching (no direct skill overlap)"
    )
    
    # Optional score breakdown for transparency
    score_breakdown: Optional[dict] = Field(
        default=None,
        description="Detailed breakdown of score components",
        examples=[{
            "overlap_score": 4.0,
            "breadth_score": 0.3,
            "experience_score": 1.5,
            "role_score": 0.5
        }]
    )


class MatchResponse(BaseModel):
    """
    Model for the complete match/suggestion response.
    
    Contains list of matched profiles and metadata about the matching process.
    """
    
    source_user_id: str = Field(
        ...,
        description="User ID of the profile requesting suggestions"
    )
    
    matches: List[MatchResult] = Field(
        default_factory=list,
        description="List of matched profiles, ordered by score (descending)"
    )
    
    total_candidates: int = Field(
        ...,
        description="Total number of profiles evaluated"
    )
    
    using_fallback: bool = Field(
        default=False,
        description="Whether fallback matching was used due to no direct overlaps"
    )
    
    message: Optional[str] = Field(
        default=None,
        description="Informational message about the matching results"
    )


class ProfileListResponse(BaseModel):
    """
    Model for listing multiple profiles.
    
    Used for admin/debug endpoints that return all profiles.
    """
    
    profiles: List[ProfileResponse] = Field(
        default_factory=list,
        description="List of profiles"
    )
    
    total: int = Field(
        ...,
        description="Total number of profiles"
    )


def generate_user_id() -> str:
    """
    Generates a unique user ID using UUID4.
    
    Returns:
        str: UUID string
    """
    return str(uuid.uuid4())
