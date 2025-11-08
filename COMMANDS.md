# 🎯 Quick Command Reference

## Local Development

```bash
# Run the app locally
streamlit run app.py

# Test if everything works
# - Upload a PDF
# - Ask a question
# - Check evaluation tab
```

---

## Git Commands

```bash
# Check status
git status

# Add all files
git add .

# Commit changes
git commit -m "Ready for deployment"

# Push to GitHub
git push origin main

# First time push
git remote add origin https://github.com/YOUR_USERNAME/rag-qa-system.git
git branch -M main
git push -u origin main
```

---

## Deployment

### Option 1: Streamlit Cloud (Recommended)
1. Go to: https://share.streamlit.io
2. Click "New app"
3. Select your repo
4. Add secrets
5. Deploy!

### Option 2: Manual Server
```bash
# Install dependencies
pip install -r requirements.txt

# Run with custom port
streamlit run app.py --server.port 8080

# Run in background
nohup streamlit run app.py &
```

---

## Troubleshooting

```bash
# Check Python version
python --version
# Should be 3.8 or higher

# Check installed packages
pip list

# Reinstall requirements
pip install -r requirements.txt --upgrade

# Clear Streamlit cache
streamlit cache clear

# Check for errors
streamlit run app.py --logger.level=debug
```

---

## Useful Links

- **Streamlit Cloud:** https://share.streamlit.io
- **GitHub:** https://github.com
- **OpenAI API Keys:** https://platform.openai.com/api-keys
- **OpenAI Usage:** https://platform.openai.com/usage

---

## Environment Variables

### Local (.env file)
```bash
OPENAI_API_KEY=sk-proj-your-key-here
```

### Streamlit Cloud (Secrets)
```toml
OPENAI_API_KEY = "sk-proj-your-key-here"
```

---

## Quick Tests

### Test 1: API Key
```python
import os
print(os.getenv('OPENAI_API_KEY'))
# Should print your key
```

### Test 2: Imports
```python
import streamlit as st
from src.rag_engine import RAGEngine
print("✅ All imports working!")
```

### Test 3: App Loads
```bash
streamlit run app.py
# Should open browser at localhost:8501
```

---

## File Locations

```
Local Development:
- Code: C:\Users\91863\Desktop\rag\
- Data: C:\Users\91863\Desktop\rag\data\chroma_db\
- Config: C:\Users\91863\Desktop\rag\.env

Streamlit Cloud:
- Code: GitHub repository
- Data: /tmp/ (temporary!)
- Config: Streamlit Cloud secrets
```

---

## Common Issues

### "Module not found"
```bash
pip install -r requirements.txt
```

### "API key not found"
```bash
# Check .env file exists
cat .env

# Or check Streamlit secrets
# Go to app settings → Secrets
```

### "Port already in use"
```bash
# Kill process on port 8501
# Windows:
netstat -ano | findstr :8501
taskkill /F /PID <PID>

# Or use different port
streamlit run app.py --server.port 8502
```

---

## Monitoring

### Check Logs
```bash
# Streamlit Cloud
# Go to app → View logs

# Local
# Logs appear in terminal
```

### Check Usage
```bash
# OpenAI usage
# https://platform.openai.com/usage

# Streamlit Cloud usage
# https://share.streamlit.io → Your app → Analytics
```

---

## Updates

### Update Code
```bash
# Make changes
git add .
git commit -m "Update feature"
git push

# Streamlit Cloud auto-deploys!
```

### Update Dependencies
```bash
# Edit requirements.txt
# Commit and push
git add requirements.txt
git commit -m "Update dependencies"
git push
```

---

## Backup

### Backup Database
```bash
# Local
cp -r data/chroma_db data/chroma_db_backup

# Or zip it
tar -czf chroma_backup.tar.gz data/chroma_db
```

### Backup Code
```bash
# Already on GitHub!
# Just make sure you pushed latest changes
git push origin main
```

---

**Keep this file handy for quick reference! 📌**
