# 🎯 QUICK REFERENCE CARD

## 📦 Files You Need
```
✅ app.py              - Main API code
✅ requirements.txt    - Dependencies
✅ test_api.py         - Testing script
```

## 🚀 Deploy on Render (5 Steps)
```
1. GitHub: Upload files to new repo
2. Render: Sign up → New Web Service
3. Connect: Link GitHub repo
4. Configure:
   Build: pip install -r requirements.txt
   Start: uvicorn app:app --host 0.0.0.0 --port $PORT
5. Deploy: Wait 10 min → Get URL
```

## 🧪 Test Your API
```bash
# Get base64 audio
python -c "import base64; print(base64.b64encode(open('test.mp3','rb').read()).decode())"

# Test endpoint
curl -X POST https://YOUR-URL/detect \
  -H "Authorization: Bearer your-secure-api-key-12345" \
  -H "Content-Type: application/json" \
  -d '{"audio_base64":"BASE64_HERE","language":"english"}'
```

## 📤 Submission Format
```
Endpoint: https://your-app.onrender.com/detect
API Key: Bearer your-secure-api-key-12345
Message: Testing AI Voice Detection API for multi-language classification
```

## ✅ Response Format
```json
{
  "classification": "AI_GENERATED",
  "confidence": 0.87,
  "language": "english",
  "explanation": "Audio exhibits..."
}
```

## 🔑 Supported Languages
```
tamil | english | hindi | malayalam | telugu
```

## 🐛 Common Fixes
```
❌ 401 Error → Check: "Bearer API_KEY" format
❌ Module Error → Run: pip install -r requirements.txt
❌ Audio Error → Ensure MP3 format, valid base64
❌ Timeout → Wait for cold start, try smaller file
```

## ⚡ Quick Commands
```bash
# Install
pip install fastapi uvicorn librosa numpy soundfile

# Run locally
python app.py

# Create test audio
python download_samples.py

# Test
python test_api.py
```

## 📋 Pre-Submit Checklist
```
☐ API deployed and accessible
☐ Tested with sample audio
☐ Returns correct JSON format
☐ All 5 languages work
☐ Response time < 10 seconds
☐ API key saved
☐ URL saved
```

## 🆘 Help
```
Logs: Check Render dashboard → Logs tab
Restart: Render → Manual Deploy → Clear cache
Test: Use hackathon's endpoint tester first
```

---
**Total Time: ~90 minutes from zero to submission**
