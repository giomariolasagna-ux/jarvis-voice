import sounddevice as sd
import soundfile as sf
import numpy as np
import io
import os
import queue
from openai import OpenAI

# Configurazione OpenAI
try:
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
except:
    client = None

TARGET_MIC_NAME = "LifeCam"

def get_mic_device():
    """Trova il dispositivo LifeCam usando SoundDevice"""
    try:
        devices = sd.query_devices()
        for i, d in enumerate(devices):
            # Cerca un dispositivo di INPUT (>0 canali) con il nome giusto
            if d["max_input_channels"] > 0 and TARGET_MIC_NAME in d["name"]:
                print(f"--- [AUDIO] Mic trovato: [{i}] {d['name']} ---")
                return i
    except Exception as e:
        print(f"Errore ricerca mic: {e}")
    
    print("--- [AUDIO] Uso dispositivo di default ---")
    return None

def listen_ptt(is_button_held_fn):
    if not client:
        print("ERRORE: API Key mancante.")
        return None

    device_idx = get_mic_device()
    q = queue.Queue()

    # Funzione che viene chiamata dalla scheda audio ogni volta che ha dati
    def callback(indata, frames, time, status):
        if status:
            print(f"Stato Audio: {status}")
        # Copia i dati nella coda
        q.put(indata.copy())

    print("PTT: Premi e parla... (Registrazione attiva)")
    
    # Dati audio raccolti
    audio_blocks = []

    try:
        # Apre lo stream a 16kHz (Standard Whisper) Mono
        with sd.InputStream(samplerate=16000, device=device_idx, channels=1, callback=callback):
            
            # CICLO DI REGISTRAZIONE SINCRONIZZATO
            while is_button_held_fn():
                # Raccogli tutto ciò che è nella coda
                while not q.empty():
                    audio_blocks.append(q.get())
                
                # Piccola pausa per non fondere la CPU, ma l'audio è gestito dal callback
                sd.sleep(50) 
            
            # Recupera gli ultimi dati rimasti
            while not q.empty():
                audio_blocks.append(q.get())

        # --- FINE REGISTRAZIONE ---
        if not audio_blocks:
            return None
            
        print(f"Rilascio. Elaborazione {len(audio_blocks)} blocchi audio...")

        # 1. Concatena i blocchi numpy in un unico array
        recording = np.concatenate(audio_blocks, axis=0)

        # 2. Salva in un buffer di memoria come WAV
        wav_buffer = io.BytesIO()
        sf.write(wav_buffer, recording, 16000, format="WAV")
        wav_buffer.seek(0)
        wav_buffer.name = "ptt.wav"

        # 3. Invia a OpenAI
        transcript = client.audio.transcriptions.create(
            model="whisper-1", 
            file=wav_buffer,
            language="it"
        )
        
        text = transcript.text.strip()
        
        # Filtro Allucinazioni
        if not text or "Sottotitoli" in text or "Amara.org" in text:
            return None
            
        return text

    except Exception as e:
        print(f"Errore PTT (SoundDevice): {e}")
        return None
