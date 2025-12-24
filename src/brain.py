import json
import os
import sys
import time
import re
from pathlib import Path

# --- IMPORTAZIONI AUTOMAZIONE ---
try:
    import pyautogui
    import pyperclip
except ImportError:
    pyautogui = None
    pyperclip = None

# --- IMPORTAZIONI AI (ROBUSTE) ---
# Cerchiamo il client Moonshot in due modi per evitare errori di percorso
try:
    # Tentativo 1: Importazione assoluta (se avviato da root)
    from src.moonshot_client import ask
except ImportError:
    try:
        # Tentativo 2: Importazione relativa (se sono nella stessa cartella)
        from moonshot_client import ask
    except ImportError as e:
        # Se fallisce tutto, mostra l'errore REALE (es. manca 'requests')
        def ask(prompt): return f"ERRORE IMPORT REALE: {e}"

# --- CARICAMENTO CONFIGURAZIONE ---
IDENTITY_PATH = Path(r"C:\Users\Administrator\JARVIS_VOICE\jarvis_identity.json")

def load_identity():
    if not IDENTITY_PATH.exists():
        # Fallback se manca il file identity
        return {"self_path": r"C:\Users\Administrator\JARVIS_VOICE", "dev_path": r"C:\Users\Administrator\JARVIS_DEV"}
    with open(IDENTITY_PATH, "r", encoding="utf-8-sig") as f:
        return json.load(f)

IDENTITY = load_identity()
SELF_PATH = Path(IDENTITY.get("self_path", r"C:\Users\Administrator\JARVIS_VOICE"))
DEV_PATH = Path(IDENTITY.get("dev_path", r"C:\Users\Administrator\JARVIS_DEV"))

# --- STRUMENTI ---
def create_file_in_dev(filename, content):
    try:
        filename = os.path.basename(filename) 
        target = DEV_PATH / filename
        target.parent.mkdir(parents=True, exist_ok=True)
        with open(target, "w", encoding="utf-8") as f:
            f.write(content)
        return f"File {filename} creato."
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
    print(f"Brain Input: {user_text}")
    if not user_text: return None
    clean = user_text.strip().lower()

    # 1. SCRITTURA RAPIDA
    if clean.startswith("scrivi"):
        if not pyautogui: return "No moduli automazione."
        send = "e invia" in clean
        prompt = user_text.strip()[6:].replace("e invia", "", 1).strip()
        
        try:
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
        except Exception as e: return f"Errore Scrittura: {e}"

    # 2. INTELLIGENZA GENERALE
    sys_prompt = f"""
    Sei Jarvis. Rispondi in italiano.
    PERCORSI: ORIGINE={SELF_PATH}, DEV={DEV_PATH}
    
    Se devi creare file usa JSON: {{ "tool": "create_file", "filename": "...", "content": "..." }}
    """
    
    try:
        # Chiamata al client AI
        response = ask([{"role": "system", "content": sys_prompt}, {"role": "user", "content": user_text}])
        
        # Gestione errori di rete/API
        if isinstance(response, dict) and "error" in response:
            return f"Errore API Moonshot: {response['error']['message']}"
            
        reply = response["choices"][0]["message"]["content"] if isinstance(response, dict) else str(response)
        
        tool_out = parse_tool(reply)
        if tool_out: return tool_out
        
        return reply
    except Exception as e:
        return f"Errore Brain Critico: {e}"
