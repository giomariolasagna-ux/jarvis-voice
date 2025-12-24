import os
from pathlib import Path
from openai import OpenAI
import pygame
import time

# Recupera la chiave
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=OPENAI_API_KEY)

# Inizializza il mixer audio (silenzioso, senza finestre)
try:
    pygame.mixer.init()
except Exception as e:
    print(f"Errore init audio: {e}")

def speak(text):
    """
    Genera audio con OpenAI e lo riproduce subito.
    """
    if not text: return

    try:
        # Percorso per il file temporaneo
        speech_file_path = Path(__file__).parent / "speech.mp3"
        
        # 1. Chiede l'audio a OpenAI (Alta qualità)
        response = client.audio.speech.create(
            model="tts-1",
            voice="alloy", # Puoi cambiare in "echo", "fable", "onyx", "nova", "shimmer"
            input=text
        )
        
        # Salva il file
        response.stream_to_file(speech_file_path)
        
        # 2. Riproduce l'audio
        pygame.mixer.music.load(str(speech_file_path))
        pygame.mixer.music.play()
        
        # Aspetta che finisca di parlare
        while pygame.mixer.music.get_busy():
            time.sleep(0.1)
            
        # Rilascia il file per poterlo sovrascrivere la prossima volta
        pygame.mixer.music.unload()

    except Exception as e:
        print(f"Errore TTS: {e}")
