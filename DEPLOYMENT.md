# Deployment Guide - Streamlit Cloud

## 🚀 Quick Deployment Steps

### 1. Push to GitHub

```bash
# Initialize git (if not already done)
git init

# Add all files
git add .

# Commit
git commit -m "Ready for Streamlit Cloud deployment"

# Create GitHub repo and push
git remote add origin https://github.com/YOUR_USERNAME/rag-qa-system.git
git branch -M main
git push -u origin main
```

### 2. Deploy on Streamlit Cloud

1. **Go to:** https://share.streamlit.io
2. **Sign in** with GitHub
3. **Click** "New app"
4. **Select:**
   - Repository: `your-username/rag-qa-system`
   - Branch: `main`
   - Main file path: `app.py`
5. **Click** "Advanced settings"
6. **Add Secrets** (copy from `.streamlit/secrets.toml.example`):

```toml
OPENAI_API_KEY = "sk-proj-your-actual-key-here"
```

7. **Click** "Deploy!"
8. **Wait** 2-5 minutes for deployment

### 3. Your App is Live! 🎉

Your app will be available at:
```
https://your-app-name.streamlit.app
```

---

## ⚠️ Important Notes

### Data Persistence

**Warning:** Streamlit Cloud has ephemeral storage. Uploaded documents will be lost when the app restarts.

**For Production:**
- Consider using Pinecone (free tier available)
- Or AWS S3 for persistent storage
- See README.md for details

### API Costs

- You pay for OpenAI API usage
- Monitor usage at: https://platform.openai.com/usage
- Typical cost: $10-50/month depending on usage

### Free Tier Limits

Streamlit Cloud Free Tier:
- 1 private app
- Unlimited public apps
- 1GB RAM
- Community support

---

## 🔧 Troubleshooting

### Build Fails

**Error:** `ModuleNotFoundError`

**Fix:** Check `requirements.txt` has all dependencies

### API Key Not Working

**Error:** `OpenAI API key not found`

**Fix:** 
1. Go to app settings → Secrets
2. Verify `OPENAI_API_KEY` is set correctly
3. Save and restart app

### App Crashes on Upload

**Error:** `PermissionError`

**Fix:** This is expected - storage is temporary. Add warning to users.

---

## 📊 Monitoring

### Check App Status

- Dashboard: https://share.streamlit.io
- Logs: Click your app → View logs
- Metrics: View app analytics

### Monitor API Usage

- OpenAI Dashboard: https://platform.openai.com/usage
- Set usage limits to avoid surprises

---

## 🔄 Updating Your App

```bash
# Make changes to your code
git add .
git commit -m "Update feature"
git push origin main

# Streamlit Cloud will auto-deploy!
```

---

## 💰 Cost Estimate

### Free Deployment

- Streamlit Cloud: $0 (free tier)
- OpenAI API: $10-50/month (usage-based)
- **Total: $10-50/month**

### Paid Deployment (if needed)

- Streamlit Cloud: $20/month (more resources)
- OpenAI API: $10-50/month
- Persistent Storage: $5-10/month
- **Total: $35-80/month**

---

## 📞 Support

- Streamlit Docs: https://docs.streamlit.io
- Community Forum: https://discuss.streamlit.io
- GitHub Issues: Create issue in your repo

---

## ✅ Deployment Checklist

Before deploying:
- [ ] All code committed to GitHub
- [ ] `.gitignore` includes `.env` and `secrets.toml`
- [ ] `requirements.txt` is up to date
- [ ] Tested locally with `streamlit run app.py`
- [ ] Have OpenAI API key ready

During deployment:
- [ ] Signed in to Streamlit Cloud
- [ ] Repository connected
- [ ] Secrets configured
- [ ] App deployed successfully

After deployment:
- [ ] Tested file upload
- [ ] Tested chat functionality
- [ ] Shared URL with client
- [ ] Monitoring set up

---

Good luck with your deployment! 🚀
