# Streamlit Community Cloud Deployment Guide

## 🚀 Quick Deploy (5 minutes)

Your app is ready for **completely FREE** deployment on Streamlit Community Cloud!

---

## 📋 Step 1: Push to GitHub

```bash
cd "E:\New Project"
git add .
git commit -m "Ready for Streamlit Cloud deployment"
git push origin main
```

---

## 📋 Step 2: Deploy on Streamlit Cloud

1. Go to [share.streamlit.io](https://share.streamlit.io)
2. Sign in with GitHub
3. Click **"New app"**
4. Configure:
   - **Repository**: `ayushuttarwar-factorial24/qa-community-platform`
   - **Branch**: `main`
   - **Main file path**: `ui/streamlit_app.py`
5. Click **"Deploy!"**

---

## 📋 Step 3: Add Secrets (CRITICAL!)

⚠️ **The app will NOT work without this step!**

1. In Streamlit Cloud dashboard, click your app
2. Click **Settings** (⚙️ gear icon)
3. Click **Secrets**
4. Paste this configuration:

```toml
[mongodb]
uri = "mongodb+srv://ayushuttarwar_db_user:tyClHreg6QKmRqNt@cluster0.fa2zknm.mongodb.net/?appName=Cluster0"
database = "qa_community_v2"

[app]
default_match_limit = 5
max_connections_per_user = 5
```

5. Click **Save**
6. App will restart automatically

---

## 📋 Step 4: Configure MongoDB Atlas

Allow Streamlit Cloud to connect to your database:

1. Go to [MongoDB Atlas](https://cloud.mongodb.com)
2. Click **Network Access** (left sidebar)
3. Click **"Add IP Address"**
4. Select **"Allow Access from Anywhere"** (`0.0.0.0/0`)
5. Click **Confirm**

---

## ✅ Verification

After deployment, test these features:

| Feature | Test |
|---------|------|
| ✅ Create Profile | Fill form, submit |
| ✅ View Matches | Should show other profiles |
| ✅ Leaderboard | Shows ranked profiles |
| ✅ Connect | Click connect, LinkedIn opens |
| ✅ My Profile | Load by email |

---

## 🔧 Troubleshooting

### "Connection failed" error
- Check MongoDB secrets are correct
- Verify Atlas IP whitelist includes `0.0.0.0/0`
- Check database name is `qa_community`

### App crashes on load
- View logs: Settings → Logs
- Check `ui/requirements.txt` is correct

### "Module not found" error
- Ensure `ui/services/` folder exists
- Check all `__init__.py` files are present

---

## 📊 Resource Usage

| Resource | Limit | Your Usage |
|----------|-------|------------|
| MongoDB Storage | 512 MB | ~2 MB (24 profiles) |
| Profiles Capacity | ~640,000 | 24 current |
| Concurrent Users | ~50 | Expected: 10-20 |

**Verdict**: ✅ You're using less than 1% of available resources!

---

## 🔄 Updating Your App

Any push to `main` branch auto-deploys:

```bash
git add .
git commit -m "Your update"
git push origin main
# ✅ App updates automatically in ~1 minute
```

---

## 💰 Total Cost: $0/month

| Service | Cost |
|---------|------|
| Streamlit Community Cloud | FREE |
| MongoDB Atlas (Free Tier) | FREE |
| **Total** | **$0** |

---

## 🎉 You're Done!

Your app URL will be:
```
https://qa-community-platform-xxxxx.streamlit.app
```

Share this URL with your 250 QA community members! 🚀
