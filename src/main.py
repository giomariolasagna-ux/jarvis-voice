import time
import os
import sys
from pathlib import Path

# Fix import: aggiunge la cartella corrente al path
sys.path.append(os.path.dirname(__file__))

# Importiamo i moduli stabili
import listener
import brain
import tts

# Percorso trigger (Deve coincidere con quello di AHK)
TRIGGER_FILE = Path(r"C:\Users\Administrator\JARVIS_VOICE\jarvis_trigger.txt")

def main():
    print("--- JARVIS DAEMON STABLE ---")
    print(f"Monitoraggio file: {TRIGGER_FILE}")
    
    # Pulizia avvio
    if TRIGGER_FILE.exists():
        try: os.remove(TRIGGER_FILE)
        except: pass

    while True:
        if TRIGGER_FILE.exists():
            print("\n>>> TRIGGER RILEVATO <<<")
            
            # 1. Rimuovi trigger per evitare loop
            try:
                os.remove(TRIGGER_FILE)
            except Exception as e:
                print(f"Errore rimozione trigger: {e}")
                time.sleep(0.5)
                continue

            # 2. Ascolta
            user_text = listener.listen()
            
            if user_text:
                print(f"Utente: {user_text}")
                
                # 3. Ragiona
                response = brain.jarvis_brain(user_text)
                
                if response:
                    print(f"Jarvis: {response}")
                    
                    # 4. Parla
                    tts.speak(response)
            else:
                print("Nessun input vocale valido.")
                
        time.sleep(0.1)

if __name__ == "__main__":
    main()
