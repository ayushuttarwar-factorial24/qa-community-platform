"""
Data Models for QA Community Platform v2
Defines the structure for Give/Ask sections and profile data.
"""
from dataclasses import dataclass, field
from typing import List, Optional
from datetime import datetime


@dataclass
class QuestionResponse:
    """
    Represents a response to a Give/Ask question.
    Contains both selected checkboxes and custom text input.
    """
    selected: List[str] = field(default_factory=list)  # Checkbox selections
    custom: List[str] = field(default_factory=list)    # Custom comma-separated inputs
    
    def get_all_items(self) -> List[str]:
        """Returns combined list of selected and custom items."""
        return self.selected + self.custom
    
    def to_dict(self) -> dict:
        return {
            "selected": self.selected,
            "custom": self.custom
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> "QuestionResponse":
        if data is None:
            return cls()
        return cls(
            selected=data.get("selected", []),
            custom=data.get("custom", [])
        )


@dataclass
class GiveSection:
    """
    GIVE Section - What the participant can contribute.
    """
    # Q1: Companies for introductions (free text only, stored as array)
    companies: List[str] = field(default_factory=list)
    
    # Q2: Professional activities (checkboxes + custom)
    professional_activities: QuestionResponse = field(default_factory=QuestionResponse)
    
    # Q3: Technical areas for training (checkboxes + custom)
    technical_areas: QuestionResponse = field(default_factory=QuestionResponse)
    
    # Q4: Volunteering activities (checkboxes + custom)
    volunteering: QuestionResponse = field(default_factory=QuestionResponse)
    
    # Q5: Job roles hiring for (checkboxes + custom)
    job_roles: QuestionResponse = field(default_factory=QuestionResponse)
    
    # Open Give: Free text for additional contributions
    open_contribution: str = ""
    
    def to_dict(self) -> dict:
        return {
            "companies": self.companies,
            "professional_activities": self.professional_activities.to_dict(),
            "technical_areas": self.technical_areas.to_dict(),
            "volunteering": self.volunteering.to_dict(),
            "job_roles": self.job_roles.to_dict(),
            "open_contribution": self.open_contribution
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> "GiveSection":
        if data is None:
            return cls()
        return cls(
            companies=data.get("companies", []),
            professional_activities=QuestionResponse.from_dict(data.get("professional_activities")),
            technical_areas=QuestionResponse.from_dict(data.get("technical_areas")),
            volunteering=QuestionResponse.from_dict(data.get("volunteering")),
            job_roles=QuestionResponse.from_dict(data.get("job_roles")),
            open_contribution=data.get("open_contribution", "")
        )


@dataclass
class AskSection:
    """
    ASK Section - What the participant needs.
    """
    # Q1: Companies for introductions (free text only, stored as array)
    companies: List[str] = field(default_factory=list)
    
    # Q2: Professional activities needed (checkboxes + custom)
    professional_activities: QuestionResponse = field(default_factory=QuestionResponse)
    
    # Q3: Technical areas to learn (checkboxes + custom)
    technical_areas: QuestionResponse = field(default_factory=QuestionResponse)
    
    # Q4: Volunteering guidance needed (checkboxes + custom)
    volunteering: QuestionResponse = field(default_factory=QuestionResponse)
    
    # Q5: Job roles looking for (checkboxes + custom)
    job_roles: QuestionResponse = field(default_factory=QuestionResponse)
    
    # Open Ask: Free text for additional requests
    open_request: str = ""
    
    def to_dict(self) -> dict:
        return {
            "companies": self.companies,
            "professional_activities": self.professional_activities.to_dict(),
            "technical_areas": self.technical_areas.to_dict(),
            "volunteering": self.volunteering.to_dict(),
            "job_roles": self.job_roles.to_dict(),
            "open_request": self.open_request
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> "AskSection":
        if data is None:
            return cls()
        return cls(
            companies=data.get("companies", []),
            professional_activities=QuestionResponse.from_dict(data.get("professional_activities")),
            technical_areas=QuestionResponse.from_dict(data.get("technical_areas")),
            volunteering=QuestionResponse.from_dict(data.get("volunteering")),
            job_roles=QuestionResponse.from_dict(data.get("job_roles")),
            open_request=data.get("open_request", "")
        )


@dataclass
class Profile:
    """
    Complete user profile with Give/Ask sections.
    """
    # Basic Info
    user_id: str = ""
    full_name: str = ""
    email: str = ""
    phone: str = ""
    linkedin_url: str = ""
    current_company: str = ""
    experience: str = ""  # Dropdown value like "4-6 years"
    current_role: str = ""
    custom_role: str = ""  # If "Other" is selected
    
    # Give/Ask Sections
    give: GiveSection = field(default_factory=GiveSection)
    ask: AskSection = field(default_factory=AskSection)
    
    # Connection Tracking
    connections_sent: List[str] = field(default_factory=list)
    connections_received: List[str] = field(default_factory=list)
    
    # Points and Metadata
    points: int = 0
    created_at: datetime = field(default_factory=datetime.utcnow)
    updated_at: datetime = field(default_factory=datetime.utcnow)
    
    def get_display_role(self) -> str:
        """Returns the role to display (custom if 'Other' selected)."""
        if self.current_role == "Other" and self.custom_role:
            return self.custom_role
        return self.current_role
    
    def to_dict(self) -> dict:
        return {
            "user_id": self.user_id,
            "full_name": self.full_name,
            "email": self.email,
            "phone": self.phone,
            "linkedin_url": self.linkedin_url,
            "current_company": self.current_company,
            "experience": self.experience,
            "current_role": self.current_role,
            "custom_role": self.custom_role,
            "give": self.give.to_dict(),
            "ask": self.ask.to_dict(),
            "connections_sent": self.connections_sent,
            "connections_received": self.connections_received,
            "points": self.points,
            "created_at": self.created_at,
            "updated_at": self.updated_at
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> "Profile":
        if data is None:
            return cls()
        return cls(
            user_id=data.get("user_id", ""),
            full_name=data.get("full_name", ""),
            email=data.get("email", ""),
            phone=data.get("phone", ""),
            linkedin_url=data.get("linkedin_url", ""),
            current_company=data.get("current_company", ""),
            experience=data.get("experience", ""),
            current_role=data.get("current_role", ""),
            custom_role=data.get("custom_role", ""),
            give=GiveSection.from_dict(data.get("give")),
            ask=AskSection.from_dict(data.get("ask")),
            connections_sent=data.get("connections_sent", []),
            connections_received=data.get("connections_received", []),
            points=data.get("points", 0),
            created_at=data.get("created_at", datetime.utcnow()),
            updated_at=data.get("updated_at", datetime.utcnow())
        )
