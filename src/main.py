import time
import os
import sys
import threading
import json
from pynput import mouse
import pyperclip
import pyautogui

sys.path.append(os.path.dirname(__file__))
import listener
import brain
import tts

BUTTON_HELD = False
IS_WORKING = False

def execute_action(response):
    if not response: return

    mode = response.get("mode", "speak")
    content = response.get("content", "")
    
    # Recuperiamo il path, se presente
    target_folder = response.get("base_path", "")

    print(f"--- AZIONE: {mode.upper()} ---")

    if mode == "speak":
        print(f"Jarvis: {content}")
        tts.speak(content)

    elif mode == "write":
        if content:
            pyperclip.copy(content)
            time.sleep(0.1)
            pyautogui.hotkey("ctrl", "v")

    elif mode == "write_send":
        if content:
            pyperclip.copy(content)
            time.sleep(0.1)
            pyautogui.hotkey("ctrl", "v")
            time.sleep(0.2)
            pyautogui.press("enter")

    elif mode == "create_file":
        # SAFETY LOCK: Impediamo scrittura fuori dal DEV_PATH
        if not target_folder or "JARVIS_DEV" not in target_folder:
            print("BLOCCO SICUREZZA: Tentativo di scrittura fuori dal Playground!")
            tts.speak("Non posso scrivere fuori dal mio playground.")
            return

        try:
            clean_json = content.replace("```json", "").replace("```", "").strip()
            data = json.loads(clean_json)
            filename = data.get("filename")
            code = data.get("code")

            if filename and code:
                full_path = os.path.join(target_folder, filename)
                os.makedirs(os.path.dirname(full_path), exist_ok=True)
                with open(full_path, "w", encoding="utf-8") as f:
                    f.write(code)
                
                msg = f"File {filename} creato nel Playground."
                print(msg)
                tts.speak(msg)
            else:
                tts.speak("Errore nei dati del file.")
        except Exception as e:
            print(f"Err: {e}")
            tts.speak("Errore creazione file.")

    elif mode == "list_dev":
        # Nuova funzione: Visione del Playground
        try:
            if os.path.exists(target_folder):
                files = os.listdir(target_folder)
                if files:
                    readable_files = ", ".join(files[:5]) # Ne legge max 5 per non annoiare
                    msg = f"Nel playground vedo: {readable_files}"
                    if len(files) > 5: msg += " e altri."
                else:
                    msg = "Il playground è vuoto."
            else:
                msg = "La cartella playground non esiste ancora."
            
            print(msg)
            tts.speak(msg)
        except Exception as e:
            tts.speak(f"Non riesco a guardare nella cartella: {e}")

def worker_vocale():
    global IS_WORKING, BUTTON_HELD
    if IS_WORKING: return
    IS_WORKING = True
    
    try:
        user_text = listener.listen_ptt(lambda: BUTTON_HELD)
        if user_text:
            print(f"\nTu: {user_text}")
            response = brain.jarvis_brain(user_text)
            execute_action(response)
        else:
            print(".", end="", flush=True)
    except Exception as e:
        print(f"Errore: {e}")
    finally:
        IS_WORKING = False

def on_click(x, y, button, pressed):
    global BUTTON_HELD
    if hasattr(button, "name") and button.name == "x1":
        BUTTON_HELD = pressed 
        if pressed and not IS_WORKING:
            threading.Thread(target=worker_vocale, daemon=True).start()

def main():
    print("--- JARVIS 2.1 (CONSCIOUSNESS UPDATE) ---")
    print(f"CORE: {brain.CORE_PATH}")
    print(f"PLAYGROUND: {brain.DEV_PATH}")
    print("Premi X1 per parlare.")
    with mouse.Listener(on_click=on_click) as l:
        l.join()

if __name__ == "__main__":
    main()