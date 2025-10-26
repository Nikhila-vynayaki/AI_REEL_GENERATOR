from dotenv import load_dotenv
from elevenlabs.client import ElevenLabs
from elevenlabs.play import play
import os
from config import ELEVENLABS_API_KEY

load_dotenv()

elevenlabs = ElevenLabs(
  api_key=ELEVENLABS_API_KEY,
)

def text_to_audio(text:str,folder:str):
    audio = elevenlabs.text_to_speech.convert(
        text=text,
        voice_id="JBFqnCBsd6RMkjVDRZzb",
        model_id="eleven_multilingual_v2",
        output_format="mp3_44100_128",
    )

  

    # Save audio file
    save_path = os.path.join(f"user_uploads/{folder}", "audio.mp3")
    with open(save_path, "wb") as f:
        for chunks in audio:    
            if chunks:
                f.write(chunks)
    print("Audio saved to:", save_path)

    return save_path

# text_to_audio("Hello, this is a test of the ElevenLabs text-to-speech API.", "1b299fe8-970e-11f0-ba8d-763153ed85a8")