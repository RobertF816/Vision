import sys
import os
import tempfile
import platform
import io
# Add the parent directory to Python's path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from config import ELEVENLABS_API_KEY
from elevenlabs.client import ElevenLabs
from pydub.playback import play as pydub_play
from pydub import AudioSegment
client = ElevenLabs(
  api_key=ELEVENLABS_API_KEY,
)

def speak(text):
    audio = client.text_to_speech.convert(
    text=text,
    voice_id="JBFqnCBsd6RMkjVDRZzb",
    model_id="eleven_multilingual_v2",
    output_format="mp3_44100_128",
    )
    
    audioBytes = b"".join(audio)
    audioSegment = AudioSegment.from_file(io.BytesIO(audioBytes), format="mp3")
    
    with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as f:
        audioSegment.export(f.name, format="wav")
        system = platform.system()
        if system == "Darwin":
            os.system(f"afplay {f.name}")
        elif system == "Linux": 
            os.system(f"aplay {f.name}")
        elif system == "Windows":
            os.system(f'start /min "" "{f.name}"')
        else:
            print("Unsupported OS. Cannot play audio");
