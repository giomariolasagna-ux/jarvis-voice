import speech_recognition as sr

# PAROLA CHIAVE DA CERCARE (Parte del nome del tuo microfono)
TARGET_MIC_NAME = "LifeCam"

def get_mic_index():
    """Cerca l'indice del microfono basandosi sul nome."""
    try:
        mics = sr.Microphone.list_microphone_names()
        for i, name in enumerate(mics):
            if TARGET_MIC_NAME in name:
                print(f"--- [AUTO-DETECT] Trovato {name} all indice {i} ---")
                return i
    except:
        pass
    print("--- [AUTO-DETECT] LifeCam non trovata, uso Default ---")
    return None # Usa il default di sistema

def listen():
    r = sr.Recognizer()
    
    # --- PARAMETRI DI ASCOLTO (VELOCI) ---
    r.energy_threshold = 400      # Soglia fissa (Niente calibrazione lenta)
    r.dynamic_energy_threshold = False 
    r.pause_threshold = 0.6       # Pausa breve per chiudere
    
    # TROVA IL MICROFONO GIUSTO ORA
    mic_idx = get_mic_index()

    try:
        # Apre il microfono trovato
        with sr.Microphone(device_index=mic_idx) as source:
            print("Ascolto...")
            
            try:
                # Timeout: Smette se non parli entro 5s
                # Limit: Taglia se parli troppo (10s)
                audio = r.listen(source, timeout=5, phrase_time_limit=10)
                
                print("Elaborazione...")
                text = r.recognize_google(audio, language="it-IT")
                return text
                
            except sr.WaitTimeoutError:
                return None
            except sr.UnknownValueError:
                return None
            except Exception as e:
                print(f"Errore SR: {e}")
                return None
                
    except OSError:
        print(f"Errore: Impossibile accedere al microfono {mic_idx}")
        return None
