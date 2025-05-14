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

 1. Clone the repo
 2. create a 'config.py' file from 'config_template.py' and insert respective keys/paths
 3. Run
