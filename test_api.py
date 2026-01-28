import base64
import requests
import json

# API configuration
API_URL = "http://localhost:8000/detect"
API_KEY = "your-secure-api-key-12345"

def encode_audio_to_base64(audio_file_path):
    """Encode an audio file to base64"""
    with open(audio_file_path, 'rb') as audio_file:
        audio_bytes = audio_file.read()
        base64_audio = base64.b64encode(audio_bytes).decode('utf-8')
    return base64_audio

def test_api(audio_file_path, language="english"):
    """Test the voice detection API"""
    
    # Encode audio
    print(f"Encoding audio file: {audio_file_path}")
    base64_audio = encode_audio_to_base64(audio_file_path)
    
    # Prepare request
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }
    
    payload = {
        "audio_base64": base64_audio,
        "language": language
    }
    
    # Send request
    print(f"\nSending request to {API_URL}")
    print(f"Language: {language}")
    
    response = requests.post(API_URL, headers=headers, json=payload)
    
    # Display results
    print(f"\nStatus Code: {response.status_code}")
    
    if response.status_code == 200:
        result = response.json()
        print("\n" + "="*60)
        print("DETECTION RESULTS")
        print("="*60)
        print(f"Classification: {result['classification']}")
        print(f"Confidence: {result['confidence']}")
        print(f"Language: {result['language']}")
        print(f"Explanation: {result['explanation']}")
        print("="*60)
    else:
        print(f"Error: {response.text}")

if __name__ == "__main__":
    # Test with a sample audio file
    # Replace this with your actual audio file path
    audio_file = "sample_audio.mp3"
    
    try:
        test_api(audio_file, language="english")
    except FileNotFoundError:
        print(f"Error: Audio file '{audio_file}' not found.")
        print("Please provide a valid MP3 file path.")
    except Exception as e:
        print(f"Error: {str(e)}")
