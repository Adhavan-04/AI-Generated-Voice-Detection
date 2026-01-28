from fastapi import FastAPI, HTTPException, Header
from pydantic import BaseModel
import base64
import io
import numpy as np
import librosa
from typing import Optional
import uvicorn
from fastapi.middleware.cors import CORSMiddleware

# Initialize FastAPI app
app = FastAPI(title="AI Voice Detection API")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# API Key for authentication
API_KEY = "your-secure-api-key-12345"

# Request model
class VoiceDetectionRequest(BaseModel):
    audio_base64: str
    language: Optional[str] = "english"

# Response model
class VoiceDetectionResponse(BaseModel):
    classification: str
    confidence: float
    language: str
    explanation: str

def extract_audio_features(audio_data, sr):
    """Extract features from audio for detection"""
    try:
        # Extract various audio features
        
        # 1. Spectral features
        spectral_centroids = librosa.feature.spectral_centroid(y=audio_data, sr=sr)[0]
        spectral_rolloff = librosa.feature.spectral_rolloff(y=audio_data, sr=sr)[0]
        spectral_bandwidth = librosa.feature.spectral_bandwidth(y=audio_data, sr=sr)[0]
        
        # 2. Zero crossing rate
        zcr = librosa.feature.zero_crossing_rate(audio_data)[0]
        
        # 3. MFCC features
        mfccs = librosa.feature.mfcc(y=audio_data, sr=sr, n_mfcc=13)
        
        # 4. Chroma features
        chroma = librosa.feature.chroma_stft(y=audio_data, sr=sr)
        
        # 5. RMS Energy
        rms = librosa.feature.rms(y=audio_data)[0]
        
        # Calculate statistics
        features = {
            'spectral_centroid_mean': np.mean(spectral_centroids),
            'spectral_centroid_std': np.std(spectral_centroids),
            'spectral_rolloff_mean': np.mean(spectral_rolloff),
            'spectral_bandwidth_mean': np.mean(spectral_bandwidth),
            'zcr_mean': np.mean(zcr),
            'zcr_std': np.std(zcr),
            'mfcc_mean': np.mean(mfccs, axis=1),
            'mfcc_std': np.std(mfccs, axis=1),
            'chroma_mean': np.mean(chroma),
            'rms_mean': np.mean(rms),
            'rms_std': np.std(rms)
        }
        
        return features
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Feature extraction failed: {str(e)}")

def detect_ai_voice(features):
    """
    Heuristic-based AI voice detection
    AI-generated voices typically have:
    - More consistent spectral characteristics
    - Lower variance in energy
    - More uniform pitch patterns
    - Less natural variations
    """
    
    # Calculate anomaly scores based on feature consistency
    consistency_score = 0
    
    # Check spectral consistency (AI voices are more consistent)
    spectral_consistency = features['spectral_centroid_std'] / (features['spectral_centroid_mean'] + 1e-6)
    if spectral_consistency < 0.15:  # Very consistent
        consistency_score += 0.3
    
    # Check zero crossing rate consistency
    zcr_consistency = features['zcr_std'] / (features['zcr_mean'] + 1e-6)
    if zcr_consistency < 0.4:  # Very consistent
        consistency_score += 0.2
    
    # Check MFCC variance (AI voices have lower variance)
    mfcc_variance = np.mean(features['mfcc_std'])
    if mfcc_variance < 50:  # Low variance
        consistency_score += 0.2
    
    # Check RMS energy consistency
    rms_consistency = features['rms_std'] / (features['rms_mean'] + 1e-6)
    if rms_consistency < 0.3:  # Very consistent energy
        consistency_score += 0.15
    
    # Check chroma features (AI voices may have less variation)
    if features['chroma_mean'] > 0.3 and features['chroma_mean'] < 0.7:
        consistency_score += 0.15
    
    # Determine classification
    if consistency_score > 0.5:
        classification = "AI_GENERATED"
        confidence = min(0.95, 0.5 + consistency_score)
        explanation = "Audio exhibits characteristics typical of AI-generated speech: high spectral consistency, uniform energy distribution, and reduced natural variation."
    else:
        classification = "HUMAN"
        confidence = min(0.95, 0.5 + (1 - consistency_score))
        explanation = "Audio shows natural human speech characteristics: varied spectral patterns, dynamic energy levels, and organic pitch variations."
    
    return classification, confidence, explanation

@app.post("/detect", response_model=VoiceDetectionResponse)
async def detect_voice(
    request: VoiceDetectionRequest,
    authorization: Optional[str] = Header(None)
):
    """
    Detect if a voice sample is AI-generated or human
    
    Headers:
    - Authorization: Bearer {API_KEY}
    
    Body:
    - audio_base64: Base64-encoded MP3 audio
    - language: One of [tamil, english, hindi, malayalam, telugu]
    """
    
    # Validate API key
    if not authorization or authorization != f"Bearer {API_KEY}":
        raise HTTPException(status_code=401, detail="Invalid or missing API key")
    
    # Validate language
    supported_languages = ["tamil", "english", "hindi", "malayalam", "telugu"]
    language = request.language.lower() if request.language else "english"
    
    if language not in supported_languages:
        raise HTTPException(
            status_code=400, 
            detail=f"Unsupported language. Must be one of: {', '.join(supported_languages)}"
        )
    
    try:
        # Decode base64 audio
        audio_bytes = base64.b64decode(request.audio_base64)
        
        # Load audio using librosa
        audio_data, sample_rate = librosa.load(
            io.BytesIO(audio_bytes),
            sr=None,
            mono=True
        )
        
        # Extract features
        features = extract_audio_features(audio_data, sample_rate)
        
        # Detect AI voice
        classification, confidence, explanation = detect_ai_voice(features)
        
        return VoiceDetectionResponse(
            classification=classification,
            confidence=round(confidence, 2),
            language=language,
            explanation=explanation
        )
        
    except base64.binascii.Error:
        raise HTTPException(status_code=400, detail="Invalid base64 encoding")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Processing error: {str(e)}")

@app.get("/")
async def root():
    return {
        "message": "AI Voice Detection API",
        "version": "1.0",
        "supported_languages": ["tamil", "english", "hindi", "malayalam", "telugu"],
        "endpoint": "/detect"
    }

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
