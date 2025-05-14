import time
import threading
from datetime import datetime
import re

class CommandRegistry:
    def __init__(self, speak=None):
        self.activeTimers = []
        self.timerCancelEvent = threading.Event()
        self.speak = speak or print  # Defaults to print if no TTS function passed

    def execute(self, intent, args):
        if intent == "getTime":
            return self.getTime()
        elif intent == "setTimer":
            return self.setTimer(args.get("duration"))
        elif intent == "controlLight":
            return self.controlLight(args.get("state"), args.get("location"))
        elif intent == "cancelTimers":
            return self.cancelTimers()
        elif intent == "getDate":
            return self.getDate()
        else:
            return "I'm not sure how to handle that yet."

    def getTime(self):
        now = datetime.now().strftime("%I:%M %p").lstrip("0")
        return f"The time is {now}."

    def setTimer(self, durationText):
        if not durationText:
            return "I need a duration for the timer."

        seconds = self._parseDuration(durationText)
        if seconds is None:
            return "I couldn't understand the duration."

        self.timerCancelEvent.clear()
        thread = threading.Thread(target=self._timerThread, args=(seconds,))
        thread.daemon = True
        thread.start()
        self.activeTimers.append(thread)

        return f"Timer set for {durationText}."

    def _parseDuration(self, text):
        text = text.lower()
        match = re.match(r"(\d+)\s*(second|seconds|minute|minutes)", text)
        if not match:
            return None
        number, unit = match.groups()
        number = int(number)
        if "minute" in unit:
            return number * 60
        elif "second" in unit:
            return number
        return None

    def _timerThread(self, seconds):
        start = time.time()
        while time.time() - start < seconds:
            if self.timerCancelEvent.is_set():
                return
            time.sleep(0.5)
        self.speak("Timer complete!")

    def cancelTimers(self):
        self.timerCancelEvent.set()
        self.activeTimers.clear()
        return "All timers cancelled."

    def controlLight(self, state, location):
        if not state or not location:
            return "Please specify both the state and location."
        return f"Turning {state} the lights in the {location}."

    def getDate(self):
        now = datetime.now()
        return now.strftime("It is %A, %B %d, %Y.")
