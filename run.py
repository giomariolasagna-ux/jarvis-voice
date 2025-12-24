import time
import os
import sys
from pathlib import Path

# Aggiungi la cartella src al percorso per importare i moduli
sys.path.append(os.path.join(os.path.dirname(__file__), "src"))

import listener
import brain
import tts

# Percorso del file grilletto
TRIGGER_FILE = Path(r"C:\Users\Administrator\JARVIS_VOICE\jarvis_trigger.txt")

def main():
    print(f"--- JARVIS ATTIVO ---")
    print(f"In attesa del file trigger: {TRIGGER_FILE}")
    
    # Pulizia iniziale
    if TRIGGER_FILE.exists():
        try:
            os.remove(TRIGGER_FILE)
        except:
            pass

    while True:
        if TRIGGER_FILE.exists():
            print("\nTrigger rilevato!")
            
            # 1. Rimuove subito il file per evitare doppi avvii
            try:
                os.remove(TRIGGER_FILE)
            except Exception as e:
                print(f"Errore rimozione trigger: {e}")
                time.sleep(1)
                continue

            # 2. Suono di attivazione (opzionale) o feedback visivo
            print(">>> MICROFONO APERTO <<<")
            
            # 3. Ascolto
            user_text = listener.listen()
            
            if user_text:
                print(f"Tu: {user_text}")
                
                # 4. Cervello
                response = brain.jarvis_brain(user_text)
                
                if response:
                    print(f"Jarvis: {response}")
                    
                    # 5. Voce
                    tts.speak(response)
            else:
                print("Nessuna voce rilevata.")
                
        time.sleep(0.1)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nArresto manuale.")
