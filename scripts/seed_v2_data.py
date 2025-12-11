"""
Seed Data Script for QA Community Platform v2

Creates sample profiles in the qa_community_v2 database for testing.
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'ui'))

from datetime import datetime
import uuid

# MongoDB connection
from pymongo import MongoClient
from dotenv import load_dotenv

load_dotenv()

# Connect to MongoDB
MONGO_URI = os.getenv("MONGODB_URI", "mongodb+srv://ayushuttarwar_db_user:tyClHreg6QKmRqNt@cluster0.fa2zknm.mongodb.net/?appName=Cluster0")
DB_NAME = "qa_community_v2"

client = MongoClient(MONGO_URI)
db = client[DB_NAME]
profiles = db.profiles

# Sample profiles data
SAMPLE_PROFILES = [
    {
        "user_id": str(uuid.uuid4()),
        "full_name": "Rajesh Kumar",
        "email": "rajesh.kumar@techcorp.com",
        "phone": "+91 9876543210",
        "linkedin_url": "https://linkedin.com/in/rajeshkumar",
        "current_company": "TechCorp India",
        "experience": "7-10 years",
        "current_role": "Test Architect",
        "custom_role": "",
        "give": {
            "companies": ["Google", "Microsoft", "Amazon"],
            "professional_activities": {
                "selected": ["Resume Review & Profile Enhancement", "Mock Interviews (QA, Automation, Leadership roles)", "Career Mentoring / Coaching"],
                "custom": []
            },
            "technical_areas": {
                "selected": ["Automation (Selenium, Cypress, Playwright, Appium)", "Test Leadership & Strategy"],
                "custom": ["CI/CD Integration", "Docker for Testing"]
            },
            "volunteering": {
                "selected": ["Speaker Support / Session Facilitation", "Mentoring New Volunteers / Students"],
                "custom": []
            },
            "job_roles": {
                "selected": ["Automation Test Engineer (Selenium / Playwright / Cypress)", "Test Architect / QA Lead"],
                "custom": []
            },
            "open_contribution": "Happy to review test strategies and automation frameworks"
        },
        "ask": {
            "companies": ["Netflix", "Uber"],
            "professional_activities": {
                "selected": ["Career Mentoring / Coaching"],
                "custom": []
            },
            "technical_areas": {
                "selected": ["AI in Testing / ML-based Test Automation"],
                "custom": ["Chaos Engineering"]
            },
            "volunteering": {"selected": [], "custom": []},
            "job_roles": {
                "selected": ["Test Manager"],
                "custom": []
            },
            "open_request": "Looking for opportunities in product companies"
        },
        "points": 150,
        "connections_sent": [],
        "connections_received": [],
        "created_at": datetime.utcnow(),
        "updated_at": datetime.utcnow()
    },
    {
        "user_id": str(uuid.uuid4()),
        "full_name": "Priya Sharma",
        "email": "priya.sharma@infosys.com",
        "phone": "+91 8765432109",
        "linkedin_url": "https://linkedin.com/in/priyasharma",
        "current_company": "Infosys",
        "experience": "4-6 years",
        "current_role": "SDET",
        "custom_role": "",
        "give": {
            "companies": ["Infosys", "Wipro", "TCS"],
            "professional_activities": {
                "selected": ["Mock Interviews (QA, Automation, Leadership roles)", "Project Guidance"],
                "custom": []
            },
            "technical_areas": {
                "selected": ["Automation (Selenium, Cypress, Playwright, Appium)", "Performance / Security / API Testing"],
                "custom": ["RestAssured", "Karate Framework"]
            },
            "volunteering": {
                "selected": ["Content Creation (Blogs, Videos, Tutorials)"],
                "custom": []
            },
            "job_roles": {
                "selected": ["API Test Engineer / Postman / REST Assured"],
                "custom": []
            },
            "open_contribution": "Can help with API testing strategies"
        },
        "ask": {
            "companies": ["Google", "Microsoft", "Amazon"],
            "professional_activities": {
                "selected": ["Resume Review & Profile Enhancement", "Career Mentoring / Coaching"],
                "custom": []
            },
            "technical_areas": {
                "selected": ["Test Leadership & Strategy", "AI in Testing / ML-based Test Automation"],
                "custom": []
            },
            "volunteering": {"selected": [], "custom": []},
            "job_roles": {
                "selected": ["SDET / Software Development Engineer in Test", "Test Architect / QA Lead"],
                "custom": []
            },
            "open_request": "Want to move to a product-based company"
        },
        "points": 80,
        "connections_sent": [],
        "connections_received": [],
        "created_at": datetime.utcnow(),
        "updated_at": datetime.utcnow()
    },
    {
        "user_id": str(uuid.uuid4()),
        "full_name": "Amit Patel",
        "email": "amit.patel@startup.io",
        "phone": "+91 7654321098",
        "linkedin_url": "https://linkedin.com/in/amitpatel",
        "current_company": "TechStartup.io",
        "experience": "1-3 years",
        "current_role": "QA Engineer",
        "custom_role": "",
        "give": {
            "companies": [],
            "professional_activities": {
                "selected": [],
                "custom": []
            },
            "technical_areas": {
                "selected": ["Manual Testing / QA Fundamentals"],
                "custom": ["Mobile App Testing"]
            },
            "volunteering": {
                "selected": ["Social Media & Community Engagement"],
                "custom": []
            },
            "job_roles": {
                "selected": [],
                "custom": []
            },
            "open_contribution": "Eager to help with manual testing and documentation"
        },
        "ask": {
            "companies": ["Google", "Microsoft", "Flipkart", "Swiggy"],
            "professional_activities": {
                "selected": ["Resume Review & Profile Enhancement", "Mock Interviews (QA, Automation, Leadership roles)", "Career Mentoring / Coaching"],
                "custom": []
            },
            "technical_areas": {
                "selected": ["Automation (Selenium, Cypress, Playwright, Appium)", "Performance / Security / API Testing"],
                "custom": []
            },
            "volunteering": {"selected": [], "custom": []},
            "job_roles": {
                "selected": ["Automation Test Engineer (Selenium / Playwright / Cypress)", "Mobile Test Engineer (Android / iOS)"],
                "custom": []
            },
            "open_request": "Looking for automation learning resources and mentorship"
        },
        "points": 20,
        "connections_sent": [],
        "connections_received": [],
        "created_at": datetime.utcnow(),
        "updated_at": datetime.utcnow()
    },
    {
        "user_id": str(uuid.uuid4()),
        "full_name": "Sneha Reddy",
        "email": "sneha.reddy@oracle.com",
        "phone": "+91 6543210987",
        "linkedin_url": "https://linkedin.com/in/snehareddy",
        "current_company": "Oracle",
        "experience": "11-15 years",
        "current_role": "QA Manager",
        "custom_role": "",
        "give": {
            "companies": ["Oracle", "IBM", "Cisco", "SAP"],
            "professional_activities": {
                "selected": ["Resume Review & Profile Enhancement", "Mock Interviews (QA, Automation, Leadership roles)", "Career Mentoring / Coaching", "Project Guidance"],
                "custom": ["Leadership Coaching"]
            },
            "technical_areas": {
                "selected": ["Test Leadership & Strategy", "Performance / Security / API Testing"],
                "custom": ["Test Strategy Development", "Team Building"]
            },
            "volunteering": {
                "selected": ["Speaker Support / Session Facilitation", "Mentoring New Volunteers / Students", "Bringing Sponsorship for events/activities"],
                "custom": []
            },
            "job_roles": {
                "selected": ["Test Manager", "Test Architect / QA Lead"],
                "custom": ["QA Director"]
            },
            "open_contribution": "Happy to mentor aspiring QA leaders and review test strategies"
        },
        "ask": {
            "companies": ["Google", "Amazon", "Netflix"],
            "professional_activities": {
                "selected": [],
                "custom": ["Executive coaching"]
            },
            "technical_areas": {
                "selected": ["AI in Testing / ML-based Test Automation"],
                "custom": []
            },
            "volunteering": {"selected": [], "custom": []},
            "job_roles": {
                "selected": [],
                "custom": ["VP of Quality"]
            },
            "open_request": "Interested in transitioning to product companies at director level"
        },
        "points": 250,
        "connections_sent": [],
        "connections_received": [],
        "created_at": datetime.utcnow(),
        "updated_at": datetime.utcnow()
    },
    {
        "user_id": str(uuid.uuid4()),
        "full_name": "Vikram Singh",
        "email": "vikram.singh@testleaf.com",
        "phone": "+91 5432109876",
        "linkedin_url": "https://linkedin.com/in/vikramsingh",
        "current_company": "TestLeaf Academy",
        "experience": "7-10 years",
        "current_role": "Other",
        "custom_role": "Trainer & Consultant",
        "give": {
            "companies": ["Cognizant", "HCL", "Capgemini"],
            "professional_activities": {
                "selected": ["Mock Interviews (QA, Automation, Leadership roles)", "Career Mentoring / Coaching", "Project Guidance"],
                "custom": ["Corporate Training"]
            },
            "technical_areas": {
                "selected": ["Manual Testing / QA Fundamentals", "Automation (Selenium, Cypress, Playwright, Appium)", "Performance / Security / API Testing"],
                "custom": ["Selenium Grid", "TestNG", "BDD with Cucumber"]
            },
            "volunteering": {
                "selected": ["Content Creation (Blogs, Videos, Tutorials)", "Speaker Support / Session Facilitation", "Mentoring New Volunteers / Students"],
                "custom": []
            },
            "job_roles": {
                "selected": [],
                "custom": []
            },
            "open_contribution": "Free weekend training sessions for beginners"
        },
        "ask": {
            "companies": [],
            "professional_activities": {
                "selected": [],
                "custom": []
            },
            "technical_areas": {
                "selected": ["AI in Testing / ML-based Test Automation"],
                "custom": ["Cloud Testing", "Kubernetes"]
            },
            "volunteering": {"selected": [], "custom": []},
            "job_roles": {
                "selected": [],
                "custom": []
            },
            "open_request": "Looking for speakers for my YouTube channel"
        },
        "points": 180,
        "connections_sent": [],
        "connections_received": [],
        "created_at": datetime.utcnow(),
        "updated_at": datetime.utcnow()
    },
    {
        "user_id": str(uuid.uuid4()),
        "full_name": "Ananya Gupta",
        "email": "ananya.gupta@flipkart.com",
        "phone": "+91 4321098765",
        "linkedin_url": "https://linkedin.com/in/ananyagupta",
        "current_company": "Flipkart",
        "experience": "4-6 years",
        "current_role": "Performance Engineer",
        "custom_role": "",
        "give": {
            "companies": ["Flipkart", "Myntra", "PhonePe"],
            "professional_activities": {
                "selected": ["Mock Interviews (QA, Automation, Leadership roles)", "Project Guidance"],
                "custom": []
            },
            "technical_areas": {
                "selected": ["Performance / Security / API Testing"],
                "custom": ["JMeter", "Gatling", "k6", "Load Testing at Scale"]
            },
            "volunteering": {
                "selected": ["Content Creation (Blogs, Videos, Tutorials)"],
                "custom": []
            },
            "job_roles": {
                "selected": ["Performance Test Engineer (JMeter / LoadRunner)"],
                "custom": []
            },
            "open_contribution": "Can help with performance testing strategy for e-commerce"
        },
        "ask": {
            "companies": ["Google", "Amazon", "Microsoft"],
            "professional_activities": {
                "selected": ["Career Mentoring / Coaching"],
                "custom": []
            },
            "technical_areas": {
                "selected": ["Test Leadership & Strategy", "AI in Testing / ML-based Test Automation"],
                "custom": ["SRE practices"]
            },
            "volunteering": {"selected": [], "custom": []},
            "job_roles": {
                "selected": ["Test Architect / QA Lead"],
                "custom": ["Performance Architect"]
            },
            "open_request": "Want to transition to tech leadership"
        },
        "points": 95,
        "connections_sent": [],
        "connections_received": [],
        "created_at": datetime.utcnow(),
        "updated_at": datetime.utcnow()
    },
    {
        "user_id": str(uuid.uuid4()),
        "full_name": "Karthik Menon",
        "email": "karthik.menon@zoho.com",
        "phone": "+91 3210987654",
        "linkedin_url": "https://linkedin.com/in/karthikmenon",
        "current_company": "Zoho Corporation",
        "experience": "4-6 years",
        "current_role": "Automation Engineer",
        "custom_role": "",
        "give": {
            "companies": ["Zoho", "Freshworks"],
            "professional_activities": {
                "selected": ["Resume Review & Profile Enhancement", "Project Guidance"],
                "custom": []
            },
            "technical_areas": {
                "selected": ["Automation (Selenium, Cypress, Playwright, Appium)"],
                "custom": ["Playwright", "TypeScript", "Page Object Model"]
            },
            "volunteering": {
                "selected": ["Content Creation (Blogs, Videos, Tutorials)"],
                "custom": []
            },
            "job_roles": {
                "selected": ["Automation Test Engineer (Selenium / Playwright / Cypress)"],
                "custom": []
            },
            "open_contribution": "Open source contributor - happy to help with Playwright"
        },
        "ask": {
            "companies": ["Google", "Meta", "Apple"],
            "professional_activities": {
                "selected": ["Mock Interviews (QA, Automation, Leadership roles)", "Career Mentoring / Coaching"],
                "custom": []
            },
            "technical_areas": {
                "selected": ["Test Leadership & Strategy"],
                "custom": ["System Design for Testing"]
            },
            "volunteering": {"selected": [], "custom": []},
            "job_roles": {
                "selected": ["SDET / Software Development Engineer in Test"],
                "custom": []
            },
            "open_request": "Preparing for FAANG interviews"
        },
        "points": 65,
        "connections_sent": [],
        "connections_received": [],
        "created_at": datetime.utcnow(),
        "updated_at": datetime.utcnow()
    },
    {
        "user_id": str(uuid.uuid4()),
        "full_name": "Meera Krishnan",
        "email": "meera.krishnan@accenture.com",
        "phone": "+91 2109876543",
        "linkedin_url": "https://linkedin.com/in/meerakrishnan",
        "current_company": "Accenture",
        "experience": "1-3 years",
        "current_role": "Manual Tester",
        "custom_role": "",
        "give": {
            "companies": [],
            "professional_activities": {
                "selected": [],
                "custom": []
            },
            "technical_areas": {
                "selected": ["Manual Testing / QA Fundamentals"],
                "custom": ["Test Case Writing", "Defect Management"]
            },
            "volunteering": {
                "selected": ["Social Media & Community Engagement", "Event Coordination / Logistics"],
                "custom": []
            },
            "job_roles": {
                "selected": [],
                "custom": []
            },
            "open_contribution": "Can help organize community events"
        },
        "ask": {
            "companies": ["Infosys", "TCS", "Wipro", "Cognizant"],
            "professional_activities": {
                "selected": ["Resume Review & Profile Enhancement", "Mock Interviews (QA, Automation, Leadership roles)", "Career Mentoring / Coaching"],
                "custom": []
            },
            "technical_areas": {
                "selected": ["Automation (Selenium, Cypress, Playwright, Appium)", "Performance / Security / API Testing"],
                "custom": ["Python for Testing"]
            },
            "volunteering": {"selected": [], "custom": []},
            "job_roles": {
                "selected": ["Automation Test Engineer (Selenium / Playwright / Cypress)", "API Test Engineer / Postman / REST Assured"],
                "custom": []
            },
            "open_request": "Want to transition from manual to automation testing"
        },
        "points": 30,
        "connections_sent": [],
        "connections_received": [],
        "created_at": datetime.utcnow(),
        "updated_at": datetime.utcnow()
    }
]


def seed_database():
    """Seed the database with sample profiles."""
    print(f"Connecting to database: {DB_NAME}")
    
    # Clear existing profiles (optional - comment out if you want to append)
    # profiles.delete_many({})
    # print("Cleared existing profiles")
    
    # Check existing count
    existing_count = profiles.count_documents({})
    print(f"Existing profiles: {existing_count}")
    
    # Insert sample profiles
    inserted = 0
    for profile in SAMPLE_PROFILES:
        # Check if email already exists
        if profiles.find_one({"email": profile["email"]}):
            print(f"  Skipping {profile['email']} (already exists)")
            continue
        
        profiles.insert_one(profile)
        print(f"  Inserted: {profile['full_name']} ({profile['email']})")
        inserted += 1
    
    print(f"\nInserted {inserted} new profiles")
    print(f"Total profiles now: {profiles.count_documents({})}")


if __name__ == "__main__":
    seed_database()
