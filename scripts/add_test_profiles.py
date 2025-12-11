"""
Test Data Generator for QA Community Platform

This script creates 15 diverse test profiles with:
- Indian names
- Mix of standard and custom skills
- Various experience levels and roles
- Edge cases for testing matching algorithm
"""

import requests
import random
from typing import List, Dict

# API Configuration
API_BASE_URL = "http://localhost:8000"
API_PROFILES_ENDPOINT = f"{API_BASE_URL}/api/v1/profiles"

# Test data
TEST_PROFILES = [
    {
        "name": "Priya Sharma",
        "email": "priya.sharma@techcorp.com",
        "phone": "+919876543210",
        "linkedin": "https://linkedin.com/in/priya-sharma-qa",
        "github": "https://github.com/priyasharma",
        "job_role": "Senior QA Engineer",
        "years_exp": 8,
        "strength_tags": ["Selenium", "Python", "TestNG", "Jenkins", "JIRA", "API Testing", "MySQL"],
        "learn_tags": ["Kubernetes", "Playwright", "Cypress", "AI Testing", "GraphQL Testing"]
    },
    {
        "name": "Rajesh Kumar",
        "email": "rajesh.kumar@startupxyz.in",
        "phone": "+919123456789",
        "linkedin": "https://linkedin.com/in/rajesh-kumar-sdet",
        "github": "https://github.com/rajeshk",
        "job_role": "SDET",
        "years_exp": 5,
        "strength_tags": ["Java", "Cucumber", "RestAssured", "Docker", "Git", "Maven"],
        "learn_tags": ["Selenium", "Python", "Cloud Testing", "Security Testing", "Load Testing"]
    },
    {
        "name": "Amit Patel",
        "email": "amit.patel@fintech.co.in",
        "phone": "+919988776655",
        "linkedin": "https://linkedin.com/in/amit-patel-qa",
        "github": "https://github.com/amitpatel",
        "job_role": "Test Automation Lead",
        "years_exp": 12,
        "strength_tags": ["Playwright", "TypeScript", "CI/CD", "Azure DevOps", "Performance Testing", "JMeter", "Security Testing"],
        "learn_tags": ["Blockchain Testing", "NFT Testing", "Web3 QA", "Smart Contract Testing"]
    },
    {
        "name": "Sneha Reddy",
        "email": "sneha.reddy@ecommerce.com",
        "phone": "+919876012345",
        "linkedin": "https://linkedin.com/in/sneha-reddy",
        "github": "https://github.com/snehareddy",
        "job_role": "QA Analyst",
        "years_exp": 3,
        "strength_tags": ["Manual Testing", "Postman", "SQL", "JIRA", "TestRail"],
        "learn_tags": ["Selenium", "Python", "API Automation", "CI/CD", "Git", "Docker"]
    },
    {
        "name": "Arjun Singh",
        "email": "arjun.singh@consulting.in",
        "phone": "+919001122334",
        "linkedin": "https://linkedin.com/in/arjun-singh-qa",
        "github": "https://github.com/arjunsingh",
        "job_role": "QA Consultant",
        "years_exp": 15,
        "strength_tags": ["Test Strategy", "Test Planning", "Agile Testing", "Scrum", "Risk Analysis", "QA Process", "Mentoring"],
        "learn_tags": ["AI/ML Testing", "Test Data Management Tools", "ServiceNow", "Salesforce Testing"]
    },
    {
        "name": "Divya Menon",
        "email": "divya.menon@mobile.app",
        "phone": "+919556677889",
        "linkedin": "https://linkedin.com/in/divya-menon",
        "github": "https://github.com/divyamenon",
        "job_role": "Mobile QA Engineer",
        "years_exp": 6,
        "strength_tags": ["Appium", "XCUITest", "Espresso", "Android Testing", "iOS Testing", "Charles Proxy"],
        "learn_tags": ["React Native Testing", "Flutter Testing", "Detox", "Fastlane", "BrowserStack"]
    },
    {
        "name": "Vikram Joshi",
        "email": "vikram.joshi@gaming.studio",
        "phone": "+919443322110",
        "linkedin": "https://linkedin.com/in/vikram-joshi",
        "github": "https://github.com/vikramjoshi",
        "job_role": "Game Tester",
        "years_exp": 4,
        "strength_tags": ["Game Testing", "Unity Testing", "Bug Tracking", "Compatibility Testing", "Usability Testing"],
        "learn_tags": ["Automated Game Testing", "Performance Profiling", "Unity Test Framework", "Unreal Engine Testing"]
    },
    {
        "name": "Kavya Iyer",
        "email": "kavya.iyer@cloudtech.com",
        "phone": "+919998887776",
        "linkedin": "https://linkedin.com/in/kavya-iyer",
        "github": "https://github.com/kavyaiyer",
        "job_role": "Cloud QA Engineer",
        "years_exp": 7,
        "strength_tags": ["AWS", "Azure", "Terraform", "Cloud Testing", "Kubernetes", "Docker", "Microservices Testing"],
        "learn_tags": ["GCP", "Serverless Testing", "Infrastructure as Code Testing", "Chaos Engineering"]
    },
    {
        "name": "Rohit Gupta",
        "email": "rohit.gupta@saas.platform",
        "phone": "+919112233445",
        "linkedin": "https://linkedin.com/in/rohit-gupta-qa",
        "github": "https://github.com/rohitgupta",
        "job_role": "Junior QA Engineer",
        "years_exp": 1,
        "strength_tags": ["Manual Testing", "Test Cases", "Bug Reporting", "Regression Testing"],
        "learn_tags": ["Selenium", "Java", "Python", "API Testing", "Git", "JIRA", "Agile", "SQL"]
    },
    {
        "name": "Ananya Krishnan",
        "email": "ananya.krishnan@data.ai",
        "phone": "+919887766554",
        "linkedin": "https://linkedin.com/in/ananya-krishnan",
        "github": "https://github.com/ananyakrishnan",
        "job_role": "Data QA Engineer",
        "years_exp": 5,
        "strength_tags": ["SQL", "Python", "Data Validation", "ETL Testing", "PostgreSQL", "Data Quality", "Apache Airflow"],
        "learn_tags": ["Spark Testing", "Databricks", "Snowflake Testing", "dbt Testing", "Great Expectations"]
    },
    {
        "name": "Karthik Rao",
        "email": "karthik.rao@security.firm",
        "phone": "+919334455667",
        "linkedin": "https://linkedin.com/in/karthik-rao",
        "github": "https://github.com/karthikrao",
        "job_role": "Security QA Specialist",
        "years_exp": 9,
        "strength_tags": ["Security Testing", "OWASP", "Penetration Testing", "Burp Suite", "SQL Injection", "XSS Testing"],
        "learn_tags": ["DevSecOps", "Container Security", "SAST Tools", "DAST Tools", "Threat Modeling"]
    },
    {
        "name": "Meera Nair",
        "email": "meera.nair@iot.devices",
        "phone": "+919223344556",
        "linkedin": "https://linkedin.com/in/meera-nair",
        "github": "https://github.com/meeranair",
        "job_role": "IoT QA Engineer",
        "years_exp": 4,
        "strength_tags": ["IoT Testing", "Embedded Systems", "MQTT", "Raspberry Pi", "Hardware Testing", "Protocol Testing"],
        "learn_tags": ["Edge Computing Testing", "5G Testing", "Network Simulation", "Device Management Platforms"]
    },
    {
        "name": "Sanjay Desai",
        "email": "sanjay.desai@elearning.edu",
        "phone": "+919776655443",
        "linkedin": "https://linkedin.com/in/sanjay-desai",
        "github": "https://github.com/sanjaydesai",
        "job_role": "QA Engineer",
        "years_exp": 6,
        "strength_tags": ["Cypress", "JavaScript", "Mocha", "Chai", "Accessibility Testing", "WCAG", "Lighthouse"],
        "learn_tags": ["Playwright", "TypeScript", "Visual Regression Testing", "Percy", "Chromatic"]
    },
    {
        "name": "Pooja Verma",
        "email": "pooja.verma@payment.gateway",
        "phone": "+919665544332",
        "linkedin": "https://linkedin.com/in/pooja-verma",
        "github": "https://github.com/poojaverma",
        "job_role": "Performance Test Engineer",
        "years_exp": 10,
        "strength_tags": ["JMeter", "LoadRunner", "Gatling", "Performance Testing", "Stress Testing", "Load Testing", "New Relic"],
        "learn_tags": ["K6", "Artillery", "Locust", "Distributed Testing", "APM Tools", "Grafana"]
    },
    {
        "name": "Aditya Pillai",
        "email": "aditya.pillai@robotics.lab",
        "phone": "+919554433221",
        "linkedin": "https://linkedin.com/in/aditya-pillai",
        "github": "https://github.com/adityapillai",
        "job_role": "Automation Architect",
        "years_exp": 14,
        "strength_tags": ["Test Architecture", "Framework Design", "Python", "Robot Framework", "BDD", "TDD", "Design Patterns"],
        "learn_tags": ["AI-Powered Testing", "Self-Healing Tests", "Visual AI", "Test Observability", "OpenTelemetry"]
    }
]


def create_profile(profile_data: Dict) -> bool:
    """
    Create a profile via API.
    
    Args:
        profile_data: Profile information dictionary
        
    Returns:
        True if successful, False otherwise
    """
    try:
        response = requests.post(
            API_PROFILES_ENDPOINT,
            json=profile_data,
            timeout=10
        )
        response.raise_for_status()
        result = response.json()
        print(f"✅ Created profile: {profile_data['name']} (ID: {result['user_id'][:8]}...)")
        return True
    except requests.exceptions.RequestException as e:
        print(f"❌ Failed to create {profile_data['name']}: {str(e)}")
        return False


def main():
    """Main function to create all test profiles."""
    print("=" * 70)
    print("QA Community Platform - Test Data Generator")
    print("=" * 70)
    print(f"\nCreating {len(TEST_PROFILES)} test profiles...\n")
    
    success_count = 0
    failed_count = 0
    
    for idx, profile in enumerate(TEST_PROFILES, 1):
        print(f"[{idx}/{len(TEST_PROFILES)}] Creating profile for {profile['name']}...")
        
        if create_profile(profile):
            success_count += 1
        else:
            failed_count += 1
        
        print()  # Blank line for readability
    
    # Summary
    print("=" * 70)
    print("Summary:")
    print(f"  ✅ Successfully created: {success_count} profiles")
    print(f"  ❌ Failed: {failed_count} profiles")
    print(f"  📊 Total: {len(TEST_PROFILES)} profiles")
    print("=" * 70)
    
    if success_count > 0:
        print("\nTest data generation complete!")
    
    return success_count == len(TEST_PROFILES)


if __name__ == "__main__":
    import sys
    
    try:
        success = main()
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\n\n⚠️  Operation cancelled by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n\n💥 Unexpected error: {str(e)}")
        sys.exit(1)
