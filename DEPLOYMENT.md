# 🚀 Deployment Guide - Render.com

## Quick Deployment Steps

### 1. Prepare Your Repository
```bash
# Remove sensitive data from .env (it's already in .gitignore)
# Make sure these files are in your project:
# - app.py (updated for production)
# - requirements-production.txt
# - render.yaml
# - .gitignore
```

### 2. Push to GitHub
```bash
git init
git add .
git commit -m "Initial commit - Astroventure ready for deployment"
git branch -M main
git remote add origin https://github.com/yourusername/astroventure-quiz.git
git push -u origin main
```

### 3. Deploy on Render.com

1. **Create Render Account**
   - Go to [render.com](https://render.com)
   - Sign up with GitHub

2. **Create New Web Service**
   - Click "New +" → "Web Service"
   - Connect your GitHub repository
   - Select your astroventure-quiz repo

3. **Configure Deployment**
   - **Name**: `astroventure-quiz`
   - **Runtime**: `Python 3`
   - **Build Command**: `pip install -r requirements-production.txt`
   - **Start Command**: `gunicorn app:app`
   - **Plan**: `Free` (or paid for better performance)

4. **Set Environment Variables**
   - Go to "Environment" tab
   - Add: `GEMINI_API_KEY` = `your_gemini_api_key_here`
   - ⚠️ **Important**: Use your actual API key, not the one from .env

5. **Deploy**
   - Click "Create Web Service"
   - Wait for deployment (5-10 minutes)
   - Your app will be live at: `https://astroventure-quiz.onrender.com`

### 4. Custom Domain (Optional)
- Go to "Settings" → "Custom Domains"
- Add your domain if you have one

## Production Environment Variables

Set these in Render.com dashboard:

```
GEMINI_API_KEY=your_actual_gemini_api_key
FLASK_ENV=production
```

## Troubleshooting

### Common Issues:

**Build Fails**
- Check if `requirements-production.txt` has correct dependencies
- Make sure Python version is compatible

**App Won't Start**
- Verify `gunicorn app:app` command
- Check that `app.py` has the updated production code

**API Key Not Working**
- Ensure environment variable is set correctly in Render dashboard
- Double-check your Gemini API key is valid

**Questions Not Generating**
- Check Render logs for API errors
- Ensure your API key has quota remaining

### Viewing Logs
- In Render dashboard → "Logs" tab
- Watch for errors during startup

## Free Tier Limitations

Render.com free tier:
- ✅ 512MB RAM
- ✅ Shared CPU
- ✅ Custom domains
- ⚠️ Sleeps after 15 minutes of inactivity
- ⚠️ 750 hours/month limit

## Upgrade Recommendations

For production use:
- **Starter Plan ($7/month)**: No sleep, more resources
- **Standard Plan ($25/month)**: Better performance, monitoring

## Post-Deployment Checklist

- [ ] App loads at your Render URL
- [ ] All three difficulty levels work
- [ ] AI questions generate properly
- [ ] Animations and visuals work
- [ ] Mobile responsiveness verified
- [ ] Custom domain configured (if applicable)

---

🎉 **Congratulations!** Your Astroventure quiz is now live on the internet!

Share your deployed game:
- 🌐 **Live URL**: `https://astroventure-quiz.onrender.com`
- 📱 **Mobile Friendly**: Works on all devices
- 🤖 **AI-Powered**: Unique questions every time
