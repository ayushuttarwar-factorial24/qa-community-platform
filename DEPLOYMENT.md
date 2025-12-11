# Deployment Guide

## ⚠️ Important MongoDB Free Tier Information

**MongoDB Atlas Free Tier (M0)**:
- Storage: 512 MB
- RAM: Shared
- Best for: Development, prototypes, small applications

**Capacity Estimate for 250 Users**:
- Average profile size: ~2 KB (with all fields)
- 250 profiles ≈ 500 KB (0.5 MB)
- With indexes and overhead: ~1.5-2 MB total
- **Verdict**: ✅ 512 MB is MORE than enough for 250 users!

**When to upgrade**: If you exceed 300-400 active profiles or need better performance.

---

## 🚀 Recommended Deployment: Streamlit Community Cloud (FREE)

This is the easiest and FREE option for deploying your app!

### Prerequisites
- GitHub account (free)
- MongoDB Atlas cluster (free tier: 512 MB - perfect for 250 users)
- Streamlit Community Cloud account (free)

### Step 1: Prepare Your Repository

1. **Create `.streamlit/config.toml`** (for Streamlit settings):
   ```toml
   [theme]
   primaryColor = "#667eea"
   backgroundColor = "#ffffff"
   secondaryBackgroundColor = "#f0f2f6"
   textColor = "#262730"
   
   [server]
   headless = true
   port = 8501
   enableCORS = false
   ```

2. **Create `requirements.txt`** (if not exists):
   ```
   streamlit>=1.28.0
   requests>=2.31.0
   python-dotenv>=1.0.0
   fastapi>=0.104.1
   uvicorn[standard]>=0.24.0
   motor>=3.3.2
   pydantic>=2.5.0
   pydantic-settings>=2.1.0
   pydantic[email]>=2.5.0
   pymongo>=4.6.0
   ```

3. **Create `.gitignore`**:
   ```
   .env
   __pycache__/
   *.pyc
   .venv/
   venv/
   .streamlit/secrets.toml
   ```

### Step 2: Push to GitHub

```powershell
git init
git add .
git commit -m "Deploy QA Community Platform"
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/qa-community-platform.git
git push -u origin main
```

### Step 3: Deploy Backend (FastAPI) - Railway (FREE)

1. Go to [Railway](https://railway.app)
2. Sign in with GitHub
3. Click "New Project" → "Deploy from GitHub repo"
4. Select your repository
5. Add environment variables:
   - `MONGODB_URI`: Your MongoDB Atlas connection string
   - `MONGODB_DB_NAME`: `qa_community`
6. In Settings, add start command:
   ```
   uvicorn app.main:app --host 0.0.0.0 --port $PORT
   ```
7. Copy your backend URL (e.g., `https://your-app.railway.app`)

### Step 4: Deploy Frontend (Streamlit Cloud) - FREE

1. Go to [share.streamlit.io](https://share.streamlit.io)
2. Sign in with GitHub
3. Click "New app"
4. Select:
   - Repository: Your GitHub repo
   - Branch: `main`
   - Main file path: `ui/streamlit_app.py`
5. Click "Advanced settings"
6. Add secrets (these are like environment variables):
   ```toml
   API_BASE_URL = "https://your-backend-url.railway.app"
   DEFAULT_MATCH_LIMIT = "5"
   ```
7. Click "Deploy"
8. Your app will be live at: `https://your-app.streamlit.app`

### Step 5: Test Your Deployment

1. Visit your Streamlit app URL
2. Create a test profile
3. View matches
4. Test the leaderboard
5. Verify connections work

---

## Alternative: Deploy Backend on Render (FREE)

If you prefer Render for backend:

1. Go to [Render](https://render.com)
2. Create new "Web Service"
3. Connect GitHub repository
4. Configure:
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`
5. Add environment variables:
   - `MONGODB_URI`
   - `MONGODB_DB_NAME`

---

## 📊 MongoDB Atlas Setup (FREE Tier)

### Create Free Cluster

1. Go to [MongoDB Atlas](https://www.mongodb.com/cloud/atlas)
2. Sign up / Log in
3. Create new project: "QA Community"
4. Build a cluster:
   - Choose FREE tier (M0)
   - Select region closest to you
   - Cluster name: `qa-community-db`

### Configure Access

1. **Database Access**:
   - Create database user
   - Username: `qa_admin`
   - Password: Generate secure password
   - User Privileges: "Atlas admin"

2. **Network Access**:
   - Click "Add IP Address"
   - Select "Allow Access from Anywhere" (0.0.0.0/0)
   - For production, restrict to your app IPs

3. **Get Connection String**:
   - Click "Connect"
   - Choose "Connect your application"
   - Copy connection string:
     ```
     mongodb+srv://qa_admin:<password>@qa-community-db.xxxxx.mongodb.net/?retryWrites=true&w=majority
     ```
   - Replace `<password>` with your actual password

---

## 🔒 Security Best Practices

1. **Never commit `.env` file** to GitHub
2. **Use secrets/environment variables** for sensitive data
3. **Rotate MongoDB password** periodically
4. **Enable MongoDB backup** (available in paid tiers)
5. **Monitor usage** in MongoDB Atlas dashboard

---

## 📈 Scaling Considerations

### When to Upgrade MongoDB:

| Tier | Storage | RAM | Price | Best For |
|------|---------|-----|-------|----------|
| M0 (Free) | 512 MB | Shared | $0 | Up to 400 users |
| M2 | 2 GB | Shared | $9/mo | 400-2000 users |
| M5 | 5 GB | 2 GB | $25/mo | 2000+ users |

### When to Upgrade Hosting:

**Streamlit Cloud (Free)**:
- 1 GB RAM
- Good for: 100-500 concurrent users
- Upgrade if: App becomes slow or times out

**Railway (Free)**:
- $5 free credit/month
- Good for: Development and small apps
- Upgrade to hobby plan: $5/month for more resources

---

## 🎯 Cost Summary for 250 Users

| Service | Plan | Cost | Notes |
|---------|------|------|-------|
| MongoDB Atlas | M0 Free | $0 | 512 MB is perfect |
| Backend (Railway) | Free Tier | $0* | $5 free credit |
| Frontend (Streamlit) | Community Cloud | $0 | Unlimited |
| **Total** | | **$0/month** | ✅ Completely FREE! |

*Railway free tier renews monthly

---

## 🚨 Troubleshooting

### App is slow
- Check MongoDB Atlas metrics
- Verify Railway/Render isn't sleeping (free tier may sleep)
- Consider adding Redis cache

### Connection errors
- Verify MongoDB URI in environment variables
- Check IP whitelist in MongoDB Atlas
- Ensure backend is running

### Deployment fails
- Check build logs
- Verify all dependencies in requirements.txt
- Ensure Python version compatibility (3.9+)

---

## 📞 Support

- Streamlit Docs: https://docs.streamlit.io
- Railway Docs: https://docs.railway.app  
- MongoDB Atlas Docs: https://docs.atlas.mongodb.com

---

## ✅ Deployment Checklist

- [ ] MongoDB Atlas cluster created and configured
- [ ] Connection string obtained and tested locally
- [ ] Code pushed to GitHub
- [ ] Backend deployed (Railway/Render)
- [ ] Backend URL obtained
- [ ] Frontend deployed (Streamlit Cloud)
- [ ] Environment variables/secrets configured
- [ ] Test profile creation works
- [ ] Test matching works
- [ ] Test leaderboard works
- [ ] Test connections work

**Congratulations! Your app is live! 🎉**

1. **Create `render.yaml`**
   ```yaml
   services:
     - type: web
       name: qa-community-api
       env: python
       buildCommand: pip install -r requirements.txt
       startCommand: uvicorn app.main:app --host 0.0.0.0 --port $PORT
       envVars:
         - key: MONGODB_URI
           sync: false
         - key: MONGODB_DB_NAME
           value: qa_community
   ```

2. **Deploy**
   - Push to GitHub
   - Go to [Render](https://render.com)
   - New → Blueprint → Connect repository
   - Add MONGODB_URI secret

### Frontend (Streamlit) on Streamlit Cloud

1. Go to [Streamlit Cloud](https://streamlit.io/cloud)
2. Connect GitHub repository
3. Set main file: `ui/streamlit_app.py`
4. Add secrets in dashboard:
   ```toml
   API_BASE_URL = "https://your-render-api-url.com"
   ```

## Option 3: Docker Deployment

### Create Dockerfiles

**Backend Dockerfile** (`Dockerfile.api`):
```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app/ app/

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

**Frontend Dockerfile** (`Dockerfile.ui`):
```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY ui/ ui/
COPY app/utils/ app/utils/

EXPOSE 8501

CMD ["streamlit", "run", "ui/streamlit_app.py", "--server.port=8501", "--server.address=0.0.0.0"]
```

**docker-compose.yml**:
```yaml
version: '3.8'

services:
  api:
    build:
      context: .
      dockerfile: Dockerfile.api
    ports:
      - "8000:8000"
    environment:
      - MONGODB_URI=${MONGODB_URI}
      - MONGODB_DB_NAME=qa_community
    restart: unless-stopped

  ui:
    build:
      context: .
      dockerfile: Dockerfile.ui
    ports:
      - "8501:8501"
    environment:
      - API_BASE_URL=http://api:8000
    depends_on:
      - api
    restart: unless-stopped
```

### Deploy with Docker

```powershell
# Build and run
docker-compose up -d

# View logs
docker-compose logs -f

# Stop
docker-compose down
```

## Option 4: AWS Deployment

### Backend on AWS EC2

1. **Launch EC2 Instance**
   - Ubuntu 22.04 LTS
   - t2.micro (free tier)
   - Open ports: 22 (SSH), 8000 (API)

2. **SSH and Setup**
   ```bash
   ssh -i your-key.pem ubuntu@your-ec2-ip
   
   # Update system
   sudo apt update && sudo apt upgrade -y
   
   # Install Python
   sudo apt install python3-pip python3-venv -y
   
   # Clone repository
   git clone https://github.com/yourusername/qa-community-platform.git
   cd qa-community-platform
   
   # Setup virtual environment
   python3 -m venv venv
   source venv/bin/activate
   
   # Install dependencies
   pip install -r requirements.txt
   
   # Create .env file
   nano .env
   # Add your MongoDB URI and other config
   
   # Run with screen or tmux
   screen -S api
   uvicorn app.main:app --host 0.0.0.0 --port 8000
   # Detach: Ctrl+A, D
   ```

3. **Use systemd for Production**
   
   Create `/etc/systemd/system/qa-api.service`:
   ```ini
   [Unit]
   Description=QA Community API
   After=network.target

   [Service]
   User=ubuntu
   WorkingDirectory=/home/ubuntu/qa-community-platform
   Environment="PATH=/home/ubuntu/qa-community-platform/venv/bin"
   ExecStart=/home/ubuntu/qa-community-platform/venv/bin/uvicorn app.main:app --host 0.0.0.0 --port 8000

   [Install]
   WantedBy=multi-user.target
   ```

   ```bash
   sudo systemctl daemon-reload
   sudo systemctl enable qa-api
   sudo systemctl start qa-api
   sudo systemctl status qa-api
   ```

## Environment Variables for Production

Create `.env.production`:

```env
# MongoDB
MONGODB_URI=mongodb+srv://user:pass@cluster.mongodb.net/?retryWrites=true&w=majority
MONGODB_DB_NAME=qa_community

# API
API_HOST=0.0.0.0
API_PORT=8000
API_RELOAD=false

# CORS (restrict in production)
ALLOWED_ORIGINS=https://your-frontend-domain.com

# Logging
LOG_LEVEL=INFO
```

## Security Checklist for Production

- [ ] Use HTTPS (SSL/TLS certificates)
- [ ] Restrict CORS origins to specific domains
- [ ] Use strong MongoDB passwords
- [ ] Enable MongoDB authentication and authorization
- [ ] Whitelist only necessary IPs in MongoDB Atlas
- [ ] Use environment variables for all secrets
- [ ] Enable API rate limiting
- [ ] Set up monitoring and logging
- [ ] Regular security updates
- [ ] Implement authentication (OAuth2/JWT)
- [ ] Use a reverse proxy (Nginx/Caddy)

## Monitoring & Maintenance

### Health Checks

API provides `/health` endpoint:
```bash
curl https://your-api-url.com/health
```

### Logging

Configure structured logging in production:

```python
# In app/main.py
import logging
import sys

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler('/var/log/qa-api/app.log')
    ]
)
```

### Backups

Regular MongoDB backups:
- Use MongoDB Atlas automated backups
- Or set up manual backup scripts
- Test restore procedures

## Scaling Considerations

As your user base grows:

1. **Database Indexing**: Already implemented in ProfileRepository
2. **Caching**: Add Redis for frequent queries
3. **Load Balancing**: Use multiple API instances
4. **CDN**: Serve static content via CDN
5. **Async Processing**: Move heavy computations to background workers
6. **Database Optimization**: Consider read replicas

## Cost Estimates (Monthly)

**Free Tier:**
- MongoDB Atlas: Free (M0 cluster)
- Railway: Free tier with limits
- Streamlit Cloud: Free tier
- **Total: $0/month** (development)

**Production (Small Scale):**
- MongoDB Atlas M2: ~$9/month
- Railway Hobby: ~$5/month (API)
- Streamlit Cloud: Free
- **Total: ~$14/month**

**Production (Medium Scale):**
- MongoDB Atlas M10: ~$57/month
- AWS EC2 t3.small: ~$15/month
- AWS RDS: ~$25/month
- Load Balancer: ~$18/month
- **Total: ~$115/month**

## Rollback Strategy

Always maintain the ability to rollback:

```bash
# Tag releases
git tag -a v1.0.0 -m "Release 1.0.0"
git push origin v1.0.0

# Rollback if needed
git checkout v1.0.0
# Redeploy
```

## Support & Resources

- [FastAPI Deployment Docs](https://fastapi.tiangolo.com/deployment/)
- [Streamlit Deployment Docs](https://docs.streamlit.io/streamlit-cloud/get-started/deploy-an-app)
- [MongoDB Atlas Docs](https://docs.atlas.mongodb.com/)
