from core.wake_word import start_listening
from core.stt import startSTT


def onTranscriptionReady(text):
    print("You said:", text)



def on_wake():
    print("Vision is now awake.")
    startSTT(onTranscriptionReady)

if __name__ == "__main__":
    start_listening(on_wake)
