import sounddevice as sd
import numpy as np
import scipy.io.wavfile as wav
import webrtcvad
import tempfile
import threading
import time
from faster_whisper import WhisperModel

sampleRate = 16000
channels = 1
frameDuration = 30
frameSize = int(sampleRate * frameDuration / 1000)

model = WhisperModel("base", compute_type="int8")

def recordAudioVad(maxSilence=1.0, maxDuration=10, ambientWindow=20):
    vad = webrtcvad.Vad(3)
    audioBuffer = []
    silenceStart = None
    startTime = time.time()

    rmsHistory = []
    ambientRms = None
    speechDetected = False

    def calcRms(frame):
        return np.sqrt(np.mean(np.square(frame.astype(np.float32))))

    def callback(indata, frames, timeInfo, status):
        nonlocal silenceStart, audioBuffer, rmsHistory, ambientRms, speechDetected

        if status:
            print("Sounddevice error:", status)

        audio = indata[:, 0].copy()
        audioInt16 = np.int16(np.clip(audio * 32767, -32768, 32767))
        audioBuffer.append(audioInt16)

        currentTime = time.time()
        isSpeakingNow = False

        for i in range(0, len(audioInt16) - frameSize + 1, frameSize):
            frame = audioInt16[i:i + frameSize]
            frameRms = calcRms(frame)

            if not speechDetected:
                rmsHistory.append(frameRms)
                if len(rmsHistory) > ambientWindow:
                    rmsHistory.pop(0)
                ambientRms = np.mean(rmsHistory)

            if ambientRms and vad.is_speech(frame.tobytes(), sampleRate) and frameRms > 2.0 * ambientRms:
                isSpeakingNow = True
                break

        if isSpeakingNow:
            print("Speech") # debug
            speechDetected = True
            silenceStart = None
        else:
            print("Silence") # debug
            if speechDetected:
                if silenceStart is None:
                    silenceStart = currentTime
                elif currentTime - silenceStart > maxSilence:
                    print("Silence timeout — stopping") # debug
                    raise sd.CallbackStop()

        if currentTime - startTime > maxDuration:
            print("Max duration reached — stopping") # debug
            raise sd.CallbackStop()

    print("Listening...") # debug

    with sd.InputStream(
        samplerate=sampleRate,
        channels=channels,
        callback=callback,
        blocksize=frameSize
    ) as stream:
        stream.start()
        while stream.active:
            time.sleep(.05)

    audioNp = np.concatenate(audioBuffer)
    return audioNp

def transcribeWhisper(audioData, callback):
    with tempfile.NamedTemporaryFile(suffix=".wav",delete=False) as tempAudio:
        wav.write(tempAudio.name, sampleRate, audioData)
        print(f"Saved to {tempAudio.name}")

        segments, _ = model.transcribe(tempAudio.name, vad_filter=True)
        result = " ".join(segment.text for segment in segments)
        callback(result)

def startSTT(callback):
    def worker():
        audioData = recordAudioVad()
        transcribeWhisper(audioData, callback)

    threading.Thread(target=worker,daemon=True).start()
