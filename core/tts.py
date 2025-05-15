import sys
import os
import tempfile
import platform
import io# Add the parent directory to Python's path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from config import ELEVENLABS_API_KEY, elevenlabs_model_id
from elevenlabs.client import ElevenLabs
# This function is imported, yet never used? I'm not going to look into it yet, but could it be used to easily play the audio without manual platform detection and commands? It looks like it simply takes in an AudioSegment object as an argument and plays it. Might also require ffmpeg though.
from pydub.playback import play as pydub_play
from pydub import AudioSegment
client = ElevenLabs(
  api_key=ELEVENLABS_API_KEY,
)

# Consider changing the default to "eleven_flash_v2_5", cheaper and faster. More practical for a home assistant.
# Alternatively, explicitly set a default string literal in the config_template to remove this statement completely 
model: str = elevenlabs_model_id if elevenlabs_model_id else "eleven_multilingual_v2"

def is_ffprobe_installed() -> bool:
    """Function checks to see if ffprobe (usually installed alongside ffmpeg) is installed on the client device. This is used to determine whether or not the program is able to convert .mp3 files to .wav or if .pcm needs to be used for Elevenlabs output.

    Returns:
        bool: Whether or not ffprobe is installed
    """
    import subprocess
    try:
        # Try to run 'ffprobe -version' and suppress output
        subprocess.run(
            ['ffprobe', '-version'],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            check=True
        )
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("WARNING!!!: ffprobe (typically a part of ffmpeg) was not detected on your device. You will hear lower quality audio output.\nCheck README.md for more info.")
        return False
    
ffprobe: bool = is_ffprobe_installed()

def speak(text):
    audio = client.text_to_speech.convert(
    text=text,
    voice_id="JBFqnCBsd6RMkjVDRZzb",
    model_id=model,
    # model_id=elevenlabs_model_id, # Only use this if the default is set in config_template.py
    output_format="mp3_44100_128" if ffprobe else "pcm_24000",
    )
    
    audioBytes = b"".join(audio)
    if ffprobe:
        audioSegment = AudioSegment.from_file(io.BytesIO(audioBytes), format="mp3")
    else:
        audioSegment = AudioSegment.from_raw(io.BytesIO(audioBytes), sample_width=2, frame_rate=24000, channels=1)

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
            print("Unsupported OS. Cannot play audio")
