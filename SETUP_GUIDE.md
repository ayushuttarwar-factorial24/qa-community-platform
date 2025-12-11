# QA Community Profile Matching Platform - Setup Guide

## Quick Start Guide

### Step 1: Create Virtual Environment

```powershell
# Navigate to project directory
cd "e:\New Project"

# Create virtual environment
python -m venv venv

# Activate virtual environment
.\venv\Scripts\Activate.ps1
```

### Step 2: Install Dependencies

```powershell
# Ensure virtual environment is activated
pip install --upgrade pip
pip install -r requirements.txt
```

### Step 3: Configure Environment

```powershell
# Copy example environment file
Copy-Item .env.example .env

# Edit .env file with your MongoDB Atlas URI
notepad .env
```

Update the following in `.env`:
```
MONGODB_URI=mongodb+srv://<username>:<password>@<cluster>.mongodb.net/?retryWrites=true&w=majority
MONGODB_DB_NAME=qa_community
```

### Step 4: Set Up MongoDB Atlas

1. Go to [MongoDB Atlas](https://www.mongodb.com/cloud/atlas)
2. Create a free account (if you don't have one)
3. Create a new cluster (free tier M0 is sufficient)
4. Create a database user:
   - Go to Database Access
   - Click "Add New Database User"
   - Choose password authentication
   - Set username and password
   - Grant "Atlas admin" role (for development)
5. Configure network access:
   - Go to Network Access
   - Click "Add IP Address"
   - For development: Click "Allow Access from Anywhere" (0.0.0.0/0)
   - For production: Add your specific IP addresses
6. Get connection string:
   - Go to Clusters
   - Click "Connect"
   - Choose "Connect your application"
   - Copy the connection string
   - Replace `<password>` with your database user password
   - Paste into your `.env` file

### Step 5: Run the Application

**Terminal 1 - Start Backend API:**
```powershell
# Activate virtual environment
.\venv\Scripts\Activate.ps1

# Run FastAPI server
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

The API will be available at:
- API: http://localhost:8000
- Swagger Docs: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

**Terminal 2 - Start Frontend UI:**
```powershell
# Activate virtual environment (in new terminal)
.\venv\Scripts\Activate.ps1

# Run Streamlit app
streamlit run ui/streamlit_app.py
```

The UI will be available at: http://localhost:8501

## Testing the Application

### Test 1: Create a Profile via API

```powershell
# Use curl or Invoke-RestMethod (PowerShell)
$body = @{
    name = "John Doe"
    email = "john.doe@example.com"
    phone = "+1234567890"
    linkedin = "https://linkedin.com/in/johndoe"
    github = "https://github.com/johndoe"
    job_role = "QA Engineer"
    years_exp = 5
    strength_tags = @("Selenium", "Python", "API Testing", "CI/CD")
    learn_tags = @("Playwright", "Performance Testing", "Kubernetes")
} | ConvertTo-Json

Invoke-RestMethod -Uri "http://localhost:8000/api/v1/profiles/" -Method POST -Body $body -ContentType "application/json"
```

### Test 2: Get Profile Suggestions

```powershell
# Replace {email} with your profile email
Invoke-RestMethod -Uri "http://localhost:8000/api/v1/profiles/john.doe@example.com/suggested?limit=5" -Method GET
```

### Test 3: Use the Streamlit UI

1. Open http://localhost:8501 in your browser
2. Fill in the profile form
3. Submit and view matches

## Development Tips

### View Database in MongoDB Compass

1. Download [MongoDB Compass](https://www.mongodb.com/products/compass)
2. Install and open
3. Paste your MongoDB URI
4. Connect and browse the `qa_community` database

### View API Logs

Logs are displayed in the terminal where you run the FastAPI server.

### Clear Database (for testing)

```powershell
# Use MongoDB Compass or run via API
# Or connect via Python shell:
python
```

```python
from motor.motor_asyncio import AsyncIOMotorClient
import asyncio

async def clear_db():
    client = AsyncIOMotorClient("your-mongodb-uri")
    db = client["qa_community"]
    await db["profiles"].delete_many({})
    print("Database cleared")

asyncio.run(clear_db())
```

## Common Issues & Solutions

### Issue: "Import could not be resolved" errors in VS Code

**Solution:** These are just linting warnings. Make sure:
1. Virtual environment is activated
2. Python interpreter in VS Code is set to the venv Python
   - Press `Ctrl+Shift+P`
   - Type "Python: Select Interpreter"
   - Choose the one in `.\venv\Scripts\python.exe`

### Issue: "Connection refused" when accessing API

**Solution:**
- Ensure FastAPI server is running
- Check that port 8000 is not blocked by firewall
- Try accessing http://127.0.0.1:8000 instead

### Issue: MongoDB connection timeout

**Solution:**
1. Verify your IP is whitelisted in MongoDB Atlas
2. Check your internet connection
3. Verify the connection string in `.env` is correct
4. Ensure `<password>` is replaced with actual password
5. Check if any special characters in password need URL encoding

### Issue: Streamlit not connecting to API

**Solution:**
- Check API is running on port 8000
- Verify API_BASE_URL in streamlit_app.py or .env
- Check CORS settings in FastAPI (should allow all origins for development)

## Project Structure Overview

```
New Project/
├── app/                      # Backend application
│   ├── main.py              # FastAPI entry point
│   ├── config.py            # Configuration settings
│   ├── models/              # Pydantic data models
│   ├── repo/                # Database repository layer
│   ├── services/            # Business logic layer
│   ├── routers/             # API route handlers
│   └── utils/               # Utility functions
├── ui/                      # Frontend application
│   └── streamlit_app.py    # Streamlit UI
├── venv/                    # Virtual environment (created)
├── .env                     # Environment variables (created)
├── .env.example            # Environment template
├── requirements.txt        # Python dependencies
└── README.md              # Main documentation
```

## Next Steps

1. **Add More Profiles**: Create multiple test profiles to see matching in action
2. **Customize Skills**: Edit `app/utils/skills_catalog.py` to add domain-specific skills
3. **Tune Algorithm**: Adjust weights in `app/config.py` or `.env`
4. **Deploy**: Consider deployment options (Heroku, Railway, AWS, etc.)

## Support

For issues or questions:
1. Check the main README.md
2. Review API documentation at http://localhost:8000/docs
3. Check application logs in terminal
