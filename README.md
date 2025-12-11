# QA Community Profile Matching Platform

A web application for QA/testing professionals to connect based on skill alignment and learning goals.

## Overview

This platform helps QA professionals find peers whose expertise aligns with their learning goals, fostering a peer-to-peer community for knowledge sharing and professional development.

## Features

- **Profile Management**: Create and update professional profiles with skills and learning goals
- **Smart Matching**: Algorithm-based profile suggestions using skill overlap, experience, and role similarity
- **Simple UI**: Streamlit-based interface for easy profile creation and match discovery
- **Scalable Design**: Built to handle 150-250 profiles with room for growth

## Tech Stack

- **Backend**: Python 3.11+, FastAPI
- **Database**: MongoDB Atlas
- **Frontend**: Streamlit
- **Deployment**: Uvicorn (ASGI server)

## Project Structure

```
qa-community-platform/
├── app/
│   ├── __init__.py
│   ├── main.py              # FastAPI application entry point
│   ├── config.py            # Configuration and environment variables
│   ├── models/
│   │   ├── __init__.py
│   │   └── profile.py       # Pydantic models
│   ├── repo/
│   │   ├── __init__.py
│   │   └── profile_repo.py  # MongoDB repository layer
│   ├── services/
│   │   ├── __init__.py
│   │   ├── matching_service.py  # Matching algorithm
│   │   └── profile_service.py   # Profile business logic
│   ├── routers/
│   │   ├── __init__.py
│   │   └── profiles.py      # API route handlers
│   └── utils/
│       ├── __init__.py
│       ├── skills_catalog.py    # Standard QA skills list
│       └── role_normalizer.py   # Job role normalization
├── ui/
│   └── streamlit_app.py     # Streamlit frontend
├── .env.example             # Environment variables template
├── .gitignore
├── requirements.txt
└── README.md
```

## Setup Instructions

### Prerequisites

- Python 3.11 or higher
- MongoDB Atlas account (free tier works)
- Git

### Installation

1. **Clone the repository**
   ```powershell
   git clone <repository-url>
   cd "New Project"
   ```

2. **Create virtual environment**
   ```powershell
   python -m venv venv
   .\venv\Scripts\Activate.ps1
   ```

3. **Install dependencies**
   ```powershell
   pip install -r requirements.txt
   ```

4. **Configure environment variables**
   ```powershell
   Copy-Item .env.example .env
   ```
   
   Edit `.env` and add your MongoDB Atlas URI:
   ```
   MONGODB_URI=mongodb+srv://<username>:<password>@<cluster>.mongodb.net/?retryWrites=true&w=majority
   MONGODB_DB_NAME=qa_community
   ```

5. **Set up MongoDB Atlas**
   - Create a free cluster at [MongoDB Atlas](https://www.mongodb.com/cloud/atlas)
   - Create a database user with read/write permissions
   - Whitelist your IP address (or use 0.0.0.0/0 for development)
   - Copy the connection string to your `.env` file

## Running the Application

### Start the Backend (FastAPI)

```powershell
# Activate virtual environment
.\venv\Scripts\Activate.ps1

# Run the API server
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

The API will be available at: http://localhost:8000

API Documentation (Swagger UI): http://localhost:8000/docs

### Start the Frontend (Streamlit)

In a separate terminal:

```powershell
# Activate virtual environment
.\venv\Scripts\Activate.ps1

# Run Streamlit app
streamlit run ui/streamlit_app.py
```

The UI will be available at: http://localhost:8501

## API Endpoints

### Create/Update Profile
```
POST /api/v1/profiles/
```
Creates a new profile or updates existing one (upsert by email)

### Get Profile
```
GET /api/v1/profiles/{identifier}
```
Retrieves a profile by user_id, email, or phone

### Get Suggested Matches
```
GET /api/v1/profiles/{identifier}/suggested?limit=5
```
Returns top N matching profiles based on skill alignment

### List All Profiles (Admin)
```
GET /api/v1/profiles/
```
Returns all profiles in the system

## Matching Algorithm

The platform uses a multi-factor scoring system:

1. **Primary Factor**: Overlap between learner's goals and candidate's strengths
2. **Experience Weight**: Years of experience (capped at 10)
3. **Breadth Bonus**: Number of skills candidate can contribute
4. **Role Similarity**: Job role alignment using normalization

### Score Formula
```
total_score = (overlap_count × 2.0) + 
              (breadth_bonus × 0.3) + 
              (experience_bonus × 1.5) + 
              role_bonus
```

### Fallback Strategy
When no direct skill overlaps exist, the system suggests profiles based on:
- Years of experience
- Breadth of skills
- Shared learning interests

## Data Model

### Profile Schema
- `user_id`: Unique UUID
- `name`, `phone`, `email`: Contact information
- `linkedin`, `github`: Professional links
- `job_role`: QA role title
- `years_exp`: Years of experience (0-30)
- `strength_tags`: Skills user can contribute (min 3)
- `learn_tags`: Skills user wants to learn (min 3)
- `created_at`, `updated_at`: Timestamps

## Skills Catalog

The platform includes a curated list of 50+ QA-relevant skills:

- **Testing Types**: Manual, Automation, API, Performance, Security, Mobile
- **Tools**: Selenium, Cypress, Playwright, Postman, JMeter, etc.
- **Processes**: Agile, CI/CD, BDD, TDD, Test Planning
- **Custom Skills**: Users can add their own tags

## Development

### Running Tests
```powershell
pytest
```

### Code Style
Follow PEP 8 guidelines. Use type hints for better code documentation.

### Adding New Features
1. Update models if schema changes
2. Implement repository methods for data access
3. Add business logic in services
4. Create/update API endpoints in routers
5. Update Streamlit UI as needed

## Configuration

Key settings in `app/config.py`:
- MongoDB connection parameters
- API server settings
- Matching algorithm weights
- Default values (e.g., top N matches)

## Security Considerations

**Current Implementation (MVP)**:
- No authentication/authorization
- Suitable for internal/trusted community use

**Future Enhancements**:
- Add OAuth2/JWT authentication
- Implement role-based access control
- Add data encryption for sensitive fields
- Rate limiting for API endpoints

## Performance

- **Current Scale**: Optimized for 150-250 profiles
- **Complexity**: O(N) matching per request
- **Future Optimization**: Add indexing and caching for 1000+ profiles

## Troubleshooting

### MongoDB Connection Issues
- Verify connection string in `.env`
- Check IP whitelist in MongoDB Atlas
- Ensure database user has proper permissions

### Port Already in Use
```powershell
# Change port in command
uvicorn app.main:app --reload --port 8001
streamlit run ui/streamlit_app.py --server.port 8502
```

### Module Import Errors
```powershell
# Ensure virtual environment is activated
.\venv\Scripts\Activate.ps1

# Reinstall dependencies
pip install -r requirements.txt
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes with proper documentation
4. Submit a pull request

## License

[Specify your license here]

## Contact

For questions or support, contact [your-email@example.com]

---

**Version**: 1.0.0  
**Last Updated**: December 2025
