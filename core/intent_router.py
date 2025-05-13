import re

class IntentRouter:
    def __init__(self):
        self.intentPatterns = {
            "getTime": [
                ["time", "clock"]
            ],
            "setTimer": [
                ["set", "start", "begin"],
                ["timer", "countdown"]
            ],
            "controlLight": [
                ["light", "lights"],
                ["on", "off"]
            ],
            "cancelTimers": [
                ["cancel", "stop"],
                ["timer", "timers"]
            ]
        }

        self.slotHints = {
            "setTimer": {
                "duration": [
                    "1 second", "5 seconds", "10 seconds", "30 seconds",
                    "1 minute", "5 minutes", "10 minutes"
                ]
            },
            "controlLight": {
                "location": ["kitchen", "bedroom", "living room", "office"],
                "state": ["on", "off"]
            }
        }

    def match(self, text):
        text = text.lower()
        bestIntent = None
        bestScore = 0

        for intent, groups in self.intentPatterns.items():
            score = self._matchGroups(text, groups)
            print(f"Intent '{intent}' matched with score {score:.2f}")
            if score > bestScore:
                bestIntent = intent
                bestScore = score

        if bestScore >= 1.0:
            args = self._extractSlots(bestIntent, text)
            return bestIntent, args
        else:
            return None, {}

    def _matchGroups(self, text, wordGroups):
        matchedGroups = 0
        for group in wordGroups:
            if any(word in text for word in group):
                matchedGroups += 1
        score = matchedGroups + (matchedGroups / len(wordGroups))
        return score

    def _extractSlots(self, intent, text):
        print(f"[DEBUG] Extracting slots for '{intent}' from: {text}")
        args = {}

        if intent == "setTimer":
            match = re.search(r"(\d{1,3})\s*(seconds?|minutes?)", text)
            if match:
                number = match.group(1)
                unit = match.group(2)
                args["duration"] = f"{number} {unit}"
            return args

    # default hint-based matching for other intents
        if intent not in self.slotHints:
            return args

        hints = self.slotHints[intent]
        for slotName, possibleValues in hints.items():
            for value in possibleValues:
                if value in text:
                    args[slotName] = value
                    break

        return args

