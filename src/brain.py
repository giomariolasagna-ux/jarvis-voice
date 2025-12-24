import json
import os
import sys
import time
from pathlib import Path

# --- LIBRERIE AUTOMAZIONE ---
try:
    import pyautogui
    import pyperclip
except ImportError:
    pyautogui = None
    pyperclip = None

# Client AI
try:
    from src.moonshot_client import ask
except ImportError:
    def ask(prompt): return "Errore critico: Client Moonshot non trovato."

IDENTITY_PATH = Path(r"C:\Users\Administrator\JARVIS_VOICE\jarvis_identity.json")

def load_identity():
    if not IDENTITY_PATH.exists():
        raise FileNotFoundError(f"Manca {IDENTITY_PATH}")
    with open(IDENTITY_PATH, "r", encoding="utf-8-sig") as f:
        return json.load(f)

print(f"Loading identity...")
IDENTITY = load_identity()

MUTABLE_PATH = Path(IDENTITY.get("mutable_path", r"C:\Users\Administrator\JARVIS_VOICE\mutable_memory"))

def jarvis_brain(user_text):
    print(f"Brain input: {user_text}")
    
    if not user_text:
        return None

    clean_text = user_text.strip()
    lower_text = clean_text.lower()

    # --- MODALITÀ: SCRITTURA AI (AI Writer) ---
    if lower_text.startswith("scrivi"):
        if pyautogui is None:
            return "Errore: Moduli automazione mancanti."

        # Identifica se premere invio alla fine
        send_mode = "e invia" in lower_text
        
        # Pulisce il prompt (rimuove 'scrivi' e 'e invia')
        # Esempio: "Scrivi e invia una mail" -> "una mail"
        prompt = clean_text.replace("scrivi", "", 1).replace("e invia", "", 1).strip()
        
        if not prompt:
            return "Cosa devo scrivere?"

        # 1. GENERAZIONE AI
        # Usiamo un system prompt che forza l'AI a dare SOLO il testo utile
        writer_messages = [
            {"role": "system", "content": "Sei un assistente di scrittura diretta. Genera ESCLUSIVAMENTE il testo richiesto dall'utente. NON aggiungere saluti, preamboli, commenti o virgolette. Il tuo output verrà incollato direttamente in un documento."},
            {"role": "user", "content": prompt}
        ]

        try:
            generated_text = ""
            response = ask(writer_messages)
            
            # Estrazione sicura
            if isinstance(response, dict):
                if "choices" in response and len(response["choices"]) > 0:
                    generated_text = response["choices"][0]["message"]["content"]
                else:
                    return "Errore nella generazione AI."
            else:
                generated_text = str(response)

            # 2. AZIONE FISICA (Incolla)
            pyperclip.copy(generated_text)
            time.sleep(0.1)  # Attesa tecnica clipboard
            pyautogui.hotkey("ctrl", "v")
            
            if send_mode:
                time.sleep(0.2)
                pyautogui.press("enter")
                return "Generato e inviato."
            
            return "Testo incollato."

        except Exception as e:
            return f"Errore scrittura AI: {e}"

    # --- MODALITÀ: ASSISTENTE VOCALE (Standard) ---
    # Se non inizia con "scrivi", è una chiacchierata normale
    messages = [
        {"role": "system", "content": "Sei Jarvis. Rispondi in modo breve e diretto in italiano."},
        {"role": "user", "content": user_text}
    ]
    
    try:
        response = ask(messages)
        if isinstance(response, dict):
            if "choices" in response and len(response["choices"]) > 0:
                return response["choices"][0]["message"]["content"]
        return str(response)

    except Exception as e:
        return f"Errore connessione: {str(e)}"
