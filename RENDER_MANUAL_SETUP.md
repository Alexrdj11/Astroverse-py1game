# 🚀 RENDER.COM DEPLOYMENT - MANUAL SETUP

## If render.yaml isn't working, use these EXACT settings in Render dashboard:

### 1. Create New Web Service
- Go to render.com → "New +" → "Web Service"
- Connect your GitHub repo

### 2. EXACT Settings to Use:

**Basic Settings:**
- Name: `astroventure-quiz`
- Environment: `Python 3`
- Region: `US West (Oregon)` or closest to you
- Branch: `main`

**Build & Deploy:**
- Build Command: `pip install Flask==2.3.3 google-generativeai==0.3.2 python-dotenv==1.0.0 gunicorn==20.1.0`
- Start Command: `gunicorn app:app --host 0.0.0.0 --port $PORT`

**Environment Variables:**
- Key: `GEMINI_API_KEY`
- Value: `AIzaSyAX3Fjr1UI7MO352LivU3L-Odkuu6yBCXs`

### 3. Advanced Settings (Optional):
- Auto-Deploy: `Yes`
- Root Directory: Leave empty (use root)

## Alternative: Use requirements-render.txt

If you want to use a requirements file:

**Build Command:** `pip install -r requirements-render.txt`

Make sure requirements-render.txt contains ONLY:
```
Flask==2.3.3
google-generativeai==0.3.2
python-dotenv==1.0.0
gunicorn==20.1.0
```

## ⚠️ IMPORTANT: 
Delete or rename your original `requirements.txt` file temporarily to avoid conflicts.

## Test Locally First:
```bash
cd "g:\astroverse_game\Astroverse-py1game"
python test_deployment.py
```

This will verify all imports work before deploying.
