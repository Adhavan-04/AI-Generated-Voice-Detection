# 🏆 HACKATHON COMPLETION GUIDE - Step by Step

## ⏱️ Timeline: Complete in 2-3 Hours

---

## 📋 PHASE 1: Setup (15 minutes)

### Step 1.1: Choose Your Version
You have 2 versions:
- **`app.py`** - Basic version (simpler, faster to deploy)
- **`app_advanced.py`** - Advanced version (better accuracy)

**Recommendation:** Start with `app.py` for faster deployment

### Step 1.2: Install Dependencies Locally (Optional - for testing)

```bash
# Open terminal/command prompt
pip install -r requirements.txt
```

If you get errors, install individually:
```bash
pip install fastapi uvicorn librosa numpy soundfile
```

### Step 1.3: Test Locally (Optional but Recommended)

```bash
# Run the server
python app.py

# Keep this terminal open
# The server will run at http://localhost:8000
```

Open another terminal and test:
```bash
# First, get a sample audio file
python download_samples.py
# Choose option 1 to create test files

# Then test the API
python test_api.py
```

---

## 🚀 PHASE 2: Deploy to Cloud (30-45 minutes)

### OPTION A: Render.com (EASIEST - RECOMMENDED)

#### Step 2A.1: Create GitHub Repository

1. Go to https://github.com/new
2. Repository name: `ai-voice-detection`
3. Make it Public
4. Click "Create repository"

#### Step 2A.2: Upload Your Code to GitHub

**If you have Git installed:**
```bash
git init
git add .
git commit -m "Initial commit"
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/ai-voice-detection.git
git push -u origin main
```

**If you DON'T have Git:**
1. Download GitHub Desktop: https://desktop.github.com/
2. File → New Repository → Choose your project folder
3. Publish repository to GitHub

**Alternative - Upload via Web:**
1. Go to your GitHub repo
2. Click "uploading an existing file"
3. Drag all files (app.py, requirements.txt, etc.)
4. Commit changes

#### Step 2A.3: Deploy on Render

1. Go to https://render.com/
2. Sign up (use GitHub account - easier)
3. Click "New +" → "Web Service"
4. Click "Connect account" → authorize GitHub
5. Select your `ai-voice-detection` repository
6. Fill in:
   - **Name:** `ai-voice-detector` (or any name)
   - **Region:** Choose closest to you
   - **Branch:** main
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `uvicorn app:app --host 0.0.0.0 --port $PORT`
   - **Instance Type:** Free
7. Click "Create Web Service"

#### Step 2A.4: Wait for Deployment (5-10 minutes)

- Watch the logs - it will install dependencies
- Wait for "Your service is live 🎉"
- Copy your URL: `https://ai-voice-detector.onrender.com`

---

### OPTION B: Railway.app (FAST ALTERNATIVE)

1. Go to https://railway.app/
2. Sign up with GitHub
3. "New Project" → "Deploy from GitHub repo"
4. Select your repository
5. Add environment variable:
   - **Key:** `PORT`
   - **Value:** `8000`
6. Railway auto-detects Python
7. In Settings → add Start Command: 
   ```
   uvicorn app:app --host 0.0.0.0 --port $PORT
   ```
8. Get your URL from "Settings" → "Domains" → "Generate Domain"

---

### OPTION C: Koyeb (ALTERNATIVE)

1. Go to https://www.koyeb.com/
2. Sign up
3. "Create App" → "GitHub"
4. Connect repository
5. Configure:
   - **Build command:** `pip install -r requirements.txt`
   - **Run command:** `uvicorn app:app --host 0.0.0.0 --port $PORT`
6. Deploy and get URL

---

## 🧪 PHASE 3: Test Your Deployed API (15 minutes)

### Step 3.1: Get Test Audio

**Option 1: Use Google Drive Sample**
- Download the MP3 from the hackathon's Google Drive link
- Save as `test_audio.mp3`

**Option 2: Create Your Own**
```bash
python download_samples.py
# Choose option 1
# Use samples/sample_english.mp3
```

### Step 3.2: Convert Audio to Base64

**Using Python:**
```python
import base64

with open('test_audio.mp3', 'rb') as f:
    audio_b64 = base64.b64encode(f.read()).decode()
    
# Save to file
with open('audio_base64.txt', 'w') as f:
    f.write(audio_b64)

print("Base64 saved to audio_base64.txt")
```

**Using Online Tool:**
- Go to: https://base64.guru/converter/encode/audio
- Upload your MP3
- Copy the base64 string

### Step 3.3: Test with curl

```bash
# Replace YOUR_DEPLOYED_URL with your actual URL
curl -X POST https://YOUR_DEPLOYED_URL/detect \
  -H "Authorization: Bearer your-secure-api-key-12345" \
  -H "Content-Type: application/json" \
  -d '{
    "audio_base64": "YOUR_BASE64_STRING_HERE",
    "language": "english"
  }'
```

### Step 3.4: Test with Python Script

Update `test_api.py`:
```python
# Change this line
API_URL = "https://YOUR_DEPLOYED_URL/detect"

# Run
python test_api.py
```

### Step 3.5: Expected Response

```json
{
  "classification": "AI_GENERATED",
  "confidence": 0.87,
  "language": "english",
  "explanation": "Audio exhibits characteristics typical of AI-generated speech..."
}
```

✅ If you get this response, your API is working!

---

## 📤 PHASE 4: Submit to Hackathon (10 minutes)

### Step 4.1: Prepare Submission Details

**API Endpoint:**
```
https://your-app-name.onrender.com/detect
```
(Copy your actual deployed URL)

**API Key:**
```
Bearer your-secure-api-key-12345
```

**Test Message:**
```
Testing AI Voice Detection API for Tamil, English, Hindi, Malayalam, and Telugu voice classification with confidence scoring
```

### Step 4.2: Test on Hackathon's Endpoint Tester

1. Go to the hackathon portal
2. Find "AI-Generated Voice Detection – API Endpoint Tester"
3. Enter:
   - **Endpoint URL:** Your deployed URL
   - **Authorization Header:** `Bearer your-secure-api-key-12345`
   - **Message:** Your test message
   - **Audio File URL:** Either paste the hackathon's sample or upload yours
4. Click "Test Endpoint"
5. Verify it returns proper JSON response

### Step 4.3: Final Submission

1. Go to submission form
2. Enter:
   - **API Endpoint:** Your URL
   - **API Key:** Your key
3. Submit!

---

## 🔧 TROUBLESHOOTING

### Issue: Deployment Failed on Render

**Solution:**
- Check Build Logs in Render dashboard
- Ensure `requirements.txt` is correct
- Try using `requirements.txt` (basic) instead of `requirements_advanced.txt`

### Issue: "Module not found" Error

**Solution:**
Add to requirements.txt:
```
Cython
numba==0.56.4
```

Then redeploy.

### Issue: API Returns 401 Unauthorized

**Solution:**
- Check Authorization header: Must be `Bearer your-secure-api-key-12345`
- Verify API key matches the one in `app.py`

### Issue: Audio Processing Error

**Solution:**
- Ensure audio is MP3 format
- Check base64 encoding is valid
- Try with smaller audio file (<5MB)

### Issue: Timeout/Slow Response

**Solution:**
- Free tier has cold starts (first request slow)
- Subsequent requests will be faster
- Keep audio files under 2MB

### Issue: Can't Access Deployed URL

**Solution:**
- Wait 10-15 minutes for deployment
- Check Render/Railway logs
- Ensure port is set to `$PORT` not hardcoded

---

## ✅ PRE-SUBMISSION CHECKLIST

- [ ] Code uploaded to GitHub
- [ ] API deployed on Render/Railway/Koyeb
- [ ] API accessible at public URL
- [ ] Tested with sample audio locally
- [ ] Tested with deployed URL
- [ ] Response format matches requirements:
  ```json
  {
    "classification": "AI_GENERATED" or "HUMAN",
    "confidence": 0.0-1.0,
    "language": "english/tamil/hindi/malayalam/telugu",
    "explanation": "string"
  }
  ```
- [ ] All 5 languages accepted
- [ ] API key configured and noted
- [ ] Tested on hackathon's endpoint tester
- [ ] Endpoint and key ready for final submission

---

## 🎯 TIPS FOR SUCCESS

1. **Start Simple:** Use basic `app.py` first, optimize later
2. **Test Early:** Deploy early and test often
3. **Save Everything:** Keep your API key, URL, and test audio safe
4. **Use Logs:** Check deployment logs if something fails
5. **Ask for Help:** Use hackathon Discord/Slack if stuck

---

## 📊 HOW THE SYSTEM WORKS

### Detection Logic:

1. **Input:** Base64 MP3 audio
2. **Processing:**
   - Decode audio
   - Extract 20+ audio features (MFCC, spectral, pitch, energy)
   - Analyze consistency patterns
3. **Detection:**
   - AI voices: More consistent, uniform, regular patterns
   - Human voices: Variable, dynamic, organic patterns
4. **Output:** Classification + confidence + explanation

### Feature Importance:

- **High Consistency** → AI likely
- **Low Variance** → AI likely
- **Uniform Energy** → AI likely
- **Regular Patterns** → AI likely
- **Smooth Transitions** → AI likely

---

## 🚀 GOING BEYOND (Optional - For Better Accuracy)

### Use Machine Learning Model:

```python
# Collect labeled dataset
# Train RandomForest/XGBoost classifier
# Save model as pickle
# Load in app.py

import pickle
model = pickle.load(open('model.pkl', 'rb'))
prediction = model.predict_proba([features])
```

### Find Training Data:

- HuggingFace datasets
- Mozilla Common Voice (human)
- AI speech synthesis datasets
- Google TTS samples (AI)

---

## 📞 EMERGENCY CONTACT

If completely stuck:

1. Check Render/Railway documentation
2. Google the specific error message
3. Ask in hackathon support channel
4. Simplify code - remove advanced features
5. Use basic version instead of advanced

---

## 🎉 YOU'RE READY!

Follow these steps in order, don't skip testing, and you'll have a working solution!

**Time Estimate:**
- Setup: 15 min
- Deployment: 30-45 min
- Testing: 15 min
- Submission: 10 min
- **Total: 70-85 minutes**

Good luck! 🍀
