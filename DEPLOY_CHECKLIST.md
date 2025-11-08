# 🚀 Streamlit Cloud Deployment Checklist

## Before You Start

- [ ] Have OpenAI API key ready
- [ ] Have GitHub account
- [ ] Have Streamlit Cloud account (free at share.streamlit.io)

---

## Step 1: Prepare Code (✅ DONE!)

- [x] Updated app.py with Streamlit secrets support
- [x] Created .gitignore
- [x] Created requirements.txt
- [x] Created packages.txt
- [x] Created .streamlit/secrets.toml.example
- [x] Tested locally

---

## Step 2: Push to GitHub

```bash
# 1. Initialize git (if not done)
git init

# 2. Add all files
git add .

# 3. Commit
git commit -m "Ready for Streamlit Cloud deployment"

# 4. Create repo on GitHub.com
# Go to github.com → New repository → Name it "rag-qa-system"

# 5. Push to GitHub
git remote add origin https://github.com/YOUR_USERNAME/rag-qa-system.git
git branch -M main
git push -u origin main
```

**Checklist:**
- [ ] Code pushed to GitHub
- [ ] Repository is public or you have Streamlit Cloud paid plan
- [ ] All files visible on GitHub

---

## Step 3: Deploy on Streamlit Cloud

### 3.1 Sign In
- [ ] Go to https://share.streamlit.io
- [ ] Click "Sign in with GitHub"
- [ ] Authorize Streamlit

### 3.2 Create New App
- [ ] Click "New app"
- [ ] Select repository: `your-username/rag-qa-system`
- [ ] Branch: `main`
- [ ] Main file path: `app.py`
- [ ] App URL: Choose a name (e.g., `my-rag-app`)

### 3.3 Configure Secrets
- [ ] Click "Advanced settings"
- [ ] Click "Secrets"
- [ ] Paste this (with YOUR actual key):

```toml
OPENAI_API_KEY = "sk-proj-YOUR-ACTUAL-KEY-HERE"
```

- [ ] Click "Save"

### 3.4 Deploy
- [ ] Click "Deploy!"
- [ ] Wait 2-5 minutes
- [ ] Watch build logs for any errors

---

## Step 4: Test Your App

Once deployed:

- [ ] App loads successfully
- [ ] No error messages
- [ ] Upload a test PDF
- [ ] PDF processes successfully
- [ ] Ask a test question
- [ ] Answer is generated
- [ ] Sources are shown

---

## Step 5: Share with Client

- [ ] Copy app URL: `https://your-app-name.streamlit.app`
- [ ] Test in incognito/private browser
- [ ] Share URL with client
- [ ] Provide usage instructions

---

## 🐛 Troubleshooting

### Build Failed?

**Check:**
- [ ] requirements.txt has all packages
- [ ] No syntax errors in code
- [ ] View logs for specific error

**Common fixes:**
```bash
# Update requirements.txt
# Commit and push
git add requirements.txt
git commit -m "Fix requirements"
git push
# App will auto-redeploy
```

### API Key Not Working?

**Check:**
- [ ] Secrets are saved correctly
- [ ] No extra spaces in API key
- [ ] API key is valid (test on OpenAI platform)

**Fix:**
1. Go to app settings
2. Edit secrets
3. Save
4. App restarts automatically

### App Crashes on Upload?

**This is expected!** Streamlit Cloud has temporary storage.

**Add warning to users:**
```python
st.warning("⚠️ Uploaded documents are temporary and will be lost when the app restarts.")
```

---

## 📊 Monitor Your App

### Usage
- [ ] Check Streamlit Cloud dashboard
- [ ] Monitor app analytics
- [ ] View logs for errors

### Costs
- [ ] Monitor OpenAI usage: https://platform.openai.com/usage
- [ ] Set usage limits if needed
- [ ] Typical cost: $10-50/month

---

## 🎉 Success!

Your RAG QA System is now live and accessible to anyone with the URL!

**Next Steps:**
- Share with users
- Gather feedback
- Monitor usage
- Plan improvements

---

## 📞 Need Help?

- Streamlit Docs: https://docs.streamlit.io
- Community: https://discuss.streamlit.io
- This project: Open GitHub issue

---

**Deployment Date:** _____________

**App URL:** _____________

**Status:** ⬜ Not Started | ⬜ In Progress | ⬜ Deployed | ⬜ Live
