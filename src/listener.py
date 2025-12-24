import speech_recognition as sr

def listen():
    r = sr.Recognizer()
    
    # --- IMPOSTAZIONI STANDARD ---
    # Torna a 0.8 (valore di default). 
    # Aspetta un attimo in più per essere sicuro che hai finito.
    r.pause_threshold = 0.8  
    
    # Energia standard
    r.energy_threshold = 300 
    r.dynamic_energy_threshold = True
    
    with sr.Microphone() as source:
        print("Ascolto...")
        # Calibrazione rumore standard (1 secondo)
        r.adjust_for_ambient_noise(source, duration=1.0)
        
        try:
            audio = r.listen(source, timeout=5, phrase_time_limit=15)
            
            print("Elaborazione audio...")
            text = r.recognize_google(audio, language="it-IT")
            return text
            
        except sr.WaitTimeoutError:
            return None
        except sr.UnknownValueError:
            return None
        except Exception as e:
            print(f"Errore ascolto: {e}")
            return None
