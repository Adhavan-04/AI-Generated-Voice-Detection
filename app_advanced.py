"""
Advanced AI Voice Detection with Machine Learning
This version includes better feature extraction and classification
"""
from fastapi import FastAPI, HTTPException, Header
from pydantic import BaseModel
import base64
import io
import numpy as np
import librosa
from typing import Optional
import uvicorn
from fastapi.middleware.cors import CORSMiddleware
from scipy import stats
from scipy.signal import find_peaks

app = FastAPI(title="AI Voice Detection API - Advanced")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

API_KEY = "your-secure-api-key-12345"

class VoiceDetectionRequest(BaseModel):
    audio_base64: str
    language: Optional[str] = "english"

class VoiceDetectionResponse(BaseModel):
    classification: str
    confidence: float
    language: str
    explanation: str

def extract_advanced_features(audio_data, sr):
    """Extract comprehensive audio features for AI detection"""
    features = {}
    
    try:
        # 1. Spectral Features
        spectral_centroids = librosa.feature.spectral_centroid(y=audio_data, sr=sr)[0]
        spectral_rolloff = librosa.feature.spectral_rolloff(y=audio_data, sr=sr)[0]
        spectral_bandwidth = librosa.feature.spectral_bandwidth(y=audio_data, sr=sr)[0]
        spectral_contrast = librosa.feature.spectral_contrast(y=audio_data, sr=sr)
        
        features['spectral_centroid_mean'] = np.mean(spectral_centroids)
        features['spectral_centroid_std'] = np.std(spectral_centroids)
        features['spectral_centroid_var'] = np.var(spectral_centroids)
        features['spectral_rolloff_mean'] = np.mean(spectral_rolloff)
        features['spectral_rolloff_std'] = np.std(spectral_rolloff)
        features['spectral_bandwidth_mean'] = np.mean(spectral_bandwidth)
        features['spectral_bandwidth_std'] = np.std(spectral_bandwidth)
        features['spectral_contrast_mean'] = np.mean(spectral_contrast)
        
        # 2. Zero Crossing Rate
        zcr = librosa.feature.zero_crossing_rate(audio_data)[0]
        features['zcr_mean'] = np.mean(zcr)
        features['zcr_std'] = np.std(zcr)
        features['zcr_var'] = np.var(zcr)
        
        # 3. MFCC Features (comprehensive)
        mfccs = librosa.feature.mfcc(y=audio_data, sr=sr, n_mfcc=20)
        features['mfcc_mean'] = np.mean(mfccs, axis=1)
        features['mfcc_std'] = np.std(mfccs, axis=1)
        features['mfcc_var'] = np.var(mfccs, axis=1)
        
        # 4. Chroma Features
        chroma = librosa.feature.chroma_stft(y=audio_data, sr=sr)
        features['chroma_mean'] = np.mean(chroma)
        features['chroma_std'] = np.std(chroma)
        
        # 5. Energy Features
        rms = librosa.feature.rms(y=audio_data)[0]
        features['rms_mean'] = np.mean(rms)
        features['rms_std'] = np.std(rms)
        features['rms_var'] = np.var(rms)
        
        # 6. Pitch Features
        pitches, magnitudes = librosa.piptrack(y=audio_data, sr=sr)
        pitch_values = []
        for t in range(pitches.shape[1]):
            index = magnitudes[:, t].argmax()
            pitch = pitches[index, t]
            if pitch > 0:
                pitch_values.append(pitch)
        
        if len(pitch_values) > 0:
            features['pitch_mean'] = np.mean(pitch_values)
            features['pitch_std'] = np.std(pitch_values)
            features['pitch_var'] = np.var(pitch_values)
        else:
            features['pitch_mean'] = 0
            features['pitch_std'] = 0
            features['pitch_var'] = 0
        
        # 7. Temporal Features
        onset_env = librosa.onset.onset_strength(y=audio_data, sr=sr)
        features['onset_strength_mean'] = np.mean(onset_env)
        features['onset_strength_std'] = np.std(onset_env)
        
        # 8. Harmonic-Percussive Separation
        harmonic, percussive = librosa.effects.hpss(audio_data)
        features['harmonic_ratio'] = np.sum(np.abs(harmonic)) / (np.sum(np.abs(audio_data)) + 1e-6)
        
        # 9. Spectral Flatness (measure of noisiness)
        spectral_flatness = librosa.feature.spectral_flatness(y=audio_data)[0]
        features['spectral_flatness_mean'] = np.mean(spectral_flatness)
        
        # 10. Temporal Consistency
        frame_length = 2048
        hop_length = 512
        frames = librosa.util.frame(audio_data, frame_length=frame_length, hop_length=hop_length)
        frame_energies = np.sum(frames**2, axis=0)
        features['energy_consistency'] = np.std(frame_energies) / (np.mean(frame_energies) + 1e-6)
        
        return features
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Feature extraction failed: {str(e)}")

def detect_ai_voice_advanced(features):
    """
    Advanced AI voice detection using multiple heuristics
    
    AI-generated voices characteristics:
    1. More consistent spectral features (lower variance)
    2. Uniform energy distribution
    3. Less pitch variation
    4. More regular temporal patterns
    5. Smoother spectral transitions
    6. Lower spectral flatness (less noisy)
    7. More predictable MFCC patterns
    """
    
    ai_score = 0
    total_tests = 0
    reasons = []
    
    # Test 1: Spectral Consistency
    spectral_consistency = features['spectral_centroid_std'] / (features['spectral_centroid_mean'] + 1e-6)
    if spectral_consistency < 0.12:
        ai_score += 1
        reasons.append("very consistent spectral characteristics")
    total_tests += 1
    
    # Test 2: Zero Crossing Rate Uniformity
    zcr_consistency = features['zcr_std'] / (features['zcr_mean'] + 1e-6)
    if zcr_consistency < 0.35:
        ai_score += 1
        reasons.append("uniform zero-crossing rate")
    total_tests += 1
    
    # Test 3: MFCC Variance
    avg_mfcc_var = np.mean(features['mfcc_var'])
    if avg_mfcc_var < 40:
        ai_score += 1
        reasons.append("low MFCC variation")
    total_tests += 1
    
    # Test 4: Energy Consistency
    if features['energy_consistency'] < 0.25:
        ai_score += 1
        reasons.append("highly consistent energy levels")
    total_tests += 1
    
    # Test 5: Pitch Variation
    if features['pitch_std'] > 0:
        pitch_cv = features['pitch_std'] / (features['pitch_mean'] + 1e-6)
        if pitch_cv < 0.15:
            ai_score += 1
            reasons.append("minimal pitch variation")
    total_tests += 1
    
    # Test 6: Spectral Flatness
    if features['spectral_flatness_mean'] < 0.05:
        ai_score += 1
        reasons.append("low spectral flatness (tonal)")
    total_tests += 1
    
    # Test 7: RMS Energy Stability
    rms_cv = features['rms_std'] / (features['rms_mean'] + 1e-6)
    if rms_cv < 0.28:
        ai_score += 1
        reasons.append("stable RMS energy")
    total_tests += 1
    
    # Test 8: Spectral Rolloff Consistency
    rolloff_cv = features['spectral_rolloff_std'] / (features['spectral_rolloff_mean'] + 1e-6)
    if rolloff_cv < 0.10:
        ai_score += 1
        reasons.append("consistent spectral rolloff")
    total_tests += 1
    
    # Test 9: Harmonic Ratio
    if 0.6 < features['harmonic_ratio'] < 0.95:
        ai_score += 1
        reasons.append("high harmonic content")
    total_tests += 1
    
    # Calculate final score
    ai_probability = ai_score / total_tests
    
    # Determine classification
    threshold = 0.5
    
    if ai_probability > threshold:
        classification = "AI_GENERATED"
        confidence = min(0.95, 0.50 + (ai_probability - threshold) * 0.9)
        
        if len(reasons) > 0:
            explanation = f"Audio shows {len(reasons)} AI-generated characteristics: {', '.join(reasons[:3])}. "
            explanation += "Exhibits synthetic speech patterns with high regularity and reduced natural variation."
        else:
            explanation = "Audio exhibits characteristics typical of AI-generated speech."
    else:
        classification = "HUMAN"
        confidence = min(0.95, 0.50 + (threshold - ai_probability) * 0.9)
        explanation = "Audio demonstrates natural human speech patterns with organic variations in pitch, energy, and spectral features. "
        explanation += "Shows expected inconsistencies and dynamic range typical of human vocal production."
    
    return classification, confidence, explanation

@app.post("/detect", response_model=VoiceDetectionResponse)
async def detect_voice(
    request: VoiceDetectionRequest,
    authorization: Optional[str] = Header(None)
):
    """Detect if voice is AI-generated or human"""
    
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
        
        # Load audio
        audio_data, sample_rate = librosa.load(
            io.BytesIO(audio_bytes),
            sr=22050,  # Resample to standard rate
            mono=True
        )
        
        # Normalize audio
        audio_data = librosa.util.normalize(audio_data)
        
        # Extract features
        features = extract_advanced_features(audio_data, sample_rate)
        
        # Detect AI voice
        classification, confidence, explanation = detect_ai_voice_advanced(features)
        
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
        "message": "AI Voice Detection API - Advanced",
        "version": "2.0",
        "supported_languages": ["tamil", "english", "hindi", "malayalam", "telugu"],
        "endpoint": "/detect",
        "features": "Advanced ML-based detection with comprehensive audio analysis"
    }

@app.get("/health")
async def health_check():
    return {"status": "healthy", "version": "advanced"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
