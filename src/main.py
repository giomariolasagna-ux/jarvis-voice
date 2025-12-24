import time
import os
import sys
from pathlib import Path

# --- FIX IMPORTAZIONI CRITICO ---
# 1. Aggiunge la cartella 'src' (per importare brain, listener, tts)
sys.path.append(os.path.dirname(__file__))
# 2. Aggiunge la cartella ROOT del progetto (per supportare 'from src.moonshot_client')
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import listener
import brain
import tts

# PERCORSO TRIGGER (Temp)
TRIGGER_FILE = Path(r"C:\Temp\jarvis_trigger.txt")

def main():
    print("--- JARVIS DAEMON STABLE ---")
    print(f"Monitoraggio file: {TRIGGER_FILE}")
    print(f"Path Root aggiunto: {sys.path[-1]}")
    
    # Assicura cartella temp
    TRIGGER_FILE.parent.mkdir(parents=True, exist_ok=True)
    
    if TRIGGER_FILE.exists():
        try: os.remove(TRIGGER_FILE)
        except: pass

    while True:
        if TRIGGER_FILE.exists():
            print("\n>>> TRIGGER RILEVATO <<<")
            try:
                os.remove(TRIGGER_FILE)
            except:
                time.sleep(0.1)
                continue

            # Ascolta
            try:
                user_text = listener.listen()
                if user_text:
                    print(f"Tu: {user_text}")
                    response = brain.jarvis_brain(user_text)
                    if response:
                        print(f"Jarvis: {response}")
                        tts.speak(response)
            except Exception as e:
                print(f"Errore: {e}")
                
        time.sleep(0.1)

if __name__ == "__main__":
    main()
