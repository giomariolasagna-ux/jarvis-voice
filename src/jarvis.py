import time
from src.stt import listen_and_transcribe
from src.brain import jarvis_brain
from src.tts import speak

def main_loop():
    print("Jarvis Voice Loop avviato.")
    while True:
        try:
            print("In attesa input vocale...")
            user_text = listen_and_transcribe()
            if not user_text or user_text.strip() == "":
                continue

            print("User:", user_text)
            response = jarvis_brain(user_text)
            print("Jarvis:", response)
            speak(response)

        except KeyboardInterrupt:
            break
        except Exception as e:
            print("Errore:", e)
            time.sleep(1)

if __name__ == "__main__":
    main_loop()
