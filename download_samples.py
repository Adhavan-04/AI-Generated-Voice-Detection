"""
Script to download sample audio from Google Drive or generate test audio
"""
import os
import sys

def create_sample_audio():
    """
    Create a simple test audio file using text-to-speech
    This is useful if you don't have the Google Drive sample yet
    """
    try:
        from gtts import gTTS
        import io
        
        # Create sample text in different languages
        samples = {
            'english': 'Hello, this is a test audio sample for voice detection.',
            'tamil': 'வணக்கம், இது குரல் கண்டறிதலுக்கான ஒரு சோதனை ஆடியோ மாதிரி.',
            'hindi': 'नमस्ते, यह आवाज पहचान के लिए एक परीक्षण ऑडियो नमूना है।',
            'malayalam': 'ഹലോ, ഇത് വോയ്‌സ് ഡിറ്റക്ഷനായുള്ള ഒരു ടെസ്റ്റ് ഓഡിയോ സാമ്പിളാണ്.',
            'telugu': 'హలో, ఇది వాయిస్ డిటెక్షన్ కోసం ఒక పరీక్ష ఆడియో నమూనా.'
        }
        
        print("Creating sample audio files...")
        os.makedirs('samples', exist_ok=True)
        
        for lang, text in samples.items():
            try:
                # Map language codes
                lang_code_map = {
                    'english': 'en',
                    'tamil': 'ta',
                    'hindi': 'hi',
                    'malayalam': 'ml',
                    'telugu': 'te'
                }
                
                tts = gTTS(text=text, lang=lang_code_map[lang])
                filename = f'samples/sample_{lang}.mp3'
                tts.save(filename)
                print(f"✓ Created: {filename}")
                
            except Exception as e:
                print(f"✗ Failed to create {lang}: {str(e)}")
        
        print("\n✓ Sample audio files created in 'samples/' directory")
        print("You can now test your API with these files!")
        
    except ImportError:
        print("gTTS not installed. Installing...")
        os.system(f"{sys.executable} -m pip install gtts")
        print("Please run this script again.")

def download_from_google_drive(drive_url):
    """
    Download audio from Google Drive URL
    Format: https://drive.google.com/file/d/FILE_ID/view
    """
    try:
        import gdown
        
        # Extract file ID from URL
        if '/file/d/' in drive_url:
            file_id = drive_url.split('/file/d/')[1].split('/')[0]
            download_url = f'https://drive.google.com/uc?id={file_id}'
        else:
            download_url = drive_url
        
        output = 'sample_from_drive.mp3'
        print(f"Downloading from Google Drive...")
        gdown.download(download_url, output, quiet=False)
        print(f"✓ Downloaded: {output}")
        
    except ImportError:
        print("gdown not installed. Installing...")
        os.system(f"{sys.executable} -m pip install gdown")
        print("Please run this script again with the Google Drive URL.")
    except Exception as e:
        print(f"✗ Download failed: {str(e)}")
        print("\nTry manual download:")
        print("1. Open the Google Drive link in browser")
        print("2. Download the file manually")
        print("3. Save as 'sample_audio.mp3' in this directory")

if __name__ == "__main__":
    print("="*60)
    print("Audio Sample Downloader/Generator")
    print("="*60)
    print("\nOptions:")
    print("1. Create sample audio files using TTS (for testing)")
    print("2. Download from Google Drive URL")
    print("3. Exit")
    
    choice = input("\nEnter choice (1-3): ").strip()
    
    if choice == '1':
        create_sample_audio()
    elif choice == '2':
        drive_url = input("Enter Google Drive URL: ").strip()
        if drive_url:
            download_from_google_drive(drive_url)
        else:
            print("No URL provided.")
    else:
        print("Exiting...")
