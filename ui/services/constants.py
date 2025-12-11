"""
Constants and Configuration Options for QA Community Platform
All checkbox options and dropdown values are defined here for easy maintenance.
"""

# =============================================================================
# DATABASE CONFIGURATION
# =============================================================================
DATABASE_NAME = "qa_community_v2"
PROFILES_COLLECTION = "profiles"

# =============================================================================
# MATCHING CONFIGURATION
# =============================================================================
DEFAULT_MATCH_LIMIT = 5
MAX_CONNECTIONS_PER_USER = 5  # Outgoing connections limit

# =============================================================================
# EXPERIENCE LEVELS
# =============================================================================
EXPERIENCE_OPTIONS = [
    "0-1 years",
    "1-3 years",
    "4-6 years",
    "7-10 years",
    "11-15 years",
    "15+ years",
]

# =============================================================================
# CURRENT ROLE OPTIONS
# =============================================================================
ROLE_OPTIONS = [
    "QA Engineer",
    "SDET",
    "Test Lead",
    "QA Manager",
    "Test Architect",
    "Automation Engineer",
    "Manual Tester",
    "Performance Engineer",
    "Security Tester",
    "DevOps Engineer",
    "Other",
]

# =============================================================================
# Q2: PROFESSIONAL ACTIVITIES
# For both Give (what I can help with) and Ask (what I need help with)
# =============================================================================
PROFESSIONAL_ACTIVITIES = [
    "Resume Review & Profile Enhancement",
    "Mock Interviews (QA, Automation, Leadership roles)",
    "Career Mentoring / Coaching",
    "Project Guidance",
]

# =============================================================================
# Q3: TECHNICAL/TESTING AREAS
# For both Give (what I can train) and Ask (what I want to learn)
# =============================================================================
TECHNICAL_AREAS = [
    "Manual Testing / QA Fundamentals",
    "Automation (Selenium, Cypress, Playwright, Appium)",
    "Performance / Security / API Testing",
    "Test Leadership & Strategy",
    "AI in Testing / ML-based Test Automation",
]

# =============================================================================
# Q4: VOLUNTEERING/COMMUNITY ACTIVITIES
# For both Give (what I can volunteer) and Ask (what guidance I need)
# =============================================================================
VOLUNTEERING_ACTIVITIES = [
    "Event Coordination / Logistics",
    "Speaker Support / Session Facilitation",
    "Content Creation (Blogs, Videos, Tutorials)",
    "Social Media & Community Engagement",
    "Mentoring New Volunteers / Students",
    "Bringing Sponsorship for events/activities",
]

# =============================================================================
# Q5: JOB ROLES
# For Give (hiring for) and Ask (looking for opportunities)
# =============================================================================
JOB_ROLES = [
    "Manual QA Engineer",
    "Automation Test Engineer (Selenium / Playwright / Cypress)",
    "SDET / Software Development Engineer in Test",
    "API Test Engineer / Postman / REST Assured",
    "Performance Test Engineer (JMeter / LoadRunner)",
    "Security Test Engineer / Pen Tester",
    "Mobile Test Engineer (Android / iOS)",
    "Test Architect / QA Lead",
    "Data Quality Engineer",
    "AI/ML Test Engineer",
    "Test Manager",
]

# =============================================================================
# FIELD LABELS FOR UI
# =============================================================================
GIVE_LABELS = {
    "q1": "I can help you get introduced to people in the following companies:",
    "q2": "I can help in the following professional activities:",
    "q3": "I can train or answer questions in the following areas:",
    "q4": "I can help communities like ATAGTR with the following volunteering initiatives:",
    "q5": "I or my company is looking for the following job talent:",
    "open": "Anything else you would like to offer or contribute?",
}

ASK_LABELS = {
    "q1": "Can someone help me get introduced to people in the following companies?",
    "q2": "I need support in the following professional activities:",
    "q3": "I want to learn or clarify doubts in the following technical/testing areas:",
    "q4": "I want to participate in community or volunteering activities but need guidance in:",
    "q5": "I am looking for job opportunities in the following areas:",
    "open": "Anything else you want to request from the community?",
}

# =============================================================================
# OPEN FIELD PLACEHOLDERS
# =============================================================================
GIVE_PLACEHOLDERS = {
    "q1": "Enter company names separated by commas (e.g., Google, Microsoft, TCS)",
    "q2": "Additional professional help you can offer",
    "q3": "Other areas you can train or mentor in",
    "q4": "Other ways you can volunteer",
    "q5": "Specific roles, skills, or collaboration needs",
    "open": "Describe any other contributions you can make...",
}

ASK_PLACEHOLDERS = {
    "q1": "Enter company names separated by commas (e.g., Amazon, Infosys, Wipro)",
    "q2": "Any other professional help you need",
    "q3": "List specific tools or topics you need help with",
    "q4": "Any other guidance you need",
    "q5": "Describe specific roles or companies you are targeting",
    "open": "Describe any other requests from the community...",
}
