from core.wake_word import start_listening

def on_wake():
    print("Vision is now awake.")

if __name__ == "__main__":
    start_listening(on_wake)
