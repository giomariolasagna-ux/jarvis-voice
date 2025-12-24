import json
import os
import sys
import time
import re
from pathlib import Path

# --- IMPORTAZIONI ---
try:
    import pyautogui
    import pyperclip
except ImportError:
    pyautogui = None
    pyperclip = None

try:
    from src.moonshot_client import ask
except ImportError:
    def ask(prompt): return "Errore critico: Client Moonshot non trovato."

# --- CARICAMENTO CONFIGURAZIONE ---
IDENTITY_PATH = Path(r"C:\Users\Administrator\JARVIS_VOICE\jarvis_identity.json")

def load_identity():
    if not IDENTITY_PATH.exists():
        raise FileNotFoundError(f"Manca {IDENTITY_PATH}")
    with open(IDENTITY_PATH, "r", encoding="utf-8-sig") as f:
        return json.load(f)

print(f"Loading identity...")
IDENTITY = load_identity()

SELF_PATH = Path(IDENTITY.get("self_path", r"C:\Users\Administrator\JARVIS_VOICE"))
DEV_PATH = Path(IDENTITY.get("dev_path", r"C:\Users\Administrator\JARVIS_DEV"))
MUTABLE_PATH = Path(IDENTITY.get("mutable_path", r"C:\Users\Administrator\JARVIS_VOICE\mutable_memory"))

# --- STRUMENTI ---
def create_file_in_dev(filename, content):
    try:
        filename = os.path.basename(filename) 
        target = DEV_PATH / filename
        target.parent.mkdir(parents=True, exist_ok=True)
        with open(target, "w", encoding="utf-8") as f:
            f.write(content)
        return f"File {filename} creato." # Risposta brevissima
    except Exception as e:
        return f"Errore: {e}"

def parse_tool(text):
    try:
        match = re.search(r'\{.*"tool":\s*"create_file".*\}', text, re.DOTALL)
        if match:
            data = json.loads(match.group(0))
            if data.get("tool") == "create_file":
                return create_file_in_dev(data.get("filename"), data.get("content"))
    except: pass
    return None

# --- LOGICA PRINCIPALE ---
def jarvis_brain(user_text):
    print(f"Input: {user_text}")
    if not user_text: return None
    clean = user_text.strip().lower()

    # 1. SCRITTURA RAPIDA
    if clean.startswith("scrivi"):
        if not pyautogui: return "No moduli."
        send = "e invia" in clean
        prompt = user_text.strip()[6:].replace("e invia", "", 1).strip()
        
        try:
            # System prompt per scrittura: Solo il testo, niente altro
            res = ask([{"role": "system", "content": "Genera SOLO il testo richiesto."}, {"role": "user", "content": prompt}])
            txt = res["choices"][0]["message"]["content"] if isinstance(res, dict) else str(res)
            pyperclip.copy(txt)
            time.sleep(0.1)
            pyautogui.hotkey("ctrl", "v")
            if send:
                time.sleep(0.2)
                pyautogui.press("enter")
                return "Inviato."
            return "Fatto."
        except: return "Errore."

    # 2. INTELLIGENZA GENERALE (Optimized for Speed)
    # Istruzioni aggiornate: "Risposte telegrafiche"
    sys_prompt = f"""
    Sei Jarvis. Rispondi in italiano.
    
    DIRETTIVA VELOCITÀ: Sii telegrafico. Usa meno parole possibili.
    Se devi fare un'azione, falla e basta.
    
    PERCORSI:
    - READ-ONLY: {SELF_PATH}
    - READ-WRITE: {DEV_PATH}
    
    TOOL CREAZIONE FILE (JSON Obbligatorio):
    {{ "tool": "create_file", "filename": "...", "content": "..." }}
    """
    
    try:
        res = ask([{"role": "system", "content": sys_prompt}, {"role": "user", "content": user_text}])
        reply = res["choices"][0]["message"]["content"] if isinstance(res, dict) else str(res)
        
        tool_out = parse_tool(reply)
        if tool_out: return tool_out
        
        return reply
    except Exception as e:
        return "Errore connessione."
