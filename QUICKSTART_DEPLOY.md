# ⚡ Quick Start - Deploy in 10 Minutes

## 1️⃣ Push to GitHub (2 minutes)

```bash
git init
git add .
git commit -m "Initial commit"
git remote add origin https://github.com/YOUR_USERNAME/rag-qa-system.git
git push -u origin main
```

## 2️⃣ Deploy to Streamlit Cloud (5 minutes)

1. Go to: **https://share.streamlit.io**
2. Click: **"New app"**
3. Select: **Your repository**
4. Click: **"Advanced settings"**
5. Add secret:
   ```toml
   OPENAI_API_KEY = "sk-proj-your-key"
   ```
6. Click: **"Deploy!"**

## 3️⃣ Done! (3 minutes)

Wait for build... then your app is live at:
```
https://your-app-name.streamlit.app
```

---

## 🎯 That's It!

**Total Time:** ~10 minutes

**Cost:** $0 (Streamlit Cloud free tier)

**What You Get:**
- ✅ Live web app
- ✅ HTTPS included
- ✅ Auto-updates from GitHub
- ✅ Shareable URL

---

## 📝 Your Secrets Configuration

When deploying, copy this into Streamlit Cloud secrets:

```toml
OPENAI_API_KEY = "sk-proj-YOUR-ACTUAL-OPENAI-KEY-HERE"
```

**Where to find your OpenAI key:**
https://platform.openai.com/api-keys

---

## ✅ Test Your Deployment

1. Open your app URL
2. Upload a PDF
3. Ask a question
4. Get an answer!

If it works → **Success!** 🎉

If not → Check [DEPLOYMENT.md](DEPLOYMENT.md) for troubleshooting

---

## 🔄 Update Your App

```bash
# Make changes
git add .
git commit -m "Update"
git push

# Streamlit auto-deploys! ✨
```

---

**Need detailed instructions?** See [DEPLOYMENT.md](DEPLOYMENT.md)

**Having issues?** See [DEPLOY_CHECKLIST.md](DEPLOY_CHECKLIST.md)
