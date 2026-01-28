# AI Voice Detection API - Complete Guide

## 📋 Project Overview
This API detects whether a voice sample is AI-generated or human-spoken, supporting 5 languages: Tamil, English, Hindi, Malayalam, and Telugu.

## 🚀 Quick Start Guide

### Step 1: Setup Local Environment

```bash
# Install Python 3.8+ if not already installed
# Install dependencies
pip install -r requirements.txt
```

### Step 2: Run the API Locally

```bash
# Start the server
python app.py

# Or using uvicorn directly
uvicorn app:app --host 0.0.0.0 --port 8000 --reload
```

The API will be available at `http://localhost:8000`

### Step 3: Test the API

```bash
# Test with sample audio
python test_api.py
```

## 📡 API Documentation

### Endpoint: POST /detect

**URL:** `https://your-domain.com/detect`

**Headers:**
```
Authorization: Bearer your-secure-api-key-12345
Content-Type: application/json
```

**Request Body:**
```json
{
  "audio_base64": "base64_encoded_mp3_string",
  "language": "english"
}
```

**Supported Languages:**
- tamil
- english
- hindi
- malayalam
- telugu

**Response:**
```json
{
  "classification": "AI_GENERATED",
  "confidence": 0.87,
  "language": "english",
  "explanation": "Audio exhibits characteristics typical of AI-generated speech..."
}
```

**Classification Values:**
- `AI_GENERATED` - Voice is detected as AI-generated
- `HUMAN` - Voice is detected as human

**Confidence Score:**
- Range: 0.0 to 1.0
- Higher values indicate stronger confidence

## 🌐 FREE Deployment Options

### Option 1: Render.com (Recommended - FREE)

1. **Create account:** https://render.com/
2. **Connect GitHub:**
   - Create a GitHub repository
   - Push your code to GitHub
3. **Deploy:**
   - Click "New +" → "Web Service"
   - Connect your repository
   - Settings:
     - **Build Command:** `pip install -r requirements.txt`
     - **Start Command:** `uvicorn app:app --host 0.0.0.0 --port $PORT`
   - Click "Create Web Service"
4. **Get URL:** Your API will be at `https://your-app-name.onrender.com`

### Option 2: Railway.app (FREE)

1. **Create account:** https://railway.app/
2. **New Project:**
   - Click "New Project"
   - Select "Deploy from GitHub repo"
3. **Configure:**
   - Railway auto-detects Python
   - Add start command: `uvicorn app:app --host 0.0.0.0 --port $PORT`
4. **Deploy:** Automatic deployment

### Option 3: Fly.io (FREE Tier)

1. **Install Fly CLI:** https://fly.io/docs/hands-on/install-flyctl/
2. **Create fly.toml:**
```toml
app = "your-app-name"

[build]
  builder = "paketobuildpacks/builder:base"

[env]
  PORT = "8000"

[[services]]
  http_checks = []
  internal_port = 8000
  processes = ["app"]
  protocol = "tcp"
  script_checks = []

  [[services.ports]]
    force_https = true
    handlers = ["http"]
    port = 80

  [[services.ports]]
    handlers = ["tls", "http"]
    port = 443
```

3. **Deploy:**
```bash
fly launch
fly deploy
```

### Option 4: Koyeb (FREE)

1. **Create account:** https://www.koyeb.com/
2. **Deploy from GitHub**
3. **Configure:** Python runtime auto-detected
4. **Start command:** `uvicorn app:app --host 0.0.0.0 --port $PORT`

## 🔧 Configuration

### Change API Key
Edit `app.py`:
```python
API_KEY = "your-custom-secure-key"
```

**IMPORTANT:** Use the same key in test scripts and submission!

### Environment Variables (Production)
```bash
export API_KEY="your-secure-key"
```

Update app.py to use:
```python
import os
API_KEY = os.getenv("API_KEY", "default-key")
```

## 🧪 Testing Your Deployed API

### Using curl:
```bash
# First, convert audio to base64
base64 sample.mp3 > audio_base64.txt

# Test the API
curl -X POST https://your-api-url.com/detect \
  -H "Authorization: Bearer your-secure-api-key-12345" \
  -H "Content-Type: application/json" \
  -d '{
    "audio_base64": "'"$(cat audio_base64.txt)"'",
    "language": "english"
  }'
```

### Using Python:
```python
import requests
import base64

# Load and encode audio
with open('sample.mp3', 'rb') as f:
    audio_base64 = base64.b64encode(f.read()).decode()

# Make request
response = requests.post(
    'https://your-api-url.com/detect',
    headers={
        'Authorization': 'Bearer your-secure-api-key-12345',
        'Content-Type': 'application/json'
    },
    json={
        'audio_base64': audio_base64,
        'language': 'english'
    }
)

print(response.json())
```

## 📊 How Detection Works

The system uses audio signal processing to identify AI-generated voices:

1. **Feature Extraction:**
   - Spectral features (centroid, rolloff, bandwidth)
   - Zero crossing rate
   - MFCC (Mel-frequency cepstral coefficients)
   - Chroma features
   - RMS energy

2. **Detection Logic:**
   - AI voices show more consistency in spectral patterns
   - Lower variance in energy levels
   - More uniform pitch patterns
   - Less natural variation compared to human speech

3. **Scoring:**
   - Consistency scores are calculated
   - Threshold-based classification
   - Confidence calculated from feature statistics

## 🎯 Improving Accuracy (Advanced)

### Add Machine Learning Model:

```python
# Install scikit-learn
pip install scikit-learn

# Train on labeled dataset
from sklearn.ensemble import RandomForestClassifier
import pickle

# After training
model = RandomForestClassifier()
# model.fit(X_train, y_train)
# pickle.dump(model, open('model.pkl', 'wb'))

# In app.py
model = pickle.load(open('model.pkl', 'rb'))
prediction = model.predict([features])
```

### Collect Training Data:
- Use datasets from HuggingFace
- Examples: AI-generated speech datasets, human voice datasets
- Train a binary classifier

## 📝 Submission Checklist

- [ ] API deployed and publicly accessible
- [ ] API endpoint URL obtained
- [ ] API key configured and noted
- [ ] Tested with sample audio
- [ ] Verified response format matches requirements
- [ ] API responds within acceptable time (<5 seconds)
- [ ] Error handling works properly
- [ ] All 5 languages accepted in request

## 🔍 Troubleshooting

**Issue: Module not found**
```bash
pip install --upgrade -r requirements.txt
```

**Issue: Audio loading error**
```bash
# Install system dependencies (Linux)
sudo apt-get install libsndfile1

# macOS
brew install libsndfile
```

**Issue: Port already in use**
```bash
# Change port in app.py
uvicorn.run(app, host="0.0.0.0", port=8001)
```

**Issue: API returns 401**
- Check Authorization header format: `Bearer your-api-key`
- Verify API key matches the one in app.py

## 🏆 Submission Format

**API Endpoint:**
```
https://your-app-name.onrender.com/detect
```

**API Key:**
```
Bearer your-secure-api-key-12345
```

**Test Message:**
```
Testing AI Voice Detection API for multi-language voice classification
```

## 📚 Additional Resources

- FastAPI Documentation: https://fastapi.tiangolo.com/
- Librosa Documentation: https://librosa.org/doc/latest/index.html
- Audio Processing Tutorial: https://realpython.com/python-speech-recognition/
- Render Deployment: https://render.com/docs/web-services

## 🆘 Need Help?

1. Check API logs in your deployment platform
2. Test locally first before deploying
3. Verify base64 encoding is correct
4. Ensure MP3 format is valid

Good luck with your hackathon! 🚀
