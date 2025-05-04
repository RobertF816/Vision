import pvporcupine
import sounddevice as sd
import struct
import config

def start_listening(on_wake_detected):
    porcupine = pvporcupine.create(
        access_key = config.PORCUPINE_ACCESS_KEY,
        keyword_paths=[config.keyword_path]
    )

    def audio_callback(indata, frames, time, status):
        if status:
            print("Audio error:", status)
        pcm = struct.unpack_from("h" * porcupine.frame_length, indata)
        result = porcupine.process(pcm)
        if result >= 0:
            print("Wake Word Detected")
            on_wake_detected()

    stream = sd.RawInputStream(
        samplerate = porcupine.sample_rate,
        blocksize = porcupine.frame_length,
        dtype = 'int16',
        channels = 1,
        callback = audio_callback
    )

    print("Listening for 'Hey Jinx'")
    with stream:
        try:
            while True:
                sd.sleep(100)
        except KeyboardInterrupt:
            print("Exitting Wake Word Detector")
        finally:
            porcupine.delete()
