# Vision
Smart Home Voice Assistant using AI inspired by Jarvis

This is Vision, my DIY voice assistant inspired by Iron Man’s AI. Built on a ThinkPad, powered by Python, and running fully offline, this project brings together wake word detection, speech-to-text, command handling, and text-to-speech. My goal is to eventually expand it into a modular smart home interface that runs on low-cost hardware, but with built in AI to give it a personality and memory so its more humanoid than a boring Alexa.

As of Right Now Vision:
 
 - Responds to a Wakeword of Your Choice - Porcupine Custom Wakeword
 - Uses Smart VAD recording
 - Fast Transcription - faster-whisper
 - threaded architecture
 - Smart Intent Parsing
 - Smart Command Handling
 - A few very simple commands (shown in commands.txt)
 - TTS with Elevenlabs (for now)
## How To Run

 1. Clone the repository: 'git clone https://github.com/RobertF816/Vision'
 2. Install the dependencies using 'pip install -r requirements.txt'
 2. create a 'config.py' file from 'config_template.py' and insert respective keys/paths
 3. run 'main.p'

### FFmpeg/FFprobe

Why should i Install ffmpeg to use this even if its not required?

Elevenlabs uses mp3 files which are encoded, they need to be converted to .wav files. 
Vision uses 'ffprobe' which comes from 'ffmpeg' to do this. If you do not install it, Vision will use lower quality audio and sound worse.

**This will likely become uneeded once polished with a local, offline model**

<details>
  <summary style="font-size: 16px; font-style: italic;">Installing FFmpeg</summary>

**Windows**

1. Visit the [FFmpeg download page] (https://ffmpeg.org/download.html).
2. Click on a Windows build (e.g. from [gyan.dev](https://www.gyan.dev/ffmpeg/builds/)).
3. Download the ZIP archive, extract it, and add the extracted 'bin' folder to your system PATH.

to verify:
'''bash
ffmpeg -version
'''

**Linux**

*Debian/Ubuntu-based distributions:*
'''bash
sudo apt update
sudo apt install ffmpeg
'''

*Fedora*
'''bash
sudo dnf install ffmpeg ffmpeg-devel
'''

*Arch Linux*
'''bash
sudo pacman -S ffmpeg
'''

**macOS**

if you have [Homebrew](https://brew.sh) installed:
'''bash
brew install ffmpeg
'''
Alternitavely, download pre-built binaries from [FFmpeg website](https://ffmpeg.org/download.html).

</details>
.
