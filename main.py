from core.wake_word import start_listening
from core.stt import startSTT
from core.intent_router import IntentRouter
from core.command_registry import CommandRegistry
from core.tts import speak
import string

intentRouter = IntentRouter()
commandRegistry = CommandRegistry(speak=speak)

def onTranscriptionReady(text):
    textout = text.lower()
    textout = textout.translate(str.maketrans('', '', string.punctuation))
    if any(phrase in textout for phrase in ["never mind", "forget it", "nothing","nevermind"]):
        print("User Cancelled Interaction")
        return
    print(f"Transcript: {text}")

    intent, args = intentRouter.match(text)
    print("Intent Router TIMING")
    if intent:
        print(f"Intent: {intent}")
        print(f"Args: {args}")
        response = commandRegistry.execute(intent, args)
        print("Command Registry TIMING")
        speak(response)
        print("TTS TIMING")
    else:
        speak("I'm not sure what you meant.")

def onWakeWordDetected():
    print("Wake word detected")
    startSTT(onTranscriptionReady)

if __name__ == "__main__":
    speak("Systems Online. Awaiting your command.")
    print("Listening for Hey Jinx")
    start_listening(onWakeWordDetected)
