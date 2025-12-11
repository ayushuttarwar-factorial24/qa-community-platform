"""
Skills Catalog Module

Maintains the standard list of QA/testing skills used across the platform.
This provides a curated vocabulary for skill tagging while allowing custom tags.
"""

from typing import List


# Standard QA skills organized by category
TESTING_TYPES: List[str] = [
    "Manual Testing",
    "Automation Testing",
    "API Testing",
    "Performance Testing",
    "Load Testing",
    "Stress Testing",
    "Security Testing",
    "Mobile Testing",
    "Web Testing",
    "Database Testing",
    "Regression Testing",
    "Smoke Testing",
    "Sanity Testing",
    "Exploratory Testing",
    "User Acceptance Testing",
    "Integration Testing",
    "System Testing",
    "End-to-End Testing",
    "Cross-Browser Testing",
    "Accessibility Testing",
]

AUTOMATION_TOOLS: List[str] = [
    "Selenium",
    "Selenium WebDriver",
    "Cypress",
    "Playwright",
    "WebdriverIO",
    "Appium",
    "Robot Framework",
    "Katalon Studio",
    "TestComplete",
    "Ranorex",
    "Puppeteer",
]

TESTING_FRAMEWORKS: List[str] = [
    "pytest",
    "unittest",
    "TestNG",
    "JUnit",
    "JUnit 5",
    "NUnit",
    "Mocha",
    "Jasmine",
    "Jest",
    "Cucumber",
    "SpecFlow",
    "Behave",
]

API_TOOLS: List[str] = [
    "Postman",
    "Newman",
    "Insomnia",
    "SoapUI",
    "REST Assured",
    "Karate Framework",
    "Pact",
    "WireMock",
    "GraphQL Testing",
    "Swagger",
]

PERFORMANCE_TOOLS: List[str] = [
    "JMeter",
    "LoadRunner",
    "Gatling",
    "Locust",
    "k6",
    "Apache Bench",
    "Artillery",
]

PROGRAMMING_LANGUAGES: List[str] = [
    "Python",
    "Java",
    "JavaScript",
    "TypeScript",
    "C#",
    "Ruby",
    "Go",
    "Shell Scripting",
    "SQL",
]

CI_CD_TOOLS: List[str] = [
    "Jenkins",
    "GitLab CI",
    "GitHub Actions",
    "CircleCI",
    "Travis CI",
    "Azure DevOps",
    "Bamboo",
    "TeamCity",
    "Docker",
    "Kubernetes",
]

TEST_MANAGEMENT: List[str] = [
    "JIRA",
    "TestRail",
    "Zephyr",
    "Xray",
    "qTest",
    "PractiTest",
    "Azure Test Plans",
    "HP ALM",
    "Test Case Design",
    "Test Planning",
    "Defect Management",
    "Test Strategy",
]

METHODOLOGIES: List[str] = [
    "Agile Testing",
    "Scrum",
    "Kanban",
    "BDD",
    "TDD",
    "ATDD",
    "Shift-Left Testing",
    "DevOps",
    "Continuous Testing",
]

VERSION_CONTROL: List[str] = [
    "Git",
    "GitHub",
    "GitLab",
    "Bitbucket",
    "SVN",
]

REPORTING_TOOLS: List[str] = [
    "Allure Reports",
    "ExtentReports",
    "TestNG Reports",
    "Cucumber Reports",
    "ReportPortal",
]

SPECIALIZED_TESTING: List[str] = [
    "Microservices Testing",
    "Cloud Testing",
    "Blockchain Testing",
    "AI/ML Testing",
    "IoT Testing",
    "ETL Testing",
    "Data Warehouse Testing",
]


def get_all_standard_skills() -> List[str]:
    """
    Returns a complete list of all standard QA skills.
    
    Returns:
        List[str]: Combined list of all curated skills
    """
    all_skills = (
        TESTING_TYPES +
        AUTOMATION_TOOLS +
        TESTING_FRAMEWORKS +
        API_TOOLS +
        PERFORMANCE_TOOLS +
        PROGRAMMING_LANGUAGES +
        CI_CD_TOOLS +
        TEST_MANAGEMENT +
        METHODOLOGIES +
        VERSION_CONTROL +
        REPORTING_TOOLS +
        SPECIALIZED_TESTING
    )
    
    # Return sorted unique list
    return sorted(list(set(all_skills)))


def get_skills_by_category() -> dict:
    """
    Returns skills organized by category.
    
    Returns:
        dict: Dictionary with category names as keys and skill lists as values
    """
    return {
        "Testing Types": sorted(TESTING_TYPES),
        "Automation Tools": sorted(AUTOMATION_TOOLS),
        "Testing Frameworks": sorted(TESTING_FRAMEWORKS),
        "API Tools": sorted(API_TOOLS),
        "Performance Tools": sorted(PERFORMANCE_TOOLS),
        "Programming Languages": sorted(PROGRAMMING_LANGUAGES),
        "CI/CD Tools": sorted(CI_CD_TOOLS),
        "Test Management": sorted(TEST_MANAGEMENT),
        "Methodologies": sorted(METHODOLOGIES),
        "Version Control": sorted(VERSION_CONTROL),
        "Reporting Tools": sorted(REPORTING_TOOLS),
        "Specialized Testing": sorted(SPECIALIZED_TESTING),
    }


# Export the complete list for easy import
STANDARD_QA_SKILLS = get_all_standard_skills()
