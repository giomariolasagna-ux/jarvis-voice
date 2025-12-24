from src.stt import record_while_pressed, transcribe_audio
import threading

print("PARLA per 4 secondi...")
recording = True

def stop():
    global recording
    recording = False

threading.Timer(4, stop).start()

audio = record_while_pressed(lambda: recording)
print("AUDIO:", "OK" if audio is not None else "NONE")

if audio is not None:
    print("TESTO:", transcribe_audio(audio))
