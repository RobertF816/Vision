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

 1. Clone the repository: `git clone https://github.com/RobertF816/Vision`
 2. Install the dependancies using `pip install -r requirements.txt`
 3. Create a 'config.py' file from 'config_template.py' and insert respective keys/paths
 4. Run `main.py`

### FFmpeg/FFprobe

*Why should I install ffmpeg to use this app if it isn't required?*

When the app plays audio files from Elevenlabs, it normally uses high-quality MP3 files. However, MP3s are encoded, meaning they need to be converted into a raw format like WAV before they can be played. The app uses a tool called `ffprobe` (which comes with `ffmpeg`) to make this conversion.

But if you don't have ffmpeg installed, the app can switch to using uncompressed `.pcm` files. Since these files aren't encoded, they can be used directly as WAV files without any extra processing.

This will likely be phased out when text-to-speech is done with a local model.

<details>
  <summary style="font-size: 16px; font-style: italic;">Installing FFmpeg</summary>

**Windows**

1. Visit the [FFmpeg download page](https://ffmpeg.org/download.html).
2. Click on a Windows build (e.g. from [gyan.dev](https://www.gyan.dev/ffmpeg/builds/)).
3. Download the ZIP archive, extract it, and add the extracted `bin` folder to your system PATH.

To verify the installation:
```bash
ffmpeg -version
```

**Linux**

*Debian/Ubuntu-based distributions:*
```bash
sudo apt update
sudo apt install ffmpeg
```

*Fedora:*
```bash
sudo dnf install ffmpeg ffmpeg-devel
```

*Arch Linux:*
```bash
sudo pacman -S ffmpeg
```

**macOS**

If you have [Homebrew](https://brew.sh) installed:
```bash
brew install ffmpeg
```
Alternatively, download pre-built binaries from the [FFmpeg website](https://ffmpeg.org/download.html).

In the case that you are paying for a higher Elevenlabs tier and really don't wanna install FFmpeg, you can go to [the api reference](https://elevenlabs.io/docs/api-reference/text-to-speech/convert#request.query.output_format.output_format) and manually set the `ouput_format` in the arguments for the `convert()` function call in `tts.py`.

</details>


