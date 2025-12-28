import time
import os
import sys
import threading
from pynput import mouse

sys.path.append(os.path.dirname(__file__))
import listener
import brain
import tts

# STATO GLOBALE DEL TASTO
BUTTON_HELD = False
IS_WORKING = False

def worker_vocale():
    global IS_WORKING, BUTTON_HELD
    
    if IS_WORKING: return
    IS_WORKING = True
    
    try:
        # Passiamo una "lambda" che controlla la variabile globale
        # Il listener continuerà a registrare finché BUTTON_HELD è True
        user_text = listener.listen_ptt(lambda: BUTTON_HELD)
        
        if user_text:
            print(f"\nTu: {user_text}")
            response = brain.jarvis_brain(user_text)
            if response:
                print(f"Jarvis: {response}")
                tts.speak(response)
        else:
            print(".", end="", flush=True) # Feedback visivo minimo
            
    except Exception as e:
        print(f"Errore: {e}")
    finally:
        IS_WORKING = False

def on_click(x, y, button, pressed):
    global BUTTON_HELD
    
    # Controlla se è il tasto X1
    if hasattr(button, "name") and button.name == "x1":
        BUTTON_HELD = pressed # Aggiorna lo stato (True=Premuto, False=Rilasciato)
        
        if pressed and not IS_WORKING:
            # Avvia il thread solo quando si preme
            t = threading.Thread(target=worker_vocale, daemon=True)
            t.start()

def main():
    print("--- JARVIS PUSH-TO-TALK ---")
    print("MODALITÀ WALKIE-TALKIE ATTIVA")
    print("1. Tieni premuto X1 -> Parla")
    print("2. Rilascia X1 -> Jarvis risponde")
    
    # Listener non bloccante per non fermare il thread principale se servisse
    with mouse.Listener(on_click=on_click) as l:
        l.join()

if __name__ == "__main__":
    main()
