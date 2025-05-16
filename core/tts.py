import sys
import os
import tempfile
import platform
import io # Add the parent directory to Python's path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from config import ELEVENLABS_API_KEY, elevenlabs_model_id
from elevenlabs.client import ElevenLabs
from pydub.playback import play as pydub_play
from pydub import AudioSegment

client = ElevenLabs(
  api_key=ELEVENLABS_API_KEY,
)

model: str = elevenlabs_model_id if elevenlabs_model_id else "elevenlabs_flash_v2_5"

def ffprobeInstalled() -> bool:
#Checks if  ffprobe is installed and returns bool, credits to ForeverPyrite :)
    import subprocess
    try:
        subprocess.run(
            ['ffprobe', '-version'],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            check=True
        )
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("WARNING!!: ffprobe (usually a part of ffmpeg) was not found on your device. A noticeably  lower quality audio file will play.\nCheck README.md for more info to resolve this.")
        return False

ffprobe: bool = ffprobeInstalled()


def speak(text):
    audio = client.text_to_speech.convert(
    text=text,
    voice_id="JBFqnCBsd6RMkjVDRZzb",
    model_id=model,
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
