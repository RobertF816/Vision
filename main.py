from core.wake_word import start_listening
from core.stt import startSTT
from core.intent_router import IntentRouter

intentRouter = IntentRouter()

def onTranscriptionReady(text):
    print("You said:", text)

    intent, args = intentRouter.match(text)
    if intent:
        print("Right Away, Sir.")
        print(f"Intent: {intent}")
        print(f"Args: {args}")
    else:
        print("No Intent Found")


def on_wake():
    print("Vision is now awake.")
    startSTT(onTranscriptionReady)

if __name__ == "__main__":
    print("Listening for Hey Jinx")
    start_listening(on_wake)
